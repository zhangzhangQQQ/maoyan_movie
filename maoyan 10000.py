# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 12:12:12 2018

@author: lenovo
"""
import requests 
from pyquery import PyQuery as pq 
from urllib.parse import quote
import csv 
import re
import os
from fontTools.ttLib import TTFont
from multiprocessing.pool import Pool

 
class MaoYan(object):
    def __init__(self,url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
        }
 
    # 发送请求获得响应
    def get_html(self, url):
        resp = requests.get(url, headers=self.headers)
        return resp.content

    def font_mate_num(self,font_file):
        font1 = TTFont('font5.woff')
        keys = font1['glyf'].keys()
        values = list(' .2481903567')
        # 构建基准 {name: num}
        dict1 = dict((k,v) for k,v in zip(keys, values))
        dict2={}
                
        font2 = TTFont('./fonts/'+font_file)
        for key in font2['glyf'].keys():
            for k, v in dict1.items():
        # 通过比较 字形定义 填充新的name和num映射关系
                if font1['glyf'][k] == font2['glyf'][key]:
                    dict2[key] = v.strip()
                    break
        return(dict2)
        
    def create_font(self,font_file):
        file_list=os.listdir('./fonts')
        if font_file not in file_list:
            print('字体不在本地，下载：',font_file)
            url = 'https://vfile.meituan.net/colorstone/'+font_file
            new_file = self.get_html(url)
            with open('./fonts/'+font_file,'wb') as f:
                f.write(new_file)
                
            #创建self.font 属性    
        self.font = TTFont('./fonts/'+font_file)
        self.font_file = font_file
        
        
    def modify_data(self,data):
        gly_num = self.font_mate_num(self.font_file)
        for k,v in gly_num.items():
            k = k.replace('uni','&#x').lower()+';'
            if k in data:
                data = data.replace(k,v)
        return data
    
    def start_crawl(self):
        
        html = self.get_html(self.url).decode('utf-8')
        
        information = {}
        # 正则匹配字体文件
        font_file = re.findall(r'vfile\.meituan\.net\/colorstone\/(\w+\.woff)', html)
        if font_file[0]:
            self.create_font(font_file[0])
        else:
            information_out_index ={'title':'null','prize_num':'null','first_star':'null','second_star':'null','third_star':'null','types':'null','origin_length':'null','post_time':'null','star':'null','people':'null','ticket_number':'null'}
            return(information_out_index)
            
        
        # 正则匹配星级
        star = re.findall(r'<span class="index-left info-num ">\s+<span class="stonefont">(.*?)</span>\s+</span>', html)
        if star:
            star = self.modify_data(star[0])
        else:
            star = 'null'
        # 正则匹配评论的人数
        people1 = re.findall(r'''<span class='score-num'><span class="stonefont">(.*?)(.*?)</span>(人评分)</span>''', html)
        if people1:   
            people = ''.join(re.findall(r'''<span class='score-num'><span class="stonefont">(.*?)(.*?)</span>(人评分)</span>''', html)[0])
            people = self.modify_data(people)
        else:
            people = 'null'
        # 正则匹配累计票房
        ticket_number1 = re.findall(r'''<span class="stonefont">(.*?)</span><span class="unit">(.*?)</span>''', html)
        if ticket_number1:
            ticket_number = ''.join(re.findall(r'''<span class="stonefont">(.*?)</span><span class="unit">(.*?)</span>''', html)[0])
            ticket_number = self.modify_data(ticket_number)
        else:
            ticket_number = 'null'
      
# =============================================================================
# 
# =============================================================================

        resp =self.get_html(self.url).decode()
        doc = pq(resp)
        first_item = doc('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(2) > ul > li:nth-child(1)')
        if first_item:    
            first_href = first_item.children().attr.href
            first_href = 'https://maoyan.com'+first_href
        else:
            first_href ='null'
        
        if first_href =='null':
            first_star = '0'
        else:
            first_star = str(self.get_star_award_num(first_href))
        
        
        second_item = doc('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(2) > ul > li:nth-child(2)')
        if second_item:
            second_href = second_item.children().attr.href
            second_href = 'https://maoyan.com'+second_href
        else:
            second_href = 'null'
            
        if second_href =='null':
            second_star = '0'
        else:
            second_star = str(self.get_star_award_num(second_href))
        
        
        
        third_item = doc('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(2) > ul > li:nth-child(3)')
        if third_item:    
            third_href = third_item.children().attr.href
            third_href = 'https://maoyan.com'+third_href
        else:
            third_href = 'null'
        
        if third_href =='null':
            third_star = '0'
        else:
            third_star =str(self.get_star_award_num(third_href))
                
        item_title = doc('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container')
        title = item_title('.name').text()
        item = doc('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul')
        types = item.children('li:nth-child(1)').text()
        origin_length = item.children('li:nth-child(2)').text()
        post_time = item.children('li:nth-child(3)').text()
        ###################dirtor
        dirtor_item = doc('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(2) > div.mod-content > div > div:nth-child(1) > ul > li > div.info')
        if dirtor_item:
            dirtor_href = 'https://maoyan.com' + dirtor_item.children().attr.href 
            prize_num =self.is_dirtor_get_award(dirtor_href)
            prize_num =str(prize_num)
        else:
            prize_num ='0'
        
      
        information = {'title':title,'prize_num':prize_num,'first_star':first_star,'second_star':second_star,'third_star':third_star,'types':types,'origin_length':origin_length,'post_time':post_time,'star':star,'people':people,'ticket_number':ticket_number}
        return(information)
# =============================================================================
#      
# =============================================================================
        
    def is_dirtor_get_award(self,url):
        resp = self.get_html(url).decode()
        doc_dirtor = pq(resp)
        items = doc_dirtor('.main .award .mod-content .item')
        awards = 0
        if items:    
            names = ['香港金像奖','台湾金马奖','中国电影金鸡奖','大众电影百花奖','亚洲电影大奖','金球奖','奥斯卡金像奖','英国电影和电视艺术学院','MTV电影奖','英国独立电影奖']
            items = items.items()
            for item in items:
                if item('.award-name'):
                    award_name = item('.award-name').text()
                    for name in names:
                        if award_name == name:
                            award_contents = item('.award-num').text()
                            if award_contents:
                                award_num = re.findall('(\d+)',award_contents)
                                if len(award_num)==2:
                                    sum_num = int(award_num[1]) +int(award_num[0])
                                    awards = awards+sum_num
                                else:
                                    sum_num =int(award_num[0])
                                    awards =awards+sum_num
                                break
        return awards

    def get_star_award_num(self,first_href):
        subresp_first = self.get_html(first_href).decode()
        doc_first =pq(subresp_first)
        first_items = doc_first('.main .award .module .mod-content .item')
        awards = 0
        names = ['香港金像奖','台湾金马奖','中国电影金鸡奖','大众电影百花奖','亚洲电影大奖','金球奖','奥斯卡金像奖','英国电影和电视艺术学院','MTV电影奖','英国独立电影奖']
        if first_items:
            first_items =first_items.items()
            for item in first_items:
                award_name =item('.award-name').text()
                if award_name:
                    for name in names:
                        if award_name==name:
                            award_contents = item('.award-num').text()
                            if award_contents:
                                award_num = re.findall('(\d+)',award_contents)
                                if len(award_num)==2:
                                    sum_num = int(award_num[1]) +int(award_num[0])
                                    awards = awards+sum_num
                                else:
                                    sum_num =int(award_num[0])
                                    awards =awards+sum_num
                                break
        return awards
# =============================================================================
# 
# =============================================================================
def save_to_excel(information):
    with open('maoyan_movies.csv','a',encoding = 'utf-8-sig',newline = '') as csvfile:
        fieldnames = ['title','prize_num','first_star','second_star','third_star','types','origin_length','post_time','star','people','ticket_number']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writerow(information)

def page_index(offset):
  
    url= 'https://maoyan.com/films?showType=3&yearId=12&offset='+quote(str(offset))
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
              }
    resp = requests.get(url,headers = headers)
    doc = pq(resp.text)
    items=doc('.movies-panel .movies-list .channel-detail.movie-item-title').items()
    for item in items:
        href ='https://maoyan.com' + item.children().attr.href
        maoyan = MaoYan(href)
        information = maoyan.start_crawl()
        save_to_excel(information)
    

    
    
    
def main(offset):
    """
    遍历每一页
    """
    page_index(offset)

#7 52
#8 41
#9 41
#10 44
#11 66
#12 46
PAGE_START = 0
PAGE_END = 46
if __name__ == '__main__':
    pool = Pool(processes=64)
    groups = ([x * 30 for x in range(PAGE_START, PAGE_END)])
    pool.map(main, groups)
    pool.close()
    pool.join()
# =============================================================================
# 网络不流畅
# =============================================================================


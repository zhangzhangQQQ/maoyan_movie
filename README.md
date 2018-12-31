# maoyan_movie
为了搞计量经济学作业写的一个小爬虫 
要看懂是很麻烦 我现在都不想看这个文件 hhh
使用说明：
1、21行的User-Agent可以换成你自己的
2、本人的python运行路径是根目录C:\Users\lenovo ， 换成你的电脑的话 ， 要将文件中对应的更改一下（很痛苦，我知道）比如37的font2 = TTFont('./fonts/'+font_file) 里面这个./fonts，表示创建文件夹，你要在前面加上你的工作路径，其余的都相似，建议像我一样将工作路径改成根目录
3、这个程序爬取的是猫眼电影的票房、评分、上映时间等，你可以点开https://maoyan.com/films?showType=3&yearId=12&offset=0 看一下这个结构，如果你要爬这些网站（其他网站爬不了）,只要把230行的url 中的 yearID= 后面的数字填你想爬的那个年份 ， 就是上面这个URL↑，最下面的PAGE_START 和 PAGE_END 是这个页面：https://maoyan.com/films?showType=3&yearId=12 的页数（往下翻到底就看得到）,yearID不同这个页数也会不同。
4、最后就可以编译了，前提是你要安装需要的包和上述操作没问题

祝好~

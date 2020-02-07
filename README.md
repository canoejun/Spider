# Spider
a set of Spiders
# spiderbychok8.py
当初用小视频网站看电影和动漫，后来觉得这个网站的流畅度很卡，觉得等待很烦，于是自己写了一个爬虫，把视频一次性全部下载下来方便本地观看。
### 使用
先打开chok8.com的网址，搜索像观看的电影和动漫，然后打开spiderbychok8.py文件，设置好对应的的下载路径和总共集数，链接即可。
etc:

    fileDir = "/Users/canoejun/Desktop/大学/haizeiwang"
    totalCount = 915
    url = "https://www.chok8.com/vodplay/315-1"
    
    spider = SpiderByChok8(fileDir,totalCount,url)
    spider.download_ts_file()
    spider.combineTSFile()
    
安静等待下载完会自动合并成一个文件。

import re,os,time
import requests
import threading
from urllib import parse

sem=threading.Semaphore(35)

class SpiderByChok8:
    def __init__(self,fileDir,totalCount,url):
        self.fileDir = fileDir
        self.totalCount = totalCount
        self.url = url
        pass


    def download_ts_file(self):
        self.__download_m3u8__(self.fileDir,self.totalCount,self.url)
        self.__download_tsfileByLink__(self.fileDir)

    def __get_real_ts__(self,text,front_url):
        # print(text)
        links = ""
        lines = text.split("\n")
        for line in lines:
            if("ts" in line):
                link = front_url+line+"\n"
                links += link

        return links


    def __download_m3u8__(self,filedir,total,origin_url):
        dir = fileDir
        if not os.path.exists(dir):
            os.mkdir(dir)
        for count in range(1,total+1):
            if(os.path.exists("{}/{}.txt".format(filedir,count))):
                continue
            link = "%s-%d.html"%(origin_url,count)
            print(link)
            gHeads = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
            try:
                res = requests.get(link, headers=gHeads)
                res.encoding = 'utf-8'
                html = res.text
                reg = re.compile(
                    r'<script type="text/javascript">var player_data={.*?,"url":"(.*?)",.*?,"from":"wlm3u8","server":"","note":""}</script>',re.S)
                url = re.findall(reg, html)
                url = parse.unquote(url[0])
                front_url = url[:23]
                html = requests.get(url)
                links = self.__get_real_ts__(html.text,front_url)
                with open('{}/{}.txt'.format(filedir,count), 'w') as f:
                    f.write(links)
            except:
                continue

    def __download_tsfileByLink__(self,filedir):
        path = "{}".format(filedir)
        fileList = os.listdir(path)
        fileList.sort()
        for file in fileList:
            if "DS_Store" in file:
                continue

            if not os.path.exists(path+"/"+file.replace(".txt","")):
                os.mkdir(path+"/"+file.replace(".txt",""))
            if file.endswith(".txt"):
                t = threading.Thread(target=self.__openFileForDown__,args=(path,file))
                t.start()

    def __openFileForDown__(self,path,file):
        with open((path + "/" + file), 'r') as f:
            with sem:
                start_time = time.time()
                for link in f.readlines():
                    link = link.replace("\n", "")
                    name = link[link.find("film"):]

                    if os.path.exists(path +"/"+file.replace(".txt", "")+"/"+ name):
                        continue
                    try:
                        t = threading.Thread(target=self.__down__, args=(link, path + "/" + file.replace(".txt", "") + "/",))
                        t.start()
                        t.join()
                    except:
                        continue
                print("结束--", time.time() - start_time, file)
                print()

    def __down__(self,link,path):
        # print(link)
        # link = "https://cn1.5311444.com/hls/20190416/109de379e54813048a58e01ca98d109e/1555403650/film_00000.ts"
        try:
            name = link[link.find("film"):]
            f = requests.get(link)
            with open(path+name,"wb") as code:
                code.write(f.content)
        except:
            print("*********%s-----*********"%len(link.replace(" ","")))
        print(path+name)


    def combineTSFile(self):
        path = "{}".format(self.fileDir)

        # 获取该目录下所有文件，存入列表中
        fileList = os.listdir(path)
        fileList.sort()
        for file in fileList:
            if ".txt" in file or "DS_Store" or ".ts" in file:
                continue
            os.chdir(path+"/"+file)
            os.system("cat *.ts  > %s/%s.ts"%(path,file))





if __name__ == '__main__':
    fileDir = "/Users/canoejun/Desktop/大学/haizeiwang"
    fileDir = "/Users/canoejun/Desktop/大学/guiguzi"

    totalCount = 915
    totalCount = 52

    url = "https://www.chok8.com/vodplay/315-1"
    url = "https://www.chok8.com/vodplay/28651-1"
    spider = SpiderByChok8(fileDir,totalCount,url)
    spider.download_ts_file()
    spider.combineTSFile()













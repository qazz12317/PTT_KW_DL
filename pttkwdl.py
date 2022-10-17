import bs4
from bs4 import BeautifulSoup
import requests
import urllib.request as req
from urllib.parse import quote
import re
import os 


def getdata(): #把程式包裝成函式
  url=input("請輸入抓取PTT網址：")
  pages=int(input("請輸入抓取頁數："))
  kw=input("請輸入關鍵字：")
  n=0

  def get_webPage(url):
    res = requests.get(url,cookies = {'over18': '1'})
    if res.status_code !=200:
        print("Invalid URL",res.url)
        return none
    else:
        return res.text

  while n<pages:
    print("------【正在抓取第"+str(n+1)+"頁資料】------")
 
    request=req.Request(url,headers={
        "cookie":"over18=1",
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
      })
 
    with req.urlopen(request) as response:
      data=response.read().decode("utf-8")
    root=bs4.BeautifulSoup(data,"html.parser")
    #titles=root.find_all("div",class_="title")
    titles=root.select("div.title")

 
    for title in titles:
      if title.a!=None and kw in title.a.get_text(): 
        
        print(title.a.string)
        print("https://www.ptt.cc"+title.a["href"])
        web = ("https://www.ptt.cc"+title.a["href"])
        fresh = get_webPage(web)
        soup = BeautifulSoup(fresh,'html5lib')
        imgs = soup.findAll('a',{'href':re.compile('https:\/\/(imgur|i\.imgur)\.com\/(.*.jpg|.*.gif)$')})
        foldername = title.a.string.strip()
        os.makedirs(foldername)

        if len(imgs)> 0 :
          try:
            for img in imgs:
              print(img['href'])
              fileName = img['href'].split("/")[-1]
              req.urlretrieve(img['href'], os.path.join(foldername, fileName))
          except Exception as e:
            print(e)
       
    nextlink=root.find("a",string="‹ 上頁")
    url=str("https://www.ptt.cc"+nextlink["href"]) 
    
    n+=1

getdata() 
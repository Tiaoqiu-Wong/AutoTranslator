import time
import http.client
import hashlib
import urllib
import random
import json
import tkinter as tk
import tkinter.font as tf
import threading
from aip import AipOcr
from PIL import ImageGrab
temp=''
crrtem=''
judge=0
crr=''    #character_recognition_result 文字识别结果收入一个字符串

#百度AI变量
APP_ID = '******************'           #请在这三行输入百度AI的文字识别项目的账号密码安全码
API_KEY = '*****************'
SECRET_KEY = '***********'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
options = {}
options["language_type"] = "JAP"
options["detect_language"] = "true"
#百度翻译变量
appid = '************************'      #请在这两行输入百度翻译的文字识别项目的账号密码
secretKey = '*******************' 
fromLang = 'jp'        #原文语种
toLang = 'zh'           #译文语种
salt = random.randint(32768, 65536)

#GUI编程
top=tk.Tk()
top.wm_attributes('-topmost',1)                                        #窗口置顶
top.geometry('250x500')                                                   #窗口默认大小设置
top.title("基于百度AI和百度翻译的屏幕文字实时翻译软件")     #窗口名
ft = tf.Font(family='微软雅黑', size=8)                                #提醒框文字字体设置
ft1 = tf.Font(family='微软雅黑', size=12)                            #文本框文字字体设置

yw=tk.Text(top,width=40,height=10,font=ft1)     #原文
yw.pack()
fyck=tk.Text(top,width=40,height=10,font=ft1)      #译文
fyck.pack()

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
def sb():
    global crr,crrtem
    global temp,judge
    global APP_ID,API_KEY,SECRET_KEY
    global image,options
    global appid,secretKey
    global fromLang,toLang,salt        #原文语种,译文语种

    crr=''

    #截图功能 两点式截图
    pic = ImageGrab.grab((219,736,1716,1018))#4个坐标分别是旧x，旧y，新x，新y
    pic.save(r"C:\beofuse\SH.jpg")

    #调用百度AI进行日语识别
    image = get_file_content(r'C:\beofuse\SH.jpg')
    text=client.basicGeneral(image, options)

    if text['words_result']!=temp:
        temp=text['words_result']
        lens=len(text['words_result'])  #关键参数：所要翻译文字的行数
        for tem1 in range(0,lens):
            if 'くらしの' not in text['words_result'][tem1]['words'] and 'しか长' not in text['words_result'][tem1]['words'] and '●●'not in text['words_result'][tem1]['words'] and '。。' not in text['words_result'][tem1]['words'] and 'くらしく' not in text['words_result'][tem1]['words']:
                crr=crr+text['words_result'][tem1]['words']
                judge=1
    else:
        crr=crrtem
        judge=0
    yw.delete(0.0, 'end')
    yw.insert('end',crr+'\n')
    crrtem=crr
    if judge==1:
        #调用百度翻译api
        tah=''     #translation results here

        httpClient = None
        myurl = '/api/trans/vip/translate'

        q= crr
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()# response是HTTPResponse对象
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            tah=result['trans_result'][0]['dst'].replace('标记', ' ')
        except Exception as e:
            print (e)
        finally:
            if httpClient:
                httpClient.close()

        fyck.delete(0.0, 'end')
        fyck.insert('end',tah+'\n')

def T1():
    sb()
    top.after(1000,T1)


try:
    top.after(1000,T1)
    top.mainloop()
except:
   print ("Error: 无法使用")
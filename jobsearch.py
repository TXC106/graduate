# -*- coding: utf-8 -*-
# @Time : 2021/1/27
# @Author : kiwi
# @File : jobsearch.py
# @Project : spider
import csv
import random
from fake_useragent import UserAgent

import requests
import re
from bs4 import BeautifulSoup
import time

# 关闭多余的链接
s = requests.session()
# 关闭多余连接
s.keep_alive = False
# 增加重试连接次数
requests.adapters.DEFAULT_RETRIES = 5

# proxies_list = ['60.191.11.241:3128', '122.224.65.197:3128', '110.243.19.138:9999',
#                 '49.67.55.216:8118', '175.43.56.13:9999']
# proxies_list = ['117.90.240.75:8118','60.191.11.241:3128']
proxies_list = ['49.86.56.40:9999']
proxy_num = 0


def getProxy(num=0):
    proxies = {
        'http': '106.14.198.6:8080',
        'https': proxies_list[num]
    }
    return proxies


def getJobInfo():
    global proxy_num
    print(proxy_num)
    url_Announce = 'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25AE%25A1%25E7%25AE%2597%25E6%259C%25BA,2,1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    headers["X-Forwarded-For"] = "%s.%s.%s.%s" % (
        random.randrange(1, 200, 20), random.randrange(1, 200, 20), random.randrange(1, 200, 20),
        random.randrange(1, 200, 20))
    try:
        # http连接数量控制
        s.headers = headers
        # s.proxies = getProxy(proxy_num)
        print("the current proxy is")
        print(s.proxies)
        resp = s.get(url_Announce)
        # resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'utf-8'

        # print(resp.text)
        # sum_num = int(
        #     re.findall('<span class="td">共 (.*?)657 页</span>', resp.text, re.I)[0])
        sum_num = int(re.findall('\"total_page\":\"(.*?)\"', resp.text, re.I)[0])
        # print(sum_num)

    except:
        print("搜索页面加载失败")
        status = {
            'status': -1,
            'description': '页面不存在或响应超时'}
        return status
    # try:
    #     resp = requests.get(url_Announce, headers=headers).text
    #     soup = BeautifulSoup(resp, 'lxml')
    #     print(soup)
    #     exit()
    # except:
    #     print("页面加载失败")
    #     status = {
    #         'status': -1,
    #         'description': '页面不存在或响应超时'}
    #     return status
    #
    # pic_sum = []
    # for i in soup.findAll(name='div', attrs={'class': 'item'}):
    #     # http://www.aao.cdut.edu.cn/info/1172/2660.htm
    #     # http://www.aao.cdut.edu.cn//__local/7/92/0A/DA8111CCC135E3FBB86C0F4782F_5847110F_2DCED.jpg
    #     # print('http://www.aao.cdut.edu.cn/' + i.a.get('href'))
    #     # print('http://www.aao.cdut.edu.cn/' + i.img.get('src'))
    #     pic = {'img': 'http://www.aao.cdut.edu.cn/' + i.img.get('src'), 'link': 'http://www.aao.cdut.edu.cn/' + i.a.get('href')}
    #     pic_sum.append(pic)

    # exit()
    page_num = 1
    announce_sum = []
    job_info_sum_dict = {}   # 总清单
    while page_num <= sum_num:
        url_Announce = 'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25AE%25A1%25E7%25AE%2597%25E6%259C%25BA,2,{}.html'.format(page_num)
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        #                   ' Chrome/77.0.3865.120 Safari/537.36'
        # }
        # headers["X-Forwarded-For"] = "%s.%s.%s.%s" % (
        #     random.randrange(1, 200, 20), random.randrange(1, 200, 20), random.randrange(1, 200, 20),
        #     random.randrange(1, 200, 20))
        # headers = {
        #     'User-Agent': UserAgent(verify_ssl=False).random
        # }

        # for page_again in range(3):
        #     try:
        #         # http连接数量控制
        #         s.headers = UserAgent(verify_ssl=False).random
        #         print("0")
        #         print(s.headers)
        #         # 换代理
        #         # proxy_num = proxy_num
        #         # s.proxies = getProxy(proxy_num % 2)
        #         # s.proxies = {}
        #         # print("the current proxy ip0 is")
        #         # print(s.proxies)
        #         resp = s.get(url_Announce)
        #         # resp = requests.get(url_Announce, headers=headers)
        #         # print(resp.status_code)
        #     except:
        #         for page_except_again in range(3):
        #             try:
        #                 s.headers = UserAgent(verify_ssl=False).random
        #                 print("1")
        #                 print(s.headers)
        #                 print("cannot get access to it0")
        #                 # time.sleep(5)
        #                 # proxy_num = proxy_num+1
        #                 # if proxy_num%2 == 0:
        #                 #     s.proxies = {}
        #                 # else:
        #                 #     s.proxies = getProxy(proxy_num%2)
        #                 s.proxies = getProxy()
        #                 print("the current proxy ip0 is")
        #                 print(s.proxies)
        #                 resp = s.get(url_Announce)
        #             except:
        #                 time.sleep(3)
        #             else:
        #                 break
        #
        #         # 换代理
        #         # for p in range(0,5):
        #         #     try:
        #         #         proxy_num = proxy_num+1
        #         #         s.proxies = getProxy(proxy_num%5)
        #         #         print("the current proxy ip0 is")
        #         #         print(s.proxies)
        #         #         resp = s.get(url_Announce)
        #         #         break
        #         #     except:
        #         #         continue
        #         # # print(resp.status_code)
        #     else:
        #         break

        try:
            # http连接数量控制
            s.headers = UserAgent(verify_ssl=False).random
            print("0")
            print(s.headers)
            # 换代理
            # proxy_num = proxy_num
            # s.proxies = getProxy(proxy_num % 2)
            # s.proxies = {}
            # print("the current proxy ip0 is")
            # print(s.proxies)
            resp = s.get(url_Announce)
            # resp = requests.get(url_Announce, headers=headers)
            # print(resp.status_code)
        except:
            for page_except_again in range(5):
                try:
                    s.headers = UserAgent(verify_ssl=False).random
                    print("1")
                    print(s.headers)
                    print("cannot get access to it0")
                    # time.sleep(5)
                    # proxy_num = proxy_num+1
                    # if proxy_num%2 == 0:
                    #     s.proxies = {}
                    # else:
                    #     s.proxies = getProxy(proxy_num%2)

                    if page_except_again == 3:
                        time.sleep(10)
                        s.proxies = {}
                        try:
                            resp = s.get(url_Announce)
                        except:
                            continue
                        else:
                            break

                    s.proxies = getProxy()
                    print("the current proxy ip0 is")
                    print(s.proxies)
                    resp = s.get(url_Announce)
                except:
                    time.sleep(3)
                else:
                    break

                # 换代理
                # for p in range(0,5):
                #     try:
                #         proxy_num = proxy_num+1
                #         s.proxies = getProxy(proxy_num%5)
                #         print("the current proxy ip0 is")
                #         print(s.proxies)
                #         resp = s.get(url_Announce)
                #         break
                #     except:
                #         continue
                # # print(resp.status_code)

        # resp.encoding = 'gbk'
        resp.encoding = resp.apparent_encoding


        # 获得总结果
        result = re.findall('engine_search_result\":\[(.*?),\"adid\":\"\"}\],', resp.text, re.I)[0]
        add_text = ',"adid":""}'
        # print(result+add_text)
        result_full = result+add_text
        result_full = result_full.split('},{')

        # 每条结果对应详情
        each_inpage = 0
        end_add = '}'
        while each_inpage < len(result_full):
        # while result_full[i] != None:
        #     print('==================================')
            # print(result_full[i] + end_add) # 首页展示信息

            # print(i)
            job_info_dict = {}
            job_info_list = []
            result_full_now = result_full[each_inpage]
            # 获得详情页面链接
            result_urls = re.findall('"job_href":"(.*?)","job_name"', result_full_now, re.I)[0]
            result_urls_text = re.sub(r'\\', '', result_urls)
            # print(result_urls_text)

            # 获得首页信息
            # print('--------首页信息------')
            try:
                # print(result_full_now)
                result_name = re.findall('"job_name":"(.*?)",', result_full_now, re.I)[0]
                result_name = re.sub(r'\\','',result_name)
                # print('result_name:'+result_name)
                # print(result_full_now)
                result_providesalary_text = re.findall('"providesalary_text":"(.*?)","workarea"', result_full_now, re.I)[0]
                result_attribute_text = re.findall('"attribute_text":(.*?),"companysize_text"', result_full_now, re.I)[0]
                # print('result_providesalary_text:'+result_providesalary_text)
                # print('result_attribute_text:'+result_attribute_text)
                result_time = re.findall('"updatedate":"(.*?)",', result_full_now, re.I)[0]
                jobwelf_list = re.findall('"jobwelf_list":(.*?),"attribute_text"', result_full_now, re.I)[0]
                # print(result_time)

                # 判断详情列表是否有学历
                if len(result_attribute_text[1:-1].split(',')) == 2:
                    experence = 'no info'
                    education = 'no info'
                elif len(result_attribute_text[1:-1].split(',')) == 3:
                    experence = result_attribute_text[1:-1].split(',')[1][1:-1]
                    education = 'no info'
                else:
                    experence = result_attribute_text[1:-1].split(',')[1][1:-1]
                    education = result_attribute_text[1:-1].split(',')[2][1:-1]

                main_temp_dict = {
                    'result_name': result_name,
                    'result_providesalary_text': result_providesalary_text,
                    'area': result_attribute_text[1:-1].split(',')[0][1:-1],
                    'experence': experence,
                    'education': education,
                    'result_time': result_time,
                    'jobwelf_list': jobwelf_list
                }
                # print(result_attribute_text)
                # print(len(result_attribute_text[1:-1].split(',')))
                # print(result_attribute_text[1:-1].split(',')[0][1:-1])
                job_info_dict.update(main_temp_dict)
            except:
                each_inpage = each_inpage + 1
                continue
                # print(i)

            # 获得详情界面信息
            # print('==================detail========================')
            for detail_again in range(3):
                try:
                    # http连接数量控制
                    # s.headers = headers
                    s.headers = UserAgent(verify_ssl=False).random
                    print("2")
                    print(s.headers)
                    # 换代理
                    # proxy_num = proxy_num
                    # s.proxies = getProxy(proxy_num % 2)
                    # print("the current proxy ip is")
                    # print(s.proxies)

                    resp_detail = s.get(result_urls_text)
                    #  = requests.get(result_urls_text, headers=headers)
                except:
                    for detail_except_again in range(3):
                        try:
                            s.headers = headers
                            print("cannot get access to it")
                            # time.sleep(3)
                            # proxy_num = proxy_num + 1
                            s.proxies = getProxy()
                            s.headers = UserAgent(verify_ssl=False).random
                            print("3")
                            print(s.headers)
                            print("the current proxy ip is")
                            print(s.proxies)
                            # s.headers = headers
                            # print("cannot get access to it")
                            # time.sleep(5)
                            # # 换代理
                            # for p in range(0, 5):
                            #     try:
                            #         proxy_num = proxy_num + 1
                            #         s.proxies = getProxy(proxy_num % 5)
                            #         print("the current proxy ip is")
                            #         print(s.proxies)
                            #         resp = s.get(url_Announce)
                            #         break
                            #     except:
                            #         continue
                            if detail_except_again == 2 & detail_again == 1:
                                time.sleep(10)
                                s.proxies = {}
                                try:
                                    resp = s.get(url_Announce)
                                except:
                                    continue
                                else:
                                    break
                            resp_detail = s.get(result_urls_text)
                        except:
                            time.sleep(3)
                        else:
                            break
                    break
                else:
                    break



            # resp_detail.encoding = 'gbk'
            resp_detail.encoding = resp_detail.apparent_encoding
            # print(resp_detail.text)

            # 所属部门
            try:
                belongs = re.findall('所属部门：<\/span>(.*?)<br \/>', resp_detail, re.I)[0]
                # print('=================所属部门======================')
                # print('所属部门'+belongs)
            except:
                # print('no info')
                belongs = 'no info'
            job_info_dict.update({'belongs': belongs})

            soup = BeautifulSoup(resp_detail.text, 'lxml')
            detail = str(soup.find('div', class_='tCompany_main'))
            # print(detail)
            t_num = 0
            keywords = []
            for t in soup.findAll(name='a', attrs={'class': 'el tdn'}):
                # print(t.span.text)
                # print(t.a.get('href'))
                # print(t.a.text)
                # print(t.get('href'))
                # keywords = []
                if t_num == 0:
                    # print('==========职能类别=========')
                    # print(t.get('href'))
                    # print(t.text)
                    category_line = t.get('href')
                    category = t.text
                    t_num = t_num + 1
                else:
                    # print('============关键字===============')
                    # print(t.get('href'))
                    # print(t.text)
                    keywords.append(t.text)
                    t_num = t_num + 1
                    # print(keywords)
            if t_num == 1:
                # print('============关键字===============')
                # print('no key words')
                keywords = []
            job_info_dict.update({
                'keywords': keywords,
                'category_line': category_line,
                'category': category
            })
            # print(job_info_dict)

            # 职位信息
            try:
                job_detail = soup.find('div', class_='bmsg job_msg inbox').text
                # print(job_detail)
            except:
                job_detail = 'noinfo'

                # print(t)
            each_inpage = each_inpage + 1
            # print(i)

            # # 写入txt
            # # print('write')
            # with open('./jobdata.txt', 'a+', encoding='utf-8') as file:
            #     file.write(str(job_info_dict) + '\n')
            #
            #     # file.write('a\n')

            # 写入csv
            with open('./jobdata.csv', 'a+',newline='',encoding='utf-8-sig') as csv_file:
                csv.writer(csv_file).writerow([result_name,result_providesalary_text,job_info_dict['area'],
                                              experence,education,belongs,
                                               keywords,category_line,category,job_detail,jobwelf_list,result_time])


            job_info_list.append(job_info_dict)
            # print('=============================')
            print(each_inpage)
            print("done")
            time.sleep(0.1)
            # resp_detail.close()


        # for li in soup.find(name='ul', attrs={'class': 'lict_cont1 clearfix'}).findAll('li'):
        #     announce = {}
        #     # print(''.join(li.text.split()))
        #     # print("http://www.lib.cdut.edu.cn/category8"+li.a['href'])
        #     announce = {
        #         'title': ''.join(li.text.split()),
        #         'link': "http://www.lib.cdut.edu.cn/category8" + li.a['href']
        #     }
        #     announce_sum.append(announce)
        # print(page_num)
        print(page_num)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        page_num += 1
        print("sleeping...")
        time.sleep(5)
        print("go on")
        # resp.close()
        # print('write')

    # exit()
    # print(announce_sum)
    # announce_sum = {
    #     'lib_announce': announce_sum,
    #     'status': 1,
    #     'description': 'success'
    # }
    # return announce_sum
    job_info_sum_dict.update({'jobinfo': job_info_list})

    # write json to file
    with open('./jobjson.txt', 'a+', encoding='utf-8') as json_file:
        json_file.write(str(job_info_sum_dict) + '\n')

    return job_info_sum_dict


if __name__ == "__main__":
    # 写入csv首行
    with open('./jobdata.csv', 'a+', newline='', encoding='utf-8-sig') as csv_file_title:
        writer = csv.writer(csv_file_title)
        writer.writerow(['result_name','result_providesalary_text','area','experence',
                         'education','belongs','keywords','category_line','category','job_detail','jobwelf_list','result_time'])

    getJobInfo()

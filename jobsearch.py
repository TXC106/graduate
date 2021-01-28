# -*- coding: utf-8 -*-
# @Time : 2021/1/27
# @Author : kiwi
# @File : jobsearch.py
# @Project : spider
import requests
import re
from bs4 import BeautifulSoup

def getJobInfo():
    url_Announce = 'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25AE%25A1%25E7%25AE%2597%25E6%259C%25BA,2,1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
    }
    try:
        resp = requests.get(url_Announce, headers=headers)
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
    while page_num <= sum_num:
        url_Announce = 'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25AE%25A1%25E7%25AE%2597%25E6%259C%25BA,2,{}.html'.format(page_num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/77.0.3865.120 Safari/537.36'
        }
        resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'gbk'

        # 获得总结果
        result = re.findall('engine_search_result\":\[(.*?),\"adid\":\"\"}\],', resp.text, re.I)[0]
        add_text = ',"adid":""}'
        # print(result+add_text)
        result_full = result+add_text
        result_full = result_full.split('},{')

        # 每条结果对应详情
        i = 0
        end_add = '}'
        while i < len(result_full):
        # while result_full[i] != None:
            print('==================================')
            # print(result_full[i] + end_add) # 首页展示信息

            print(i)
            result_full_now = result_full[i]
            # 获得详情页面链接
            result_urls = re.findall('"job_href":"(.*?)","job_name"', result_full_now, re.I)[0]
            result_urls_text = re.sub(r'\\', '', result_urls)
            print(result_urls_text)

            # 获得首页信息
            print('--------首页信息------')
            try:
                # print(result_full_now)
                result_name = re.findall('"job_name":"(.*?)",', result_full_now, re.I)[0]
                result_name = re.sub(r'\\','',result_name)
                print('result_name:'+result_name)
                # print(result_full_now)
                result_providesalary_text = re.findall('"providesalary_text":"(.*?)","workarea"', result_full_now, re.I)[0]
                result_attribute_text = re.findall('"attribute_text":(.*?),"companysize_text"', result_full_now, re.I)[0]
                print('result_providesalary_text:'+result_providesalary_text)
                print('result_attribute_text:'+result_attribute_text)
            except:
                i = i + 1
                continue
                # print(i)

            # 获得详情界面信息
            print('==================detail========================')
            resp_detail = requests.get(result_urls_text, headers=headers)
            resp_detail.encoding = 'gbk'
            # print(resp_detail.text)

            try:
                belongs = re.findall('所属部门：<\/span>(.*?)<br \/>', resp_detail, re.I)[0]
                print('=================所属部门======================')
                print('所属部门'+belongs)
            except:
                print('no info')

            soup = BeautifulSoup(resp_detail.text, 'lxml')
            detail = str(soup.find('div', class_='tCompany_main'))
            # print(detail)
            t_num = 0
            for t in soup.findAll(name='a', attrs={'class': 'el tdn'}):
                # print(t.span.text)
                # print(t.a.get('href'))
                # print(t.a.text)
                # print(t.get('href'))
                if t_num == 0:
                    print('==========职能类别=========')
                    print(t.get('href'))
                    print(t.text)
                    t_num = t_num + 1
                else:
                    print('============关键字===============')
                    print(t.get('href'))
                    print(t.text)
                    t_num = t_num + 1
            if t_num == 1:
                print('============关键字===============')
                print('no key words')


                # print(t)
            i = i + 1
            print(i)
            print('=============================')

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
        page_num += 1
    exit()
    # print(announce_sum)
    announce_sum = {
        'lib_announce': announce_sum,
        'status': 1,
        'description': 'success'
    }
    return announce_sum


if __name__ == "__main__":
    getJobInfo()

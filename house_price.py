#合肥市房价信息爬取 网站：安居客 参考：python爬取房天下
import requests
import parsel
import csv
import time
import json
'''
1.获取url地址
2.python代码发送指定地址的请求
3.数据提取
4.数据保存
'''
#区名:对应页数
area_name = {'baohequ':3,'yaohaiqu':3,'shushanqu':3,'xinzhanqu':2,'luyangqu':2,'jingjikaifaqu':2,'gaoxinqu':2,'zhengwuqu':1}
for name in area_name.keys():
    page_range = area_name[name] #页数
    url = 'https://hf.fang.anjuke.com/loupan/'+name+'/' #例如 https://hf.fang.anjuke.com/loupan/baohequ/
    for page in range(1,page_range+1):
        if page == 1:
            url = url
        else:
            url = url+'p'+str(page)

        #请求伪装, headers是一个字典
        headers = {
            #user-agent 浏览器的身份标识
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }
        #发送地址请求
        res = requests.get(url=url, headers=headers) #post put delete
        # print(res.text)
        #断言
        # 断言状态码是否为200
        assert res.status_code == 200

        # # 将响应内容转换为JSON格式
        # response_json = json.loads(res.text)
        # 
        # # 断言响应内容中title字段是否为"json-server"
        # assert response_json['title'] == 'json-server'

        # 断言响应时间是否小于1秒
        assert res.elapsed.total_seconds() < 1


        # print(res) #<Response [200]>
        html_text = res.text #请求返回对象的文本内容
        # print(html_text)

        #数据提取 css + xpath + 正则表达式 bs4 lxml
        selector = parsel.Selector(html_text) #把字符串转换为对象
        # print(selector) #<Selector xpath=None data='<html>\n<head>\n<meta charset="utf-8">\n...'>
        divs = selector.xpath('//div[@class="key-list imglazyload"]/div') #获取所有房源div
        for div in divs:
            #xpath提取房源标题
            item_name = div.xpath('.//div/a[@class="lp-name"]/span[@class="items-name"]/text()').get()
            #xpath提取房源周边均价
            around_price = div.xpath('./a[@class="favor-pos"]/p[@class="favor-tag around-price"]/span/text()').get()
            price = div.xpath('./a/p/span/text()').get()
            if around_price != None or price != None:

                if around_price == None:
                    #沙皮判断方式 是none说明这房子是在售房 它的tag是价格而不是周边均价
                    if price == None: #售价待定 不输出
                        pass
                    else:
                        price_res = price #要显示的是price
                else:#否则就是待售房 输出周边均价完事
                    price_res = around_price
                print(item_name, price_res)
                #4.保存到csv文件中
                csv_name = name+'.csv'
                # print(csv_name)
                with open(csv_name, mode='a', encoding='utf-8', newline='') as f:
                    '''
                    追加的方式写入baohequ.csv shushanqu.csv yaohaiqu.csv luyangqu.csv jingkaiqu.csv
                                gaoxinqu.csv zhengwuqu.csv
                    '''
                    csv_writer = csv.writer(f) #实例化写入对象
                    csv_writer.writerow([item_name, price_res]) #写入房源名称 价格
        #爬一页停止五秒
        time.sleep(5)


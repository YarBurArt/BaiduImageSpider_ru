#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import os
import re
import sys
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# задержка отправки пакетов
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # период задержки
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    # потенциальный косяк, баиду может принять паука за бота
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0', 'Cookie': ''}
    __per_page = 30

    # получить url содержимого изображения и т.д.
    # t интервал между изображениями
    def __init__(self, t=0.1):
        self.time_sleep = t

    # имя суффикса, для определения формата
    @staticmethod
    def get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    @staticmethod
    def handle_baidu_cookie(original_cookie, cookies):
        """
        :param string original_cookie:
        :param list cookies:
        :return string:
        """
        if not cookies:
            return original_cookie
        result = original_cookie
        for cookie in cookies:
            result += cookie.split(';')[0] + ';'
        result.rstrip(';')
        return result

    # основная загрузка изображений
    def save_image(self, rsp_data, word):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # определяет следующее свободное имя файла в папке (тупо по номеру)
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['data']:
            try:
                if 'replaceUrl' not in image_info or len(image_info['replaceUrl']) < 1:
                    continue
                obj_url = image_info['replaceUrl'][0]['ObjUrl']
                thumb_url = image_info['thumbURL']
                url = 'https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=%s&thumburl=%s' % (urllib.parse.quote(obj_url), urllib.parse.quote(thumb_url))
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(obj_url)
                # смените юзер-агент и реферер для обхода ошибки доступа 403
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'),
                ]
                urllib.request.install_opener(opener)
                # ниже блок кода сохранения через системные либы
                filepath = './%s/%s' % (word, str(self.__counter) + str(suffix))
                urllib.request.urlretrieve(url, filepath)
                if os.path.getsize(filepath) < 5:
                    print("Загруженны битые файлы, пропускаем!")
                    os.unlink(filepath)
                    continue
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("возникло ошибка, можешь убить мой процесс")
                continue
            else:
                print("+ одно изображение, " + str(self.__counter) + " уже загруженно")
                self.__counter += 1
        return

    # получить урлык изображения и загрузить
    def get_images(self, word):
        search = urllib.parse.quote(word)
        # pn int количество изображений
        pn = self.__start_amount
        while pn < self.__amount:
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=%s&rn=%d&gsm=1e&1594447993172=' % (search, search, str(pn), self.__per_page)
            # установить заголовки для обхода 403
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                self.headers['Cookie'] = self.handle_baidu_cookie(self.headers['Cookie'], page.info().get_all('Set-Cookie'))
                rsp = page.read()
                page.close()
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # нарезать json
                rsp_data = json.loads(rsp, strict=False)
                if 'data' not in rsp_data:
                    print("Сработала защита от паучих лапок, сломанная лапка перезагруженна!")
                else:
                    self.save_image(rsp_data, word)
                    # pn - page , шагаем по пагинации
                    print("Следующая страница: " + str(pn))
                    pn += self.__per_page
        print("завершение загрузки")
        return

    def start(self, word, total_page=1, start_page=1, per_page=30):
        """
        запуск паучка
        :param word: ключевое слово
        :param total_page: количество страниц, которые необходимо просмотреть x per_page
        :param start_page: первая страница
        :param per_page: кол-во изображений на каждой странице
        :return:
        """
        self.__per_page = per_page
        self.__start_amount = (start_page - 1) * self.__per_page
        self.__amount = total_page * self.__per_page + self.__start_amount
        self.get_images(word)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--word", type=str, help="ключевое слово", required=True)
        parser.add_argument("-tp", "--total_page", type=int, help="количество страниц, которые необходимо просмотреть", required=True)
        parser.add_argument("-sp", "--start_page", type=int, help="первая страница", required=True)
        parser.add_argument("-pp", "--per_page", type=int, help="кол-во изображений на каждой странице", choices=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], default=30, nargs='?')
        parser.add_argument("-d", "--delay", type=float, help=" задержка между запросами (интервал)", default=0.05)
        args = parser.parse_args()
        # передача ответов на паучьи вопросы, начало работы 
        crawler = Crawler(args.delay)
        crawler.start(args.word, args.total_page, args.start_page, args.per_page)  # 抓取关键词为 “美女”，总数为 1 页（即总共 1*60=60 张），开始页码为 2
    else:
        # 如果不指定参数，那么程序会按照下面进行执行
        crawler = Crawler(0.05)  # 抓取延迟为 0.05
        # это лучше самому увидеть на практике
        crawler.start('美女', 10, 2, 30)  # 抓取关键词为 “美女”，总数为 1 页，开始页码为 2，每页30张（即总共 2*30=60 张）
        # crawler.start('二次元 美女', 10, 1)  # 抓取关键词为 “二次元 美女”
        # crawler.start('帅哥', 5)  # 抓取关键词为 “帅哥”

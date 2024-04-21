# ГрафическийПаучекБаиду
Паучек для загрузки изображений по ключевым словам через Baidu, основанный на python3

Для личного обучения и творчества

Ползание по изображениям Baidu пока что одной лапкой.

# Паучьи требования

**Установленный python версии >= 3.6**

# Использование
```
$ python crawling.py -h
usage: crawling.py [-h] -w WORD -tp TOTAL_PAGE -sp START_PAGE
                   [-pp [{10,20,30,40,50,60,70,80,90,100}]] [-d DELAY]

optional arguments:
  -h, --help            показать это сообщение помощи 
  -w WORD, --word WORD  ключевое слово (на китайском либо перевод)
  -tp TOTAL_PAGE, --total_page TOTAL_PAGE
                        количество страниц, которые необходимо просмотреть
  -sp START_PAGE, --start_page START_PAGE
                        первая страница
  -pp [{10,20,30,40,50,60,70,80,90,100}], --per_page [{10,20,30,40,50,60,70,80,90,100}]
                        количество изображений на странице
  -d DELAY, --delay DELAY
                        задержка между запросами (интервал)
```

Запуск поиска изображений (в примере ищет котиков 猫 / Māo, на скрине ищет девущек по своему паучьему вкусу, но с учётом великого китайского фаервола)
```
python crawling.py --word "猫" --total_page 10 --start_page 1 --per_page 30
```
(пока что ищет только на китайском)

Также вы можете изменить ключевое слово поиска в самой строке `crawling.py`.
По умолчанию изображения сохраняются в пути проекта + слово поиска

Запустите поисковик:
``` python
python crawling.py
```

# Записи в блоге автора (имя вроде Цзян Вэйлун)

[кратко использование / как работает](http://www.jwlchina.cn/2016/02/06/python%E7%99%BE%E5%BA%A6%E5%9B%BE%E7%89%87%E7%88%AC%E8%99%AB/)

Примерно что в итоге получится：
![效果图](http://blog-image.jwlchina.cn/kong36088/kong36088.github.io/master/uploads/python%E5%9B%BE%E7%89%87%E7%88%AC%E8%99%AB%E6%88%AA%E5%9B%BE.png)

# задонатить автору на развитие этого чуда 

Спасибо！
![wechatpay](http://blog-image.jwlchina.cn/kong36088/kong36088.github.io/master/uploads/site/wechat-pay.png)
![alipay](http://blog-image.jwlchina.cn/kong36088/kong36088.github.io/master/uploads/site/zhifubao.jpg)


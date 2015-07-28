#===istalismanplugin===
# -*- coding: utf-8 -*-

# (C) Gigabyte
# * Распространять без указания ссылки на ресурс и автора ЗАПРЕЩЕНО!
# * Применимо только в личных целях, никакой коммерции!!!

import urllib, re

def tags_code(text):
    return text.replace('<p align="left">', u'').replace('<p>', u'').replace('<p>', u'').replace('</p>', u'').replace('&mdash;', u' — ').replace('&nbsp;', ' ').replace('&laquo;', u'«').replace('&raquo;', u'»')

def get_detail_news(url):

    sh = u'<div class="bold"><p>(.*)</p></div>'

    sh1 = u'<div>(.*)</div>'

    sh2 = u'.*<a href=".page=(.*)" class="f7">След.</a>'
    
#    r = urllib.urlopen('http://wap.news.mail.ru.sixxs.org%s' % (url))
    r = urllib.urlopen('http://news.yandex.ru.sixxs.org%s' % (url))
    target = unicode(r.read(), 'utf-8')
    r.close()
    m = re.findall(sh2, target )

    TXT = {'subject':None, 'body':[]}
    TXT['subject'] = tags_code( re.findall(sh, target)[0] )

    mas = []

    mas.append( tags_code(re.findall(sh1, target)[1]) )
    
    while len(m)>0:
        r = urllib.urlopen('http://wap.news.mail.ru.sixxs.org%s?page=%s' % (url, m[0]))
        target = unicode(r.read(), 'utf-8')
        r.close()

        mas.append( tags_code(re.findall(sh1, target)[1]) )
        
        m = re.findall(sh2, target )


    TXT['body'] = mas

    return TXT

def get_last_news():
#    bb = u'<div class="inner" style="font-family:Tahoma;	font-size:10pt;">'
	bb = u'<table class="b-news-hot">'
#    ee = u'<br />'
	ee = u'</div></td><td class="l-page-main-r"><div class="h-page-main-r"><div class="b-news b-news-regions">'
#    sh = u'<a href="(.*)"><img src=".*" class="img_news" alt="" /></a><div style="padding-bottom:3px;"><a href="(.*)">(.*)</a>'

#    sh2 = u"""<div style="padding-bottom:3px;"><a href="(.*)">(.*)</a>"""
	sh2 = u"""<a class="title" href="(.*)" .*onclick.*>(.*)</a> <span class"""

#    r = urllib.urlopen('http://wap.news.mail.ru.sixxs.org/')
	r = urllib.urlopen('http://news.yandex.ru.sixxs.org/')
	target = r.read()
	r.close()

	od = re.search(bb, target)
	b1 = target[od.end():]
	b1 = b1.replace('"><!--beg_','">')
	b1 = b1.replace('"><!--end_','">')
	b1 = b1[:re.search(ee, b1).start()]
	
	m = re.findall(sh2, b1)

	NEWS = {}
	for j, NEW in enumerate(m):
		NEWS[j+1] = {'text':tags_code(unicode(NEW[1], 'utf-8')), 'link':NEW[0].replace('" class="bold', '')}
	
	return NEWS


def get_l_n(t, s, b):
    if b =='info':
        news_help(t, s, b)
        return
    NEWS = get_last_news()

    if not b:
        out = ''
        for nw in NEWS:
            out+=u'%i. %s\n' % (nw, NEWS[nw]['text'])
        else:
            if out == '':
                reply(t, s, u'Ошибка. Обратитесь к владельцу бота')
            else:
                reply(t, s, out)
    else:
        try:
            ind = int(b)
        except:
            reply(t, s, u'Ошибка. Номер должен быть цифрами')
            return
        if ind in NEWS:
            NEW = get_detail_news( NEWS[ind]['link'] )
            o = ''
            for i in NEW['body']:
                o+=i+'\n'
            out = u'%s\n* * * * * * *\n%s' % (NEW['subject'], o)
            if t != 'private':
		reply(t, s, u'Журналюги те всё в привате обрисовали')
            reply('private', s, out)
        else:
            reply(t, s, u'Ошибка. Данной статьи нет')
        

def news_help(t, s, b):
        out = u"""Новости v0.001
(C) CEP}|{

Новости забираются с http://news.yandex.ru/"""
        reply(t, s, out)

register_command_handler(get_l_n, 'новости', ['инфо','все'], 10, '(c) CEP}|{\nПоказывает сводку новостей по России с ресурса mail.ru, чтобы узнать подробности введите новости и номер интересующей новости. ВНИМАНИЕ! Порой сыпет огромные многостраничные новости ;-)', 'новости [номер новости]', ['новости', 'новости 5'])

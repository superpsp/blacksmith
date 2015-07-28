#===istalismanplugin===
# -*- coding: utf-8 -*-

# author ferym@jabbim.org.ru
# yandex search beta version plugin 1.0-beta
# for only http://jabbrik.ru

# update, fix parse html code


def handler_yandex(type, source, parameters):
#		try:
				if parameters:
#						req = urllib2.Request('http://yandex.ru.sixxs.org/msearch?s=all&query='+parameters.encode('utf-8').replace(' ','%20').replace('@','%40'))
						link = 'http://yandex.ru.sixxs.org/msearch?text='+parameters.encode('utf-8').replace(' ','%20').replace('@','%40') + '&lr=10'
						link = 'http://yandex.ru/msearch?text='+parameters.encode('utf-8').replace(' ','%20').replace('@','%40') + '&lr=10'
#						req.add_header = ('User-agent', 'Mozilla/5.0')
						r = urllib.urlopen(link)
						target = r.read()
						od = re.search('<li >',target)
						message = target[od.end():]
						message = message[:re.search('</span>',message).start()]
						message = '\n' + message.strip()
#						reply('private', source, '2 '+message)
#						message = message.replace('<a href="','ссылка на источник: ').replace('" target="_blank">','\n').replace('</a>','').replace('</div>','').replace('<b>','').replace('</b>','').replace('<br/>',' ').replace('<br>',' ').replace('<div class="info">',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('<span class="b-results__text">','').replace('.sixxs.org','')
						message = message.replace('<a href="','ссылка на источник: ').replace('" target="_blank">','\n').replace('</a>','').replace('</div>','').replace('<b>','').replace('</b>','').replace('<br/>',' ').replace('<br>',' ').replace('<div class="info">',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('<span class="b-results__text">','')
						reply(type, source, unicode(message,'UTF-8'))
				else:
						reply(type, source, u'а что искать то?')
#		except:
#				reply(type, source, u'По вашему запросу ничего не найдено')

register_command_handler(handler_yandex, 'yandex', ['все','mod','инфо'], 10, 'Поиск в yandex', 'yandex <запрос>', ['yandex jabbrik\nby ferym'])
register_command_handler(handler_yandex, 'яндекс', ['все','mod','инфо'], 10, 'Поиск в yandex', 'яндекс <запрос>', ['яндекс jabbrik\nby ferym'])
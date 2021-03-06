# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  quotes_plugin.py

# Some of ideas and part of code:
#  Gigabyte (gigabyte@ngs.ru)
#  ferym (ferym@jabbim.org.ru)
# --> http://jabbrik.ru/
# Coded By:
#  WitcherGeralt (WitcherGeralt@jabber.ru)
#  *MAG* (admin@jabbon.ru)
# --> http://witcher-team.ucoz.ru/

strip_tags = re.compile(r'<[^<>]+>')

def url_dec(body):
	body = strip_tags.sub('', replace_all(body, {'<br />': ' ', '<br>': '\n'}))
	body = replace_all(body, {'&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"', '\t': '', '||||:]': '', '>[:\n': '', '&deg;': '°'})
	return body.strip()

def handler_bashorgru(type, source, body):
	try:
		if body:
			site = read_url('http://bash.org.ru/quote/%s' % (body), 'Mozilla/5.0')
#			site = read_url('http://bash.org.ru.sixxs.org/quote/%s' % (body), 'Mozilla/5.0')
		else:
			site = read_url('http://bash.org.ru/random', 'Mozilla/5.0')
#			site = read_url('http://bash.org.ru.sixxs.org/random', 'Mozilla/5.0')
		od = re.search(r'<div class="q">.*?<div class="vote">.*?</div>.*?<div>(.*?)</div>.*?</div>', site, re.DOTALL)
		b1 = strip_tags.sub('', re_search(site, '<div class="vote">', '</a>').replace('\n', ''))
		repl = replace_all('%s\n%s' % (b1, od.group(1)), {'&nbsp;': ' ', '<br />': '\n', '&lt;': '<', '&gt;': '>', '&quot;': '"', '\t': '', '||||:]': '', '>[:\n': '', '&deg;': '°', '<br>': '\n', '\n\n\n': '\n', '\n\n': '\n'}).strip()
		reply(type, source, 'http://bash.org.ru/quote/%s' % (unicode(repl, 'windows-1251')))
	except:
		reply(type, source, u'очевидно, они опять сменили разметку')

def handler_nyash(type, source, body):
	try:
#		target = read_url('http://nya.sh/', 'Mozilla/5.0')
		target = read_url('http://nya.sh.sixxs.org/', 'Mozilla/5.0')
#		b1 = re_search(target, '<div align="right" class="sm"><a href="/', '"><b>')
		b1 = u"""<div align="right" class="sm"><a href="/post/([0-9]*)"><b>"""
		a = re.findall(b1, target)
#		post = random.randrange(1, int(b1.split('/')[1]))
		post = int(a[(random.randrange(0, len(a)-1))])
#		post = int(b1)
#		target = read_link('http://nya.sh.sixxs.org/post/%d' % (post))
		target = read_link('http://nya.sh/post/%d' % (post))
#		b1 = re_search(target, '</a></div><div class="content">', '</div>')
		b1 = re_search(target, '</a></div></noindex><div class="content">', '</div>')
		reply(type, source, u'Цитата #%d:\n%s' % (post, unicode(url_dec(b1), 'windows-1251')))
	except:
		reply(type, source, u'Поломка на сайте')

def handler_ithappens(type, source, body):
	try:
		target = read_url('http://ithappens.ru/', 'Mozilla/5.0')
#		target = read_url('http://ithappens.ru.sixxs.org/', 'Mozilla/5.0')
		b1 = re_search(target, '<h3><a href="/', '">')
		post = random.randrange(1, int(b1.split('/')[1]))
		target = read_link('http://ithappens.ru/story%d' % (post))
#		target = read_link('http://ithappens.ru.sixxs.org/story%d' % (post))
		b1 = re_search(target, '<p class="text">', '</p>')
		reply(type, source, u'Цитата #%d:\n%s' % (post, unicode(url_dec(b1), 'windows-1251')))
	except:
		reply(type, source, u'повторите запрос')

def handler_sonnik(type, source, body):
	if body:
		try:
			target = read_url('http://sonnik.ru/search.php?key=%s' % (body.encode('windows-1251')), 'Mozilla/5.0')
#			target = read_url('http://sonnik.ru.sixxs.org/search.php?key=%s' % (body.encode('windows-1251')), 'Mozilla/5.0')
#			data = re_search(target, '</p><br><p class="smalltxt"><strong>', '<br><strong>')
			data = re_search(target, '<p class="smalltxt"><strong>', ' <br><strong>')
			data1 = re_search(data, 'html">', '</a>')
#			data2 = re_search(target, '<title>', '</title>')
			data2 = re_search(target, '<h1 class="hr" title="', '">')
			data3 = re_search(target, '<p>', '</p>')
#			reply(type, source, u'Тема: %s\n%s\n%s' % (unicode(data1, 'windows-1251'), unicode(data2, 'windows-1251'), unicode(data3, 'windows-1251')))
			if type == 'public':
					reply(type, source, u'Я в привате оракулом поработал...')
#			reply('private', source, u'Тема: %s\n%s\n%s' % (unicode(data1, 'windows-1251'), unicode(data2, 'windows-1251'), unicode(data3, 'windows-1251')))
			reply('private', source, u'Тема: %s\n%s\n%s' % (data1, data2, data3))
		except:
			reply(type, source, u'Странные у тебя сны... Нет такого в соннике!')
	else:
		reply(type, source, u'Введи ключевое слово сна')

def handler_anek(type, source, body):
	try:
		list = re_search(read_link('http://www.hyrax.ru/cgi-bin/an_java.cgi'), 'td aling=left><br>', '</td></tr></table>').split('<br><br><hr>')
#		list = re_search(read_link('http://www.hyrax.ru.sixxs.org/cgi-bin/an_java.cgi'), 'td aling=left><br>', '</td></tr></table>').split('<br><br><hr>')
		list.pop(3)
		anek = u'Анекдот:\n%s' % unicode(random.choice(list), 'windows-1251')
		reply(type, source, replace_all(anek, {'<br>': '', '&nbsp;&nbsp;&nbsp;&nbsp;': '\n', '&nbsp;': '', '\n\n': '\n'}).strip())
	except:
		reply(type, source, u'что-то сломалось...')

def handler_afor(type, source, body):
	try:
		data = re_search(read_url('http://skio.ru/quotes/humour_quotes.php', 'Mozilla/5.0'), '<form id="qForm" method="post"><div align="center">', '</div>')
#		data = re_search(read_url('http://skio.ru.sixxs.org/quotes/humour_quotes.php', 'Mozilla/5.0'), '<form id="qForm" method="post"><div align="center">', '</div>')
		data = strip_tags.sub('', replace_all(data, {'<br />': '\n', '<br>': '\n'}))
		reply(type, source, unicode(data, 'windows-1251'))
	except:
		reply(type, source, u'что-то сломалось...')

def handler_pyorg(type, source, body):
	try:
		data = re_search(read_link('http://python.org/'), '<h2 class="news">', '</div>')
#		data = re_search(read_link('http://python.org.sixxs.org/'), '<h2 class="news">', '</div>')
		data, repl = replace_all(strip_tags.sub('', data.replace('<br>','\n')), {'&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&quot;': '"', '<br />': '\n', '<li>': '\r\n'}).strip(), '\n'
		for line in data.splitlines():
			if line.strip():
				repl += '%s\r\n' % (line)
		reply(type, source, unicode(repl, 'koi8-r'))
	except:
		reply(type, source, u'что-то сломалось...')

HORO_SIGNS = {u'день': 0, u'овен': 1, u'телец': 2, u'близнецы': 3, u'рак': 4, u'лев': 5, u'дева': 6, u'весы': 7, u'скорпион': 8, u'стрелец': 9, u'козерог': 10, u'водолей': 11, u'рыбы': 12}

def handler_horo(type, source, body):
	if body:
		body, number = body.lower(), None
		if body in [u'хелп', 'help']:
			reply(type, source, '\n'+'\n'.join(sorted(['%s - %d' % (x, y) for x, y in HORO_SIGNS.iteritems()])))
		else:
			if HORO_SIGNS.has_key(body):
				number = HORO_SIGNS[body]
			elif check_number(body):
				chislo = int(body)
				if -1 < chislo < 13:
					number = chislo
			if number != None:
				try:
					data = re_search(read_link('http://www.hyrax.ru/cgi-bin/bn_html.cgi'), '<!-- %d --><b>' % (number), '<br><br>')
#					data = re_search(read_link('http://www.hyrax.ru.sixxs.org/cgi-bin/bn_html.cgi'), '<!-- %d --><b>' % (number), '<br><br>')
					horo = replace_all(data, [' </b><br>', '</b><br>'], ':')
					repl = unicode(horo, 'windows-1251')
				except:
					repl = u'что-то сломалось...'
				reply(type, source, repl)
			else:
				reply(type, source, u'не понимаю')
	else:
		reply(type, source, u'введи знак')

def handler_jabber_quotes(type, source, body):
	if body:
		body = body.lower()
	if body in [u'ранд', 'rand']:
		link = 'http://jabber-quotes.ru/random'
#		link = 'http://jabber-quotes.ru.sixxs.org/random'
	elif body in [u'топ20', 'top20']:
		link = 'http://jabber-quotes.ru/up'
#		link = 'http://jabber-quotes.ru.sixxs.org/up'
	else:
		link = 'http://jabber-quotes.ru/'
#		link = 'http://jabber-quotes.ru.sixxs.org/'
	try:
		list = read_link(link).split('<blockquote>')
		list.pop(0)
		quote = random.choice(list).split('</blockquote>')[0]
		quote = replace_all(quote, {'<br>': '\n', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&amp;': '&', '&middot;': ';'})
		while quote.count('\n\n\n'):
			quote = quote.replace('\n\n\n', '\n\n')
		reply(type, source, 'Quote:\n%s' % unicode(quote, 'windows-1251'))
	except:
		reply(type, source, u'что-то сломалось...')

register_command_handler(handler_pyorg, 'питон', ['фан','все'], 10,'показывает последнии новости с http://python.org/', 'питон', ['питон'])
register_command_handler(handler_afor, 'афоризм', ['фан','все'], 10,'показывает случайный афоризм с ресурса skio.ru', 'афор', ['афор'])
register_command_handler(handler_anek, 'анек', ['все', 'фан'], 10, 'Отображает анекдоты с ресурса http://www.hyrax.ru/\nBy *MAG*', 'анек', ['анек'])
register_command_handler(handler_bashorgru, 'баш', ['фан','все'], 10, 'Показывает случайную цитату (или по номеру) с баш.орг', 'баш', ['баш','баш 3557'])
register_command_handler(handler_nyash, 'няш', ['фан','все'], 10, 'Показывает случайную цитату из НЯШа .', 'няш', ['няш'])
register_command_handler(handler_ithappens, 'ит', ['фан','все'], 10, 'Показывает случайную цитату с http://ithappens.ru/', 'ит', ['ит'])
register_command_handler(handler_sonnik, 'сон', ['фан','все'], 10, 'Сонник.', 'сон', ['сон вода'])
register_command_handler(handler_horo, 'хоро', ['фан','все'], 10, 'Гороскоп "на сегодня" с сайта http://www.hyrax.ru/\nЧтобы посмотреть общую характеристику дня используем параметр - "день"\nВместо знака можно вводить число (пишем: "хоро хелп")\nBy *MAG* & WitcherGeralt for http://witcher-team.ucoz.ru/', 'хоро [знак]', ['хоро 11','хоро день', 'хоро овен'])
register_command_handler(handler_jabber_quotes, 'цитата', ['фан','все'], 10, 'Достаёт цитату с http://jabber-quotes.ru/\nПараметры:\nТоп20 - выбирает 1 из самых популярных\nРанд - абсолютно случайная цитата\nБез параметров - выбирает из 20ти новейших', 'цитата [топ20/ранд]', ['цитата','цитата топ20'])

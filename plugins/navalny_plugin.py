#===istalismanplugin===
# -*- coding: utf-8 -*-

# (C) CEP}|{
# * Распространять без указания ссылки на автора ЗАПРЕЩЕНО!
# * Применимо только в личных целях, никакой коммерции!!!

import urllib, re

def get_detail_themes(url):

#	url = 'http://navalny.livejournal.com.sixxs.org/' + url + '.html'
	url = 'http://navalny.livejournal.com/' + url + '.html'
	r = urllib.urlopen(url)
	target = unicode(r.read(), 'utf-8')
	r.close()
	
#	TXT = u'Ссылка: ' + url.replace('.sixxs.org','') + '\n\n'
	TXT = u'Ссылка: ' + '\n\n'
	TXT = TXT + u'Тема: ' + re.findall(u"""name="title" content="(.*)" />""", target)[0].replace('&quot;', '') + '\n\n'
#	TXT = TXT + re.findall(u"""\,"description":"(.*)"}\);</script>""", target)[0].replace('&nbsp;', '').replace("""\\\&quot;""", '"').replace('amp;', '').replace('&ndash;', '-').replace('&laquo;', '"').replace('&raquo;', '"').replace ('.sixxs.org', '')
	TXT = TXT + re.findall(u"""\,"description":"(.*)"}\);</script>""", target)[0].replace('&nbsp;', '').replace("""\\\&quot;""", '"').replace('amp;', '').replace('&ndash;', '-').replace('&laquo;', '"').replace('&raquo;', '"')

	return TXT

def get_themes():
	bb = u'</tbody></table></dd>\n                    </dl>\n\n                            <dl class="sidebar-block sidebar-summary">\n                                <dt>Page Summary</dt>\n                                <dd>\n                                    \n    <ul>\n'
	ee = u'\n    </ul>\n\n                                </dd>\n                            </dl>\n<div class='
	patsplit = u'<li><a'
#	linkfind = u""" href="#post-navalny-(.*)">.*</a>\xa0<span class="emdash">\u2014</span> <a class="summary-comments" href="http://navalny.livejournal.com.sixxs.org/.*.html">.* comments</a></li>"""
	linkfind = u""" href="#post-navalny-(.*)">.*</a>\xa0<span class="emdash">\u2014</span> <a class="summary-comments" href="http://navalny.livejournal.com/.*.html">.* comments</a></li>"""
#	textfind = u""" href="#post-navalny-.*">(.*)</a>\xa0<span class="emdash">\u2014</span> <a class="summary-comments" href="http://navalny.livejournal.com.sixxs.org/.*.html">.* comments</a></li>"""
	textfind = u""" href="#post-navalny-.*">(.*)</a>\xa0<span class="emdash">\u2014</span> <a class="summary-comments" href="http://navalny.livejournal.com/.*.html">.* comments</a></li>"""

#	r = urllib.urlopen('http://navalny.livejournal.com.sixxs.org/')
	r = urllib.urlopen('http://navalny.livejournal.com/')
	target = r.read()
	r.close()
	target = unicode(target,'utf-8')

	od = re.search(bb, target)
	b1 = target[od.end():]
	b1 = b1[:re.search(ee, b1).start()]

	a = b1.split(patsplit)

	THEMES = {}
	for i in range(1, len(a)-1):
		THEMES[i] = {'text': re.findall(textfind, a[i])[0], 'link': re.findall(linkfind, a[i])[0]}

	return THEMES

def navalny_handler(type, source, body):
	if body =='info':
		navalny_help(type, source, body)
		return

	THEMES = get_themes()

	if body:
		try:
			ind = int(body)
		except:
			reply(type, source, u'Ошибка. Номер должен быть цифрами!')
			return
		if ind in THEMES:
			THEME = get_detail_themes(THEMES[ind]['link'])
			t = type
			if type == 'public':
				reply(type, source, u'Смотри про партию жуликов и воров в привате!')
				t = 'private'
			reply(t, source, THEME)
		else:
			reply(type, source, u'Ошибка! Данной темы нет!')
	else:
		if len(THEMES) < 11:
			limit = len(THEMES)
		else:
			limit = 11
		out = ''
		for th in range(1, limit):
			out += u'%i. %s\n' % (th, THEMES[th]['text'])
		if out == '':
			reply(type, source, u'Ошибка. Обратитесь к владельцу бота!')
			return
		out1 = ''
		for th in range(limit, len(THEMES)):
			out1 += u'%i. %s\n' % (th, THEMES[th]['text'])
		if type == 'public':
			reply(type, source, out)
			reply(type, source, u'Остальные темы смотри в привате!')
			reply('private', source, out1)
		else:
			out = out + out1
			reply(type, source, out)

def navalny_help(type, source, body):
	out = u"""Проект Навального v1.00fpv - first public version\n(C) CEP}|{\nmail: superpsp@mail.ru\nxmpp:\nrabota_работа@conference.qip.ru\n\nНовости с проекта Навального\nhttp://navalny.livejournal.com/"""
	reply(type, source, out)

register_command_handler(navalny_handler, 'навальный', ['инфо','все'], 10, '(C) CEP}|{\nПоказывает темы проекта navalny.livejournal.com, направленного на борьбу с партией жуликов и воров (т. н. единая россия), чтобы узнать подробности введите навальный и номер интересующей темы. ВНИМАНИЕ! Порой сыпет огромные многостраничные темы ;-)', 'навальный [номер темы]', ['навальный', 'навальный 5'])

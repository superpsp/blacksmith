#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  weather_plugin.py

# (C) Gigabyte
# Сайт:   http://www.jabbrik.ru/
# Конфа:  stalker@conference.jabbrik.ru
# e-mail: gigabyte@ngs.ru
#
# После очередного изменения на сайте http://m.gismeteo.ru

import urllib, re

def weather_gis_search(type, source, parameters):
	if not parameters:
		reply(type, source, u'Команда без параметров не допускается. Наберите: хелп погода.')
		return
	parameters = parameters.strip()
	if re.findall(u'[а-яА-Я]+[^\.]\**$', parameters):	# Force search
		parameters = parameters + '.'
	if parameters == u'инфо':
		reply(type, source, u'Наберите: хелп погода' )
	elif parameters != re.findall(u'[а-яА-Я\d\.\*\- ]*', parameters)[0]:
		reply(type, source, u'В параметрах команды обнаружен недопустимый символ. Допускаются только: русские буквы, цифры, пробел, дефис, точка, звёздочка. Наберите: хелп погода.' )
	elif re.findall(u'[\.\*][^\.\*]', parameters):
		reply(type, source, u'В параметрах команды после точки(звёздочки) не допускаются какие-либо символы. Наберите: хелп погода.' )
	else:
		first_city = 0
		tomorrow = None
		while parameters[-1] in ['.', '*']:
			if parameters[-1] == '.':
				first_city = 1
			elif parameters[-1] == '*':
				tomorrow = 1
			parameters = parameters[0:-1]
		parameters = parameters.strip()
		if re.findall(u'[^\d]', parameters):
			first_city = 1	# Force search
		try:
			body = weather_gis_get(parameters, first_city)
			if body == 'No':
				reply(type, source, u'По вашему запросу <%s>, ничего не найдено. Если Вы задавали <код_города>, точка НЕ ДОПУСКАЕТСЯ' % (parameters))
			else:
				if type == 'public':
					reply(type, source, u'Я те в привате весь гидромедцентр собрал')
				reply('private', source, weather_parcer(body, tomorrow) )
			return
		except:
			pass

def weather_gis_get(code, first_city):
	if first_city == 1:
		city = urllib.quote_plus(code.encode('utf-8'))
		link = 'https://www.gismeteo.ru/city/?gis20150723120123362=%s&searchQueryData=' % (city)
		f = urllib.urlopen(link)
		body = f.read()
		f.close()
		body = unicode(body,'utf-8')
		tmp = re.findall("""<li><a href="/city/daily/(.+)/"><span><b>.*?</b></span></a>""", body)
		if tmp:
			code = tmp[0]
		else:
			body = 'No'
			return body
	link = 'https://www.gismeteo.ru/city/daily/%s/' % (code)
	f = urllib.urlopen(link)
	body = f.read()
	f.close()
	body = unicode(body,'utf-8')
	return body

def weather_parcer(body, tomorrow):
	address = (body.split(u'<div class="scity"')[1]).split(u'</div>')[0]
	
	result = (address.split(u'rel="v:url" property="v:title">')[1]).split(u'</a></span>')[0]	#City
	for i in range(2, 4):
		result += ', ' + (address.split(u'rel="v:url" property="v:title">')[i]).split(u'</a></span>')[0]	#Region, Country
	
	date_and_time = (body.split(u'data-hr="">')[1]).split(u'</span>')[0]
	date_and_time = date_and_time.replace('\n', '').replace('\t', '')
	result += '\n' + u'Погода сейчас (по данным на ' + date_and_time + ')\:'
	
	current = '\t<div class="MyClass">\n' + (body.split(u'</span>\n\t</div>')[1]).split(u'"wrap f_link">')[0]
	i = 1
	while True:
		try:
			block = (current.split(u'<div ')[i]).split(u'</div')[0]
		except:
			break
		try:
			title = (block.split(u'title="')[1]).split(u'"')[0] + ' '
		except:
			title = ''
		try:
			value = re.findall(u""".*?class=.*?>(.+?)<span class=".+?">(.+?)<.*""", block)
			result += '\n' + title + value[0][0].replace('&deg;', '') + ' ' + value[0][1].replace('&deg;', '')
		except:
			result += '\n' + title
		i += 1
	if tomorrow:
		daily = (body.split(u'<tbody id="tbwdaily2"')[1]).split(u'</tbody>')[0]
		tmp = u'завтра'
	else:
		daily = (body.split(u'<tbody id="tbwdaily1"')[1]).split(u'</tbody>')[0]
		tmp = u'сегодня'
	date = (daily.split(u'id="wrow-')[1]).split(u'">')[0]
	date = date[:10]
	result += '\n' + u'Погода на ' + tmp + ' ' + date + ':'
	pattern = """<th title=".+?">\n\t\t(.+)\t</th>\n\t<td class=.+?</td>\n\t<td class="cltext">(.+)</td>\n\t<td class="temp"><span class='.*?'>(.+?)</span.*/td>\n\t<td><span class='.*?'>(.+?)</span.*/td>\n\t<td><dl class="wind"><dt class=".*?" title=".*?">(.+?)</dt.*?'>(.+?).*</td>\n\t<td>(.+?)</td>\n\t<td>.*?>(.+?)<.*td>"""
	value = re.findall(pattern, daily)
	result += '\n' + '\t' + u'Атмосферные' + '\t' + u'Tемпература' + '\t' + u'Атм. давл.,' + '\t' + u'Ветер,' + '\t' + u'Влажность' + '\t' + u'Ощущается,'
	result += '\n' + '\t' + u'явления' + '\t\t' + u'воздуха, °C' + '\t' + u'мм рт. ст.' + '\t' + u'м/с' + '\t' + u'воздуха, %' + '\t' + u'°C'
	for i in value:
		tmp = i[1].split(', ')
		result += '\n' + i[0] + '\t' + tmp[0].ljust(15, ' ') + '\t' + i[2] + '\t\t' + i[3] + '\t\t' + i[4].rjust(2, ' ') + ', ' + i[5] + '\t' + i[6] + '\t\t' + i[7]
		if len(tmp) > 1:
			result += '\n' + '\t' + tmp[1]
	return result

#weather_gis_get('4690')
#weather_gis_search('', '', u'усть-абакан')

register_command_handler(weather_gis_search, 'погода', ['инфо','все', 'new'], 10, 'Погода v6.0 (hotfix 24.07.2015 by CEP}|{)\nПоказывает погоду с ресурса gismeteo.ru', 'погода <город_русскими_буквами>\nпогода <город_русскими_буквами><.> (точка после города!!! - автоматически выберет самый подходящий город из региона)\nпогода <город_русскими_буквами><*> (звёздочка после города!!! - погода назавтра)\nпогода <код_города> (точка НЕ ДОПУСКАЕТСЯ, действие звёздочки аналогично описанному выше)\nТочку и звездочку можно применять вместе\nНаписал: Gigabyte\nИдея: ManGust\nИсправил: CEP}|{', ['погода Новосибирск', 'погода 4690'])

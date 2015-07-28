# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  BlackSmith plugin
#  hollydays_plugin.py

# Coded by: 40tman (40tman@qip.ru)

def handler_hollydays(type, source, body):
	try:
		data = read_url('http://wap.n-urengoy.ru/cgi-bin/wappr.pl', 'Mozilla/5.0')
#		data = read_url('http://wap.n-urengoy.ru.sixxs.org/cgi-bin/wappr.pl', 'Mozilla/5.0')
		data = re_search(data, '<div class="title">', 'назад')
		list = {'<': '', '.': '', '>': '', '/': '\n', '_': '', 'a': '', 's': '', 'd': '', ':': '', 'f': '', 'g': '', 'h': '', '=': '', '-': '', 'j': '', 'k': '', 'l': '', 'q': '', '%': '', 'w': '', 'e': '', 'r': '', 't': '', 'y': '', 'u': '', 'L': ' ', 'Q': ' ', 'W': ' ', 'E': '', 'H': '', 'K': ' ', 'Y': '', '<br/>': '\n', 'I': '', 'O': '', 'P': '', 'Z': '', 'X': '', 'C': '', 'V': '', 'B': '', 'N': '', 'M': '', ';': '', '[': '', ']': '', 'i': '', '"': '', 'o': '', 'p': '', 'z': '', 'x': '', 'c': '', 'v': '', '#': '', 'b': '', 'n': '', 'm': '', 'A': '', 'S': '', 'D': '', 'F': '', 'G': '', '\n\n\n': '\n\n'}
		data = replace_all(data, list).strip()
		reply(type, source, unicode('\n%s' % (data), 'UTF-8'))
	except:
		reply(type, source, u'По вашему запросу ничего не найдено')

register_command_handler(handler_hollydays, 'праздники', ['все','фан'], 10, 'Показывает праздники сегодня/завтра', 'праздники', ['праздники'])

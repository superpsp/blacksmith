# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  new_boltun_plugin.py

# Coded: by WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

BASE_LINES = eval(read_file('static/boltun/lines.txt'))

IDENT_BASE = 'static/boltun/ident_base.txt'
RAND_BASE = 'static/boltun/random_base.txt'

FLOOD = {}
MAFIA_REMOTE={}

def handler_get_reply(fraza):
	fraza = string.lower(fraza).strip()
	fi = open(IDENT_BASE, 'r')
	INFA['fr'] += 1
	while True:
		line = fi.readline()
		if not line:
			break
		base_fraza = unicode(line, 'utf-8')
		(key, otvet) = string.split(base_fraza, ' = ', 1)
		key = string.lower(key).strip()
		if fraza.count(key):
			if otvet.count('/'):
				list = otvet.split('/')
				otvet = random.choice(list)
			return otvet
	fr = open(RAND_BASE, 'r')
	INFA['fr'] += 1
	col = random.randrange(1, BASE_LINES)
	tryes = 0
	while True:
		tryes += 1
		rand_base_fraza = fr.readline()
		if tryes >= col:
			otvet = unicode(rand_base_fraza, 'utf-8')
			return otvet

def boltun_work(raw, type, source, body):
	if source[1] not in FLOOD or FLOOD[source[1]] != 'off':
		to_ret = random.randrange(1, 10)
		if to_ret != 7:
			bot_nick = handler_botnick(source[1])
			direct = Prefix_state(body, bot_nick)
			if direct:
				reply(type, source, handler_get_reply(body))
			elif type == 'private':
				jid=handler_jid(source[1]+'/'+source[2])
				if jid not in MAFIA_REMOTE.keys():
					reply(type, source, handler_get_reply(body))

def boltun_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/flood.txt'
			if body in [u'вкл', 'on', '1']:
				FLOOD[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'болталка включена')
			elif body in [u'выкл', 'off', '0']:
				FLOOD[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'болталка выключена')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if FLOOD[source[1]] == 'off':
				reply(type, source, u'сейчас болталка выключена')
			else:
				reply(type, source, u'сейчас болталка включена')
	else:
		reply(type, source, u'только в чате мудак!')

def boltun_work_init(conf):
	if check_file(conf, 'flood.txt', "'on'"):
		state = eval(read_file('dynamic/'+conf+'/flood.txt'))
	else:
		state = 'on'
		delivery(u'Внимание! Не удалось создать flood.txt для "%s"!' % (conf))
	FLOOD[conf] = state

register_message_handler(boltun_work)
register_command_handler(boltun_control, 'голос', ['болтун','все'], 20, 'Включение/выключение болталки, без параметра покажет текущее состояние', 'голос [вкл/on/1/выкл/off/0]', ['голос вкл','голос выкл'])

register_stage1_init(boltun_work_init)

# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  autoroles_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

AMODER = {}
AKICK = {}
AVSTR = {}

def handler_amoder(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				check = args[0].strip()
				item = args[1].strip()
				nick = body[(body.find(' ') + 1):].strip()
				if item.count('@') and item.count('.'):
					jid = item
				elif nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = False
				if jid:
					if jid in ADLIST:
						repl = u'%s мой BOSS, он и без того глобальный амодер' % (item)
					elif check == '+':
						if jid in AMODER[source[1]]:
							repl = u'%s итак в списке амодеров' % (item)
						elif jid in AKICK[source[1]]:
							repl = u'%s в списке автокика, прежде чем добавлять в амодеры удалите его оттуда' % (item)
						elif jid in AVSTR[source[1]]:
							repl = u'%s в списке авизиторов, прежде чем добавлять в амодеры удалите его оттуда' % (item)
						else:
							AMODER[source[1]].append(jid)
							handler_autoroles_resave(source[1], 'amoder', AMODER[source[1]])
							repl = u'%s добавлен в список амодеров' % (item)
					elif check == '-':
						if jid in AMODER[source[1]]:
							AMODER[source[1]].remove(jid)
							handler_autoroles_resave(source[1], 'amoder', AMODER[source[1]])
							repl = u'%s удалён из списка амодеров' % (item)
						else:
							repl = u'%s итак нет в списке амодеров' % (item)
					else:
						repl = u'инвалид синтакс'
				else:
					repl = u'Если %s это ник, то таких юзеров я тут невидел, если же нет то ты просто хрень пишеш' % (nick)
			else:
				repl = u'инвалид синтакс'
			reply(type, source, repl)
		else:
			list, col = '', 0
			for jid in AMODER[source[1]]:
				col = col + 1
				list += '\n'+str(col)+'. '+jid
			if col != 0:
				if type == 'public':
					reply(type, source, u'глянь в приват')
				reply('private', source, u'Всего в базе амодеров '+str(col)+u' жидов:'+list)
			else:
				reply(type, source, u'В базе амодеров пусто')
	else:
		reply(type, source, u'Гг юморист блин')

def handler_akick(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				check = args[0].strip()
				item = args[1].strip()
				nick = body[(body.find(' ') + 1):].strip()
				if item.count('@') and item.count('.'):
					jid = item
				elif nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = False
				if jid:
					if jid in ADLIST:
						repl = u'%s мой BOSS, он глобальный амодер' % (item)
					elif check == '+':
						if jid in AKICK[source[1]]:
							repl = u'%s итак в списке автокика' % (item)
						elif jid in AMODER[source[1]]:
							repl = u'%s в списке амодеров, прежде чем добавлять в автокик удалите его оттуда' % (item)
						elif jid in AVSTR[source[1]]:
							repl = u'%s в списке авизиторов, прежде чем добавлять в амодеры удалите его оттуда' % (item)
						else:
							AKICK[source[1]].append(jid)
							handler_autoroles_resave(source[1], 'akick', AKICK[source[1]])
							repl = u'%s добавлен в список автокика' % (item)
					elif check == '-':
						if jid in AKICK[source[1]]:
							AKICK[source[1]].remove(jid)
							handler_autoroles_resave(source[1], 'akick', AKICK[source[1]])
							repl = u'%s удалён из списка автокика' % (item)
						else:
							repl = u'%s итак нет в списке автокика' % (item)
					else:
						repl = u'инвалид синтакс'
				else:
					repl = u'Если %s это ник, то таких юзеров я тут невидел, если же нет то ты просто хрень пишеш' % (nick)
			else:
				repl = u'инвалид синтакс'
			reply(type, source, repl)
		else:
			list, col = '', 0
			for jid in AKICK[source[1]]:
				col = col + 1
				list += '\n'+str(col)+'. '+jid
			if col != 0:
				if type == 'public':
					reply(type, source, u'глянь в приват')
				reply('private', source, u'Всего в базе автокика '+str(col)+u' жидов:'+list)
			else:
				reply(type, source, u'В базе автокика пусто')
	else:
		reply(type, source, u'Гг юморист блин')

def handler_avisitor(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				check = args[0].strip()
				item = args[1].strip()
				nick = body[(body.find(' ') + 1):].strip()
				if item.count('@') and item.count('.'):
					jid = item
				elif nick in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+nick)
				else:
					jid = False
				if jid:
					if jid in ADLIST:
						repl = u'%s мой BOSS, он глобальный амодер' % (item)
					elif check == '+':
						if jid in AVSTR[source[1]]:
							repl = u'%s итак в списке авизиторов' % (item)
						elif jid in AKICK[source[1]]:
							repl = u'%s в списке автокика, прежде чем добавлять в авизиторы удалите его оттуда' % (item)
						elif jid in AMODER[source[1]]:
							repl = u'%s в списке амодеров, прежде чем добавлять в авизиторы удалите его оттуда' % (item)
						else:
							AVSTR[source[1]].append(jid)
							handler_autoroles_resave(source[1], 'avisitor', AVSTR[source[1]])
							repl = u'%s добавлен в список авизиторов' % (item)
					elif check == '-':
						if jid in AVSTR[source[1]]:
							AVSTR[source[1]].remove(jid)
							handler_autoroles_resave(source[1], 'avisitor', AVSTR[source[1]])
							repl = u'%s удалён из списка авизиторов' % (item)
						else:
							repl = u'%s итак нет в списке авизиторов' % (item)
					else:
						repl = u'инвалид синтакс'
				else:
					repl = u'Если %s это ник, то таких юзеров я тут невидел, если же нет то ты просто хрень пишеш' % (nick)
			else:
				repl = u'инвалид синтакс'
			reply(type, source, repl)
		else:
			list, col = '', 0
			for jid in AVSTR[source[1]]:
				col = col + 1
				list += '\n'+str(col)+'. '+jid
			if col != 0:
				if type == 'public':
					reply(type, source, u'глянь в приват')
				reply('private', source, u'Всего в базе авизиторов '+str(col)+u' жидов:'+list)
			else:
				reply(type, source, u'В базе авизиторов пусто')
	else:
		reply(type, source, u'Гг юморист блин')

def handler_autoroles_resave(conf, key, list):
	filename = 'dynamic/'+conf+'/autoroles.txt'
	base = eval(read_file(filename))
	base[key] = list
	write_file(filename, str(base))

def handler_autoroles_work(conf, nick, afl, role):
	jid = handler_jid(conf+'/'+nick)
	if jid in AMODER[conf]:
		handler_moder(conf, nick, u'амодер')
	elif jid in AKICK[conf]:
		handler_kick(conf, nick, u'акик')
	elif jid in AVSTR[conf]:
		handler_visitor(conf, nick, u'авизитор')

def autoroles_init(conf):
	if check_file(conf, 'autoroles.txt', str({'amoder': [], 'akick': [], 'avisitor': []})):
		base = eval(read_file('dynamic/'+conf+'/autoroles.txt'))
		amoder, akick, avisitor = base['amoder'], base['akick'], base['avisitor']
	else:
		amoder, akick, avisitor = [], [], []
		delivery(u'Внимание! Не удалось создать autoroles.txt для "%s"!' % (conf))
	AMODER[conf], AKICK[conf], AVSTR[conf] = amoder, akick, avisitor

register_join_handler(handler_autoroles_work)
register_command_handler(handler_amoder, 'амодер', ['все','админ'], 20, 'Автомодератор - бот атоматически даёт модера юзерам из списка при каждом входе\nДля добавления юзера в список пишем "+", а для удаления "-", без параметра покажет список', 'амодер <+/-> <jid/nick>', ['амодер + Петька','амодер - Петька','амодер + chuvak@loh.com','амодер - chuvak@loh.com','амодер'])
register_command_handler(handler_akick, 'акик',['все','админ'], 20, 'Автокик - бот атоматически кикает юзеров из списка при каждом входе\nДля добавления юзера в список пишем "+", а для удаления "-", без параметра покажет список', 'акик <+/-> <jid/nick>', ['акик + Петька','акик - Петька','акик + chuvak@loh.com','акик - chuvak@loh.com','акик'])
register_command_handler(handler_avisitor, 'авизитор',['все','админ'], 20, 'Автовизитор - бот атоматически лишает права голоса юзеров из списка при каждом входе\nДля добавления юзера в список пишем "+", а для удаления "-", без параметра покажет список', 'визитор <+/-> <jid/nick>', ['авизитор + Петька','авизитор - Петька','авизитор + chuvak@loh.com','авизитор - chuvak@loh.com','авизитор'])

register_stage1_init(autoroles_init)

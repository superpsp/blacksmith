# |-|-| lytic bot |-|-|
# -*- coding: utf-8 -*-

#  Лютик Bot plugin
#  getkey_plugin.py

# Coded by: CEP}|{

FROMDIR = 'dynamic/'

#def si_request(frm,fjid,sid,name,size,entity=''):
def si_request(frm, fjid, sid, name, size):
	iq = xmpp.Protocol(name = 'iq', to = fjid, typ = 'set')
	ID = 'si' + str(random.randrange(1000, 9999))
	iq.setID(ID)
	si = iq.setTag('si')
	si.setNamespace(xmpp.NS_SI)
#	si.setNamespace(xmpp.NS_SI.replace('jabber.org', 'jabber.org.sixxs.org'))
	si.setAttr('profile', xmpp.NS_FILE)
#	si.setAttr('profile', xmpp.NS_FILE.replace('jabber.org', 'jabber.org.sixxs.org'))
	si.setAttr('id', sid)
	file_tag = si.setTag('file')
	file_tag.setNamespace(xmpp.NS_FILE)
#	file_tag.setNamespace(xmpp.NS_FILE.replace('jabber.org', 'jabber.org.sixxs.org'))
	file_tag.setAttr('name', name)
	file_tag.setAttr('size', size)
	desc = file_tag.setTag('desc')
	desc.setData(u'Файл ключа.')
	file_tag.setTag('range')
	feature = si.setTag('feature')
	feature.setNamespace(xmpp.NS_FEATURE)
#	feature.setNamespace(xmpp.NS_FEATURE.replace('jabber.org', 'jabber.org.sixxs.org'))
	_feature = xmpp.DataForm(typ='form')
	feature.addChild(node=_feature)
	field = _feature.setField('stream-method')
	field.setAttr('type', 'list-single')
	field.addOption(xmpp.NS_IBB)
#	field.addOption(xmpp.NS_IBB.replace('jabber.org', 'jabber.org.sixxs.org'))
	field.addOption('jabber:iq:oob')
	return iq

def handler_load_answ(coze, resp, type, source, sid, to, fp):
	rtype = resp.getType()
	reply(type, source, u'rtype = ' + rtype)
	
	if rtype == 'result':
		JCON.IBB.OpenStream(sid, to, fp, 1024)
	else:
		fp.close()
		reply(type, source, u'Неудачная передача!')

def handler_getkey(type, source, body):

	global FROMDIR
	groupchat=source[1]
	nick = source[2]
	
	if groupchat not in GROUPCHATS.keys():
		reply(type, source, u'Эта команда может быть использована только в конференции!')
		return

	keyfiles = glob(FROMDIR + '*.key')
	if len(keyfiles) != 1:
		reply(type, source, u'Нет файла с ключом или обнаружено больше одного файла - обратитесь к админу!')
		return
	fromfile = keyfiles[0]

	to = ''
	if nick in GROUPCHATS[groupchat].keys():
		to = GROUPCHATS[groupchat][nick]['jid']
	if not to:
		reply(type, source, u'Не могу определить ник адресата в конференции!')
		return

	try:
		fp = open(fromfile)
	except:
		reply(type, source, u'Невозможно открыть файл ключа - обратитесь к админу!')
		return

	botjid = USERNAME + '@' + SERVER
#	frm = botjid + '/bot'
	frm = botjid
	sid = 'file' + str(random.randrange(10000000, 99999999))
	name = os.path.basename(fromfile)
#	sireq = si_request(frm, to, sid, name, len(data), entity)
	sireq = si_request(frm, to, sid, name, os.path.getsize(fromfile))
	
#	JCON.SendAndCallForResponse(sireq, handler_load_answ, args = {'type': type,'source': source,'sid': sid,'to': to,'fp': fp})
	JCON.SendAndCallForResponse(sireq, handler_load_answ, {'type': type,'source': source,'sid': sid,'to': to,'fp': fp})
	
	try:
		fp.close()
	except:
		pass

#def handler_file_create(type, source, body):
#	if body:
#		args = body.split()
#		filename = args[0].strip()
#		if filename.count('.'):
#			filename = encode_filename(filename)
#			if check_nosimbols(filename):
#				if initialize_file(filename):
#					if len(args) >= 2:
#						text = body[(body.find(' ') + 1):].strip()
#						try:
#							data = unicode(text).encode('utf-8')
#							write_file(filename, data)
#							reply(type, source, u'Файл был успешно записан!')
#						except:
#							reply(type, source, u'Файл не был записан!')
#					else:
#						reply(type, source, u'Записал со стандарной data -> "{}"')
#				else:
#					reply(type, source, u'Не удалось создать файл, перебор директорий или системная ошибка!')
#			else:
#				reply(type, source, u'Содержание кириллических символов разрешается только если директорией является конференция!')
#		else:
#			reply(type, source, u'Необходимо установить расширение, например ".txt"')
#	else:
#		reply(type, source, u'Инвалид синтакс!')

register_command_handler(handler_getkey, 'дайключ', ['суперадмин','все'], 100, 'Передаёт рабочий ключ для KIS2010, KIS2011\nBy CEP}|{', 'дайключ', ['дайключ'])

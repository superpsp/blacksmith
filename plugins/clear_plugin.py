#===istalismanplugin===
# -*- coding: utf-8 -*-

# Talisman - bot
# http://www.bots.ucoz.ru/
# (C) Gigabyte


def handler_clean_conf_ex(type, source, parameters):
	if GROUPCHATS.has_key(source[1]):
		otvet = u'Зачистка кишлака в разгаре!/Нифига не буду - плати бабло!/Ведро-тряпку давай!'
		list = otvet.split('/')
		otvet = random.choice(list)
		reply(type, source, otvet)
		change_bot_status(source[1], u'Чищу конфу', 'dnd')
		for x in range(1, 20):
			msg(source[1], '')
			time.sleep(1.7)
		otvet = u'Кишлак зачищен, командир!'
		reply(type,source,otvet)
		change_bot_status(source[1], u'Вкалываю', 'chat')

register_command_handler(handler_clean_conf_ex, 'чисть', ['фан','мук','все','new'], 15, 'Очищает конференцию, при этом не видимо для юзеров!\nНаписал: Gigabyte\nИдея: zozo', 'чисть', ['чисть'])

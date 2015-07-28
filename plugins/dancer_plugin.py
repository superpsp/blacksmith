#===istalismanplugin===
# -*- coding: utf-8 -*-

#  dancer_plugin.py

#  Author: CEP}|{ (pspsuperpsp@qip.ru)
#  Idea: Mэpи (marina199804@jabber.ru)

def handler_dancer(type, source, nick):
	if type == 'public':
		if not nick == handler_botnick(source[1]):
			if nick in GROUPCHATS[source[1]]:
				dances = []
				dances.extend(dancer_work(source[1]))
				dances.extend(eval(read_file('static/dances.txt'))['dance'])
				repl = random.choice(dances)
				msg(source[1], u'/me '+repl % (nick))
			else:
				reply(type, source, u'нету его')
		else:
			reply(type, source, u'пшел вон!')
	else:
		reply(type, source, u'неа')

def handler_dancer_control(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			cmd = args[0].strip().lower()
			if cmd in [u'адд', '+']:
				text = body[(body.find(' ') + 1):].strip()
				if text.count('%s'):
					if dancer_work(source[1], 1, text):
						reply(type, source, u'добавлено')
					else:
						reply(type, source, u'больше нельзя')
				else:
					reply(type, source, u'не вижу %s')
			elif cmd in [u'дел', '-']:
				text = args[1].strip()
				if check_number(text):
					if dancer_work(source[1], 2, text):
						reply(type, source, u'удалено')
					else:
						reply(type, source, u'такой нет')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		repl, res = '', dancer_work(source[1], 3)
		if res:
			res = sorted(res.items(), lambda x,y: int(x[0]) - int(y[0]))
			for num, phrase in res:
				repl += num+') '+phrase+'\n'
			reply(type, source, repl.strip())
		else:
			reply(type, source, u'нет пользовательских фраз')

def dancer_work(conf, action = None, phrase = None):
	if check_file(conf, 'dances.txt'):
		base = 'dynamic/'+conf+'/dances.txt'
		try:
			dancedb = eval(read_file(base))
		except:
			dancedb = {}
		if action == 1:
			for number in range(1, 21):
				if str(number) not in dancedb:
					dancedb[str(number)] = phrase
					write_file(base, str(dancedb))
					return True
			return False
		elif action == 2:
			if phrase == '0':
				dancedb.clear()
				write_file(base, str(dancedb))
				return True
			elif phrase in dancedb:
				del dancedb[phrase]
				write_file(base, str(dancedb))
				return True
			else:
				return False
		elif action == 3:
			return dancedb
		else:
			dances = []
			for dance in dancedb.itervalues():
				dances.append(dance)
			return dances
	return False

register_command_handler(handler_dancer, 'плясун', ['фан','все'], 10, 'Заставляет человека с указанным ником плясать/танцевать', 'плясун <ник>|<параметр>', ['плясун qwerty','плясун'])
register_command_handler(handler_dancer_control, 'плясун*', ['фан','все'], 10, 'Добавить/удалить пользовательскую фразу, без параметров покажет текущие пользовательские фразы. Переменная %s во фразе обозначает место для вставки ника (обязательный параметр). Фраза должна быть написана от третьего лица, т.к. будет использоваться в виде "/me ваша фраза". max кол-во пользовательских фраз - 20', 'плясун* [+/адд/-/дел]', ['плясун* + пригласил %s на тур вальса','плясун* - 4','плясун*'])

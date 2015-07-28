#===istalismanplugin===
# -*- coding: utf-8 -*-

#  bar_plugin.py

#  Author: CEP}|{ (pspsuperpsp@qip.ru)
#  Idea: Mэpи (marina199804@jabber.ru)

def handler_bar(type, source, body):
	drinks = []
	drinks.extend(bar_work(source[1]))
	drinks.extend(eval(read_file('static/drinks.txt'))['drink'])
	repl = ''
	if body:
		args = body.split()
		last = len(args)
		nick = args[0].strip()
		words = 1
		if nick == u'мне':
			nick = source[2]
		else:
			while words <= last:
				if nick in GROUPCHATS[source[1]]:
					break
				words = words + 1
				try:
					nick = nick + ' ' + args[words - 1].strip()
				except:
					reply(type, source, u'%s неправильный синтаксис или пробелы по краям ника!' % (nick))
					return
			else:
				reply(type, source, u'%s не с нашей улицы - нефик чужаков поить за наш счёт!' % (nick))
				return
			if nick == handler_botnick(source[1]):
				reply(type, source, u'Иди вон! Я не пью!')
				return
		if last > words:
			try:
				number = int(args[last - 1].strip())
				drink = drinks[number - 1]
			except:
				reply(type, source, u'Где ты такую выпивку видел?!=-O')
				return
			repl = drink
		else:
			repl = random.choice(drinks)
		msg(source[1], u'/me достал из бара '+ repl + ' для %s *DRINK*' % (nick))
	else:
		for i in range(1, len(drinks)):
			repl = repl + str(i) + '. ' + drinks[i - 1] + '\n'
		if type == 'public':
			reply(type, source, u'Я чё те - лох всем показывать выпивку?! В привате смотри!')
		reply('private', source, repl)

def handler_bar_control(type, source, body):
	if body:
		args = body.split()
		if len(args) > 1:
			cmd = args[0].strip().lower()
			if cmd in [u'адд', '+']:
				drink = body[((body.lower()).find(cmd) + (len(cmd) + 1)):].strip()
				if bar_work(source[1], 1, drink):
					reply(type, source, u'Добавлено!')
				else:
					reply(type, source, u'Больше нельзя!')
			elif cmd in [u'дел', '-']:
				text = args[1].strip()
				if check_number(text):
					if bar_work(source[1], 2, text):
						reply(type, source, u'Удалено!')
					else:
						reply(type, source, u'Где ты такую выпивку видел?!=-O')
				else:
					reply(type, source, u'Где ты такую выпивку видел?!=-O')
			else:
				reply(type, source, u'Инвалид синтакс - читай хелп!')
		else:
			reply(type, source, u'Инвалид синтакс - читай хелп!')
	else:
		repl, res = '', bar_work(source[1], 3)
		if res:
			res = sorted(res.items(), lambda x,y: int(x[0]) - int(y[0]))
			for num, phrase in res:
				repl += num+'. '+ phrase + '\n'
#			for i in range(1, len(res)):
#				repl = repl + str(i) + '. ' + res + '\n'
			reply('private', source, repl.strip())
		else:
			reply(type, source, u'Бар пустой!')

def bar_work(conf, action = None, phrase = None):
	if check_file(conf, 'drinks.txt'):
		base = 'dynamic/' + conf + '/drinks.txt'
		try:
			bardb = eval(read_file(base))
		except:
			bardb = {}
		if action == 1:
			for number in range(1, 999):
				if str(number) not in bardb:
					bardb[str(number)] = phrase
					write_file(base, str(bardb))
					return True
			return False
		elif action == 2:
			if phrase == '0':
				bardb.clear()
				write_file(base, str(bardb))
				return True
			elif phrase in bardb:
				del bardb[phrase]
				write_file(base, str(bardb))
				return True
			else:
				return False
		elif action == 3:
			return bardb
		else:
			drinks = []
			for drink in bardb.itervalues():
				drinks.append(drink)
			return drinks
	return False

register_command_handler(handler_bar, 'бар', ['фан','все'], 10, 'Раздаёт напитки из бара на выбор. Без параметров показывает содержимое бара в привате. Без указания номера напитка выбирает случайный напиток', 'бар [ник/мне] [номер]', ['бар qwerty 4','бар мне','бар'])
register_command_handler(handler_bar_control, 'бар*', ['фан','все'], 10, 'Добавить/удалить напитки в бар, без параметров покажет содержимое бара. Название напитка должно быть написано в винительном (для одной тары) или родительном (для нескольких тар) падеже, т.к. будет использоваться в виде "/me достал из бара <название_напитка> для <ник>". max кол-во пользовательских напитков - 998', 'бар* [+/адд/-/дел]', ['бар* + бочонок пива','бар* - 4','бар*'])
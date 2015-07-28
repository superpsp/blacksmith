#===istalismanplugin===
# -*- coding: utf-8 -*-

# (C) Gigabyte
# * Распространять без указания ссылки на ресурс и автора ЗАПРЕЩЕНО!
# * Применимо только в личных целях, никакой коммерции!!!


KARMA = {}

KARM_OUT = {}


def karma_save():
        #print 'SAVING KARMA'
        try:
                C = {'KARMA':KARMA,
                     'KARM_OUT':KARM_OUT
                     }
                fp = open('dynamic/karma.txt', 'w')
                fp.write( str(C) )
                fp.close()
                return 1
        except:
                return 0

def karma_load():
        global KARMA
        global KARM_OUT
        #print 'LOADING KARMA'
        try:
                fp = open('dynamic/karma.txt', 'r')
                C = eval(fp.read())
                fp.close()
                KARMA = C['KARMA']
                KARM_OUT = C['KARM_OUT']
                return 1
        except:
                KARMA = {}
                KARM_OUT = {}
                return 0



def karmaut(t, s, n):
        global KARM_OUT

        TIMEOUT = 20
        LENOUT = 3
        LENTIMEOUT = 120
        

        mj = handler_jid(s[0])
        uj = handler_jid(s[1]+'/'+n)


        ul = user_level(s[0], s[1])
        if (ul >0) and (ul<11): # Недомембер
                TIMEOUT = 273600 # 3 суток
                LENOUT = 1 # один человек в период
                LENTIMEOUT = 300 # период 5 минут
                #print 'User'
        elif (ul >=11) and (ul<=19): # чиста мембер
                TIMEOUT = 86400 # 1 сутки
                LENOUT = 3 # 3 человекa в период
                LENTIMEOUT = 180 # период 3 минуты
                #print 'member'
        elif (ul >=20) and (ul<=29): # чиста админ
                TIMEOUT = 18000 # 5 часов
                LENOUT = 5 # 5 человек в период
                LENTIMEOUT = 120 # период 2 минуты
                #print 'admin'
        elif (ul >=30) and (ul<=39): # чиста овнер
                TIMEOUT = 7200 # 2 часа
                LENOUT = 10 # 10 человек в период
                LENTIMEOUT = 60 # период 1 минута
                #print 'owner'
        elif (ul >=40): # чиста Бог
                TIMEOUT = 0
                LENOUT = 0
                LENTIMEOUT = 0
                #print 'God'

        

        if not mj in KARM_OUT:
                KARM_OUT[mj] = {'chkarm':{}, 'lasttime':0, 'count':0}

        if not uj in KARM_OUT[mj]['chkarm']:
                KARM_OUT[mj]['chkarm'][uj] = 0
        else:
                pass

        t = time.time() - KARM_OUT[mj]['lasttime']
        
        if (KARM_OUT[mj]['count'] >= LENOUT) and (t < LENTIMEOUT):
                R = {'type':'error',
                     'desc':u'Нельзя за период в %s менять карму более %i раз. Подождите ещё %s' % (timeElapsed(LENTIMEOUT), LENOUT, timeElapsed(LENTIMEOUT-t)),
                     'code':'002'}
                return R
        elif (KARM_OUT[mj]['count'] >= LENOUT) and (t >= LENTIMEOUT):
                KARM_OUT[mj]['lasttime'] = 0
                KARM_OUT[mj]['count'] = 0

        tt = time.time() - KARM_OUT[mj]['chkarm'][uj]



        
        if tt < TIMEOUT:
                R = {'type':'error',
                     'desc':u'Нельзя так часто изменять карму, подождите ещё %s' % (timeElapsed(TIMEOUT-tt) ),
                     'code':'001'}

        elif tt >= TIMEOUT:
                KARM_OUT[mj]['chkarm'][uj] = time.time()
                if KARM_OUT[mj]['lasttime'] == 0:
                        KARM_OUT[mj]['lasttime'] = time.time()
                KARM_OUT[mj]['count'] += 1
                R = {'type':'ok',
                     'desc':u'Без ошибок',
                     'code':'000'}
        return R
        
        


def karma_plus(t, s, n, z):
        jm = handler_jid(s[0])
        j = handler_jid(s[1]+'/'+n)
        if not j in KARMA.keys():
                KARMA[j] = {'karma':0, 'plus':0, 'minus':0, 'history':[]}
        R = karmaut(t, s, n)
        if R['type'] == 'error':
                reply(t, s, R['desc'])
                karma_save()
                return
        if z == '+1':
                a = '+'
                KARMA[j]['karma']+=1
                KARMA[j]['plus']+=1
                r = u'Вы повысили карму %s до %i' % (n, KARMA[j]['karma'])
                
        elif z == '-1':
                a = '-'
                KARMA[j]['karma']-=1
                KARMA[j]['minus']+=1
                r = u'Вы понизили карму %s до %i' % (n, KARMA[j]['karma'])
                
        else:
                a = '0'
                r = u'Вы не изменили карму %s, она равна %i' % (n, KARMA[j]['karma'])
        C = {'room':s[1], 'user':s[2], 'jid':jm,'action':a, 'time':time.time()}
        KARMA[j]['history'].insert(0, C)
        karma_save()
        reply(t, s, r)
        
def karma_get(t, s, b):
        if b == 'info':
                karma_help(t, s, b)
                return
        if not b:
                jm = handler_jid(s[0])
        else:
                if b in GROUPCHATS[s[1]].keys():
                        jm = handler_jid(s[1]+'/'+b)
                else:
                        reply(t, s, u'Его тут нет')
                        return
        
        if jm in KARMA.keys():
                MK = KARMA[jm]['karma']
                MP = KARMA[jm]['plus']
                MM = KARMA[jm]['minus']
                MH = KARMA[jm]['history']

                SH = u'Карма %s: %i\nвсего плюсов: %i\nвсего минусов: %i' % (b, MK, MP, MM)

                reply(t, s, SH)
        else:
                reply(t, s, u'Карма ноль')

        
def karma_get_det(t, s, b):
        if not b:
                jm = handler_jid(s[0])
        else:
                if b in GROUPCHATS[s[1]].keys():
                        jm = handler_jid(s[1]+'/'+b)
                else:
                        reply(t, s, u'Его тут нет')
                        return

        if jm in KARMA.keys():
                MK = KARMA[jm]['karma']
                MP = KARMA[jm]['plus']
                MM = KARMA[jm]['minus']
                MH = KARMA[jm]['history']
                o = ''
                for j, i in enumerate(MH):
                        o+=u'%i. %s из %s в %s установил %s карму\n' % (j+1, i['user'], i['room'], time.strftime("%d-%b-%Y %H:%M:%S", time.localtime(i['time'])), i['action'])

                SH = u'Ваша карма: %i\nвсего плюсов: %i\nвсего минусов: %i\nстатистика:\n%s' % (MK, MP, MM, o)

                reply(t, s, SH)
        else:
                reply(t, s, u'Карма ноль')
        
def karma_scan(w, t, s, b):
        if int(time.time() - INFO['start']) < 10:
                #print 'ret'
                return
#        if get_bot_nick(s[1]) == s[2]:
                #print 'bot'
#                return
        b = b.strip()
        rs = ['+1', '-1']
        zn = b[-2:].strip()
        if not zn in rs:
#                reply(t, s, u'Вы можете указать только: %s' % (u', или '.join(rs) ) )
                return
        nk = b[:-2]
        nk = nk.strip()
        if nk[-1] in [':', ',']:
                nk = nk[:-1]
        
        for c in GROUPCHATS.keys():
                for n in GROUPCHATS[c].keys():
                        if n == nk:
                                if GROUPCHATS[c][n]['ishere']:
                                        #print '%s %s' % (n, zn)
                                        karma_plus(t, s, n, zn)
                                        return
                                else:
                                        #print '%s - is not chat' % (n)
                                        karma_plus(t, s, n, zn)
                                        return
                        else:
                                pass
        else:
                #print 'end'
                return

def karma_help(t, s, b):
        out = u"""Карма v1.00fpv - first public version
(C) Gigabyte
www: http://jabbrik.ru
mail: gigabyte@ngs.ru
xmpp: stalker@conference.jabbrik.ru"""
        reply(t, s, out)

register_command_handler(karma_get, 'карма', ['karma', 'все'], 0, 'Посмотреть свою или чужую карму.', 'karm [user]', ['karm guy','karm'])
register_command_handler(karma_get_det, 'карма_детали', ['karma', 'все'], 0, 'Посмотреть статистическую свою или чужую карму.', 'karm [user]', ['karm guy','karm'])
register_message_handler(karma_scan)
register_stage2_init(karma_load)

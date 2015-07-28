#===istalismanplugin===
# -*- coding: utf-8 -*-

# Перевод CEP}|{

import urllib, re

def distance_q(type, source, parameters):
    try:
        if not parameters or not parameters.count(' '):
            return
        s=parameters.split()
        a=urllib.quote(s[0].encode('cp1251'))
        b=urllib.quote(s[1].encode('cp1251'))
#        a=urllib.quote(s[0])
#        b=urllib.quote(s[1])
        adr='http://www.ati.su/Trace/default.aspx?EntityType=Trace&City1=%s&City5=%s' % (a,b)
        page = urllib.urlopen(adr)
        r=page.read()
        r=r.decode('cp1251')
        city1=''
        city2=''
        rep=''
        f=re.findall('<span id="[^>]*?>(.+)</td>',r)
        w=re.findall('<input name=\"[^>]*?value=\"(.+)\"',r)
        if w and len(w)>1:
            city1=w[0].split('\"')[0]
            city2=w[1].split('\"')[0]
#        rep=u'Расстояние между: '+city1+u' и '+city2+' '+decode_log(f[0])+u';\nВремя в пути: '+decode_log(f[1])
        rep=u'Расстояние между: '+city1+u' и '+city2+' '+ f[0][:f[0].find('</span>')] +u';\nВремя в пути: '+ f[1][:f[1].find('</span>')]
        reply(type, source, rep)
    except Exception, err:
        reply(type, source, u'расстояние неизвестно')
    

register_command_handler(distance_q, 'расстояние', ['все'], 10, 'Расстояние v1.0 (hotfix 27.04.2013 by CEP}|{)\nПоказывает расстояние между городами. Информация с сайта http://www.ati.su/Trace', 'расстояние город_1 город_2', ['расстояние киев одесса'])

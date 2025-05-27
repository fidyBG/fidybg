# -*- coding: utf-8 -*-
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import xbmcvfs
import shutil
import os
from datetime import datetime, timedelta
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database

__addon__ = xbmcaddon.Addon()

msgtext = ''

if __addon__.getSetting('checktemp') == 'true':    
    temp_folder = xbmcvfs.translatePath('special://temp')
    
    try:
        try:
            shutil.rmtree(temp_folder, ignore_errors=False, onerror=None)
        except:
            pass
        try:
            os.mkdir(temp_folder)
        except:
            pass
    except:
        pass
        
    msgtext = 'Папка за временни файлове:  [COLOR FF00FF00][B]ИЗПЪЛНЕНО[/B][/COLOR]'


if __addon__.getSetting('checkpack') == 'true':
    pack_folder = xbmcvfs.translatePath('special://home/addons/packages')
    
    try:
        try:
            shutil.rmtree(pack_folder, ignore_errors=False, onerror=None)
        except:
            pass
        try:
            os.mkdir(pack_folder)
        except:
            pass
    except:
        pass
        
    if msgtext == '':
        msgtext = 'Папка за файлове на добавки:   ИЗПЪЛНЕНО!'
    else:
        msgtext = msgtext + '\n' + 'Папка за файлове на добавки:  [COLOR FF00FF00][B]ИЗПЪЛНЕНО[/B][/COLOR]'
    

if __addon__.getSetting('checkthumb') == 'true':
    current_date = datetime.date(datetime.utcnow())
    dbfile = xbmcvfs.translatePath(os.path.join('special://database', 'Textures13.db'))
    item_list = []
    minimum_uses = 30
    days = 0
    back_date = (current_date - timedelta(days=int(days))).strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(dbfile):
        dbcon = database.connect(dbfile, isolation_level=None)
        dbcur = dbcon.cursor()
        dbcur.execute('''PRAGMA synchronous = OFF''')
        dbcur.execute('''PRAGMA journal_mode = OFF''')
    else: pass
    dbcur.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (minimum_uses, str(back_date)))
    result = dbcur.fetchall()
    result_length = len(result)
    if not result_length > 0:
        pass
    else:
        for count, item in enumerate(result):
        	_id = item[0]
        	dbcur.execute("SELECT cachedurl FROM texture WHERE id = ?", (_id, ))
        	url = dbcur.fetchall()[0][0]
        	item_list.append((_id,))
        line = 'Removing Database Entries...[CR]Please Wait...[CR]%s'
        dbcur.executemany("DELETE FROM sizes WHERE idtexture = ?", item_list)
        dbcur.executemany("DELETE FROM texture WHERE id=?", item_list)
        dbcur.execute("VACUUM")
        dbcon.commit()
        
    thumbs_folder = xbmcvfs.translatePath('special://thumbnails')
    try:
        try:
            shutil.rmtree(thumbs_folder, ignore_errors=False, onerror=None)
        except:
            pass
        try:
            os.mkdir(thumbs_folder)
        except:
            pass
    except:
        pass
        
    if msgtext == '':
        msgtext = 'Папка за миниатюри:   ИЗПЪЛНЕНО!'
    else:
        msgtext = msgtext + '\n' + 'Папка за миниатюри:  [COLOR FF00FF00][B]ИЗПЪЛНЕНО[/B][/COLOR]'


if __addon__.getSetting('checksub') == 'true':
    sub_folder = xbmcvfs.translatePath('special://subtitles')
    
    try:
        try:
            shutil.rmtree(sub_folder, ignore_errors=False, onerror=None)
        except:
            pass
        try:
            os.mkdir(sub_folder)
        except:
            pass
    except:
        pass
        
    if msgtext == '':
        msgtext = 'Папка за субтитри:  ИЗПЪЛНЕНО!'
    else:
        msgtext = msgtext + '\n' + 'Папка за субтитри:  [COLOR FF00FF00][B]ИЗПЪЛНЕНО[/B][/COLOR]'
        
if __addon__.getSetting('checksub') == 'false' and __addon__.getSetting('checktemp') == 'false' and __addon__.getSetting('checkpack') == 'false' and __addon__.getSetting('checkthumb') == 'false':
    xbmcgui.Dialog().ok('Изтриване на временни файлове ...', "[COLOR FFFF0000][B]НЯМА НИЩО ИЗБРАНО![/B][/COLOR]")
else:    
    xbmcgui.Dialog().ok('Изтриване на временни файлове ...', msgtext)

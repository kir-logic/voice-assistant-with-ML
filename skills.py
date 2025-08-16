import webbrowser
import sys
from time import sleep
import pyautogui as pg

def music_rock():
	#Эта команда включает плейлист с роком на Яндекс.музыка
	webbrowser.open('https://music.yandex.ru/playlists/ge.93a03bfe-185a-480b-a74c-9584c1dbd7bd')
	sleep(7)
	pg.click(300, 790)
 
def music_study():
	#Эта команда включает плейлист с low-fi музыкой на Яндекс.музыка
	webbrowser.open('https://music.yandex.ru/playlists/f7efde37-1ae5-d8ba-b3bd-367168541a14')
	sleep(7)
	pg.click(300, 790)

def music_next():
	#Эта команда переключает трек на следующий
	pg.press('nexttrack')

def music_prev():
	#Эта команда переключает трек на предыдущий
	pg.press(['prevtrack'] * 3)
 
def music_volume_down():
    #Эта команда увеличивает громкость
	pg.press(['volumedown'] * 10)

def music_volume_up():
    #Эта команда уменьшает громкость
	pg.press(['volumeup'] * 10)

def offBot():
    #Эта команда отключает Сонату
	sys.exit()

def passive():
	#Эта команда для мини-разговора с Сонатой
	pass






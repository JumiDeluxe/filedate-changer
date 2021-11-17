#!/usr/bin/python3
import sys, os
from datetime import datetime

#date in yyyy-MM-dd HH:mm:ss format

def print_usage():
    print('''Usage:

python3 filedate-changer.py DATE FILES
or
python3 filedate-changer.py DATE -d DIRECTORY

example:
python3 filedate-changer.py 2005-04-02T21:37:00 /home/john/secret_archives/

DATE format: yyyy-MM-ddTHH:mm:ss''')


def epoch_time(time):
    return float(datetime.fromisoformat(time).strftime('%s'))

def change_system_time(time):
    os.system(f'/usr/bin/date --set=\"{time}\"')

def get_system_time():
    return os.system('date')

def recreate_file(file, directory): # used to change btime
    os.system(f'/usr/bin/cat {directory}/{file} > /tmp/{file} && /usr/bin/mv /tmp/{file} {directory}/{file}')

def change_file_time(time, file, directory):
    recreate_file(file, directory)
    epoch = epoch_time(time)
    print(epoch)
    os.utime(file, (float(epoch), float(epoch)))

def remove_last_slash(s): # prevent doubleslash
    if s[-1] == '/':
        return s[:-1]
    return s


if len(sys.argv) > 2: # multiple files
    time = sys.argv[1]
    now = get_system_time()
    change_system_time(time)

    # entire directory mode
    if sys.argv[2] == '-d': 
        directory = remove_last_slash(sys.argv[3])
        files = os.listdir(directory)

    else: # only selected files
        directory = '.'
        files = sys.argv[2:]

    for file in files:
        change_file_time(time, file, directory)
    change_system_time(now)

else:
    print_usage()
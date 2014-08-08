#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Restore POM permissions
"""

import sys
import os
import traceback
import argparse
import time
import logging
from subprocess import call, check_output, Popen
import tempfile
from multiprocessing import pool
import json

# create file handler which logs even debug messages
log = logging.getLogger()
log.setLevel(logging.ERROR)  # DEBUG | INFO | WARNING | ERROR | CRITICAL
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - Line: %(lineno)d\n%(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)
sh.setFormatter(formatter)
log.addHandler(sh)
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pom-permissions.log'))
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
log.addHandler(fh)

def localSettings():
    with open('pom-permissions-fix.json', 'r') as permissions:
        theSettings = json.loads(permissions.read())
        print(theSettings)
    return theSettings

def get_backup(date, tempDir):
    thepath = localSettings()['full_backup_path'].format(date)
    print(thepath)
    call(['scp','pom:'+thepath, os.path.join(tempDir.name, date + 'sql')])

def main():

    global args
    backups = check_output(['ssh','pom','ls',localSettings()['backup_dir']]).decode("utf-8").split("\n")
    backups = [x for x in backups if x.startswith('20')] # show only date-based entries
    tempDir = tempfile.TemporaryDirectory()
    p = pool.Pool(4)
    items = []
    for date in sorted(backups, reverse=True)[0:args.number]:
        items.append((date,tempDir))
    p.starmap_async(get_backup, items)
    p.close()
    p.join()
    localFiles = [f for f in os.listdir(tempDir.name) if os.path.isfile(os.path.join(tempDir.name, f))]
    try:
        os.remove('pomfix.sql')
    except FileNotFoundError:
        pass

    for f in localFiles:
        theInputFile = os.path.join(tempDir.name,f)
        with open(theInputFile, 'r') as fpointer:
            proc = Popen(['mysql','-u','root','-proot'], stdin=fpointer)
            proc.wait()
            os.remove(theInputFile) # removing each time since I'm running out of room.
        with open('pomfix.sql','a') as fpointer:
            proc = Popen(['mysqldump', '-u','root','-proot','--insert-ignore',
                '--no-create-info','powerofmoms_wp','wp_uam_accessgroup_to_object'
                ], stdout=fpointer)
            proc.wait()
    tempDir.cleanup()


if __name__ == '__main__':
    try:
        start_time = time.time()
        # Parser: See http://docs.python.org/dev/library/argparse.html
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_argument('-ver', '--version', action='version', version='0.0.1')
        parser.add_argument('-n', '--number', default=5, type=int)
        args = parser.parse_args()
        if args.verbose:
            fh.setLevel(logging.DEBUG)
            log.setLevel(logging.DEBUG)
        log.info("%s Started" % parser.prog)
        main()
        log.info("%s Ended" % parser.prog)
        log.info("Total running time in seconds: %0.2f" % (time.time() - start_time))
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

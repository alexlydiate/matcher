#!/usr/bin/env python3
import os, shutil, time
from multiprocessing import Process
from datetime import datetime

import config, matcherlib

start = datetime.now()

if config.split_match_enabled:
    print("We're off, using " + str(config.processes) + ' processes and split matching')
else:
    print("We're off, using " + str(config.processes) + ' processes, without split matching enabled.')

#Freshen up file system
try:
    os.remove(config.results_file_path)
except:
    pass

if not os.path.exists(config.tmp_path):
    os.makedirs(config.tmp_path)

#Split Products file into one for each process, with roughly the same amount of products in each, returning a list of those files
split_files = matcherlib.split_file(config.product_file_path, config.processes)

#For each split file, spin up a thread and process it against the listings file:
processes = []
process_number = 1
for split_file in split_files:
    p = Process(target = matcherlib.process_product_file, args = (split_file, process_number))
    processes.append(p)
    p.start()
    process_number = process_number + 1
    
stayalive = True

#Keep going until all the processes are finished:
while stayalive:
    stayalive = False
    for p in processes:
        if p.is_alive():
            stayalive = True
            
    time.sleep(1)

#Merge results files into results.txt    
matcherlib.merge_files(split_files)       

#Remove temp files
shutil.rmtree(config.tmp_path)

print('And done, completed in ' + str(datetime.now() - start))
print('Results output to the file at data/results.txt')

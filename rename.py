# -*- coding: utf-8 -*-

# =============================================================================

# This script is written to rename the files with UTC timestamp which are added
# to files while performing windows backup using file history. 
# Incase the file history gets corrupted then Files can be renamed using this 
# script after after deleting the duplicates using a third party software

# Created on Thu Jan 21 21:28:42 2021

# @author: Pratik Walawalkar

# =============================================================================


import os
import sys
import re
import time
import curses

path = sys.argv[1]

files_renamed = 0
files_skipped = 1
total_files_scanned = 1
action = ''
t0_start = time.time()
listOfFiles = list()


total_files = sum(len(files) for path, directory, files in os.walk(os.path.join(path)))

for (dirpath, dirnames, filenames) in os.walk(path):
    listOfFiles += [ os.path.join(dirpath, file) for file in filenames if re.search(r"\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", os.path.join(dirpath, file))]
filesWithUTC = len(listOfFiles)

def main():
    
    navigateFileTree(listOfFiles)  
    curses.initscr().getch()       #Hold the curses screen after execution
    
def status(filename):
    
    curses.initscr().clear()
    curses.initscr().addstr(0, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(1, 0,"File's renamed                                     :" + str(files_renamed))
    curses.initscr().addstr(2, 0,"Filename already exists                            :" + str(files_skipped))
    curses.initscr().addstr(3, 0,"Total file's scanned                               :" + str(total_files_scanned))
    curses.initscr().addstr(4, 0,"Total file's with UTC timestamp in the Directory   :" + str(filesWithUTC))
    curses.initscr().addstr(5, 0,"Total file's in the Directory                      :" + str(total_files))
    curses.initscr().addstr(6, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(7, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(8, 0,'checking for files in : ' + path)
    curses.initscr().addstr(9, 0,'Filename : ' + str(os.path.basename(filename)))
    curses.initscr().addstr(10, 0,">>> " + str(action))
    curses.initscr().addstr(11, 0,"------------------------------------------------------------------------------")

    curses.initscr().addstr(13, 0,str(progressBar(total_files_scanned, total_files)))
    
    curses.initscr().addstr(15, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(16, 0,"Time elapsed = " + str(time_conversion(time_elapsed())))
    curses.initscr().addstr(17, 0,"Estimated time left = " + str(time_conversion(time_left())))
    curses.initscr().addstr(18, 0,"------------------------------------------------------------------------------")    
    curses.initscr().addstr(19, 0,"")  
    
    time.sleep(0.1)

def time_conversion(time):
    '''Convert time to hh mm ss format'''
    
    if time == "Completed!!!":
        return time
    else:
        hours, rem = divmod(time, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}h {:0>2}m {:0>2}s".format(int(hours), int(minutes), int(seconds))
    
def time_elapsed():
    '''Calculate time elapsed since initiating the code'''
    
    time_elapsed = (time.time() - t0_start)     #Difference between the program execution end and start time
    return time_elapsed        
        
def time_left():
    '''Calculate the difference between the approximate time left to complete the process'''
    
    time_left = ((filesWithUTC - total_files_scanned) * time_elapsed())/(total_files_scanned)
    
    if time_left <= 0:
        return ("Completed!!!")
    else:
        return time_left
    
def navigateFileTree(listOfFiles):
    
    global total_files_scanned, action
   
    for item in listOfFiles:
  
        status(item)                             #exeute the code for user interface
        action = rename(item)                    #save action performed on a file as a string
        total_files_scanned += 1                 #count the total files scanned
                    
def checkFileName(filename):
    '''Return True if timestamp exists in the filename'''
    
    if re.search(r"\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", filename):
        return True                              #return true if UTC timestamp exists
    else:
        return False

def rename(path):
    
    global files_skipped, files_renamed 
    
    if os.path.isfile(path):

        src = path
        dst = re.sub(r" ?\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", "", src, flags=re.I)   #subtract UTC timestamp from the file name
	
        if os.path.exists(dst):
            '''Execute if a file with the same name already exist'''
            files_skipped += 1                                          #count the number of files skipped

            return "The filename already exists "         
                     
        else:
            '''Rename the file '''
            os.rename(src, dst)                                         #rename the file
            files_renamed += 1                                          #count the number of files renamed

            head_src, tail_src = os.path.split(src)                     #split the path and filename of source file
            head_dst, tail_dst = os.path.split(dst)                     #split the path and filename of renamed file
            return 'Renamed {src} >>TO>> {dst}\r'.format(src=tail_src, dst=tail_dst)
    else:
        return 'The Path You Entered is not Valid' + path

def progressBar(total_files_scanned, total_files, decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    '''Block of code which represents the process bar'''
      
    percent = round(100*(total_files_scanned/float(filesWithUTC)), 2)   #calculate the percent of process completed
    filled_length = int(length * total_files_scanned // filesWithUTC)   #calculate the length of filled bar
    progress_bar = fill * filled_length + '-' * (length - filled_length)#design process bar
    return f'Progress |{progress_bar}| {percent}% complete'
        
    if total_files_scanned == total_files: 
        print()   
    
if __name__ == "__main__":
    main()





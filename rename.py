import os
import sys
import re
import time
import curses

path = sys.argv[1]
list = os.listdir(path)

files_renamed = 0
files_skipped = 0
total_files_scanned = 1
action = ''
t0_start = time.time()

total_files = sum(len(files) for path, directory, files in os.walk(os.path.join(path)))

def main():
    
    navigateFileTree(path, list)
    curses.initscr().getch()

def status(filename):
    
    curses.initscr().clear()
    curses.initscr().addstr(0, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(1, 0,"File's renamed: " + str(files_renamed))
    curses.initscr().addstr(2, 0,"Filename already exists: " + str(files_skipped))
    curses.initscr().addstr(3, 0,"Total file's scanned: " + str(total_files_scanned))
    curses.initscr().addstr(4, 0,"Total file's in Directory: " + str(total_files))
    curses.initscr().addstr(5, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(6, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(7, 0,'checking for files in : ' + path)
    curses.initscr().addstr(8, 0,'Filename : ' + str(filename))
    curses.initscr().addstr(9, 0,">>> " + str(action))
    curses.initscr().addstr(10, 0,"------------------------------------------------------------------------------")

    curses.initscr().addstr(12, 0,str(progressBar(total_files_scanned, total_files)))
    
    curses.initscr().addstr(14, 0,"------------------------------------------------------------------------------")
    curses.initscr().addstr(15, 0,"Time elapsed = " + str(time_conversion(time_elapsed())))
    curses.initscr().addstr(16, 0,"Estimated time left = " + str(time_conversion(time_left())))
    curses.initscr().addstr(17, 0,"------------------------------------------------------------------------------")    
    
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
    
    time_elapsed = (time.time() - t0_start)
    return time_elapsed        
        
def time_left():
    '''Calculate the difference between the approximate time left to complete the process'''
    
    time_left = ((total_files - total_files_scanned) * time_elapsed())/(total_files_scanned)
    
    if time_left == 0:
        return ("Completed!!!")
    else:
        return time_left
    
def navigateFileTree(workingPath, items):
    
    global total_files_scanned, action
   
    for item in items:
  
        status(item)
        newPath = os.path.join(workingPath, item)      
               
        if os.path.isdir(newPath):
           newList = os.listdir(newPath)
           navigateFileTree(newPath, newList)         
            
        elif os.path.isfile(newPath) and checkFileName(item):
           '''Check if file exists and contains UTC timestamp'''
           total_files_scanned += 1
           action = rename(newPath)
                
        else:
            action = 'Filename does not contain UTC timestamp'
            total_files_scanned += 1

        
def checkFileName(filename):
    '''Return True if timestamp exists in the filename'''
    
    if re.search(r"\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", filename):
        return True
    else:
        return False

def rename(path):
    global files_skipped, files_renamed 
    if os.path.isfile(path):

        src = path
        dst = re.sub(r" ?\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", "", src, flags=re.I)
        #os.system('chflags nouchg {}'.format(src))
	
        if os.path.exists(dst):
            '''Execute if a file with the same name already exist'''
            files_skipped += 1 

            return "The filename already exists "         
                     
        else:
            '''Rename the file '''
            os.rename(src, dst)
            files_renamed += 1

            head_src, tail_src = os.path.split(src)
            head_dst, tail_dst = os.path.split(dst)
            return 'Renamed {src} >>TO>> {dst}\r'.format(src=tail_src, dst=tail_dst)
    else:
        return 'The Path You Entered is not Valid' + path

def progressBar(total_files_scanned, total_files, decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    '''Block of code which represents the process bar'''
      
    percent = round(100*(total_files_scanned/float(total_files)), 2)
    filled_length = int(length * total_files_scanned // total_files)
    progress_bar = fill * filled_length + '-' * (length - filled_length)
    return f'Progress |{progress_bar}| {percent}% complete'
        
    if total_files_scanned == total_files: 
        print()   
    
if __name__ == "__main__":
    main()





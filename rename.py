import os
import sys
import re


#print (sys.argv)

path = sys.argv[1]


list = os.listdir(path)

#print (list)

files_renamed = 0
files_skipped = 0
total_files_scanned = 0

def main():

    navigateFileTree(path, list)
    print("\n-------------------------------------------------")
    print("File's renamed: " + str(files_renamed))
    print("Filename already exists: " + str(files_skipped))
    print("Total files scanned: " + str(total_files_scanned))
    print("-------------------------------------------------")

def navigateFileTree(workingPath, items):
    global total_files_scanned
    print("\n-----------------------------------------------------------")
    print ('checking for files in : ' + workingPath)
    print("-----------------------------------------------------------")

    for item in items:
        
        global total_files_scanned
        newPath = workingPath + '/' + item
        total_files_scanned += 1
        #print (newPath) 
        
        if os.path.isdir(newPath):
            newList = os.listdir(newPath)
            navigateFileTree(newPath, newList)
        
        elif os.path.isfile(newPath) and checkFileName(item):
            '''Check if file exists and contains UTC timestamp'''
            
            print (rename(newPath))
            
        else:
            print ('no item',)

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
        os.system('chflags nouchg {}'.format(src))
	
        if os.path.exists(dst):
            print("The filename already exists ")
            files_skipped += 1
            pass

        else:
            os.rename(src, dst)
            files_renamed += 1
            head_src, tail_src = os.path.split(src)
            head_dst, tail_dst = os.path.split(dst)
            return 'Renamed {src} >>TO>> {dst}'.format(src=tail_src, dst=tail_dst)
    else:
        return 'The Path You Entered is not Valid' + path

if __name__ == "__main__":
    main()





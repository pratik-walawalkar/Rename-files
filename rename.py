import os
import sys
import re


#print (sys.argv)

path = sys.argv[1]

list = os.listdir(path)

#print (list)

files_renamed = 0
files_skipped = 0


def main():


    navigateFileTree(path, list)
    print("File's renamed: " + str(files_renamed))
    print("File's skipped: " + str(files_skipped))

def navigateFileTree(workingPath, items):
    print ('checking for files in : ' + workingPath)


    for item in items:
        newPath = workingPath + '/' + item
        print (newPath) 
        if os.path.isdir(newPath):
            newList = os.listdir(newPath)
            #print ('found directory, recursivly going into: ' + newPath)
            navigateFileTree(newPath, newList)
        elif os.path.isfile(newPath):
            print (rename(newPath))
        else:
            print ('no item')



def rename(path):
    global files_skipped, files_renamed 
    if os.path.isfile(path):

        src = path
        dst = re.sub(r" ?\(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)", "", src, flags=re.I)
        os.system('chflags nouchg {}'.format(src))
	
        if os.path.exists(dst):
            print("The file already exists")
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





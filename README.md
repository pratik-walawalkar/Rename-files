# File-Rename-Script

### Why I made this?

I have writen this script to solve an issue I was facing while restoring windows file history. Due to some issue I was unable to restore the files I had backed up. I managed to remove the duplicate files (versions) using a third party software but the software had no option to remove the UTC timestamp (for e.g. (2019_06_24 05_40_08 UTC)) :
<br>


This script will fix all the files in a provided directory.

to run this script just install python and run this file 

```
python rename.py '<absolute path to the folder containing files to be renamed>'
```

***Limitations:***
```
1. Unable to process duplicates: The script cannot overwrite files if the file name already exists in the same folder after renaming it. It will skip renaming such files.
2. It renames all the file even it the timestamp isn't there. This increases the run time.
```

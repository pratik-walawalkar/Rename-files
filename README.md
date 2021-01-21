# File-Rename-Script

### Why I made this?

I have writen this script to solve an issue I was facing while restoring windows file history. Due to some issue I was unable to restore the files I had backed up. I managed to remove the duplicate files (versions) using a third party software but the software had no option to remove the UTC timestamp:
<br>

***Original files:***
```
.gitignore
Endpoints.txt
Readme.md
package-lock.json
```
<br>

***Backed Up files:***
<br>
```
(2019_06_24 05_40_08 UTC).gitignore
Endpoints (2019_06_24 05_40_08 UTC).txt
Readme (2019_06_24 05_40_08 UTC).md
package-lock (2019_06_24 05_40_08 UTC).json
```

This script will fix all the files in a provided directory.

to run this script just install python and run this command:

```
python rename.py 'absolute/path/to/the/directory/containing/the/files/with/timestamps'
```

***When i ran it:***
```
python rename.py '/Users/dylancorbus/Desktop/test'
```

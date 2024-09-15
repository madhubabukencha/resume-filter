
## Troubleshooting
Here you can find solutions for possible errors
### dbshell error
If you face below error:
``` shell
PS D:\Projects\MCA-Project\resume-filter\resume_filter> python manage.py dbshell

CommandError: You appear not to have the 'sqlite3' program installed or on your path.
```
Download file like below one (sqlite-tools-win-x64-3460100.zip) from below url and unzip it. Copy and paste all files inside it in the place where manage.py exists:
https://www.sqlite.org/download.html

sqlite-tools-win-x64-3460100.zip: 
A bundle of command-line tools for managing SQLite database files, including the command-line shell program, the sqldiff.exe program, and the sqlite3_analyzer.exe program. 64-bit.


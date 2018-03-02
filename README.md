# pycracker
A simple program to crack passwords on Linux (/etc/passwd)

Download the files and use pycracker.py and pycracker_def.py in the same directory.
Assuming that some version of Python 3 is installed.

## **Attention**: 
If you are not using python 3.6 and are using other version of Pyhton 3, change the shebang _/usr/bin/python3.6_ for that version.

#### **Suggestion**: 
The dictionary file "dictionary.txt" have 4.64MB.
If you are using for simple testing purposes, you can write you own dictionary file with 10 or 20 words more or less, with the same format, just to not spend cpu/time resources.

-----------------------------------------------------------------------------------------------------------------------------------
## **Syntax:**

```

[user@server pycracker]# ./pycracker.py --help
usage: 
[-h] -d <dictionary> [-p <path>] [-u <user>] [-v --verbose] [--version]

pycracker.py, Made by: Pedro Pereira & Pedro Lourenço (CET06_2017) on
05/05/2017 <> Version 1.2 improved by Pedro Pereira (Fev-2018)

optional arguments:
  -h, --help            show this help message and exit
  -p PATH               Specifies the path for the password file,
                        default=/etc/shadow.
  -u USER [USER ...], --user= USER [USER ...]
                        specifies the user to search.
  -v, --verbose         does the verbose of every step.
  --version             Shows version and ends.

required arguments:
  -d DICTIONARY         specifies a dictionary file.
  
  
  (to all users)      EX_1: [user@server pycracker]# ./pycracker.py -d dictionary.txt
  (to specific users) EX_2: [user@server pycracker]# ./pycracker.py -d dictionary.txt -u john peter
  ```
  -----------------------------------------------------------------------------------------------------------------------------------

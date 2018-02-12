# pycracker
One simple program to crack the users password with dictionary file.
This a academic construction of a program to crack passwords in Linux environments. 
It was made by me, Pedro Pereira and my dear colleage Pedro Lourenço.

We had chose the module argparse and not docopt.

The output phrases are in Portuguese but the core is in English. Later I will do this update to be totally in English.

We made this with Python3
The syntax of the program(argparse) is:

./pycracker.py [-h] -d <dicionario> [-p <passwords>] [-u <user>] [-v --verbose] [--version]

So, you have to create a dictionary file with possible passwords. If you put the right password the program will match.

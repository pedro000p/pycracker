#!/usr/bin/python3

import crypt, argparse, os, platform

def process(argP):
     def parse(*args, **kwargs):
         return argP(parse, *args, **kwargs)
     return parse

@process
def arg_Parser(this):
	# Arg Parser 
	parser = argparse.ArgumentParser(description="%(prog)s, Made by: Pedro Pereira & Pedro Lourenço (CET06_2017) on 05/05/2017"\
	" <> Version 1.2 improved by Pedro Pereira\n"
	,usage = '\n[-h] -d <dictionary> [-p <path>] [-u <user>] [-v --verbose] [--version]')
	requeridos = parser.add_argument_group('required arguments')
	requeridos.add_argument('-d', dest='dictionary', required=True, help='specifies a dictionary file.')
	parser.add_argument('-p', dest='path', default='/etc/shadow', help='Specifies the path for the password file, default=/etc/shadow.')
	parser.add_argument('-u', '--user=',nargs='+', dest='user', help='specifies the user to search.')
	parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='does the verbose of every step.')
	parser.add_argument('--version', action='version', version='%(prog)s 1.2', help='Shows version and ends.')
	this.options = parser.parse_args()
	this.usg = parser.usage

	


def no_User(options, usg):
	"""If option [-u / --user=] is not used """

	if isSudo(usg) == True:
		if vef_File(options.path) == True and vef_File(options.dictionary) == True:	
			chkEnd = 0
			foundU = []
			with open(options.path) as file:
				for line in file:
					if (":") in line:
						user = line.split(':')[0]
						cryptPass = line.split(':')[1].strip(' ')
						salt = chkDistro(cryptPass)
						if options.verbose:
							print ("[+] Trying for user " + "'" + user + "'" + ' ...')
						if cryptPass == '':
							if options.verbose:
								print("...ignored. Account without password ('::').\n")
								continue
							print("[+]  " + user + "\t: " + "Account without password.")
							continue
						if cryptPass[0] == '!':
							if options.verbose:
								if 'root' in user:
									print("...ignored. For security reasons. lol \n")
								else:
									print("...ignored. Account locked. Login disable ('!' or '*').\n")
							continue
						if cryptPass[0] == '':
							if options.verbose:
								print("...ignored. Account without password ('::').\n")
							continue
						if '!' in line or '*' in line:
							if options.verbose:
								print("...ignored. Account locked. Login disable ('!' or '*')\n")
							continue
						sha = chkPassAlg(cryptPass)
						with open(options.dictionary) as file1:
							for word in file1:
								chkEnd += 1
								word = word.strip('\n')
								cryptWord = crypt.crypt(word, salt)
								if cryptWord == cryptPass:
									if options.verbose:
										print("The user's password was found!")
										print("[=] PASSWORD DISCOVERED ==> " + "'" + word + "'")
										print("[+]  " + user + "\t: " + word + '\t' + sha + '\n')
										foundU += "user: " + user + " >> " + "password: " + word + " >> " + "encryption: " + sha + "\n" # to make the summary of found passwords with verbose enable
										break
									else:
										if chkEnd == 1:
											print("----------------------------------------")
											print("Password found for the following users:")
											print("----------------------------------------\n")
										print("[+]  " + user + "\t: '" + word + "'\t" + sha )
									break
							else:
								print("[-] ...Could not determine user password  " + '\t' + "'" + user + "'" + "\n")
			if options.verbose:
				print("---------------------------")
				print("SUMMARY OF PASSWORDS FOUND:")
				print("---------------------------")
				print(''.join(foundU))


def w_User(options, usg):
	"""If option [-u / --user=] is used """

	if isSudo(usg) == True:
		if vef_File(options.path) == True and vef_File(options.dictionary) == True:	
			chkEnd = 0
			for user in options.user:
				countchk = 0
				with open(options.path) as file:
					for line in file:
						if line.split(":")[0] == user:
							countchk += 1
							cryptPass = line.split(':')[1].strip(' ')
							salt = chkDistro(cryptPass)
							if options.verbose:
								print ("[+] Trying for user " + "'" + str(user) + "'" + ' ...')
							if cryptPass == '':
								if options.verbose:
									print("...ignored. Account without password ('::').\n")
									continue
								print("[+]  " + user + "\t: " + "Account without password.")
								continue
							if cryptPass[0] == '!':
								if options.verbose:
									if 'root' in user:
										print("...ignored. For security reasons. lol \n")
									else:
										print("...ignored. Account locked. Login disable ('!' or '*').\n")
								continue
							if cryptPass[0] == '':
								if options.verbose:
									print("...ignored. Account without password ('::').\n")
								continue
							if '!' in line or '*' in line:
								if options.verbose:
									print("...ignored. Account locked. Login disable ('!' or '*')\n")
								continue
							sha = chkPassAlg(cryptPass)
							with open(options.dictionary) as file1:
								for word in file1:
									chkEnd += 1
									word = word.strip('\n')
									cryptWord = crypt.crypt(word, salt)
									if cryptWord == cryptPass:
										if options.verbose:
											print("The user's password was found!")
											print("[=] PASSWORD DISCOVERED ==> " + "'" + word + "'")
											print("[+]  " + str(user) + "\t: " + word + '\t' + sha + '\n')
											break
										else:
											if chkEnd == 1:
												print("----------------------------------------")
												print("Password found for the requested users:")
												print("----------------------------------------\n")
											print("[+]  " + str(user) + "\t: '" + word + "'\t" + sha )
											break
								else:
									print("[-] ...Could not determine user password  " + '\t' + "'" + str(user) + "'" + "\n")
				if countchk == 0:			
					print("[-] ...There is no account for user:  " + '\t' + "'" + str(user) + "'")		



def chkPassAlg(cryptPass):
	"""Check the encryption algorythm """

	sha = cryptPass[1]
	if sha == '6':
		return '\t(SHA-512)'
	elif sha == '5':
		return '\t(SHA-256)'
	elif sha =='1':
		return '\t(MD5)'
	else:
		return 'BLOWFISH'


def chkDistro(cryptPass):
	"""EVALUATION OF LINUX DISTRO"""

	distro = platform.linux_distribution()	 
	if distro[0] == 'Ubuntu' or 'Fedora':              
		salt = cryptPass.split('.')[0]
		return salt
	if distro[0] == 'CentOS Linux':			 
		salt = cryptPass.split('/')[0]
		return salt

def isSudo(usg):
	"""Check if user is with root privileges, otherwise cant proceed."""
	if not 'SUDO_UID' in os.environ.keys():
		print("You need privileges for this operation!\n Run with SUDO.\n")
		print("usage:", usg,"\n")
		exit(1)
	else:
		return True
		
def vef_File(chkFile):
	"""Check if the path is valid and the file exists."""
	resul = os.path.isfile(chkFile)
	if resul == False:
		print("File/Path not found Error!")
		print("Check both: '-d' and '-p' file options.")
		print("This error message will appear while one of them is not valid!")
		exit(1)
	else:
		return resul









		










		

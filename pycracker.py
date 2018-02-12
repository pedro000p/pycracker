#!/usr/bin/python3

import crypt, argparse, os, platform

def main():

	"""
	Programa para decifrar palavras-chave de utilizador(es) em Distribuições Linux.
	Feito por: Pedro Pereira & Pedro Lourenço (CET06_2017) na data de 05/05/2017.
	"""

	ld,v,v1=platform.linux_distribution()
	parser = argparse.ArgumentParser(description="Programa %(prog)s feito por Pedro Pereira & Pedro Lourenço (05/05/2017)\n"\
		 ,usage='\n[-h] -d <dicionario> [-p <passwords>] [-u <user>] [-v --verbose] [--version]')
	requeridos = parser.add_argument_group('required arguments')
	requeridos.add_argument('-d', dest='dicionario', required=True, help='especifica um ficheiro dicionario.')
	parser.add_argument('-p', dest='password', default='/etc/shadow', help='especifica um ficheiro passwords, default=/etc/shadow.')
	parser.add_argument('-u', '--user=', dest='user', help='especifica o utilizador a pesquisar.')
	parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", help='faz o verbose da cada passo.')
	parser.add_argument('--version', action='version', version='%(prog)s1.0', help='Mostra a versão e termina.')
	options = parser.parse_args()
	

	#if options.verbose:
	print("««pycracker«»Distro Linux: "+ld+", versão: "+v+" "+v1+"»»\n")
		

	if (options.password == '/etc/shadow') and  not (options.user): 
		if not 'SUDO_UID' in os.environ.keys():
			print("Precisa de privilégios para esta operação!\nSe os tem, entre na conta com privilégios e depois execute o programa.")
			print("usage:",parser.usage)
			exit(1)

		else:
			contagem=0
			u=[]
			with open(options.password) as file:
				for line in file:
					if (":") in line:
						user = line.split(':')[0]
						cryptPass = line.split(':')[1].strip(' ')
						distro=platform.linux_distribution()	 ## AVALIAÇÃO DE DISTRO LINUX
						if distro[0] == 'Ubuntu':                ## SE A DISTRO FOR UBUNTU
							salt=cryptPass.split('.')[0]
						if distro[0] == 'CentOS Linux':			 ## SE A DISTRO FOR CENTOS
							salt=cryptPass.split('/')[0]
						if options.verbose:
							print ("[+] A tentar utilizador "+"'"+user+"'"+' ...')
						if cryptPass == '':
							if options.verbose:
								print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
								continue
							print("[+]  "+user+"\t: "+"Conta sem palavra-passe.")
							continue
						if cryptPass[0] == '!':
							if options.verbose:
								if 'root' in user:
									print("...ignorado. Por motivos de segurança. \n")
								else:
									print("...ignorado. Conta bloqueada (começa com '!').\n")
							continue
						if cryptPass[0] == '':
							if options.verbose:
								print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
							continue
						if '!' in line or '*' in line:
							if options.verbose:
								print("...ignorado. Conta bloqueada/inactiva ('!' ou '*')\n")
							continue
						sha = cryptPass[1]
						if sha == '6':
							sha1 ='\t(SHA-512)'
						elif sha == '5':
							sha1 ='\t(SHA-256)'
						elif sha =='1':
							sha1 = '\t(MD5)'
						else:
							sha1 = 'BLOWFISH'
						ct=1
						n=['ou']
						with open(options.dicionario) as file1:
							for word in file1:
								
								contagem+=1
								ct+=1

								word = word.strip('\n')
								cryptWord = crypt.crypt(word, salt)
								if cryptWord == cryptPass:
									if options.verbose:
										print("Foi encontrada a palavra-passe do utilizador(a):")
										print ("[=] PALAVRA-PASSE DESCOBERTA ==> "+"'"+word+"'")
										print ("[+]  "+user+"\t: "+word+'\t'+sha1+'\n'  )
										break
									else:
										if contagem == 1:
											print("Foi encontrada a palavra-passe do(s) seguinte(s) utilizador(es): \n")
									print ("[+]  "+user+"\t: "+word+'\t'+sha1  )
								
										
									break
							else:
								print("[-] ...não foi possivel determinar a palavra-passe do utilizador(a) "+'\t'+"'"+user+"'"+"\n")

	if (options.user) and (options.password == '/etc/shadow'):
		contagem=0
		if not 'SUDO_UID' in os.environ.keys():
			print("Precisa de privilégios para esta operação!\nSe os tem, entre na conta com privilégios e depois execute o programa.")
			print("usage:",parser.usage)
			exit(1)
		else:
			verificacao_conta=0
			user = (options.user)
			with open(options.password) as file:
				for line in file:
					if line.split(":")[0]== user:
						cryptPass = line.split(':')[1].strip(' ')
						distro=platform.linux_distribution()     ## AVALIAÇÃO DE DISTRO LINUX
						if distro[0] == 'Ubuntu':                ## SE A DISTRO FOR UBUNTU
							salt=cryptPass.split('.')[0]
						if distro[0] == 'CentOS Linux':          ## SE A DISTRO FOR CENTOS
							salt=cryptPass.split('/')[0]
						if options.verbose:
							print ("[+] A tentar utilizador "+"'"+user+"'"' ...\n')
						if cryptPass == '':
							verificacao_conta=1
							if options.verbose:
								print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
								continue
							print("[+]  "+user+"\t: "+"Conta sem palavra-passe.")
							break
						if cryptPass[0] == '!':
							if 'root' in user:
								print("...ignorado. Por motivos de segurança \n")
							else:
								print("...ignorado. Conta bloqueada (começa com '!').\n")
							break
						sha = cryptPass[1]
						if sha == '6':
							sha1 ='\t(SHA-512)'
						elif sha == '5':
							sha1 ='\t(SHA-256)'
						elif sha =='1':
							sha1 = '\t(MD5)'
						else:
							sha1 = 'BLOWFISH'
						if '!' in line or '*' in line:
							print("...ignorado. Conta bloqueada (começa com '!' ou '*').\n")
							break
						with open(options.dicionario) as file1:
							for word in file1:
								#contagem+=1
								word = word.strip('\n')
								cryptWord = crypt.crypt(word, salt)
								if cryptWord == cryptPass:
									if options.verbose:
										print("Foi encontrada a palavra-passe!")
										print ("[=] PALAVRA-PASSE DESCOBERTA ==> "+"'"+word+"'")
									else:
										print("Foi encontrada a palavra-passe do utilizador(a): \n")
									print ("[+]  "+user+"\t: "+word+'\t'+sha1+'\n'  )
									verificacao_conta+=1
									break
							else:
								print("[-] ...não foi possivel determinar a palavra-passe do utilizador(a) "+'\t'+"'"+user+"'"+"\n")
								
				else:
					if verificacao_conta < 1:
						print("[-] ...não existe conta de utilizador para o(a):\t"+user)

	if (options.password is not '/etc/shadow') and not options.user:
			contagem=0
			with open(options.password) as file:
				for line in file:
					if (":") in line:
						user = line.split(':')[0]
						cryptPass = line.split(':')[1].strip(' ')
						distro=platform.linux_distribution()	 ## AVALIAÇÃO DE DISTRO LINUX
						if distro[0] == 'Ubuntu':                ## SE A DISTRO FOR UBUNTU
							salt=cryptPass.split('.')[0]
						if distro[0] == 'CentOS Linux':			 ## SE A DISTRO FOR CENTOS
							salt=cryptPass.split('/')[0]
						if options.verbose:
							print ("[+] A tentar utilizador "+"'"+user+"'"+' ...')
						if cryptPass == '':
							if options.verbose:
								print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
								continue
							print("[+]  "+user+"\t: "+"Conta sem palavra-passe.")
							continue
						if cryptPass[0] == '!':
							if options.verbose:
								if 'root' in user:
									print("...ignorado. Por motivos de segurança. \n")
								else:
									print("...ignorado. Conta bloqueada (começa com '!').\n")
							continue
						if cryptPass[0] == '':
							if options.verbose:
								print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
							continue
						if '!' in line or '*' in line:
							if options.verbose:
								print("...ignorado. Conta bloqueada/inactiva ('!' ou '*')\n")
							continue
						sha = cryptPass[1]
						if sha == '6':
							sha1 ='\t(SHA-512)'
						elif sha == '5':
							sha1 ='\t(SHA-256)'
						elif sha =='1':
							sha1 = '\t(MD5)'
						else:
							sha1 = 'BLOWFISH'
						with open(options.dicionario) as file1:
							for word in file1:
								contagem+=1
								word = word.strip('\n')
								cryptWord = crypt.crypt(word, salt)
								if cryptWord == cryptPass:
									if options.verbose:
										print("Foi encontrada a palavra-passe!")
										print ("[=] PALAVRA-PASSE DESCOBERTA ==> "+"'"+word+"'")
										print ("[+]  "+user+"\t: "+word+'\t'+sha1+'\n' )
										break
									else:
										if contagem == 1:
											print("Foi encontrada a palavra-passe do(s) seguinte(s) utilizador(es): \n")
										print ("[+]  "+user+"\t: '"+word+"'\t"+sha1  )
									break
							else:
								print("[-] ...não foi possivel determinar a palavra-passe do(a) utilizador(a) "+'\t'+"'"+user+"'"+"\n")

	if (options.password is not '/etc/shadow') and options.user:
		contagem=0
		user = (options.user)
		with open(options.password) as file:
			for line in file:
				if line.split(":")[0]== user:
					cryptPass = line.split(':')[1].strip(' ')
					distro=platform.linux_distribution()     ## AVALIAÇÃO DE DISTRO LINUX
					if distro[0] == 'Ubuntu':                ## SE A DISTRO FOR UBUNTU
						salt=cryptPass.split('.')[0]
					if distro[0] == 'CentOS Linux':          ## SE A DISTRO FOR CENTOS
						salt=cryptPass.split('/')[0]
					if options.verbose:
						print ("[+] A tentar utilizador "+"'"+user+"'"' ...\n')
					if cryptPass == '':
						if options.verbose:
							print("...ignorado. Conta sem palavra-passe (começa com '::').\n")
							break
						print("[+]  "+user+"\t: "+"Conta sem palavra-passe.")
						break
					if cryptPass[0] == '!':
						if 'root' in user:
							print("...ignorado. Por motivos de segurança \n")
						else:
							print("...ignorado. Conta bloqueada (começa com '!').\n")
						break
					sha = cryptPass[1]
					if sha == '6':
						sha1 ='\t(SHA-512)'
					elif sha == '5':
						sha1 ='\t(SHA-256)'
					elif sha =='1':
						sha1 = '\t(MD5)'
					else:
						sha1 = 'BLOWFISH'
					if '!' in line or '*' in line:
						print("...ignorado. Conta bloqueada (começa com '!' ou '*').\n")
						break
					with open(options.dicionario) as file1:
						for word in file1:
							
							word = word.strip('\n')
							cryptWord = crypt.crypt(word, salt)
							if cryptWord == cryptPass:
								contagem+=1
								if options.verbose:
									print("Foi encontrada a palavra-passe!")
									print ("[=] PALAVRA-PASSE DESCOBERTA ==> "+"'"+word+"'")
									

								else:
									print("Foi encontrada a palavra-passe do utilizador(a): \n")
								print ("[+]  "+user+"\t: '"+word+"'\t"+sha1+'\n' )
								if contagem == 1:
									return
								break
						else:
							print("[-] ...não foi possivel determinar a palavra-passe do utilizador(a) "+'\t'+"'"+user+"'"+"\n")
			else:
				print("[-] ...não existe conta de utilizador para o(a):\t"+user)

if __name__ == "__main__":
	main()

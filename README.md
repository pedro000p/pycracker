# pycracker
Read me in Portuguese

.1 --> No trabalho de projecto pycracker, foram implementados os módulos argparse para a construção de sintaxe na linha de comandos. O módulo crypt para fazer a conversão da hash e do salt para uma palavra-passe. O módulo os para verificar se o utilizador pertence aos sudoers ou não, se por ventura quiser usar o ficheiro por default do argumento '-p ' que tem o /etc/shadow por default, e por último o módulo platform para identificar a distro que o user está a utilizar assim como a sua versão.

[1]
import crypt, argparse, os, platform


.2 --> 1º, as variaveis 'ld', 'v' e 'v1' recebem em paralelo toda a informação que o 'platform.linux_distribuition()' dá.
Na implementação do argparse foi passado para a variavel parser os argumentos através da sintaxe do módulo com o argparse.ArgumentParser() onde insere a descrição, assim como o usage.
Em cada argumento que só necessita do caractere para validar como por exemplo o -'v', dá-se um nome com a atribuição 'dest=', a 'action=' permite dar a ação a esse mesmo argumento que neste caso para o '-v' de store_true, com este ação o argumento não precisa de argumentos suplementares para ser validado.
No argumento '-d', define-se o 'dest=' como dicionário onde ele assume esse nome, como é requerido atribui-se a definição 'required=True'.
No argumento '-u' acaba po ser o mesmo mas tem a versão longa e como o argparse assume as duas, óptimo.
No final, passa-se todos os argumentos para a varivel options definida, através do 'parser.parse_args()'. 


[2]

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



.3 (1ªparte) --> No bloco que se segue, por ser um pouco extenso vai ser dividido em secções para não ficar demasiado massudo.
Na 1ª entrada IF contempla-se a hipotese de ser usado o /etc/shadow que está por default e não ser introduzido um utilizador em concreto.
Assim sendo, verifica-se 1º se o mesmo utilizador está no grupo dos sudoers, e se não estiver, faz-se o print com um aviso a dizer que precisa de privilégios para completar a ação. O ELSE é para o caso de existirem essas permissões.
Na entrada do ELSE usa-se o 'with open()' para abrir o /etc/shadow como ficheiro e sobre essa informação na mémória usa-se o ciclo FOR para iterar essa informação linha a linha, ou melhor por segmentos baseados na referência ':', se existir. A variavel 'user' vai receber o campo zero do line.split a 'cryptPass' vai receber o campo 1 que é a hash e o salt já com o strip de espaços. Depois é verificado a distro que está a ser usada porque a composição da hash é diferente em CentOS do Ubuntu, porque a variavél cryptPass vai dar a parte referente ao salt onde começa a partir do '.' através do split('.') em Ubuntu. Em CentOS comaça a partir da da slash '/'. isto verificou-se por querermos um programa versátil para várias distros. 

[3] (1ª parte)
if (options.password == '/etc/shadow') and  not (options.user): 
        if not 'SUDO_UID' in os.environ.keys():
                print("Precisa de privilégios para esta operação!\nSe os tem, entre na conta com privilégios e depois execute o programa.")
                print("usage:",parser.usage)
                exit(1)

        else:
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



.3 (2ª parte) --> Dando continuidade ao bloco, começa-ase a fazer os IFS para PRINTs através das possibilidades que podem existir na linha do shadow por user, se a varivel cryptPass através da segmentação por (':') ficar vazia, é porque o user não tem palavra-passe e por ai fora.
O código é bastante simples e descritivo nesta parte.



[3] (2ª parte)

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
"""

.3 (3ª parte) --> Nesta parte começa-se por fazer uma distinção ao campo 1 do algoritmo hash que nos diz que tipo d encriptação foi usada. Assim consegue-se dizer ao utilizador do programa o que apanhou no percurso da descodificação, assim sendo temos um IF para cada tipo de algoritmo hash. Logo de seguida vem o ciclo FOR interior que verifica o ficheiro dicionário com quase a mesma abordagem que o anterior mas neste caso faz-se um strip às linhas(palavras), junta-se a palavra e o salt para verificar se é igual à palavra encontrada. Se for e a opção verbose estiver ON, mostra-se o print respectivo, senão mostra-se o print do ELSE. A variavél 'contagem' é para só ser feito o print uma vez.
O último ELSE é só para constar se por ventura não foi encontrada a palavra-passe.



[3] (3ª parte)

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
				print ("[=] PALAVRA-PASSE DESCOBERTA ==> "+"'"+word+"'"+'\n')
				break
			else:
				if contagem == 1:
					print("Foi encontrada a palavra-passe do(s) seguinte(s) utilizador(es): \n")
				print ("[+]  "+user+"\t: "+word+'\t'+sha1  )
			break
	else:
		print("[-] ...não foi possivel determinar a palavra-passe do utilizador(a) "+'\t'+"'"+user+"'"+"\n")


4 --> Todo o programa é construido nesta base, a única variância são os IFs de entrada para não haver ambiguidades. Gostavamos de ter o programa mais simplificado mas o não uso das 'DEFs' levou-nos a criar estes blocos com um tamanho considerável, contudo faz o que se pede.
Vai-se expor agora as pequenas diferenças existentes.
Na entrada principal do IF seguinte temos esta variante, onde a entrada é clara e especifica.

[4]

if (options.user) and (options.password == '/etc/shadow'):




5 --> A outra entrada principal IF.Assim como a última. Os prints onde inclui a opção de 'user' está no singular e sem a opção está no plural.

[5.1]
if (options.password is not '/etc/shadow') and not options.user:

[5.2]
	if (options.password is not '/etc/shadow') and options.user:


De resto não há nada mais significativo a acrescentar.

FIM

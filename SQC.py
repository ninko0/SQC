#!/bin/python3

import os 
import sys
import paramiko
import argparse
import textwrap
import time

## requirement ?
#python 3 update manager pour update pgrade
#


def main():
	version = "version 0.0.1"


	#---------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------

	### gestion d'argument pour SSH

	parser = argparse.ArgumentParser()

	# version
	parser.add_argument("-v","--version",help="show version, actually " + version, action="store_true")


	# file and how to use file
	parser.add_argument("-f","--file",help=textwrap.dedent('''\
			use a file to list host, port, user, password.
			The file must be like this : \n
			host1 225 user1 password1 \n
			192.168.0.1 223 user2 password2\n
			...
			 '''), type=str)


	# list of hosts without using file
	parser.add_argument("--hosts",help="put a list of all your hosts", type=list, metavar="hosts")

	# list of ports without using file
	parser.add_argument("--ports",help="put a list of all your ports", type=list, metavar="ports")

	# list of users without using file
	parser.add_argument("--users",help="put a list of all your users", type=list, metavar="users")

	# list of password without using file
	parser.add_argument("--passwd",help="put a list of all your password", type=list, metavar="passwd")


	#---------------------------------------------------------------------------------------


	## Parametre pour les scripts

	parser.add_argument("--upgrade",help="this do update and upgrade of all systeme", action="store_true")

	parser.add_argument("--adduser", help= "give a user and it create it", type=str)

	parser.add_argument("--quick_install", help= "install every thing you want to deploy", type=list)
	
	parser.add_argument("--gitclone", help= "gitclone a list of all your fav tools", type=list)
	
	parser.add_argument("--ssh_conf", help= "change the configuration file of ssh, it will ask you questions", action="store_true") 
	
	parser.add_argument("--netplan_conf", help= "change the configuration file of netplan, it apply it after all configuration are done", type=str) 

	#---------------------------------------------------------------------------------------
	
	#read all args of the one line
	args = parser.parse_args()

	#---------------------------------------------------------------------------------------
	
	
	#print version
	if args.version:
		print(version)
		exit()
	
	#check if file is good	
	if args.file:
		try:
			file_function(args.file)
			
			print(str(glob_lenth) + " lenth test")
			
		except Exception as error:
			print(str(error) + "this is at line 82")
			print(textwrap.dedent('''\
			  use a file to list host, port, user, password.
			  The file must be like this :
			
			  HOST/IP PORT USER PASSWORD
			  host1 225 user1 password1
			  192.168.0.1 223 user2 password2
			 ...
			 '''))
			exit()
			
	#---------------------------------------------------------------------------------------
	
	#check if host/port/user/passwd are good
	elif args.hosts and args.ports and args.users and args.passwd:
		try:
			file_function(0, args.hosts, args.ports, args.users, args.passwd)
			
		except Exception as error:
			print(str(error) + "this is at line 105\n")
			print('you need to define host, port, users and passwords to make it work')
			exit()
	else:
		print("all arguments are needed (host, port, user, passwd), or a file with all information")
		exit()
	
	#---------------------------------------------------------------------------------------
	
	#
	#check all parameter to execute code
	#

	if glob_lenth != 0:
		for i in range(glob_lenth-1):
			
			connect = connecting_ssh(glob_ip[i], glob_user[i], glob_password[i], glob_port[i])
			
			if args.adduser:
				print(args.adduser)
				addusr(args.adduser, connect)
				
			if args.upgrade:
				print("update en cours")
				upgrade(connect)
				
			if args.quick_install:
				print("install of all packages")
				quick_install(args.quick_install,connect)
				
			if args.gitclone:
				print("git_cloning...")
				#git_clone(args.gitclone,connect)
				
				
			if args.ssh_conf:
				port = input("change port ?")
				CA = input("add CA? ")
				no_pass = input("add no password connexion ?")
				ssh_config(port, CA, no_pass, connect)
				
			if args.netplan_conf:
				netplan_config(args.netplan_conf, connect)	
				
				
			#restart_all(connect)


	#---------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------
	

#---------------------------------------------------------------------------------------

#verification des list pour la connexion ssh


	
def file_function(file=0,ip=[],port=[],user=[],password=[]):

	# extract lenth, create list of IP,hosts / ports / user / password
	global glob_lenth 
	global glob_ip 
	global glob_port 
	global glob_user 
	global glob_password 
	glob_lenth = 0
	glob_ip = []
	glob_port = []
	glob_user = []
	glob_password = []
	
	if file != 0:
		f = open(file,"r")
		L=f.readlines()
		for i in range(len(L)-1):
			glob_ip.append(L[i].split()[0])
			glob_port.append(L[i].split()[1])
			glob_user.append(L[i].split()[2])
			glob_password.append(L[i].split()[3])
			glob_lenth = len(L)
		print(glob_lenth, glob_ip, glob_port, glob_user, glob_password)
		
	elif ip != [] and port != [] and user != [] and password != []:
	
		ip = parsing_list(ip)
		port = parsing_list(port)
		user = parsing_list(user)
		password = parsing_list(password)
					
		if len(ip) == len(port) == len(user) == len(password):
			glob_ip = ip
			glob_port = port
			glob_user = user
			glob_password = password
			glob_lenth = len(ip)+1
		else:
			print("error, all list need to be the same lenth")
			exit()
		print(glob_lenth, glob_ip, glob_port, glob_user, glob_password)
	else:
		print("error ligne 182, error parsing argument of the command")
	
	return 0
	
	
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------


#creation du lien SSH

def connecting_ssh(ip, user, password, port):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh_client.connect(hostname=ip, port=port, username=user, password=password)
	return ssh_client


	
#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------	
#---------------------------------------------------------------------------------------	

#all function linked with options	
	
	
def addusr(user, ssh_client):
	#specify user and group name to add them in the machin
	for i in range(glob_lenth-1):
		
		stdin,stdout,stderr=ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S useradd " + user) 
		
		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())
		
		channel=ssh_client.invoke_shell()
		channel.send('sudo passwd '+user+'\n')
		time.sleep(0.2)
		channel.send('azer\n')
		time.sleep(0.2)
		channel.send('azer\n')
		time.sleep(0.2)
		channel.send('azer\n')
		channel.close()

	
	print("user " + user + " bien ajoutés")
	return ("user " + user + " bien ajoutés")
	
	
	
	
def upgrade(ssh_client):
	for i in range(glob_lenth-1):
		stdin,stdout,stderr=ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S apt update" ) 
		
		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())
		
		stdin,stdout,stderr=ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S apt upgrade -y" ) 
		
		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())





def quick_install(packages,ssh_client):
	packages = ', '.join(parsing_list(packages))
	print(packages)
	for i in range(glob_lenth-1):
		stdin,stdout,stderr = ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S apt-get install " + packages + " -y ") 
		
		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())
		
	
	
###############################
##############
###
#verifier la fonction !!!!		
def git_clone(git_link,ssh_client):
	git_links = ', '.join(parsing_list(git_link))
	print(git_links)
	for i in range(glob_lenth-1):
		for j in range(nombre_de_repo_git):
		
			stdin,stdout,stderr = ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S gitclone " + L_git_links[j]) 
			print(L_git_links[j] + " cloned successfuly")
			print("Sortie : " , stdout.readlines())
			print("Erreur : " , stderr.readlines())
			




def ssh_config(port, CA, no_pass, ssh_client):
	
	conf = "Port " + port + "\nPubkeyAuthentication yes \nAuthorizedKeysFile " + CA + "\nPasswordAuthentication " + no_pass + "\n"
	
	for i in range(glob_lenth-1):
		stdin,stdout,stderr = ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S touch /etc/ssh/sshd_config.d/ssh_skull.conf")		

		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())
		
		channel=ssh_client.invoke_shell()
		channel.send("sudo echo '"+ conf +"' | sudo tee /etc/ssh/sshd_config.d/ssh_skull.conf \n")
		time.sleep(0.2)
		channel.send(glob_password[i] + "\n")
		time.sleep(0.2)
		channel.send(glob_password[i] + "\n")
		time.sleep(0.2)
		channel.close()
	
		
def netplan_config(file, connect):

	print(type(file))
		
	for i in range(glob_lenth-1):
		# github link
		cmd = "scp -P 44" + " " + file + " azer@192.168.60.109:/etc/netplan/00-installer-config.yaml" 
		print(cmd)
		os.system(cmd)
	print("c bon je pense")
			  




#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------	
#---------------------------------------------------------------------------------------	

# fonction do dont do redondance

#usefull to parse list generated by args.parse
def parsing_list(L):
	L1 = L
	L2 = [L[0]]
	for i in range(1,len(L1)):
		L2[0] = (L2[0]+L1[i])
		L = L2[0].split(",")
	return (L)



def restart_all(ssh_client):
	for i in range(glob_lenth-1):
		stdin,stdout,stderr = ssh_client.exec_command("echo '" + glob_password[i] + "' | sudo -S reboot")		
		print("Sortie : " , stdout.readlines())
		print("Erreur : " , stderr.readlines())
	



	
	
if __name__=="__main__":
	main()		
	
	
	
	
	
	
	
	
	
	


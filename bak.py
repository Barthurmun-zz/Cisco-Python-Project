import paramiko
import re
from pprint import pprint
import time
import sys
import os

text = '''
-----------------------------------------------
Authors: 
Urszula Lis urszula.lis95@gmail.com
Jakub Bryl kuba.bryl1996@gmail.com
Krzysztof Krawiec krzysztof.krawiec3@gmail.com
-----------------------------------------------

This is python project documentation.
This script was developed for linux operation system.

In this directory you can find documentation for each device.\n
It was created with device name, for example Device_R1.txt 

This directory contains exact number of files like devices in topology.

This folder contains:
'''
os.system('mkdir Dev_Documentation')
w = open('./Dev_Documentation/README.txt','w') 
w.write(text)
w.close()


class Main_module():
	def __init__(self):
		self.range_dic={}
		self.password_dic={}
		self.commands_list = ['show version','show cdp neighbors','show ip int brief','show inventory']
		self.container = []

		self.parse_password()
		self.parse_range()
		self.parse_data()
		self.make_connection()
		self.parse_output()

	def parse_password(self):
		with open('password.txt','r') as f:
			for line in f:
				(key,val)=line.split()
				self.password_dic[key]=val

	def parse_range(self):
		with open('range.txt','r') as f:
			for line in f:
				(key,val)=line.split()
				self.range_dic[key]=val

	def parse_data(self):
		for device in self.range_dic:
			self.user = device
			self.password= self.password_dic[device]
			self.ip = self.range_dic[device]
			#print(self.user,self.password,self.ip)

	def make_connection(self):
		for device,ip in self.range_dic.items():
			print" --------LOGIN TO:%s ------ IP:%s -------PASSWORD:%s------- " %(device,ip,self.password_dic[device])
			ssh_client=paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(hostname = ip,
					   username = device,
					   password = self.password_dic[device])
			
			remote_conn = ssh_client.invoke_shell()
			w = open('./Dev_Documentation/Device_'+device+'.txt', 'w')
			for item in self.commands_list:
				remote_conn.send('\n'+item+'\n')
				time.sleep(0.2)
				remote_conn.send(' ')
				time.sleep(0.1)
				output = remote_conn.recv(9000)
				w.write(output)
			
			ssh_client.close()	
			w.close()

	def parse_output(self):
		module_regex = r'NAME:\s\"((\w+\s|\w+)+)\"'
		ios_regex = r'Version\s\d+.\d+\(\d+\)\w+'
		version_regex = r'Software\s\((((\w+\-)+)\w+)\)'
		modules_compiler = re.compile(module_regex)
		modules = []

		for device,ip in self.range_dic.items():
			neighbors = []
			neigh_var = device
			filepath = './Dev_Documentation/Device_'+device+'.txt'
			with open(filepath) as f:
				file=f.read()
			
			w = open('./Dev_Documentation/Device_'+device+'.txt', 'w')
			software = re.search(ios_regex,file)
			ios_type = software.group()
			w.write('\t\t\t $$$$$  DEVICE: %s  $$$$$ \n\n - IOS_TYPE: %s - \n' %(device,ios_type))
			w.close()

			a = open('./Dev_Documentation/Device_'+device+'.txt', 'a')
			b = open('./Dev_Documentation/README.txt','a')
			hardware = re.search(version_regex, file)
			hardware_type = hardware.group(1)
			b.write('\n->Device_'+device+'.txt')
			a.write(' - HARDWARE_VERSION: %s - \n\n' %(hardware_type))
			a.write(' -- MODULES INSTALLED ON DEVICE: -- \n')
			for match in modules_compiler.finditer(file):
				modules.append(match.group(1))
				a.write(' -     %s     - \n' %(match.group(1))) 	
				
			line_list=file.split('\n')
			#print (line_list)
			a.write('\n -- INTERFACES OF DEVICE -- \n\n')
			for i in range (len(line_list)):
				if "Device ID" in line_list[i]:
					while neigh_var not in line_list[i+1]:
						i+=1
						neighbors.append(line_list[i])
				if "NVRAM" in line_list[i] and "YES" in line_list[i]:
					tmp=line_list[i].split()
					if "administratively" in line_list[i]:
						a.write(' - Interface Name: %s - \n - Interface Status: %s %s - \n - Protocol: %s - \n\n'
						        %(tmp[0],tmp[4],tmp[5],tmp[6]))
 					else:
						a.write(' - Interface Name: %s - \n - Interface Status: %s - \n - Protocol: %s - \n\n'
						        %(tmp[0],tmp[4],tmp[5]))
			a.write(' -- NEIGHBORS LIST: -- \n\n')
			for i in range (len(neighbors)):
				tmp=neighbors[i].split()
				a.write(' - '+tmp[0]+' - \n')
			
			a.write('\t\t\t $$$$$  END  $$$$$ \n ')
			a.close()   		
			

if __name__ == '__main__':
	obj = Main_module()	

#!/usr/bin/python

import socket
import threading
import time
import random
import datetime

bind_ip = "192.168.1.35"
bind_port = 2323

log_file = "./baiter.log"

# client-handling thread
def handle_client(client_socket, client_ip, client_port):
	
	# send title
	client_socket.send(("\nVery nice very hackable CCTV camera."
		"\n====================================\n\n"))
	
	
	while True:
	
		try:
			# send fake login prompt
			client_socket.send("login: ")
			
			# get login
			data_login = client_socket.recv(256).strip()
			
			# removes initial telnet header
			if not all(ord(char) < 128 for char in data_login):
				data_login = client_socket.recv(256).strip()

			# send fake password prompt
			client_socket.send("password: ")
			
			# get password
			data_pass = client_socket.recv(256).strip()
			
			# print harvested data
			# print "%s %s" % (data_login, data_pass)
			
			# log harvested data
			write_to_log(data_login, data_pass, client_ip)
			
			# send fake try again prompt
			time.sleep(random.uniform(1.0, 3.0))
			client_socket.send("no dice, try again\n\n")
			
			# break out of loop on long inputs or exit command
			if data_pass == "exit" or len(data_login) == 256 or len(data_pass) == 256:
				break
		
		except:
			break
	
	# close connection
	print "[*] Closing connection from %s:%d" % (client_ip, client_port)
	client_socket.close()


# write login attempts to log file
def write_to_log(username, password, client_ip):
	
	# get timestamp
	timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
	
	# open and append file
	try:
		with open(log_file, "a") as fp:
			fp.write("%s %s >> %s %s\n" % (timestamp, client_ip, username, password))
	except:
		print "[*] Error writing to log file"


# main function creates socket, listens for connections    
def main():
	
	# create socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind listener to socket
	server.bind((bind_ip, bind_port))

	# listen for requests (maximum backlog 5)
	server.listen(5)
	
	print "[*] Listening on %s:%d" % (bind_ip, bind_port)
		
	while True:
		
		try:
			client, addr = server.accept()
			
			print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
			
			# spin up client thread to handle incoming data
			client_handler = threading.Thread(target=handle_client, args=(client,addr[0],addr[1],))
			client_handler.start()
			
		except:
			print "\n[*] Closing all connections to %s:%d" % (bind_ip, bind_port)
			break

if __name__ == "__main__":
    main()

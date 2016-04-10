#!/bin/env python
import sys
import os
import json

def opener(path, flags):
	dir_fd = os.open(os.path.expanduser("~/"), os.O_RDONLY)
	return os.open(path, flags, dir_fd=dir_fd)

def loadTibiaClients():
	tibia_clients = {}
	file = None
	try:
		with open(".tibia-clients", "r", opener=opener) as clients:
			tibia_clients = json.load(clients)
	except FileNotFoundError:
		file = open(".tibia-clients", "x", opener=opener)

	if not tibia_clients:
		tibia_path = ""
		while not tibia_path:
			tibia_path = input("First time running. Input the absolute path to one Tibia client: ")
			if not os.path.isfile(tibia_path):
				tibia_path = ""
				print("Invalid file path")

		tibia_version = ""
		while not tibia_version:
			try:
				tibia_version = input("Input Tibia version: ")
				float(tibia_version)
			except ValueError:
				tibia_version = ""

		tibia_clients[tibia_version] = tibia_path

	if file:
		json.dump(tibia_clients, file)
		file.close()

	return tibia_clients

def insertTibiaClient(tibia_clients, tibia_version, tibia_path):
	tibia_clients[tibia_version] = tibia_path
	with open(".tibia-clients", "w", opener=opener) as f:
		json.dump(tibia_clients, f)



if __name__ == '__main__':
	tibia_clients = loadTibiaClients()
	valid_version = sys.argv[1] == "new"
	if valid_version:
		tibia_path = ""
		while not tibia_path:
			tibia_path = input("Input the absolute path to one Tibia client: ")
			if not os.path.isfile(tibia_path):
				tibia_path = ""
				print("Invalid file path")

		tibia_version = ""
		while not tibia_version:
			try:
				tibia_version = input("Input Tibia version: ")
				float(tibia_version)
			except ValueError:
				tibia_version = ""

		insertTibiaClient(tibia_clients, tibia_version, tibia_path)

	while not valid_version:
		try:
			tibia_version = sys.argv[1]
			float(tibia_version)
			valid_version = True
		except ValueError:
			tibia_version = input("Invalid Tibia version, input it again: ")
			valid_version = False

	if not os.path.isfile(tibia_clients[tibia_version]):
		print("Update Tibia path for version " + tibia_version)
		exit()

	startTibia(tibia_clients[tibia_version], sys.argv[1])

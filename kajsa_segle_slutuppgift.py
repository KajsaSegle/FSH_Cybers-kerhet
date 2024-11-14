#Målet är att all input ska ges innan programmet körs.
#Användaren ska kunna skapa en ny nyckel.
#Användaren ska också kryptera eller dekryptera en fil med hjälp av valfri existerande nyckel.

import argparse
import os 
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="Kajsa's encryption tool")
parser.add_argument("task", choices=["key", "encrypt", "decrypt"], help="In order to generate a new key: write 'key' followed by the name you wish to give to the new key file. In order to encrypt: write 'encrypt' followed by the name of the key you want to use and then '-v' followed by the name of the file you wish to encrypt. In order to decrypt: write 'decrypt' followed by the name of the key you want to use and then '-v' followed by the name of the file you wish to decrypt.")
parser.add_argument("keyname", help="This is either the name of the key you wish to create or the name of the key you wish to use.")
parser.add_argument("-v" "file", help="Choose a file to either encrypt or decrypt.")

args = parser.parse_args()

filename = args.vfile
keyname = args.keyname
 
#Genererar och sparar nyckel i ny key-fil. 
#Programmet tillåter inte att man skriver över en redsan existerande nyckel.
#Tanken är att undvika en situation där man krypterat filer med en viss nyckel och sedan råkar skriva över den för att man väljer samma namn på en ny nyckel.
if args.task == "key":
    if os.path.isfile(keyname):
        print("That name is taken. Choose another name for your key.")
    else:
        key = Fernet.generate_key()
    
        with open(keyname, "wb") as file:
            file.write(key)     
            print(f"The key was successfully generated and is now stored in {keyname}. It looks like this: {key}")  


elif args.task == ("encrypt").lower():
    #Om användaren skriver 'encrypt' sker en kontroll av huruvida filen som ska krypteras redan finns eller inte.
    if not os.path.isfile(filename):
        print(f"{filename} does not exist. Choose another file.")
    else: 
        #Det genomförs även en kontroll av huruvida den angedda nyckeln finns. Om inte ges ett felmeddelande.
        if not os.path.isfile(keyname):
            print(f"This key does not exist. Choose an existing key or create a new one in order to encrypt {filename}")
        else: 
            #Läser in den önskade nyckeln
            with open(keyname, 'rb') as file:
                key = file.read()

            cipher_suite = Fernet(key)
    
            #Läser in och krypterar filen
            with open(filename, "rb") as file_object:
                content = file_object.read()
                cipher_text = cipher_suite.encrypt(content)
        
            with open(filename, "wb") as file:
                file.write(cipher_text)
                print(f"{filename} was succesfully encrypted.")

elif args.task == ("decrypt").lower():
    #Om användaren skriver 'decrypt' så genomförs en kontroll av huruvida filen som ska dekrypteras finns. 
    #Om den inte finns ges ett felmeddelande.
    if not os.path.isfile(filename):
        print(f"{filename} does not exist. Choose another file.")
    else: 
        #Det sker även en kontroll av huruvida den angedda nyckeln finns. Om den inte finns ges ett felmeddelande.
        if not os.path.isfile(keyname):
            print(f"This key does not exist. Choose an existing key or create a new one in order to decrypt {filename}")
        else:
            #Läser in nyckeln som ska användas
            with open(keyname, 'rb') as file:
                key = file.read()

            cipher_suite = Fernet(key)

            #Läser in och dekrypterar filen
            with open(filename, "rb") as file:
                encrypted = file.read()
                plain_text = cipher_suite.decrypt(encrypted)

            with open(filename, "wb") as file:
                file.write(plain_text)
                print(f"{filename} was succesfully decrypted.")

    









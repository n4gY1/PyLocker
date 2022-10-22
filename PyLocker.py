import argparse
import os
import sys
import uuid
from os import path
from termcolor import colored
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)


def banner():
    _banner = ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,,,,,.   .,,,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,                 ,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,                      .,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,          ,,,,,          ,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,.        ,,,,,,,,,,,        ,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,       ,,,,,,,,,,,,,,        ,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,                                 ,,,,,,,,\n"
    _banner += ",,,,,,,,,                                 ,,,,,,,,\n"
    _banner += ",,,,,,,,,               .,,,              ,,,,,,,,\n"
    _banner += ",,,,,,,,,              ,,,,,,             ,,,,,,,,\n"
    _banner += ",,,,,,,,,               ,,,,              ,,,,,,,,\n"
    _banner += ",,,,,,,,,               ,,,,              ,,,,,,,,\n"
    _banner += ",,,,,,,,,               ,,,,,             ,,,,,,,,\n"
    _banner += ",,,,,,,,,              ,,,,,,             ,,,,,,,,\n"
    _banner += ",,,,,,,,,                                 ,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,, PyLOCKER ,,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,, HyBase -HU ,,,,,,,,,,,,,,,,,,,\n"
    _banner += ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n"
    print(_banner)


def encrypt_file(file_name):
    try:

        with open(file_name, 'rb') as file:
            content = file.read()
            file.close()

        encrypt_content = fernet.encrypt(content)
        with open(file_name, 'wb') as enc_file:
            enc_file.write(encrypt_content)

            print(colored("[+]", 'green'), "File encrypt success", file_name)

            enc_file.close()

    except Exception as e:
        print(colored("[-]", 'red'), "Encrypt error", e)


def start_encrypt():
    try:
        key_name = str(uuid.uuid1()).replace("-", "")[:7] + ".kex"

        with open(key_name, 'wb') as filekey:
            filekey.write(key)
            filekey.close()

        print(colored("[+]", 'green'), "Created recovery key", key_name)
    except Exception as e:
        print(colored("[-]", 'red'), e)


def decrypt(file_name, key_path):
    try:
        with open(key_path, 'rb') as key:
            decrypt_key = key.read()
            key.close()
        fernet = Fernet(decrypt_key)
        with open(file_name, 'rb') as file:
            content = file.read()
            file.close()
        with open(file_name, 'wb') as file:
            dec_content = fernet.decrypt(content)
            file.write(dec_content)
            print(colored("[+]", 'green'), "file decrypt success :", file_name)
            file.close()

    except Exception as e:
        print(colored("[-]", 'red'), "Decrypting error", e)


def initial(options, directory, key=None):
    if path.isdir(directory) is False and path.exists(directory) is False:
        print(colored("[-]", 'red'), "Error, path is not exist: ", directory)
        return
    print(colored('[+]', 'green'), "Directory is exist:", directory)
    if options == 'Encrypt':
        print(colored("[!]", 'yellow'),
              "Warning, your all files encrypted this directory. If you loose recovery key, your data never can "
              "restore", "Print 'yes' to continuous &=> ", end="")
        ok = input()
        if ok != "yes":
            return
        else:
            start_encrypt()  # init key recover

    for root, subdirs, files in os.walk(directory):
        i = 1
        for file in files:
            xpath = os.path.join(root, file)
            # print("[+] ", xpath, "[", os.stat(xpath).st_size, "byte]")
            i += 1
            if options == "Decrypt":
                decrypt(xpath, key)

            elif options == "Encrypt":
                encrypt_file(xpath)

    print("Program is finish")
    input()


if __name__ == '__main__':
    banner()

    parser = argparse.ArgumentParser(add_help=True, description="Encrypt - Decrypt Directory with recursive. "
                                                                "Warning, if you leave encrypt key, your data never "
                                                                "can be restored")

    parser.add_argument('-options', help='[Encrypt] : Encrypt all files and generate recover key or \n'
                                         '[Decrypt] : Decrypt directory all files with use recover key',
                        choices=['Encrypt', 'Decrypt'])
    parser.add_argument('-directory', help='Directory location path. Warning, all files encrypted (or decrypted with '
                                           'restore key)')
    parser.add_argument('-key', help='Recover key file location path')

    args = parser.parse_args()

    if args.options == 'Decrypt' and args.key is None:
        print(colored('[-]', 'yellow'), "You selected 'Decrypt' options but not added recovery key [-key 'file']")
        sys.exit(0)
    if args.options is not None and args.directory is not None:
        initial(args.options, args.directory, args.key)
    else:
        print("")
        print(colored("usage: PyLocker.py [-h] [-options {Encrypt,Decrypt}] [-directory DIRECTORY] [-key KEY]",'yellow'))
        print("")

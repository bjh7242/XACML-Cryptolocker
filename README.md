# XACML Cryptolocker
This project implements RC4 encryption for files and uses role based access control via XACML and authentication using a shadow file with SHA512 hashes. 

Sample run:
```
python main.py -A encrypt -D /path/to/directory -R -K Key -C -V
```
The above command will recursively encrypt the contents in the directory specified (relative paths are supported). This uses RC4 with the key 'Key' and will deleted the unencrypted files (-C for cleanup). It will add .enc to all of the encrypted files. The -V argument is used for verbose output.

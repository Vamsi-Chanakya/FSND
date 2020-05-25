# Import Package
from cryptography.fernet import Fernet

# Generate a Key and Instantiate a Fernet Instance
#key = Fernet.generate_key()
key = b'8cozhW9kSi5poZ6TWFuMCV123zg-9NORTs3gJq_J5Do='
f = Fernet(key)

print(key)# Define our message
#plaintext = b"encryption is very useful"
plaintext = b'encrypting is just as useful'

# Encrypt
ciphertext = f.encrypt(plaintext)
print(ciphertext)

# Decrypt
decryptedtext = f.decrypt(ciphertext)
print(decryptedtext)
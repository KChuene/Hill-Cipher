# Hill-Cipher (Under ongoing testing and debugging)

An experimental project; a hill cypher encryption tool. Uses matrices (arrays of numbers) to encrypt and decrypt text. Both the message and the key (key for encrypting/decrypting) are converted into matrices in the process. The inverse of the encryption matrix is used to decrypt.

In summary, if we have a 2 x 2 encryption matrix (key) then the message (converted to a 2 x n or n x 2 matrix) will be devided into n 2 x 1 (or 1 x 2) vectors each of which are multiplied with the encryption matrix to produce the cyphers (these are vectors still). The cypher text is produced from the cyphers (vectors) by convertion of the components (remember these are numbers) to corresponding unicode characters.

## Components
1. <b>matrixops.py</b> - Defines the martix operations used in encryption and decryption process.
2. <b>hillcipher.py</b> - Defines the encryption and decryption process making use of matrixops library.
3. <b>hillserver.py / hillclient.py </b> - A client-server arch. that makes use of the hillcypher library to establish encrypted (symmetric) communication 
between clients, with the server acting as a "switch" (just forwards communication between clients)

## Observed limitations of this implementation:
- Encryption limited to ASCII characters
- Encryption key must not be numeric

## Fixes/Improvements to be made:
- Remove trailing characters after decryption (involves finding a way to include 
trailing character information in encryption)
- Establish an authorization process, whereby when starting up the server is configured to allow only specific clients to connect (whitelisting) 
and each client needs to communicate their id (mayhap a hash of their user name) to connect.

## Extras:
- Generate a unique encryption key for each client using a base key known to all, by salting the base key for each client (using their info). 
The aim is to have communication between each client and the server use a unique key; clients need only know their keys, whereas the server will 
know all keys.




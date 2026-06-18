# X3DH
This repository contains a Python implementation of the Extended Triple Diffie-Hellman (X3DH) key agreement protocol. It is a cryptographic handshake used by messaging apps like Signal and WhatsApp to establish a secure, shared secret key between two parties (Alice and Bob) asynchronously meaning they don't both need to be online at the same time.

📖 What Does This Code Do?
This script simulates a complete X3DH conversation. It demonstrates how Bob generates his "prekeys" and leaves them on a server, how Alice fetches those keys to encrypt an initial message, and how Bob uses his private keys to decrypt that message when he finally comes online.

🛠 Dependencies and Libraries
This script uses Python's built-in libraries alongside one external cryptographic library.

External Dependency:

cryptography: The core library used for all cryptographic operations (curve math, hashing, key derivation, and encryption).

Built-in Python Libraries:

os: Used to generate secure random bytes (for the encryption nonce).

binascii: Used to convert raw bytes into readable hexadecimal strings for the console output.

🚀 Installation & Setup
Ensure you have Python installed (Python 3.7+ is recommended).

Install the required external library using pip:

Bash
pip install cryptography
Run the script:

Bash
python x3dh_implementation.py
(Note: Replace x3dh_implementation.py with whatever you named your Python file).

🧠 Easy Step-by-Step Explanation
The protocol runs in three main phases. Here is exactly what is happening in the code:

Phase 1: Bob Prepares for Messages (Publishing Prekeys)
Before Alice can even say hello, Bob needs to set up a mailbox with specific locks.

Identity Key (IKB): Bob generates a long-term identity key. This proves he is Bob.

Signed Prekey (SPKB): He generates a medium-term key and signs it with his Identity Key. This proves the key actually belongs to him.

One-Time Prekeys (OPKB): He generates a batch of single-use keys.

Publishing: He "uploads" these public keys to a central server (simulated in the code).

Phase 2: Alice Initiates the Chat
Alice wants to send Bob a secure message, but Bob is currently offline.

Fetching Keys: Alice contacts the server and downloads Bob's public keys.

Verification: Alice verifies the signature on Bob's Signed Prekey to ensure she isn't being tricked by an attacker.

Ephemeral Key (EKA): Alice generates a temporary "throwaway" key pair just for this interaction.

The Math (DH1 to DH4): Alice mixes her private keys with Bob's public keys using an algorithm called Elliptic Curve Diffie-Hellman. She does this 4 times to create an incredibly strong mix of cryptographic material.

Key Derivation (KDF): Alice uses a Key Derivation Function (HKDF) to smash those 4 math outputs into a single, secure 32-byte Shared Key (SK).

Encryption: Alice uses this Shared Key to encrypt her message ("Hello Bob!...") using AES-GCM, a standard encryption algorithm. She then "sends" this ciphertext to Bob.

Phase 3: Bob Receives and Decrypts
Bob finally comes online and receives Alice's encrypted message, along with her public Identity Key and her throwaway Ephemeral Key.

The Reverse Math: Because Bob holds the private halves of the public keys Alice used, he can perform the exact same Diffie-Hellman math on his end.

Recreating the Shared Key: Bob runs the math through the same KDF and successfully recreates the exact same Shared Key (SK) that Alice generated.

Decryption: Bob uses the Shared Key to decrypt the ciphertext and reads the message.

Forward Secrecy: To ensure ultimate security, Bob deletes the single-use One-Time Prekey (OPKB). Even if an attacker steals Bob's phone tomorrow, they cannot decrypt this message because the specific one-time key used for it has been destroyed.

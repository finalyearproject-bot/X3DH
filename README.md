# X3DH Protocol Simulation in Python

This repository contains a Python implementation of the **Extended Triple Diffie-Hellman (X3DH)** key agreement protocol. 

X3DH is the cryptographic protocol used by modern secure messaging apps (like Signal and WhatsApp) to establish a shared secret key between two parties, even if they are not online at the same time (asynchronous communication).

---

## 🛠 Dependencies & Libraries

This script relies on a mix of Python standard libraries and one powerful third-party cryptography package.

**Standard Libraries (Built-in):**
* `os`: Used for generating cryptographically secure random numbers (the nonce).
* `binascii`: Used to format the raw byte outputs into readable hexadecimal strings for the console.

**Third-Party Libraries:**
* `cryptography`: The core library used for all cryptographic primitives. 
    * *Algorithms used:* `x25519` (Key Exchange), `ed25519` (Signatures), `HKDF` (Key Derivation), `AESGCM` (Authenticated Encryption).

### Installation

To install the required third-party dependencies, simply run:


pip install -r requirements.txt

🚀 How to Run the Code
Simply execute the Python script from your terminal:

Bash
python x3dh_simulation.py
(Note: Replace x3dh_simulation.py with whatever you named your Python file).

📖 How It Works: The Easy Steps
The code simulates an interaction between two users: Alice and Bob. The execution is broken down into three main phases:

Phase 1: Key Generation & Publishing (Bob's Setup)
Before Alice can send Bob a message, Bob needs to tell the world how to encrypt messages for him.

Identity Keys: Both Alice and Bob generate long-term Identity Keys (IKA and IKB).

Prekeys: Bob generates a Signed Prekey (SPKB) and a One-Time Prekey (OPKB).

Publish: Bob signs his Prekey to prove it belongs to him and "publishes" all these keys to a central server.

Phase 2: Fetch & Initiate (Alice's Action)
Alice wants to send Bob a secure "Hello!" but Bob is offline.

Fetch: Alice downloads Bob's "Prekey Bundle" from the server.

Verify: She checks Bob's signature to ensure the keys are legit.

Ephemeral Key: Alice generates a temporary (ephemeral) key pair (EKA) just for this session.

The Math (DH1 to DH4): Alice mixes her keys with Bob's keys using Elliptic Curve Diffie-Hellman (ECDH) math. This generates four shared secrets.

The Master Key (SK): Alice mashes those four secrets together using a Key Derivation Function (HKDF) to create a single, super-secure Session Key (SK).

Encrypt & Send: Alice uses the SK to encrypt her payload ("Hello Bob!") using AES-GCM and sends it off. She then immediately deletes her temporary keys.

Phase 3: Receive & Decrypt (Bob's Action)
Bob comes online and receives Alice's encrypted message.

The Math (Repeated): Using his own private keys and the public keys Alice sent along with the message, Bob repeats the exact same DH math.

The Master Key (SK): Because math is awesome, Bob arrives at the exact same Session Key (SK) that Alice generated.

Decrypt: Bob uses the SK to decrypt the ciphertext and read the message.

Cleanup: Bob deletes the One-Time Prekey (OPKB) he used to ensure "Forward Secrecy" (meaning even if his keys are stolen in the future, this specific message can never be decrypted again).

🔒 Security Concepts Demonstrated
Mutual Authentication: Both parties know who they are talking to.

Forward Secrecy: Past messages cannot be decrypted if long-term keys are compromised in the future.

Cryptographic Deniability: Either party can forge a transcript after the fact, meaning the messages cannot be mathematically proven to third parties.

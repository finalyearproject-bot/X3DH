# 🔐 X3DH Protocol Implementation in Python

A simple educational implementation of the **X3DH (Extended Triple Diffie-Hellman)** key agreement protocol using **Python** and the **cryptography** library.

This project demonstrates how two parties (**Alice** and **Bob**) can securely establish a shared secret key and exchange an encrypted message, even when they are not online at the same time.

---

# 📖 What is X3DH?

**X3DH (Extended Triple Diffie-Hellman)** is a key agreement protocol used in modern secure messaging applications such as **Signal**.

It allows:

✅ End-to-End Encryption
✅ Asynchronous Communication
✅ Forward Secrecy
✅ Authentication of Parties
✅ Secure Session Key Establishment

---

# 🎯 Objective

The goal of this project is to:

1. Generate long-term identity keys.
2. Generate signed prekeys and one-time prekeys.
3. Verify Bob's signed prekey.
4. Perform four Diffie-Hellman calculations.
5. Derive a shared secret using HKDF.
6. Encrypt a message using AES-GCM.
7. Allow Bob to derive the same key and decrypt the message.

---

# 🛠 Technologies Used

| Technology           | Purpose                       |
| -------------------- | ----------------------------- |
| Python 3             | Programming Language          |
| Cryptography Library | Cryptographic Operations      |
| X25519               | Diffie-Hellman Key Exchange   |
| Ed25519              | Digital Signatures            |
| HKDF (SHA-256)       | Key Derivation                |
| AES-GCM              | Authenticated Encryption      |
| OS Module            | Random Nonce Generation       |
| Binascii             | Hexadecimal Output Formatting |

---

# 📦 Libraries Used

```python
import os
import binascii

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.asymmetric import ed25519

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
```

---

# 📚 Purpose of Each Library

## os

Used for generating cryptographically secure random bytes.

Example:

```python
nonce = os.urandom(12)
```

---

## binascii

Used to convert binary data into readable hexadecimal format.

Example:

```python
binascii.hexlify(data)
```

---

## x25519

Used for:

* Identity Keys
* Signed Prekeys
* One-Time Prekeys
* Ephemeral Keys
* Diffie-Hellman Operations

Example:

```python
private_key = x25519.X25519PrivateKey.generate()
```

---

## ed25519

Used for digital signatures.

Bob signs his Signed Prekey (SPKB).

Example:

```python
signature = private_key.sign(message)
```

---

## serialization

Used for converting keys into byte format.

Example:

```python
public_key.public_bytes(...)
```

---

## HKDF

Used to derive the final shared secret key.

Hash Function:

```text
SHA-256
```

Output:

```text
32-byte session key
```

---

## AESGCM

Used for authenticated encryption.

Provides:

* Confidentiality
* Integrity
* Authentication

Example:

```python
ciphertext = aes.encrypt(...)
```

---

# 🔑 Keys Used in X3DH

## Alice

### IKA (Identity Key)

Long-term key pair.

```text
IKA_private
IKA_public
```

---

### EKA (Ephemeral Key)

Temporary key pair used only for this session.

```text
EKA_private
EKA_public
```

---

## Bob

### IKB (Identity Key)

Long-term key pair.

```text
IKB_private
IKB_public
```

---

### SPKB (Signed Prekey)

Medium-term key pair signed by Bob.

```text
SPKB_private
SPKB_public
```

---

### OPKB (One-Time Prekey)

Used only once and then deleted.

```text
OPKB_private
OPKB_public
```

---

# 🏗 Protocol Workflow

## Phase 1: Bob Publishes Keys

Bob generates:

* Identity Key (IKB)
* Signed Prekey (SPKB)
* One-Time Prekey (OPKB)

Then Bob signs:

```text
Sig(IKB, Encode(SPKB))
```

and uploads the following to the server:

```text
IKB
SPKB
Signature
OPKB
```

---

## Phase 2: Alice Initiates

Alice downloads Bob's prekey bundle from the server.

Bundle contains:

```text
IKB
SPKB
Signature
OPKB
```

---

### Signature Verification

Alice verifies:

```text
Sig(IKB, Encode(SPKB))
```

If verification fails:

```text
Abort Protocol
```

---

### Generate Ephemeral Key

Alice generates:

```text
EKA
```

---

### Compute DH Values

Alice calculates:

#### DH1

```text
DH(IKA, SPKB)
```

#### DH2

```text
DH(EKA, IKB)
```

#### DH3

```text
DH(EKA, SPKB)
```

#### DH4

```text
DH(EKA, OPKB)
```

---

### Create Key Material

```text
KM = DH1 || DH2 || DH3 || DH4
```

Where:

```text
||
```

means concatenation.

---

### Derive Shared Secret

```text
SK = KDF(KM)
```

using:

```text
HKDF-SHA256
```

---

### Encrypt Message

Alice encrypts:

```text
Hello Bob!
```

using:

```text
AES-GCM
```

and sends:

```text
IKA
EKA
Ciphertext
Nonce
```

to Bob.

---

## Phase 3: Bob Receives Message

Bob receives:

```text
IKA
EKA
Ciphertext
Nonce
```

---

### Recompute DH Values

Bob calculates:

```text
DH1 = DH(SPKB, IKA)
DH2 = DH(IKB, EKA)
DH3 = DH(SPKB, EKA)
DH4 = DH(OPKB, EKA)
```

---

### Derive Shared Secret

Bob computes:

```text
SK = KDF(DH1 || DH2 || DH3 || DH4)
```

---

### Decrypt Ciphertext

Using:

```text
AES-GCM
```

Bob decrypts the message.

If successful:

```text
Handshake Complete
```

---

# 🔒 Security Features Demonstrated

## Authentication

Bob signs the Signed Prekey.

```text
Ed25519 Signature
```

---

## Confidentiality

Messages are encrypted using:

```text
AES-256-GCM
```

---

## Forward Secrecy

Ephemeral and One-Time keys are deleted after use.

```python
del OPKB_private
```

---

## Shared Secret Agreement

Both parties independently derive:

```text
SK
```

without transmitting it.

---

# 🔄 Key Derivation Function

The implementation uses:

```text
HKDF-SHA256
```

Parameters:

| Parameter     | Value            |
| ------------- | ---------------- |
| Hash          | SHA-256          |
| Output Length | 32 Bytes         |
| Salt          | 32 Zero Bytes    |
| Info          | "MyProtocol"     |
| Prefix F      | 32 Bytes of 0xFF |

Formula:

```text
SK = HKDF(F || KM)
```

---

# 🔐 Encryption Details

Algorithm:

```text
AES-GCM
```

Key Length:

```text
256 bits
```

Nonce Length:

```text
12 bytes
```

Associated Data:

```text
AD = Encode(IKA) || Encode(IKB)
```

This protects the identity keys from tampering.

---

# 📂 Project Structure

```text
project/
│
├── x3dh.py
└── README.md
```

---

# 📜 Protocol Reference

This implementation follows the concepts described in:

### X3DH Specification

Developed by:

```text
Open Whisper Systems (Signal)
```

Official Specification:

https://signal.org/docs/specifications/x3dh/

---

# ⚠ Educational Disclaimer

This project is intended for:

* Learning
* Research
* Academic Demonstration
* Understanding X3DH Workflow

It is **not intended for production use** without additional security reviews, protocol hardening, error handling, secure key storage, and full XEdDSA support.

---

# ✅ Output Example

```text
PHASE 1: BOB PUBLISHES PREKEYS

PHASE 2: ALICE FETCHES BUNDLE & INITIATES

Verification SUCCESS

Alice calculates DH1, DH2, DH3, DH4

Alice derives SK

Ciphertext Generated

PHASE 3: BOB RECEIVES AND DECRYPTS

Bob derives same SK

SUCCESS: Ciphertext decrypts successfully

HANDSHAKE COMPLETE
```

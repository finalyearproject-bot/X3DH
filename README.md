# 🔐 X3DH Protocol Implementation in Python

A simple educational implementation of the **X3DH (Extended Triple Diffie-Hellman)** protocol using **Python** and the **Cryptography** library.

This project demonstrates how Alice and Bob establish a shared secret key and securely exchange encrypted messages using:

* X25519 Key Exchange
* Ed25519 Digital Signatures
* HKDF-SHA256 Key Derivation
* AES-256-GCM Encryption

---

## 📁 Project Structure

```text
project/
│
├── x3dh.py
└── README.md
```
Rename your Python file to x3dh.py (recommended).
---

## 📦 Installation

Install the required dependency:

```bash
pip install cryptography
```

Verify installation:

```bash
pip show cryptography
```

---

## ▶️ Run

```bash
python x3dh.py
```

No code modifications are required.

---

## 🔑 Keys Used

### Alice

| Key | Purpose       |
| --- | ------------- |
| IKA | Identity Key  |
| EKA | Ephemeral Key |

### Bob

| Key  | Purpose         |
| ---- | --------------- |
| IKB  | Identity Key    |
| SPKB | Signed Prekey   |
| OPKB | One-Time Prekey |

---

## 🔄 Protocol Flow

### 1. Bob Publishes

Bob generates:

```text
IKB
SPKB
OPKB
```

Bob signs the Signed Prekey using Ed25519 and publishes:

```text
IKB
SPKB
Signature
OPKB
```

---

### 2. Alice Initiates

Alice:

1. Downloads Bob's prekey bundle
2. Verifies the signature
3. Generates EKA
4. Computes:

```text
DH1 = DH(IKA, SPKB)
DH2 = DH(EKA, IKB)
DH3 = DH(EKA, SPKB)
DH4 = DH(EKA, OPKB)
```

5. Creates:

```text
KM = DH1 || DH2 || DH3 || DH4
```

6. Derives:

```text
SK = HKDF(KM)
```

7. Encrypts the message using AES-GCM

---

### 3. Bob Receives

Bob:

1. Recomputes DH1–DH4
2. Derives the same shared secret
3. Decrypts the ciphertext

Result:

```text
HANDSHAKE COMPLETE
```

---

## 🛠 Libraries Used

| Library       | Purpose                  |
| ------------- | ------------------------ |
| os            | Random nonce generation  |
| binascii      | Hex formatting           |
| x25519        | Diffie-Hellman exchange  |
| ed25519       | Digital signatures       |
| serialization | Key encoding             |
| HKDF          | Key derivation           |
| AESGCM        | Authenticated encryption |

---

## 🔒 Security Features

* Authentication via Ed25519 signatures
* X25519 secure key exchange
* HKDF-SHA256 session key derivation
* AES-256-GCM authenticated encryption
* Forward secrecy using ephemeral and one-time keys

---

## 📚 Reference

X3DH Specification:

https://signal.org/docs/specifications/x3dh/

---

## ⚠ Disclaimer

This implementation is intended for:

* Learning
* Research
* Academic Demonstration

It is **not production-ready** and should not be used in real-world secure messaging systems without additional security reviews and protocol hardening.

---

## ✅ Sample Output

```text
PHASE 1: BOB PUBLISHES PREKEYS

PHASE 2: ALICE FETCHES BUNDLE

Verification SUCCESS

Alice derives shared secret

Ciphertext Generated

PHASE 3: BOB RECEIVES MESSAGE

Bob derives same shared secret

SUCCESS: Ciphertext decrypts successfully

HANDSHAKE COMPLETE
```

---

## 👨‍💻 Author

Educational implementation of the X3DH Protocol using Python and the Cryptography library.

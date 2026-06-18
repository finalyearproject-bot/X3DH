# 🔐 X3DH Protocol Implementation in Python

A simple implementation of the **X3DH (Extended Triple Diffie-Hellman)** protocol using **Python** and the **Cryptography** library.

This project demonstrates how **Alice** and **Bob** establish a shared secret key and securely exchange an encrypted message using:

* X25519 Key Exchange
* Ed25519 Digital Signatures
* HKDF-SHA256 Key Derivation
* AES-GCM Encryption

---

## 📁 File Structure

```text
project/
│
├── x3dh.py
└── README.md
```

> Rename your Python file to **x3dh.py** (recommended).

---

## 📦 Dependencies

Install the required library:

```bash
pip install cryptography
```

Check installation:

```bash
pip show cryptography
```

---

## ▶️ Run the Project

```bash
python x3dh.py
```

---

## ⚠️ Important Note

This implementation follows the X3DH workflow for educational purposes.

✅ No code changes are required to run the project.

If the `cryptography` package is installed correctly, the code should execute successfully and produce:

* Key Generation
* Signature Verification
* DH Calculations
* Shared Secret Derivation
* AES-GCM Encryption
* Successful Decryption

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

## 🔄 X3DH Workflow

### Phase 1: Bob Publishes Keys

Bob generates:

```text
IKB
SPKB
OPKB
```

Bob signs:

```text
Encode(SPKB)
```

and uploads the public keys to the server.

---

### Phase 2: Alice Initiates

Alice:

1. Downloads Bob's Prekey Bundle
2. Verifies Bob's Signature
3. Generates Ephemeral Key (EKA)
4. Calculates:

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

### Phase 3: Bob Receives Message

Bob:

1. Receives Alice's keys and ciphertext
2. Recomputes DH1–DH4
3. Derives the same shared secret
4. Decrypts the ciphertext

Result:

```text
HANDSHAKE COMPLETE
```

---

## 🛠 Libraries Used

| Library       | Purpose                     |
| ------------- | --------------------------- |
| os            | Random nonce generation     |
| binascii      | Hex output formatting       |
| x25519        | Diffie-Hellman key exchange |
| ed25519       | Digital signatures          |
| serialization | Key encoding                |
| HKDF          | Shared key derivation       |
| AESGCM        | Authenticated encryption    |

---

## 🔒 Security Features

* Authentication using Ed25519 signatures
* Secure key exchange using X25519
* HKDF-SHA256 session key derivation
* AES-GCM authenticated encryption
* One-Time Prekey deletion for forward secrecy

---

## 📚 Protocol Reference

X3DH Specification:

https://signal.org/docs/specifications/x3dh/

---

## 📝 Sample Output

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

### Educational Purpose

This project was created to understand and demonstrate the working of the **X3DH Protocol** and secure asynchronous key exchange in modern messaging systems such as Signal.

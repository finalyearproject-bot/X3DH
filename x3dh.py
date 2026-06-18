import os
import binascii
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# 2. Preliminaries


# 2.1. X3DH parameters
# curve: X25519 or X448 | hash: SHA-256 | info: "MyProtocol"
# For example, an application could choose curve as X25519... and info as "MyProtocol".


INFO = b"MyProtocol"

def Encode(pk):
    """
    An application must additionally define an encoding function Encode(PK) to 
    encode an X25519 or X448 public key PK into a byte sequence.
    """
    return pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def DH(private_key, public_key):
    """
    DH(PK1, PK2) represents a byte sequence which is the shared secret 
    output from an Elliptic Curve Diffie-Hellman function...
    """
    return private_key.exchange(public_key)

def KDF(key_material):
    """
    KDF(KM) represents 32 bytes of output from the HKDF algorithm [3]
    HKDF input key material = F || KM ... F is a byte sequence containing 32 0xFF bytes if curve is X25519
    HKDF salt = A zero-filled byte sequence with length equal to the hash output length.
    HKDF info = The info parameter from Section 2.1.
    """
    F = b'\xFF' * 32
    hkdf_input = F + key_material
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\x00' * 32,
        info=INFO
    )
    return hkdf.derive(hkdf_input)

# Helper function to print keys nicely in the console

def print_key(name, priv_key=None, pub_key=None):
    print(f"\n--- {name} ---")
    if priv_key:
        priv_bytes = priv_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        print(f" Private: {binascii.hexlify(priv_bytes).decode()}")
    if pub_key:
        print(f" Public:  {binascii.hexlify(Encode(pub_key)).decode()}")



# MAIN EXECUTION FLOW


if __name__ == "__main__":
    
    print("\n X3DH PROTOCOL EXECUTION WITH PDF SOURCE MAPPING \n")
    
    print(f"Parameters loaded -> Curve: X25519, Hash: SHA-256, Info: {INFO.decode()}")


    # 2.4. Keys


    print("\nGENERATING LONG-TERM & PREKEYS\n")
    
    # Each party has a long-term identity public key (IKA for Alice, IKB for Bob).
    print("-> Generating IKA (Alice) and IKB (Bob)...")
    IKA_private = x25519.X25519PrivateKey.generate()
    IKA_public = IKA_private.public_key()
    
    IKB_private = x25519.X25519PrivateKey.generate()
    IKB_public = IKB_private.public_key()


    # Sig(PK, M) represents a byte sequence that is an XEdDSA signature...
    # (Note: Using standard Ed25519 for Bob's signing capability to mimic XEdDSA)


    IKB_sign_private = ed25519.Ed25519PrivateKey.generate()
    IKB_sign_public = IKB_sign_private.public_key()

    print_key("Alice Identity Key (IKA)", IKA_private, IKA_public)
    print_key("Bob Identity Key (IKB)", IKB_private, IKB_public)

    
    # 3.2. Publishing keys
    

    print("\nPHASE 1: BOB PUBLISHES PREKEYS TO SERVER\n")
    
    # Bob's signed prekey SPKB

    SPKB_private = x25519.X25519PrivateKey.generate()
    SPKB_public = SPKB_private.public_key()
    print_key("Bob Signed Prekey (SPKB)", SPKB_private, SPKB_public)

    # Bob's prekey signature Sig(IKB, Encode(SPKB))

    spkb_encoded = Encode(SPKB_public)
    signature = IKB_sign_private.sign(spkb_encoded)
    print(f"\n -> Bob generates prekey signature Sig(IKB, Encode(SPKB)):\n    {binascii.hexlify(signature).decode()}")

    # A set of Bob's one-time prekeys (OPKB...)

    OPKB_private = x25519.X25519PrivateKey.generate()
    OPKB_public = OPKB_private.public_key()
    print_key("Bob One-Time Prekey (OPKB)", OPKB_private, OPKB_public)

    print("\n -> Bob publishes a set of elliptic curve public keys to the server.")

    
    # 3.3. Sending the initial message
   

    print("\nPHASE 2: ALICE FETCHES BUNDLE & INITIATES\n")
    print(" -> Alice contacts the server and fetches a 'prekey bundle'...")
    
    # Server provides Bob's bundle to Alice

    bundle_IKB = IKB_public
    bundle_SPKB = SPKB_public
    bundle_signature = signature
    bundle_OPKB = OPKB_public 

    # Alice verifies the prekey signature and aborts the protocol if verification fails.

    try:
        IKB_sign_public.verify(bundle_signature, Encode(bundle_SPKB))
        print(" -> Verification SUCCESS: Alice verifies the prekey signature.")
    except Exception:
        print(" -> Verification FAILED: Alice aborts the protocol.")
        exit(1)

    # Alice then generates an ephemeral key pair with public key EKA.

    print(" -> Alice generates an ephemeral key pair with public key EKA.")
    EKA_private = x25519.X25519PrivateKey.generate()
    EKA_public = EKA_private.public_key()

    # DH Calculations

    print("\n -> Alice calculates DH1, DH2, DH3, and DH4:")
    DH1_alice = DH(IKA_private, bundle_SPKB)   # DH1=DH(IKA,SPKB)
    DH2_alice = DH(EKA_private, bundle_IKB)    # DH2=DH(EKA,IKB)
    DH3_alice = DH(EKA_private, bundle_SPKB)   # DH3=DH(EKA,SPKB)
    DH4_alice = DH(EKA_private, bundle_OPKB)   # DH4=DH(EKA,OPKB)

    print(f"    DH1: {binascii.hexlify(DH1_alice).decode()}")
    print(f"    DH2: {binascii.hexlify(DH2_alice).decode()}")
    print(f"    DH3: {binascii.hexlify(DH3_alice).decode()}")
    print(f"    DH4: {binascii.hexlify(DH4_alice).decode()}")

    # SK = KDF(DH1 || DH2 || DH3 || DH4)

    KM_alice = DH1_alice + DH2_alice + DH3_alice + DH4_alice
    SK_alice = KDF(KM_alice)
    print(f"\n -> Alice calculates SK = KDF(DH1 || DH2 || DH3 || DH4):\n    {binascii.hexlify(SK_alice).decode()}")

    # After calculating SK, Alice deletes her ephemeral private key and the DH outputs.

    print(" -> Alice deletes her ephemeral private key and the DH outputs.")
    del EKA_private, DH1_alice, DH2_alice, DH3_alice, DH4_alice

    # AD = Encode(IKA) || Encode(IKB)

    print("\n -> Alice calculates 'associated data' byte sequence AD = Encode(IKA) || Encode(IKB).")
    AD = Encode(IKA_public) + Encode(bundle_IKB)
    
    # An initial ciphertext encrypted with some AEAD encryption scheme...

    aesgcm_alice = AESGCM(SK_alice)
    nonce = os.urandom(12)
    plaintext = b"Hello Bob! This is an encrypted asynchronous payload via X3DH."
    ciphertext = aesgcm_alice.encrypt(nonce, plaintext, AD)

    print(f" -> Alice encrypts the initial ciphertext using an AEAD scheme.")
    print(f"    Ciphertext: {binascii.hexlify(ciphertext).decode()}")


    
    # 3.4. Receiving the initial message
    

    print("\nPHASE 3: BOB RECEIVES AND DECRYPTS\n")
   
    # Upon receiving Alice's initial message, Bob retrieves Alice's identity key and ephemeral key...

    print(" -> Bob receives message and retrieves Alice's IKA and EKA.")
    received_IKA = IKA_public
    received_EKA = EKA_public

    # Using these keys, Bob repeats the DH and KDF calculations...

    print("\n -> Bob repeats the DH and KDF calculations to derive SK:")
    DH1_bob = DH(SPKB_private, received_IKA)
    DH2_bob = DH(IKB_private, received_EKA)
    DH3_bob = DH(SPKB_private, received_EKA)
    DH4_bob = DH(OPKB_private, received_EKA)
    
    KM_bob = DH1_bob + DH2_bob + DH3_bob + DH4_bob
    SK_bob = KDF(KM_bob)
    print(f"    Bob's derived SK:\n    {binascii.hexlify(SK_bob).decode()}")

    # Bob then constructs the AD byte sequence using IKA and IKB...

    print(" -> Bob constructs the AD byte sequence using IKA and IKB.")
    AD_bob = Encode(received_IKA) + Encode(IKB_public)
    
    # Finally, Bob attempts to decrypt the initial ciphertext using SK and AD.

    try:
        aesgcm_bob = AESGCM(SK_bob)
        decrypted = aesgcm_bob.decrypt(nonce, ciphertext, AD_bob)
        print("\n -> SUCCESS: The initial ciphertext decrypts successfully. Protocol is complete for Bob.")
        print(f" -> DECRYPTED MESSAGE: '{decrypted.decode()}'")
    except Exception:

        # If the initial ciphertext fails to decrypt, then Bob aborts the protocol and deletes SK.

        print("\n -> FAILURE: Ciphertext fails to decrypt. Bob aborts and deletes SK.")
        del SK_bob
        exit(1)

    # Bob deletes any one-time prekey private key that was used, for forward secrecy.

    del OPKB_private
    print(" -> Bob deletes the one-time prekey (OPKB) private key for forward secrecy.")

    print("\n HANDSHAKE COMPLETE \n")
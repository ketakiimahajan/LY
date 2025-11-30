from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image
import numpy as np

def extract_data_lsb(stego_img_path):
    """Extract hidden data from stego image using LSB technique"""
    print("\n[LSB EXTRACTION START]")
    
    # Load stego image
    img = Image.open(stego_img_path)
    img_array = np.array(img)
    print(f"✓ Stego image loaded: {img_array.shape}")
    
    # Flatten image
    flat = img_array.flatten()
    
    # Extract length of hidden data (first 32 bits)
    data_length_binary = ''.join(str(flat[i] & 1) for i in range(32))
    data_len = int(data_length_binary, 2)
    print(f"✓ Hidden data length detected: {data_len} bits")
    
    # Extract actual data
    print("✓ Extracting data from LSBs...")
    data_binary = ''.join(str(flat[32 + i] & 1) for i in range(data_len))
    
    # Convert binary to bytes
    extracted_bytes = bytearray()
    for i in range(0, len(data_binary), 8):
        byte = data_binary[i:i+8]
        extracted_bytes.append(int(byte, 2))
    
    print(f"✓ Extracted {len(extracted_bytes)} bytes from image")
    return bytes(extracted_bytes)

def decrypt_message(encrypted_data, key):
    """Decrypt message using AES-256"""
    print("\n[AES DECRYPTION START]")
    
    # Extract IV and ciphertext
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    print(f"✓ Message decrypted successfully")
    print(f"  Decrypted length: {len(plaintext)} bytes")
    return plaintext.decode()

def main():
    print("="*60)
    print("IMAGE STEGANOGRAPHY WITH CRYPTOGRAPHY - DECRYPTION")
    print("="*60)
    
    # Get inputs
    stego_image = input("\nEnter stego image path (e.g., stego_image.png): ")
    key_file = input("Enter key file path (e.g., secret_key.bin): ")
    
    # Load key
    print("\n[KEY LOADING]")
    with open(key_file, "rb") as f:
        aes_key = f.read()
    print(f"✓ AES-256 key loaded (32 bytes)")
    
    # Step 1: Extract encrypted data from image
    encrypted_data = extract_data_lsb(stego_image)
    
    # Step 2: Decrypt the data
    secret_message = decrypt_message(encrypted_data, aes_key)
    
    print("\n" + "="*60)
    print("✅ EXTRACTION & DECRYPTION COMPLETE!")
    print("="*60)
    print(f"🔓 Secret Message:")
    print(f"\n   \"{secret_message}\"\n")
    print("="*60)

if __name__ == "__main__":
    main()
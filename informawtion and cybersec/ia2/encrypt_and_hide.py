from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np
import os

def encrypt_message(plaintext, key):
    """Encrypt message using AES-256"""
    print("\n[AES ENCRYPTION START]")
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    print(f"✓ Message encrypted successfully")
    print(f"  Original length: {len(plaintext)} chars")
    print(f"  Encrypted length: {len(ciphertext)} bytes")
    return iv + ciphertext  # Prepend IV for decryption

def embed_data_lsb(cover_img_path, secret_data, output_path):
    """Hide encrypted data in image using LSB technique"""
    print("\n[LSB STEGANOGRAPHY START]")
    
    # Load cover image
    img = Image.open(cover_img_path)
    img_array = np.array(img)
    print(f"✓ Cover image loaded: {img_array.shape}")
    
    # Convert secret data to binary
    data_binary = ''.join(format(byte, '08b') for byte in secret_data)
    data_len = len(data_binary)
    print(f"✓ Secret data converted to binary: {data_len} bits")
    
    # Check capacity
    max_capacity = img_array.size
    if data_len > max_capacity:
        raise ValueError(f"Image too small! Need {data_len} bits, have {max_capacity}")
    
    print(f"  Image capacity: {max_capacity} bits")
    print(f"  Data size: {data_len} bits")
    print(f"  Capacity used: {(data_len/max_capacity)*100:.2f}%")
    
    # Flatten image for easier bit manipulation
    flat = img_array.flatten()
    
    # Embed length of data (first 32 bits)
    data_length_binary = format(data_len, '032b')
    for i in range(32):
        flat[i] = (flat[i] & ~1) | int(data_length_binary[i])
    
    # Embed actual data
    print("✓ Embedding data into LSBs...")
    for i in range(data_len):
        flat[32 + i] = (flat[32 + i] & ~1) | int(data_binary[i])
    
    # Reshape back to original shape
    stego_array = flat.reshape(img_array.shape)
    stego_img = Image.fromarray(stego_array.astype('uint8'))
    
    # Save stego image
    stego_img.save(output_path)
    print(f"✓ Stego image saved: {output_path}")
    
    return output_path

def main():
    print("="*60)
    print("IMAGE STEGANOGRAPHY WITH CRYPTOGRAPHY - ENCRYPTION")
    print("="*60)
    
    # Get inputs
    secret_message = input("\nEnter secret message to hide: ")
    cover_image = input("Enter cover image path (e.g., cover.png): ")
    
    # Generate AES key
    print("\n[KEY GENERATION]")
    aes_key = get_random_bytes(32)  # 256-bit key
    print(f"✓ AES-256 key generated (32 bytes)")
    
    # Save key to file
    with open("secret_key.bin", "wb") as f:
        f.write(aes_key)
    print("✓ Key saved to: secret_key.bin")
    print("  ⚠️  KEEP THIS FILE SAFE! You need it for decryption")
    
    # Step 1: Encrypt message
    encrypted_data = encrypt_message(secret_message, aes_key)
    
    # Step 2: Hide encrypted data in image
    stego_path = "stego_image.png"
    embed_data_lsb(cover_image, encrypted_data, stego_path)
    
    print("\n" + "="*60)
    print("✅ ENCRYPTION & HIDING COMPLETE!")
    print("="*60)
    print(f"📁 Files created:")
    print(f"   - {stego_path} (contains hidden message)")
    print(f"   - secret_key.bin (needed for decryption)")
    print("\n💡 Share the stego image publicly - message is invisible!")
    print("="*60)

if __name__ == "__main__":
    main()
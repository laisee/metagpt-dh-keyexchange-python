from diffie_hellman import DiffieHellman
from secure_storage import AzureKeyVault, AWSSecrets, KeeperSecurity

def main():
    # Initialize DiffieHellman
    dh = DiffieHellman()

    try:
        private_key, public_key = dh.generate_keys()
    except Exception as e:
        print(f"Error generating keys: {e}")
        return

    # Choose a secure storage service
    ss = AzureKeyVault('https://my-vault-url.vault.azure.net/')  # Replace with actual vault URL

    # Store the public key in the secure storage
    key_id = 'my-key-id'  # Replace with actual key ID
    try:
        ss.store_key(public_key, key_id)
    except Exception as e:
        print(f"Error storing key: {e}")
        return

    # Retrieve the public key from the secure storage
    try:
        public_key = ss.retrieve_key(key_id)
    except Exception as e:
        print(f"Error retrieving key: {e}")
        return

    # Compute the shared secret using the other party's public key
    other_public_key = 123456789  # Replace with the other party's public key
    try:
        shared_secret = dh.compute_shared_secret(other_public_key)
    except Exception as e:
        print(f"Error computing shared secret: {e}")
        return

    print(f'Shared secret: {shared_secret}')

if __name__ == '__main__':
    main()

from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from typing import Tuple

class DiffieHellman:
    """
    Class for implementing Diffie-Hellman key exchange protocol.
    """

    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self) -> Tuple[int, int]:
        """
        Generate a pair of private and public keys.
        """
        # Generate a DSA key pair
        key = DSA.generate(2048)

        # Extract the private and public keys
        self.private_key = key.x
        self.public_key = key.y

        return self.private_key, self.public_key

    def compute_shared_secret(self, other_public_key: int) -> int:
        """
        Compute the shared secret using the other party's public key.
        """
        # Compute the shared secret
        shared_secret = pow(other_public_key, self.private_key, key.p)  # Use DSA.p instead of DSA.q

        # Hash the shared secret to get a 256-bit key
        h = SHA256.new()
        h.update(shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, 'big'))
        shared_secret = int.from_bytes(h.digest(), 'big')

        return shared_secret

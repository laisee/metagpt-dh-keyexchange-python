## secure_storage.py
from abc import ABC, abstractmethod
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from keepercommander.record import Record
from keepercommander.params import KeeperParams
from keepercommander.api import communicate

class SecureStorage(ABC):
    """
    Abstract class for secure storage services.
    """

    @abstractmethod
    def store_key(self, key: int, key_id: str):
        """
        Store the key in the secure storage.
        """
        pass

    @abstractmethod
    def retrieve_key(self, key_id: str) -> int:
        """
        Retrieve the key from the secure storage.
        """
        pass


class AzureKeyVault(SecureStorage):
    """
    Class for Azure Key Vault service.
    """

    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        self.client = SecretClient(vault_url=self.vault_url, credential=DefaultAzureCredential())

    def store_key(self, key: int, key_id: str):
        """
        Store the key in the Azure Key Vault.
        """
        self.client.set_secret(key_id, str(key))

    def retrieve_key(self, key_id: str) -> int:
        """
        Retrieve the key from the Azure Key Vault.
        """
        secret = self.client.get_secret(key_id)
        return int(secret.value)


class AWSSecrets(SecureStorage):
    """
    Class for AWS Secrets Manager service.
    """

    def __init__(self, region_name: str):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def store_key(self, key: int, key_id: str):
        """
        Store the key in the AWS Secrets Manager.
        """
        self.client.create_secret(Name=key_id, SecretString=str(key))

    def retrieve_key(self, key_id: str) -> int:
        """
        Retrieve the key from the AWS Secrets Manager.
        """
        secret = self.client.get_secret_value(SecretId=key_id)
        return int(secret['SecretString'])


class KeeperSecurity(SecureStorage):
    """
    Class for Keeper Security service.
    """

    def __init__(self, email: str, password: str):
        self.params = KeeperParams()
        self.params.user = email
        self.params.password = password
        communicate(self.params, 'login')

    def store_key(self, key: int, key_id: str):
        """
        Store the key in the Keeper Security.
        """
        record = Record()
        record.record_uid = key_id
        record.set_field('key', str(key))
        communicate(self.params, 'add', record)

    def retrieve_key(self, key_id: str) -> int:
        """
        Retrieve the key from the Keeper Security.
        """
        record = communicate(self.params, 'get', key_id)
        return int(record.get_field('key'))

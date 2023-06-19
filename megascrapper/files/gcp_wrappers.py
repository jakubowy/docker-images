from google.cloud import storage, secretmanager
import yaml

def get_config(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('config.yaml')
    x = blob.download_as_text()
    return yaml.safe_load(x)
    
def get_secret(secret_path):
    secretmanager_client = secretmanager.SecretManagerServiceClient()
    name = f"{secret_path}"
    return secretmanager_client.access_secret_version(request={'name': name}).payload.data.decode("UTF-8")

def update_secret(secret_path, payload):
    secretmanager_client = secretmanager.SecretManagerServiceClient()
    name = f"{secret_path.rsplit('/',2)[0]}"
    secretmanager_client.add_secret_version(request={"parent": name, "payload": {"data": payload.encode("UTF-8")}})

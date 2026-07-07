import uuid
import os
import yaml
import hashlib
# endpoint = os.getenv('fusekiURL') or "http://34.246.140.123:3030/scubeOntology"
endpoint = os.getenv('fusekiURL') or "http://34.246.140.123:3030/"


def generate_id(name: str):
    encoded_name = name.upper().replace(" ", "").encode()
    hashed_name = hashlib.md5(encoded_name).hexdigest()
    return hashed_name


def generate_uuid():
    return uuid.uuid1().hex


queries = None

with open('sparql-queries.yaml', 'r') as stream:
    try:
        queries = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

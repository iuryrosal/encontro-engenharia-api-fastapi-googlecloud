from google.cloud import secretmanager
import google_crc32c
import os
import time
import requests
import json
import jwt
import urllib
from dotenv import load_dotenv


class SecretManager:
    def __init__(self) -> None:
        self.project_id = os.getenv("project_id", None)
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, secret_id, version_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})

        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response

        payload = response.payload.data.decode("UTF-8")
        return payload


def create_signed_jwt(credentials_json, run_service_url):
    iat = time.time()
    exp = iat + 3600
    payload = {
        'iss': credentials_json['client_email'],
        'sub': credentials_json['client_email'],
        'target_audience': run_service_url,
        'aud': 'https://www.googleapis.com/oauth2/v4/token',
        'iat': iat,
        'exp': exp
        }
    additional_headers = {
        'kid': credentials_json['private_key_id']
        }
    signed_jwt = jwt.encode(
        payload,
        credentials_json['private_key'], 
        headers=additional_headers,
        algorithm='RS256'
    )
    return signed_jwt


def exchange_jwt_for_token(signed_jwt):
    body = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': signed_jwt
    }
    token_request = requests.post(
        url='https://www.googleapis.com/oauth2/v4/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data=urllib.parse.urlencode(body)
    )
    return token_request.json()['id_token']


def main():
    if os.getenv("env", "dev") == "dev":
        load_dotenv()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test_api_apoena/credentials.json"

    sm = SecretManager()
    credentials_of_api = json.loads(sm.access_secret(secret_id=os.getenv("secret_id"),
                                                     version_id=1))
    jwt_token = create_signed_jwt(credentials_json=credentials_of_api,
                                  run_service_url=os.getenv("cloudrun_url"))
    token = exchange_jwt_for_token(jwt_token)

    return token

import os
import requests
from token_logic import generate_token


class ApiClient:
    def __init__(self) -> None:
        if os.environ["ENV"] == "dev":
            self.url_base = "http://0.0.0.0:8080"
        elif os.environ["ENV"] == "prd":
            self.url_base = os.environ["CLOUDRUN_URL"]

    def get_customers(self, sg_state: str = None):
        query_params = "?"
        if sg_state:
            query_params += f"{sg_state=}"

        url = f"{self.url_base}/customers/"
        if len(url) > 1:
            url += query_params

        if os.environ["ENV"] == "dev":
            response = requests.get(url)
        elif os.environ["ENV"] == "prd":
            response = requests.get(url,
                                    headers={
                                        "Authorization": f"Bearer {generate_token()}"
                                    })

        if response.status_code in range(200, 300):
            return response.json()
        else:
            raise response.raise_for_status()
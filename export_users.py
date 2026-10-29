"""Fetch users from the Okta Users API and print them."""
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # read .env into environment variables

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")


def main():
    url = f"{ORG_URL}/api/v1/users"
    headers = {
        "Authorization": f"SSWS {TOKEN}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=10)
    print("Status:", response.status_code)
    response.raise_for_status()

    users = response.json()
    # TODO: loop over users and print each one's status and login

    for user in users:
        print(f"Status :  {user["status"]}")
        print(f"Login :  {user["profile"]["login"]}")



if __name__ == "__main__":
    main()
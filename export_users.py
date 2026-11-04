"""Fetch users from the Okta Users API and print them.
Export all Okta users to users.csv, following pagination.
"""
import os

import requests
import csv   # top of file
from dotenv import load_dotenv

load_dotenv()  # read .env into environment variables

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")


def main():
    users = []
    url = f"{ORG_URL}/api/v1/users"
    params = {"limit": 2}
    headers = {
                    "Authorization": f"SSWS {TOKEN}",
                    "Accept": "application/json",
                }
    while url:
        
        response = requests.get(url, headers=headers, timeout=10,params= params)     # GET url with headers + params, timeout=10
        print("Status:", response.status_code)
        response.raise_for_status()     # raise_for_status()
        page = response.json()
        users.extend(page)     # add this page's users to `users` (extend, not append — extend adds each user; append would add the whole page as one item.)
        next_url = response.links.get("next", {}).get("url")     # url = next link, safely (yesterday's one-liner)
        url = next_url
        params ={}     # params = None  ← because next_url already has it  (hint: look at what the next URL already contains)
    print("Total users:", len(users))

    with open("users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","login","status","created"])
        writer.writeheader()
        for u in users:
            writer.writerow({
                "id": u['id'],
                "login": u['profile']['login'],
                "status": u['status'],
                "created": u['created']
            })   # login comes from u["profile"]["login"]
    print("Wrote", len(users), "rows to users.csv")



if __name__ == "__main__":
    main()
    
"""Export all Okta users to users.csv, following pagination."""
import csv
import os

import requests
from dotenv import load_dotenv

load_dotenv()

ORG_URL = os.getenv("OKTA_ORG_URL")
TOKEN = os.getenv("OKTA_API_TOKEN")


def fetch_all_users(url, headers):
    """Follow Okta pagination and return every user as one list."""
    users = []
    params = {"limit": 2}
    while url:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        users.extend(response.json())
        url = response.links.get("next", {}).get("url")
        params = None   # the next URL already contains limit + after
    return users


def write_csv(users, path):
    """Write id, login, status, created for each user to a CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "login", "status", "created"])
        writer.writeheader()
        for u in users:
            writer.writerow({
                "id": u["id"],
                "login": u["profile"]["login"],
                "status": u["status"],
                "created": u["created"],
            })


def main():
    url = f"{ORG_URL}/api/v1/users"
    headers = {"Authorization": f"SSWS {TOKEN}", "Accept": "application/json"}
    users = fetch_all_users(url, headers)
    print("Total users:", len(users))
    write_csv(users, "users.csv")
    print("Wrote", len(users), "rows to users.csv")


if __name__ == "__main__":
    main()
import os

TOKEN = os.getenv("TOKEN")

ADMIN_IDS = list(
    map(
        int,
        os.getenv("ADMIN_IDS").split(",")
    )
)
import os

folders = [
    "uploads",
    "reports",
    "logs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
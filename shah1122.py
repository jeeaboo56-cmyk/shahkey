#!/usr/bin/env python3

"""
Shah1122 Clean Key Manager
Termux / Python compatible.

One approved key per line in GitHub keys.txt.
"""

import os
import sys
import time
import urllib.request
from pathlib import Path

APP_NAME = "Shah1122"

# Apna GitHub username yahan lagao
KEY_URL = os.getenv(
    "SHAH1122_KEY_URL",
    "https://raw.githubusercontent.com/jeeaboo56-cmyk/shahkey/main/keys.txt"
)

LOCAL_KEYS = Path(__file__).with_name("keys.txt")


def banner():
    print("\033[1;36m" + "=" * 56 + "\033[0m")
    print("\033[1;32m" + " " * 17 + "SHAH1122" + "\033[0m")
    print("\033[1;36m" + " " * 8 + "Clean Key Manager • Termux Ready" + "\033[0m")
    print("\033[1;36m" + "=" * 56 + "\033[0m")


def clean_keys(text):
    return {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def get_remote_keys():
    request = urllib.request.Request(
        KEY_URL,
        headers={
            "User-Agent": "Shah1122-Key-Manager/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = response.read().decode(
            "utf-8",
            errors="replace"
        )

    return clean_keys(data)


def get_local_keys():
    if not LOCAL_KEYS.exists():
        return set()

    data = LOCAL_KEYS.read_text(
        encoding="utf-8",
        errors="replace"
    )

    return clean_keys(data)


def validate_key(key):
    try:
        keys = get_remote_keys()
        source = "GitHub"
    except Exception as error:
        print()
        print(f"[!] GitHub key list unavailable: {error}")

        keys = get_local_keys()
        source = "local keys.txt"

    if key in keys:
        return True, source

    return False, source


def main():
    banner()

    print()
    print(f"App: {APP_NAME}")
    print("Enter your approved key.")
    print("Type 'exit' to quit.")
    print()

    while True:
        try:
            key = input("Shah1122 Key > ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            return

        if key.lower() == "exit":
            return

        if not key:
            print("[!] Please enter a key.")
            continue

        print("[*] Checking key...")

        approved, source = validate_key(key)

        if approved:
            print()
            print("\033[1;32m[+] KEY APPROVED\033[0m")
            print(f"[+] Source: {source}")
            print("[+] Access granted.")
            print()
            return

        print()
        print("\033[1;31m[-] KEY NOT APPROVED\033[0m")
        print("[!] Add this key to your authorized GitHub keys.txt")
        print("[!] and commit the change.")
        print()

        time.sleep(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

SOURCE_URL = "https://raw.githubusercontent.com/CharlesPikachu/freeproxy/master/proxies.json"
OUTPUT_JSON = Path("proxiesus.json")
OUTPUT_TXT = Path("proxiesus.txt")
TIMEOUT = 30


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "proxiesus-updater/1.0 (+https://github.com/)"
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))


def main() -> int:
    payload = fetch_json(SOURCE_URL)
    items = payload.get("data", []) if isinstance(payload, dict) else []

    result: list[str] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        protocol = str(item.get("protocol", "")).strip().lower()
        country = str(item.get("country", "")).strip().upper()
        anonymity = str(item.get("anonymity", "")).strip().lower()
        ip = item.get("ip")
        port = item.get("port")

        if country == "US" and "socks5" in protocol and ip and port:
            result.append(f"{ip}:{port}")

    result = sorted(set(result))

    OUTPUT_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_TXT.write_text(
        ("\n".join(result) + "\n") if result else "",
        encoding="utf-8",
    )

    print(f"Updated {OUTPUT_JSON} with {len(result)} US SOCKS5 Elite proxies")
    print(f"Updated {OUTPUT_TXT} with {len(result)} US SOCKS5 Elite proxies")
    return 0


if __name__ == "__main__":
    sys.exit(main())

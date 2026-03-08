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

ALLOWED_PROTOCOLS = {"http", "https", "socks5"}


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "proxiesus-updater/1.0"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset))


def normalize(value: Any) -> str:
    return str(value or "").strip().lower()


def main() -> int:
    payload = fetch_json(SOURCE_URL)

    items = payload.get("data", []) if isinstance(payload, dict) else []

    result = []

    for item in items:
        if not isinstance(item, dict):
            continue

        protocol = normalize(item.get("protocol"))
        country = normalize(item.get("country"))

        ip = item.get("ip")
        port = item.get("port")

        if country != "us":
            continue

        if protocol not in ALLOWED_PROTOCOLS:
            continue

        if not ip or not port:
            continue

        proxy = f"{protocol}://{ip}:{port}"
        result.append(proxy)

    result = sorted(set(result))

    OUTPUT_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    OUTPUT_TXT.write_text(
        ("\n".join(result) + "\n") if result else "",
        encoding="utf-8",
    )

    print(f"US proxies: {len(result)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

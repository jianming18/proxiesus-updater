#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.request
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SOURCE_URL = "https://raw.githubusercontent.com/CharlesPikachu/freeproxy/master/proxies.json"
OUTPUT_FILE = Path("proxiesus.json")
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


def iter_proxy_items(payload: Any) -> Iterable[dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return

    if isinstance(payload, dict):
        for value in payload.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item


def normalize_protocol(value: Any) -> str:
    return str(value or "").strip().lower()


def normalize_country(value: Any) -> str:
    return str(value or "").strip().upper()


def is_us_socks5(proxy: dict[str, Any]) -> bool:
    return (
        normalize_protocol(proxy.get("protocol")) == "socks5"
        and normalize_country(proxy.get("country_code")) == "US"
    )


def dedupe_keep_order(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for item in items:
        key = f"{item.get('ip', '')}:{item.get('port', '')}:{normalize_protocol(item.get('protocol'))}"
        if key not in seen:
            seen[key] = item
    return list(seen.values())


def main() -> int:
    payload = fetch_json(SOURCE_URL)
    filtered = dedupe_keep_order(item for item in iter_proxy_items(payload) if is_us_socks5(item))

    output = {
        "source": SOURCE_URL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(filtered),
        "proxies": filtered,
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT_FILE} with {len(filtered)} US SOCKS5 proxies")
    return 0


if __name__ == "__main__":
    sys.exit(main())

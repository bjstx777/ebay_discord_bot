import json
import os
import time
from typing import Any, Dict, Optional

import boto3
import requests

secrets = boto3.client("secretsmanager")
dynamodb = boto3.resource("dynamodb")


def _get_secret_json(secret_name: str) -> Dict[str, Any]:
    resp = secrets.get_secret_value(SecretId=secret_name)
    s = resp.get("SecretString")
    if not s:
        raise RuntimeError(f"Secret {secret_name} has no SecretString")
    return json.loads(s)


def _get_discord_webhook_url(secret_name: str) -> str:
    data = _get_secret_json(secret_name)
    url = data.get("url")
    if not url:
        raise RuntimeError(f"Secret {secret_name} missing key 'url'")
    return url


def _post_discord(webhook_url: str, content: str) -> None:
    r = requests.post(webhook_url, json={"content": content}, timeout=10)
    r.raise_for_status()


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Modes:
      - {"mode":"test"}  -> posts a test message to bowman webhook
      - {"mode":"scan"}  -> placeholder (no-op for now)
      - {"mode":"digest"}-> placeholder (no-op for now)
    """
    mode = (event or {}).get("mode", "test")

    # Load secret names from environment variables
    secret_ebay = os.environ.get("SECRET_EBAY_KEYS", "ebay/keys")
    secret_bowman = os.environ.get("SECRET_DISCORD_BOWMAN", "discord/webhook/bowman")

    # Touch eBay keys secret just to verify permissions + JSON shape
    ebay_keys = _get_secret_json(secret_ebay)
    _ = ebay_keys.get("client_id")
    _ = ebay_keys.get("client_secret")

    if mode == "test":
        url = _get_discord_webhook_url(secret_bowman)
        _post_discord(url, f"[ebay_discord_bot] Lambda test OK @ {int(time.time())}")
        return {"ok": True, "mode": mode}

    # Placeholders for next steps
    return {"ok": True, "mode": mode, "note": "scan/digest not implemented yet"}

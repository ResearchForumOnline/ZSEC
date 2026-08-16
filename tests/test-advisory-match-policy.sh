#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
script="$root/zsec"

grep -Fq 'item_tags = set(item.get("tags") or [])' "$script"
grep -Fq 'if item.get("kind") == "news" and marker in ("ssh", "openssh") and "ssh" not in item_tags:' "$script"

echo "ZSEC advisory matching policy: ok"

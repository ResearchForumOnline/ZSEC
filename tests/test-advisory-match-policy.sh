#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
script="$root/zsec"

grep -Fq 'item_tags = set(item.get("tags") or [])' "$script"
grep -Fq 'if item.get("kind") == "news" and marker in ("ssh", "openssh") and "ssh" not in item_tags:' "$script"
grep -Fq 'if marker == "kernel" and structured_product and not structured_linux_kernel:' "$script"
grep -Fq 'apt-get -o "DPkg::Lock::Timeout=${lock_wait}" "$@"' "$script"
grep -Fq 'deferring security package work until the next timer run' "$script"

echo "ZSEC advisory matching policy: ok"

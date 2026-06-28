#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 user@host [ssh-args...]" >&2
  exit 2
fi

TARGET="$1"
shift || true

ssh "$@" "$TARGET" 'curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash'

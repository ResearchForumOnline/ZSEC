#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

assert_timer() {
    local file=$1
    local calendar=$2

    grep -Fqx "OnCalendar=$calendar" "$file"
    grep -Fqx "Persistent=true" "$file"
    grep -Fqx "AccuracySec=1min" "$file"

    if grep -Eq '^(OnBootSec|OnUnitActiveSec)=' "$file"; then
        echo "Monotonic-only timer directive found in $file" >&2
        exit 1
    fi
}

assert_timer "$root/systemd/zsec.timer" '*-*-* 00,12:00:00'
assert_timer "$root/site/talktoai-zsec/talktoai-zsec-feed.timer" '*-*-* 00,06,12,18:00:00'

if command -v systemd-analyze >/dev/null 2>&1; then
    systemd-analyze verify \
        "$root/systemd/zsec.service" \
        "$root/systemd/zsec.timer" \
        "$root/site/talktoai-zsec/talktoai-zsec-feed.service" \
        "$root/site/talktoai-zsec/talktoai-zsec-feed.timer"
fi

echo "ZSEC calendar timers: ok"

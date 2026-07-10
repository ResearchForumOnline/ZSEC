#!/usr/bin/env bash
set -Eeuo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
script="$root/zsec"

grep -Fq 'ZSEC_PACKAGE_LOCK_WAIT_SECONDS="${ZSEC_PACKAGE_LOCK_WAIT_SECONDS:-180}"' "$script"
grep -Fq 'package_manager_busy()' "$script"
grep -Fq 'wait_for_package_manager()' "$script"
grep -Fq 'if have fuser; then' "$script"
grep -Fq 'deferring package work until the next timer run' "$script"
grep -Fq 'ZSEC run completed with package work deferred' "$script"

if grep -Fq 'fail "apt is already running"' "$script"; then
  echo "ZSEC still fails immediately on apt lock contention" >&2
  exit 1
fi

echo "ZSEC package lock policy: ok"

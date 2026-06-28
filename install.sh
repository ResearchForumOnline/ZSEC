#!/usr/bin/env bash
set -euo pipefail

ZSEC_VERSION="0.1.0"
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local/sbin}"
CONFIG_DIR="${CONFIG_DIR:-/etc/zsec}"
SYSTEMD_DIR="${SYSTEMD_DIR:-/etc/systemd/system}"
SOURCE_BASE="${ZSEC_SOURCE_BASE:-https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main}"

say() { printf '[zsec-install] %s\n' "$*"; }
die() { printf '[zsec-install] ERROR: %s\n' "$*" >&2; exit 1; }

need_root() {
  if [ "${EUID:-$(id -u)}" -ne 0 ]; then
    die "Run as root, for example: sudo bash install.sh"
  fi
}

fetch_file() {
  local source_path="$1"
  local destination="$2"
  if [ -f "$source_path" ]; then
    install -m 0644 "$source_path" "$destination"
    return
  fi
  command -v curl >/dev/null 2>&1 || die "curl is required for remote install"
  local remote_url separator
  remote_url="${SOURCE_BASE}/${source_path}"
  separator="?"
  case "$remote_url" in
    *\?*) separator="&" ;;
  esac
  curl -fsSL "${remote_url}${separator}cachebust=$(date +%s)" -o "$destination"
}

detect_admin_ip() {
  if [ -n "${ZSEC_ADMIN_IP:-}" ]; then
    printf '%s\n' "$ZSEC_ADMIN_IP"
    return
  fi
  if [ -n "${SSH_CONNECTION:-}" ]; then
    printf '%s\n' "$SSH_CONNECTION" | awk '{print $1}'
  fi
}

install_files() {
  install -d -m 0755 "$INSTALL_PREFIX" "$CONFIG_DIR" "$CONFIG_DIR/allowlist.d" "$SYSTEMD_DIR"

  if [ -f "./zsec" ]; then
    install -m 0755 "./zsec" "${INSTALL_PREFIX}/zsec"
  else
    local tmp
    tmp="$(mktemp)"
    fetch_file "zsec" "$tmp"
    install -m 0755 "$tmp" "${INSTALL_PREFIX}/zsec"
    rm -f "$tmp"
  fi

  if [ ! -f "${CONFIG_DIR}/zsec.conf" ]; then
    if [ -f "./config/zsec.conf" ]; then
      install -m 0644 "./config/zsec.conf" "${CONFIG_DIR}/zsec.conf"
    else
      local tmp_conf
      tmp_conf="$(mktemp)"
      fetch_file "config/zsec.conf" "$tmp_conf"
      install -m 0644 "$tmp_conf" "${CONFIG_DIR}/zsec.conf"
      rm -f "$tmp_conf"
    fi
  fi

  if [ -f "./systemd/zsec.service" ]; then
    install -m 0644 "./systemd/zsec.service" "${SYSTEMD_DIR}/zsec.service"
    install -m 0644 "./systemd/zsec.timer" "${SYSTEMD_DIR}/zsec.timer"
  else
    local tmp_service tmp_timer
    tmp_service="$(mktemp)"
    tmp_timer="$(mktemp)"
    fetch_file "systemd/zsec.service" "$tmp_service"
    fetch_file "systemd/zsec.timer" "$tmp_timer"
    install -m 0644 "$tmp_service" "${SYSTEMD_DIR}/zsec.service"
    install -m 0644 "$tmp_timer" "${SYSTEMD_DIR}/zsec.timer"
    rm -f "$tmp_service" "$tmp_timer"
  fi

  local admin_ip
  admin_ip="$(detect_admin_ip || true)"
  if [ -n "$admin_ip" ]; then
    printf 'ZSEC_ADMIN_IP="%s"\n' "$admin_ip" > "${CONFIG_DIR}/allowlist.d/admin-ip.conf"
    chmod 0600 "${CONFIG_DIR}/allowlist.d/admin-ip.conf"
    say "saved admin SSH IP: $admin_ip"
  else
    say "no SSH admin IP detected; you can set ZSEC_ADMIN_IP in ${CONFIG_DIR}/allowlist.d/admin-ip.conf"
  fi
}

enable_systemd() {
  if command -v systemctl >/dev/null 2>&1 && [ -d /run/systemd/system ]; then
    systemctl daemon-reload
    systemctl enable --now zsec.timer
    say "enabled zsec.timer"
  else
    say "systemd not detected; install complete, but timer was not enabled"
  fi
}

main() {
  need_root
  install_files
  "${INSTALL_PREFIX}/zsec" lockout-guard || true
  "${INSTALL_PREFIX}/zsec" check || true
  enable_systemd
  say "ZSEC Auto Updates ${ZSEC_VERSION} installed"
  say "Run: sudo zsec status"
}

main "$@"

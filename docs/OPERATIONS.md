# Operations Guide

ZSEC is designed for operators who want a small, deterministic baseline for Linux server patching and hardening.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
sudo zsec status
```

Clone install:

```bash
git clone https://github.com/ResearchForumOnline/ZSEC.git
cd ZSEC
sudo bash install.sh
```

## First Checks

After install:

```bash
sudo zsec status
sudo zsec check
sudo zsec audit
sudo zsec todo
```

Confirm:

- the systemd timer is enabled
- SSH backups exist under `/var/backups/zsec`
- the current admin SSH IP was recorded when available
- security update candidates are reported correctly
- exposed AI/dev ports are expected or closed

## Normal Operation

ZSEC runs from a systemd timer every 12 hours with randomized delay. It writes logs to `/var/log/zsec/zsec.log` and local advisory TODOs to `/var/lib/zsec/todo.txt`.

Useful commands:

```bash
zsec check
zsec run
zsec audit
zsec lockout-guard
zsec todo
zsec status
zsec version
```

## Security Boundary

The advisory feed is read-only data. It can create local TODOs and warnings, but it must not execute actions.

ZSEC does not accept:

- shell commands from the feed
- package names to install from the feed
- firewall rules from the feed
- SSH config changes from the feed
- AI-generated runtime actions

## Hosting Panel Use

For FreeWebPanel or other hosting panels, keep ZSEC as a separate baseline utility:

1. Install the panel normally.
2. Install ZSEC as a companion hardening step.
3. Review `sudo zsec status`.
4. Keep panel support and ZSEC logs separate.
5. Use ZSEC warnings to guide operator review, not automatic web-panel actions.

## Incident Review

When investigating a server issue:

1. Check `/var/log/zsec/zsec.log`.
2. Confirm what updates the OS package manager applied.
3. Review `/var/lib/zsec/todo.txt`.
4. Check SSH access, fail2ban status, firewall rules, and public ports.
5. Use `/var/backups/zsec` for SSH config reference if needed.

ZSEC should make server state easier to inspect, not harder.

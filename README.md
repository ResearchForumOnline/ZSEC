# ZSEC Auto Updates

Security-only auto updates and lightweight hardening for Linux servers.

Made by [FreeWebPanel.com](https://freewebpanel.com/) and [talktoai.org](https://talktoai.org/).

ZSEC is a standalone open-source server utility. It does not depend on FreeWebPanel and it does not run AI by default. The project is currently promoted and maintained on GitHub.

## What It Does

- Checks every 12 hours with a systemd timer.
- Applies security updates only.
- Supports Ubuntu first, with AlmaLinux and Rocky Linux support through DNF security updates.
- Records the active SSH admin IP during install to reduce lockout risk.
- Backs up SSH configuration and authorized keys before hardening.
- Adds optional SSH firewall allow rules for the admin IP without adding a deny policy.
- Configures safe kernel/network hardening sysctls.
- Configures fail2ban for SSH when available.
- Audits exposed AI/dev service ports locally without opening any API door.
- Keeps logs in `/var/log/zsec/zsec.log`.

## Quick Install

```bash
git clone https://github.com/ResearchForumOnline/ZSEC.git
cd ZSEC
sudo bash install.sh
```

Run a non-changing check first:

```bash
sudo zsec check
```

Run the updater manually:

```bash
sudo zsec run
```

Check status:

```bash
sudo zsec status
```

## One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
```

## Supported Systems

- Ubuntu 22.04, 24.04, and newer compatible releases
- AlmaLinux 8/9/10 compatible releases
- Rocky Linux 8/9/10 compatible releases
- Other Debian/RHEL-like systems may work, but are not the main support target yet

## Security Model

ZSEC is intentionally conservative.

- It updates only security packages.
- It does not install feature upgrades.
- It does not change SSH ports.
- It does not disable password login automatically.
- It does not add firewall deny rules automatically.
- It does not expose a web panel, agent socket, AI endpoint, or remote command API.

The optional AI audit is local-only. It checks for commonly exposed AI/dev service ports such as Ollama, Jupyter, Gradio, Open WebUI, and common development ports. It reports warnings only.

## Why ZSEC Exists

Current Linux server attacks continue to exploit three boring but dangerous gaps:

- slow kernel/security patching
- exposed SSH and brute-force attempts
- public development or AI services left listening on the internet

ZSEC turns those lessons into a small operational baseline: security updates, lockout guardrails, SSH abuse reduction, and local exposure checks.

See [docs/threat-model.md](docs/threat-model.md).

## FreeWebPanel Integration

FreeWebPanel can install ZSEC as a separate hardening step, but ZSEC remains independent.

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
```

See [docs/freewebpanel-integration.md](docs/freewebpanel-integration.md).

## Configuration

Main config:

```bash
/etc/zsec/zsec.conf
```

Admin IP allowlist:

```bash
/etc/zsec/allowlist.d/admin-ip.conf
```

Systemd units:

```bash
/etc/systemd/system/zsec.service
/etc/systemd/system/zsec.timer
```

## Commands

```bash
zsec check          # dry-run security update and audits
zsec run            # apply security updates and hardening
zsec audit          # local hardening and exposed-port audit only
zsec lockout-guard  # refresh SSH backups and admin IP record
zsec status         # show timer and latest log
zsec version        # print version
```

## Zero Boundary Algebra Note

The Zero Boundary Algebra material is used only as a design metaphor for deterministic safety checks: build, mirror, red-team, reset to facts, then apply. ZSEC does not use AI or hidden reasoning at runtime.

See [docs/zero-boundary-algebra.md](docs/zero-boundary-algebra.md).

## Open Source and Tamper Resistance

ZSEC is open source. The code should be visible and auditable. Hiding code is not treated as a security feature.

For tamper resistance, the installer makes runtime files root-owned and non-writable by normal users. Optional immutable file locking can be enabled in config, but it is off by default because it can make legitimate updates harder.

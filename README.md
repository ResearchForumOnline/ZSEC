# ZSEC Auto Updates

<p align="center">
  <strong>Security-only Linux auto updates, SSH lockout guardrails, and read-only advisory TODOs for real servers.</strong>
</p>

<p align="center">
  <a href="https://talktoai.org/zsec/">Website</a>
  |
  <a href="https://www.youtube.com/watch?v=_ZTn8SGT0VU">Video</a>
  |
  <a href="https://talktoai.org/zsec/feed.json">Advisory Feed</a>
  |
  <a href="docs/advisory-feed.md">Feed Design</a>
  |
  <a href="docs/freewebpanel-integration.md">FreeWebPanel Integration</a>
  |
  <a href="SECURITY.md">Security Policy</a>
</p>

<p align="center">
  <img alt="Linux" src="https://img.shields.io/badge/Linux-servers-111827?style=for-the-badge&logo=linux&logoColor=white">
  <img alt="Security only" src="https://img.shields.io/badge/updates-security_only-008767?style=for-the-badge">
  <img alt="No remote commands" src="https://img.shields.io/badge/feed-no_remote_commands-c93632?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/github/license/ResearchForumOnline/ZSEC?style=for-the-badge">
</p>

Made by [FreeWebPanel.com](https://freewebpanel.com/) and [talktoai.org](https://talktoai.org/).

ZSEC is a standalone open-source server utility. It does not depend on FreeWebPanel, does not run AI by default, and does not expose a web panel, socket, or remote command API.

## Video Walkthrough

<p align="center">
  <a href="https://www.youtube.com/watch?v=_ZTn8SGT0VU">
    <img src="https://img.youtube.com/vi/_ZTn8SGT0VU/hqdefault.jpg" alt="Watch the ZSEC Auto Updates video walkthrough on YouTube" width="640">
  </a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=_ZTn8SGT0VU"><strong>Watch the ZSEC Auto Updates video walkthrough</strong></a>
</p>

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
sudo zsec status
sudo zsec check
```

Clone install:

```bash
git clone https://github.com/ResearchForumOnline/ZSEC.git
cd ZSEC
sudo bash install.sh
```

## What ZSEC Does

| Area | Behavior |
| --- | --- |
| Update policy | Applies operating-system security updates only. |
| Schedule | Runs every 12 hours using a systemd timer with randomized delay. |
| Ubuntu/Debian/Proxmox | Selects apt candidates from security origins only. |
| AlmaLinux/Rocky/RHEL | Uses DNF security metadata with `dnf --security upgrade`. |
| SSH safety | Backs up SSH config and authorized keys, then records the active admin SSH IP. |
| Abuse reduction | Configures fail2ban for SSH when available. |
| Host hardening | Applies conservative kernel/network sysctl hardening. |
| Container hosts | Preserves unprivileged user namespaces on detected Proxmox, LXC, Docker, Podman, or Kubernetes-style hosts. |
| AI/dev exposure | Locally audits public ports often used by AI/dev tools such as Ollama, Jupyter, Gradio, Open WebUI, and Node dev services. |
| Advisory TODOs | Reads `https://talktoai.org/zsec/feed.json` as read-only data and writes local TODOs. |

## Why It Exists

Linux servers are attacked constantly by scanners, SSH botnets, exploit chains, and increasingly automated tooling. The highest-value baseline is still disciplined and boring:

- patch security updates quickly
- keep SSH from becoming a lockout or brute-force problem
- reduce public development and AI service exposure
- keep server hardening deterministic and inspectable

ZSEC is built for that baseline. It is not a magic black box. It is a small, auditable updater with guardrails.

## Hard Security Boundary

ZSEC intentionally does not allow its advisory feed to become a command channel.

Allowed:

- read public feed data
- cache advisory JSON locally
- create `/var/lib/zsec/todo.txt`
- warn about locally relevant risks

Not allowed:

- shell commands from the feed
- package names to install from the feed
- firewall rules from the feed
- SSH configuration changes from the feed
- AI-generated actions from the feed

The package manager remains the authority for security updates.

## Commands

```bash
zsec check          # dry-run security update and audits
zsec run            # apply security updates and hardening
zsec audit          # local hardening and exposed-port audit only
zsec lockout-guard  # refresh SSH backups and admin IP record
zsec todo           # show local advisory feed TODOs
zsec status         # show timer, latest log, and TODO preview
zsec version        # print version
```

## Files

| Path | Purpose |
| --- | --- |
| `/usr/local/sbin/zsec` | Runtime command |
| `/etc/zsec/zsec.conf` | Main config |
| `/etc/zsec/allowlist.d/admin-ip.conf` | Saved admin SSH IP |
| `/var/log/zsec/zsec.log` | Runtime log |
| `/var/lib/zsec/todo.txt` | Human-readable advisory TODOs |
| `/var/lib/zsec/todo.json` | Structured advisory TODOs |
| `/var/backups/zsec` | SSH backup snapshots |
| `/etc/systemd/system/zsec.timer` | 12-hour systemd timer |

## Supported Systems

Primary support:

- Ubuntu 22.04, 24.04, and compatible newer releases
- AlmaLinux 8/9/10 compatible releases
- Rocky Linux 8/9/10 compatible releases

Also used in practice:

- Debian-like systems
- Proxmox VE hosts
- Linux Mint/Ubuntu-derived server desktops

## Advisory Feed

Public page:

```text
https://talktoai.org/zsec/
```

Public data feed:

```text
https://talktoai.org/zsec/feed.json
```

The feed currently combines:

- CISA Known Exploited Vulnerabilities
- relevant server-security news from The Hacker News RSS
- static ZSEC baseline checks for SSH brute-force protection and exposed AI/dev ports

See [docs/advisory-feed.md](docs/advisory-feed.md).

## FreeWebPanel Integration

FreeWebPanel can offer ZSEC as a separate hardening step:

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
```

ZSEC remains independent and can be used on any supported Linux server.

See [docs/freewebpanel-integration.md](docs/freewebpanel-integration.md).

## Owner Maintenance

The project owner runs a weekly Codex/OpenAI maintenance task to refresh public TODOs, rebuild the advisory feed, check docs, validate scripts, and push useful updates. This is an owner workflow, not a public remote-control system.

See [docs/owner-maintenance.md](docs/owner-maintenance.md).

## Optional AI Stance

AI is optional and off the runtime path. ZSEC does not require an API key, model, local LLM, or hosted AI service. That is deliberate: security tooling should not open another attack surface just to patch servers.

AI can help the owner review public advisories and improve documentation, but server-side ZSEC behavior stays deterministic.

## Zero Boundary Algebra Note

The Zero Boundary Algebra material is used only as a design metaphor for deterministic safety checks: build, mirror, red-team, reset to facts, then apply. ZSEC does not use AI or hidden reasoning at runtime.

See [docs/zero-boundary-algebra.md](docs/zero-boundary-algebra.md).

## License

Open source under the repository license. The code should be visible and auditable. Hiding code is not treated as a security feature.

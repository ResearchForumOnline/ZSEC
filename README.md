# ZSEC Auto Updates

<p align="center">
  <img src="site/talktoai-zsec/talktoai-investor-cover.png" alt="ZSEC server security automation cover image" width="960">
</p>

<p align="center">
  <strong>Security-only Linux updates, SSH lockout guardrails, fail2ban direction, local exposure checks, and read-only advisory TODOs.</strong>
</p>

<p align="center">
  <a href="https://talktoai.org/zsec/"><img alt="Website" src="https://img.shields.io/badge/website-talktoai.org%2Fzsec-19f2b4?style=for-the-badge"></a>
  <a href="https://github.com/ResearchForumOnline/ZSEC/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/ResearchForumOnline/ZSEC?include_prereleases&style=for-the-badge"></a>
  <a href="https://github.com/ResearchForumOnline/ZSEC/actions"><img alt="Repo checks" src="https://img.shields.io/github/actions/workflow/status/ResearchForumOnline/ZSEC/repo-checks.yml?branch=main&label=checks&style=for-the-badge"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/ResearchForumOnline/ZSEC?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="docs/OPERATIONS.md">Operations</a>
  |
  <a href="docs/DOWNLOADS_AND_RELEASES.md">Downloads</a>
  |
  <a href="docs/advisory-feed.md">Advisory Feed</a>
  |
  <a href="docs/threat-model.md">Threat Model</a>
  |
  <a href="docs/freewebpanel-integration.md">FreeWebPanel</a>
  |
  <a href="SECURITY.md">Security</a>
</p>

ZSEC is a small open-source utility for Linux servers that need predictable security maintenance without turning a public feed, web panel, or AI system into a control plane.

It has one clear purpose: keep a real server patched, safer to access over SSH, easier to inspect, and harder to accidentally expose.

## Install

Review the installer before running it:

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh -o zsec-install.sh
less zsec-install.sh
sudo bash zsec-install.sh
```

Fast install on a server you control:

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
```

Clone install:

```bash
git clone https://github.com/ResearchForumOnline/ZSEC.git
cd ZSEC
sudo bash install.sh
```

Check the install:

```bash
sudo zsec status
sudo zsec check
sudo zsec audit
```

## What It Does

| Area | Behavior |
| --- | --- |
| Security updates | Applies operating-system security updates only. |
| Schedule | Runs every 12 hours through a systemd timer with randomized delay. |
| Debian family | Selects apt candidates from security origins on Ubuntu, Debian, Proxmox, and compatible systems. |
| RHEL family | Uses DNF security metadata on AlmaLinux, Rocky Linux, RHEL-like systems, and compatible hosts. |
| SSH safety | Backs up SSH config and authorized keys before guardrail work. |
| Lockout awareness | Records the current admin SSH IP when available. |
| Abuse reduction | Configures fail2ban for SSH when available. |
| Host hardening | Applies conservative kernel/network sysctl hardening. |
| Container hosts | Preserves unprivileged user namespaces on detected container or virtualization hosts. |
| AI/dev exposure | Warns about public ports often used by Ollama, Jupyter, Gradio, Open WebUI, and Node dev services. |
| Advisory TODOs | Reads the public ZSEC feed as data and writes local TODO files for operator review. |

## Hard Security Boundary

ZSEC is intentionally not a remote administration platform.

| Allowed | Not allowed |
| --- | --- |
| Read a public advisory feed | Run shell commands from the feed |
| Cache advisory JSON locally | Install packages requested by the feed |
| Create local TODO text and JSON | Change firewall rules from the feed |
| Warn about locally relevant risks | Change SSH config from the feed |
| Use the OS package manager for updates | Let AI perform runtime server actions |

The local package manager remains the authority for security updates. The advisory feed is guidance, not a command channel.

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

## Downloads

| Need | Link |
| --- | --- |
| Latest source ZIP | [Download ZIP](https://github.com/ResearchForumOnline/ZSEC/archive/refs/heads/main.zip) |
| GitHub releases | [ZSEC releases](https://github.com/ResearchForumOnline/ZSEC/releases) |
| Install script | [install.sh](install.sh) |
| Operations guide | [docs/OPERATIONS.md](docs/OPERATIONS.md) |
| Advisory feed design | [docs/advisory-feed.md](docs/advisory-feed.md) |
| Public website | [talktoai.org/zsec](https://talktoai.org/zsec/) |

## Supported Systems

Primary support:

- Ubuntu 22.04, 24.04, and compatible newer releases
- Debian-like systems
- Proxmox VE hosts
- AlmaLinux 8/9/10 compatible releases
- Rocky Linux 8/9/10 compatible releases

ZSEC should be tested on a spare server, VM, or staging host before wide rollout.

## Files On A Server

| Path | Purpose |
| --- | --- |
| `/usr/local/sbin/zsec` | Runtime command |
| `/etc/zsec/zsec.conf` | Main config |
| `/etc/zsec/allowlist.d/admin-ip.conf` | Saved admin SSH IP when available |
| `/var/log/zsec/zsec.log` | Runtime log |
| `/var/lib/zsec/todo.txt` | Human-readable advisory TODOs |
| `/var/lib/zsec/todo.json` | Structured advisory TODOs |
| `/var/backups/zsec` | SSH backup snapshots |
| `/etc/systemd/system/zsec.timer` | 12-hour systemd timer |

## Videos

<p align="center">
  <a href="https://www.youtube.com/watch?v=_ZTn8SGT0VU">
    <img src="https://img.youtube.com/vi/_ZTn8SGT0VU/hqdefault.jpg" alt="Watch the ZSEC Auto Updates video walkthrough on YouTube" width="420">
  </a>
  <a href="https://www.youtube.com/watch?v=R52hsRdCmSM">
    <img src="https://img.youtube.com/vi/R52hsRdCmSM/hqdefault.jpg" alt="Watch the TalkToAI ecosystem overview on YouTube" width="420">
  </a>
</p>

- [ZSEC Auto Updates video walkthrough](https://www.youtube.com/watch?v=_ZTn8SGT0VU)
- [TalkToAI ecosystem overview](https://www.youtube.com/watch?v=R52hsRdCmSM)
- [ZSEC YouTube Short](https://www.youtube.com/shorts/z2keIOqCkio)

## Documentation

- [Operations guide](docs/OPERATIONS.md)
- [Downloads and releases](docs/DOWNLOADS_AND_RELEASES.md)
- [Threat model](docs/threat-model.md)
- [Advisory feed design](docs/advisory-feed.md)
- [FreeWebPanel integration](docs/freewebpanel-integration.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Why ZSEC Exists

Linux servers are attacked constantly by scanners, SSH botnets, exploit chains, and increasingly automated tooling. The highest-value baseline is still disciplined and practical:

- apply security updates quickly;
- avoid SSH lockouts while reducing brute-force exposure;
- warn about public AI and development services;
- keep server hardening deterministic and inspectable;
- avoid remote-control behavior hidden behind a feed or dashboard.

ZSEC is built for that baseline.

## Search-Friendly Topics

ZSEC is for people searching for security-only Linux updates, unattended security updates, SSH lockout protection, fail2ban setup, server hardening scripts, AI server exposure checks, Ollama public port warnings, Proxmox security updates, AlmaLinux security updates, Rocky Linux security updates, and safe Linux update automation.

## License

Open source under the repository license. The code should be visible and auditable. Hiding code is not treated as a security feature.

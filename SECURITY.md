# Security Policy

ZSEC Auto Updates is a security tool, so the project keeps a strict boundary between advisory data and server actions.

## Supported Scope

Primary support:

- Ubuntu 22.04, 24.04, and compatible newer releases
- AlmaLinux 8/9/10 compatible releases
- Rocky Linux 8/9/10 compatible releases

Best-effort support:

- Debian-like systems
- Proxmox VE hosts
- Linux Mint/Ubuntu-derived systems used as servers

## Reporting a Security Issue

Please do not publish exploit details publicly before the maintainer has had a fair chance to review them.

Report security issues through the repository issue tracker if the issue is not sensitive. If sensitive details are involved, contact the maintainer through the public project links on [talktoai.org](https://talktoai.org/).

Useful report details:

- affected ZSEC version or commit
- operating system and version
- exact command used
- expected behavior
- observed behavior
- logs with secrets removed

Never include passwords, private keys, API keys, tokens, or full server credential files.

## Security Design Promises

ZSEC must not:

- run commands from the advisory feed
- install packages named by the advisory feed
- change firewall rules from the advisory feed
- change SSH policy from the advisory feed
- require AI, an API key, or a local model to run
- silently switch from security updates to feature upgrades

ZSEC may:

- apply OS security updates through apt or dnf
- create local advisory TODOs
- back up SSH files before hardening
- configure fail2ban for SSH
- warn about public AI/dev-like listeners
- apply conservative sysctl hardening

## Owner Automation

The owner may use Codex/OpenAI to review public advisories, update documentation, rebuild the public feed, and push repository updates. That owner workflow is not part of the server runtime and must not create a public remote-control channel.


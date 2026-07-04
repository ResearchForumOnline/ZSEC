# Downloads And Releases

ZSEC is a small Linux security utility for security-only updates, SSH guardrails, fail2ban direction, local exposure checks, and read-only advisory TODOs.

## Public Links

| Need | Link |
| --- | --- |
| Website | <https://talktoai.org/zsec/> |
| GitHub repository | <https://github.com/ResearchForumOnline/ZSEC> |
| Source ZIP | <https://github.com/ResearchForumOnline/ZSEC/archive/refs/heads/main.zip> |
| GitHub releases | <https://github.com/ResearchForumOnline/ZSEC/releases> |
| Advisory feed | <https://talktoai.org/zsec/feed.json> |
| Operations guide | [OPERATIONS.md](OPERATIONS.md) |

## Install

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

## Release Notes Should Cover

- supported distro behavior;
- apt or dnf security-update behavior;
- SSH backup and lockout guardrail changes;
- fail2ban changes;
- AI/dev exposure check changes;
- advisory feed format changes.

## Search-Friendly Summary

ZSEC is for security-only Linux updates, Ubuntu security updates, AlmaLinux security updates, Rocky Linux security updates, SSH lockout protection, fail2ban hardening, AI server exposure checks, Ollama port warnings, and server hardening automation.

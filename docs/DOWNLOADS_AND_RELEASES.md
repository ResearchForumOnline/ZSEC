# Downloads And Releases

ZSEC is a small Linux security utility for security-only updates, SSH guardrails, fail2ban direction, local exposure checks, and read-only advisory TODOs.

## Public Links

| Need | Link |
| --- | --- |
| Website | <https://talktoai.org/zsec/> |
| GitHub repository | <https://github.com/ResearchForumOnline/ZSEC> |
| Source ZIP | <https://github.com/ResearchForumOnline/ZSEC/archive/refs/heads/main.zip> |
| GitHub releases | <https://github.com/ResearchForumOnline/ZSEC/releases> |
| Current ZSEC Linux utility release | <https://github.com/ResearchForumOnline/ZSEC/releases/tag/v0.1.0> |
| ZSEC Shield immutable prerelease | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.1.2> |
| Advisory feed | <https://talktoai.org/zsec/feed.json> |
| Operations guide | [OPERATIONS.md](OPERATIONS.md) |

## ZSEC Shield Immutable Prerelease

ZSEC Shield v0.1.2 is a separate, immutable GitHub prerelease of the deterministic
on-demand scanner for Windows, macOS, and Linux. GitHub's release attestation covers
the published tag and asset digests. The native archives are unsigned preview builds:
they do not carry Authenticode, Apple Developer ID/notarization, or Linux package
signatures. Verify the checksum from the authenticated release before extracting an
archive, and do not bypass operating-system protections merely to run the preview.

| Need | Exact download |
| --- | --- |
| Release notes and all assets | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.1.2> |
| Windows x64 ZIP | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/zsec-shield-0.1.2-windows-x86_64.zip> |
| macOS arm64 tar.gz | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/zsec-shield-0.1.2-macos-arm64.tar.gz> |
| Linux x86_64 tar.gz | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/zsec-shield-0.1.2-linux-x86_64.tar.gz> |
| Combined checksums | <https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/SHA256SUMS.txt> |

Verify the automatic immutable-release attestation with a current GitHub CLI:

```bash
gh release verify v0.1.2 -R ResearchForumOnline/ZSEC-Shield
```

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

## Current Public Release

### v0.1.0

- Security-only Linux update runner.
- Systemd timer with randomized delay.
- SSH config and authorized-key backup guardrails.
- fail2ban direction for SSH when available.
- Conservative sysctl hardening.
- Container and virtualization host detection.
- AI/dev public-port exposure warnings.
- Read-only advisory feed cache and local TODO output.
- Public docs, operations guide, threat model, and FreeWebPanel integration notes.

## Search-Friendly Summary

ZSEC is for security-only Linux updates, Ubuntu security updates, AlmaLinux security updates, Rocky Linux security updates, SSH lockout protection, fail2ban hardening, AI server exposure checks, Ollama port warnings, and server hardening automation.

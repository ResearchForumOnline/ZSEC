# ZSEC Documentation

These docs explain how ZSEC works, how to operate it safely, and how it fits into the TalkToAI and FreeWebPanel server stack. The rendered public guide is available at <https://docs.talktoai.org/zsec/>.

## Start Here

| Need | Page |
| --- | --- |
| Install and daily operation | [OPERATIONS.md](OPERATIONS.md) |
| Download and release links | [DOWNLOADS_AND_RELEASES.md](DOWNLOADS_AND_RELEASES.md) |
| Security assumptions | [threat-model.md](threat-model.md) |
| Advisory feed behavior | [advisory-feed.md](advisory-feed.md) |
| Hosting panel integration | [freewebpanel-integration.md](freewebpanel-integration.md) |
| Roadmap | [ROADMAP.md](ROADMAP.md) |
| Rendered operational guide | <https://docs.talktoai.org/zsec/> |

## Core Boundary

ZSEC can read public advisory data and write local TODO files. It must not turn that data into remote shell commands, package install instructions, firewall changes, SSH configuration changes, or AI-driven runtime actions.

For security issues, see [../SECURITY.md](../SECURITY.md).

## Product Boundaries

- **ZSEC Auto Updates v0.1.0** is the Linux server utility in this repository.
- **ZSEC Shield v0.1.2** is a separate immutable, unsigned endpoint-scanner prerelease in [`ResearchForumOnline/ZSEC-Shield`](https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.1.2).
- Neither product accepts runtime instructions from an AI system or public advisory feed.
- ZSEC Shield is not certified antivirus or real-time malware prevention.


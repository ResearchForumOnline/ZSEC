# ZSEC Documentation

These docs explain how ZSEC works, how to operate it safely, and how it fits into the TalkToAI and FreeWebPanel server stack.

## Start Here

| Need | Page |
| --- | --- |
| Install and daily operation | [OPERATIONS.md](OPERATIONS.md) |
| Download and release links | [DOWNLOADS_AND_RELEASES.md](DOWNLOADS_AND_RELEASES.md) |
| Security assumptions | [threat-model.md](threat-model.md) |
| Advisory feed behavior | [advisory-feed.md](advisory-feed.md) |
| Hosting panel integration | [freewebpanel-integration.md](freewebpanel-integration.md) |
| Roadmap | [ROADMAP.md](ROADMAP.md) |

## Core Boundary

ZSEC can read public advisory data and write local TODO files. It must not turn that data into remote shell commands, package install instructions, firewall changes, SSH configuration changes, or AI-driven runtime actions.

For security issues, see [../SECURITY.md](../SECURITY.md).


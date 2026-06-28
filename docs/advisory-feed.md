# ZSEC Advisory Feed

ZSEC can read `https://talktoai.org/zsec/feed.json` during `zsec check`, `zsec run`, and `zsec audit`.

The feed is intentionally data-only.

Allowed:

- create local TODOs in `/var/lib/zsec/todo.txt`
- cache source advisories in `/var/lib/zsec/advisory-feed.json`
- warn about locally relevant risks such as Linux kernel advisories, SSH botnet activity, web server issues, and public AI/dev service ports

Not allowed:

- shell commands from the feed
- package names to install from the feed
- firewall rules from the feed
- SSH configuration changes from the feed
- AI-generated actions from the feed

This keeps the useful part of live security intelligence without turning the public website into a control plane for servers.

## Sources

The feed builder currently uses:

- CISA Known Exploited Vulnerabilities catalog
- The Hacker News RSS items that match server-security keywords
- Static ZSEC baseline checks for SSH brute-force protection and exposed AI/dev ports

The feed builder lives at `tools/build-feed.py`.

## Client Behavior

ZSEC downloads the feed with `curl`, validates `schema: zsec.feed.v1`, then uses local package, OS, kernel, and listening-port context to decide which items deserve a TODO.

Package updates still come only from the operating system package manager:

- Debian/Ubuntu/Proxmox/ZeroMint-like systems: apt security candidate selection
- AlmaLinux/Rocky/RHEL-like systems: `dnf --security upgrade`


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

Each item preserves its public source URL and a bounded summary. Feed generation applies token-boundary and security-context filters to reduce generic Linux, AI, Jupyter, Node and port-number false positives.

## Client Behavior

ZSEC downloads the feed with `curl`, validates `schema: zsec.feed.v1`, then uses local package, OS, kernel, and listening-port context to decide which items deserve a TODO.

Package updates still come only from the operating system package manager:

- Debian/Ubuntu/Proxmox/ZeroMint-like systems: apt security candidate selection
- AlmaLinux/Rocky/RHEL-like systems: `dnf --security upgrade`

## Applicability And Failure Behaviour

Feed matches are deliberately conservative review prompts. A generic product name, port or CVE does not prove exposure on a host. Operators must confirm listening scope, firewall reachability, installed software and affected versions.

If the feed is unavailable, malformed or has the wrong schema, the client must not infer or execute replacement actions. Security-package checks remain local; remote instructions remain disabled.

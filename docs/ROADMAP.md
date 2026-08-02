# Roadmap

ZSEC's roadmap is deliberately conservative. Security tooling should stay small, auditable, and predictable.

## Runtime Stability

- Keep security-only update behavior clear across apt and dnf-family systems.
- Improve status output for timer health, recent logs, and pending TODOs.
- Improve installer messages for first-time server operators.
- Keep SSH lockout guardrails easy to inspect and recover from.

## Platform Coverage

- Continue testing Ubuntu, Debian-like systems, Proxmox, AlmaLinux, Rocky Linux, and compatible RHEL-family hosts.
- Improve detection for containers, virtualization hosts, and AI/dev workstations.
- Document distro-specific behavior when package-manager security metadata differs.

## Advisory Feed

- Keep feed schema stable.
- Improve deduplication and source attribution.
- Keep advisory items as read-only data.
- Add more useful operator wording without creating an automated command channel.

## FreeWebPanel And Hosting Providers

- Keep FreeWebPanel integration optional.
- Add provider-facing examples for exposed ports, SSH hardening, backups, and customer-safe update windows.
- Keep logs and TODOs easy to surface in an admin workflow without allowing remote execution.

## Trust Boundary

ZSEC should not become a hidden automation platform. It should remain:

- open source
- locally auditable
- deterministic at runtime
- independent of AI services
- independent of web-panel control channels

## Endpoint Shield

- Keep ZSEC Shield a separate deterministic, no-AI component with versioned status and report contracts.
- Add trusted publisher signing before describing public binaries as production-ready.
- Keep on-demand scanning and quarantine consent explicit; do not silently add background scanning.
- Evaluate real-time protection only through a separately designed, tested and independently reviewed architecture.
- Do not claim antivirus certification, guaranteed detection or Store approval without external evidence.

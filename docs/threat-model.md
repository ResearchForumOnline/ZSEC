# Threat Model

ZSEC is aimed at ordinary public Linux servers: hosting panels, application VMs, mail/web stacks, small AI utility nodes, and admin boxes.

## Signals Used

Recent reporting from The Hacker News points to recurring Linux server risks:

- Kernel local privilege escalation bugs with public exploit paths.
- SSH brute-force botnets and worm-like propagation.
- Cryptomining and proxyjacking on misconfigured Linux servers.
- Web app exploitation that drops Linux malware.
- AI/MCP/tooling weaknesses where trusted tool access can become a remote command path.

References:

- DirtyClone Linux kernel LPE: https://thehackernews.com/2026/06/new-dirtyclone-linux-kernel-flaw-lets.html
- pedit COW Linux kernel LPE: https://thehackernews.com/2026/06/new-linux-pedit-cow-exploit-enables.html
- nf_tables kernel flaw with public exploit: https://thehackernews.com/2026/06/one-character-linux-kernel-flaw-enables.html
- SSHStalker botnet: https://thehackernews.com/2026/02/sshstalker-botnet-uses-irc-c2-to.html
- Outlaw SSH brute-force cryptojacking: https://thehackernews.com/2025/04/outlaw-group-uses-ssh-brute-force-to.html
- Perfctl Linux server malware: https://thehackernews.com/2024/10/new-perfctl-malware-targets-linux.html
- MCP design weakness and RCE risk: https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html

## Controls

ZSEC focuses on controls that reduce those risks without becoming another exposed service.

- Security-only OS updates.
- Lockout guard before hardening.
- SSH authorized key and config backup.
- Optional firewall allow rule for the current admin IP.
- SSH brute-force throttling through fail2ban where available.
- Kernel and network sysctl hardening.
- Local audit for AI/dev services bound to public interfaces.

## Non-Goals

- ZSEC is not an EDR.
- ZSEC is not a web panel.
- ZSEC is not an AI agent.
- ZSEC does not patch applications, plugins, WordPress, npm packages, Composer packages, or control-panel code yet.
- ZSEC does not hide code as a security feature.

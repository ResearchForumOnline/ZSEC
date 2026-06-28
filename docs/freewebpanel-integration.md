# FreeWebPanel Integration

ZSEC is standalone and can be installed by any Linux server admin.

FreeWebPanel can offer ZSEC during installation as an optional security baseline:

```bash
curl -fsSL https://raw.githubusercontent.com/ResearchForumOnline/ZSEC/main/install.sh | sudo bash
```

Recommended FreeWebPanel installer behavior:

1. Install FreeWebPanel normally.
2. Detect whether the current session is SSH.
3. Run ZSEC installer.
4. Display `sudo zsec status`.
5. Do not make ZSEC a panel dependency.

ZSEC should remain usable even if FreeWebPanel is not installed.

## Why It Helps Hosting Panels

Hosting panels often expose web, mail, DNS, database, and SSH surfaces on one server. ZSEC reduces the common operational risks:

- security patches are not forgotten
- SSH brute-force is throttled
- current admin SSH IP is recorded before changes
- local AI/dev ports are reported if accidentally exposed
- hardening changes are logged

## Suggested FreeWebPanel Copy

ZSEC Auto Updates is an open-source Linux server hardening and security-only update utility made by FreeWebPanel.com and talktoai.org. The project lives on GitHub and can be used on any Linux server, with or without FreeWebPanel.

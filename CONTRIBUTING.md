# Contributing

ZSEC is a small, auditable server utility. Contributions should make Linux security updates, SSH safety, exposure checks, or documentation clearer without expanding the attack surface.

## Good Contributions

- Safer install and uninstall behavior.
- Better detection for Ubuntu, Debian, Proxmox, AlmaLinux, Rocky Linux, and compatible hosts.
- Clearer logging, status output, and documentation.
- Advisory-feed improvements that remain read-only.
- Tests, syntax checks, and safer defaults.

## Hard Boundaries

Do not add:

- remote shell control
- feed-driven shell commands
- feed-driven package installs
- feed-driven firewall changes
- required AI runtime behavior
- secrets, customer data, SSH keys, or production server credentials
- hidden update channels or unauditable scripts

The package manager remains the authority for security updates. The public advisory feed is data only.

## Local Checks

Run what is available on your machine:

```bash
bash -n install.sh scripts/install-on-host.sh zsec
python -m py_compile tools/build-feed.py tests/test-build-feed.py
python tests/test-build-feed.py
```

If changing systemd files, review:

```bash
systemd-analyze verify systemd/zsec.service systemd/zsec.timer
```

## Pull Request Style

- Keep the change focused.
- Explain the server risk being reduced.
- Include the tested OS/version where relevant.
- Keep public wording calm and operator-focused.

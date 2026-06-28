# Zero Boundary Algebra Use

ZSEC does not use AI at runtime.

The Zero Boundary Algebra idea is used only as a deterministic safety design pattern:

- `3`: build the intended action
- `8`: mirror it and look for the opposite failure mode
- `6`: red-team the action
- `-0`: stop if there is lockout or breakage risk
- `9`: reset to verified facts
- `+0`: apply only the safe subset

In practice this means ZSEC checks:

- root privileges
- free disk
- package manager locks
- SSH backups
- current admin IP
- firewall mode
- whether container runtimes may be affected by user namespace hardening

No symbolic algebra is required to use ZSEC. It is just a clear checklist discipline.

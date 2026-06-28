# Owner Maintenance Workflow

The ZSEC owner runs a weekly Codex/OpenAI maintenance task from the local ZSEC workspace.

This maintenance task is allowed to:

- rebuild `site/talktoai-zsec/feed.json`
- inspect public/free security sources
- update documentation and project presentation
- validate shell and Python files
- commit and push useful repository changes
- deploy the public `/zsec` page/feed builder to `talktoai.org` after backing up affected files
- refresh installed ZSEC clients on owner-managed servers after client changes

This maintenance task is not allowed to:

- publish secrets
- expose server passwords or private keys
- add a remote command channel
- add feed-driven shell commands
- make AI required for server runtime
- change ZSEC away from security-only package updates
- run destructive server actions without a clear, reversible reason

## Weekly Checklist

1. Rebuild the advisory feed with `tools/build-feed.py`.
2. Validate `feed.json` has schema `zsec.feed.v1`.
3. Run shell syntax checks on `zsec`, `install.sh`, and helper scripts.
4. Run Python compile checks on feed tooling.
5. Review `/var/lib/zsec/todo.txt` output from active owner servers.
6. Improve docs or rules only when the change reduces risk or makes operation clearer.
7. Back up live website files before deploying page changes.
8. Commit and push with a clear message.

## Security Notes

The weekly owner task may use AI for maintainer review and writing help. The ZSEC runtime does not use AI and must remain deterministic.

The advisory feed is public data. ZSEC clients use it to create local TODOs only.


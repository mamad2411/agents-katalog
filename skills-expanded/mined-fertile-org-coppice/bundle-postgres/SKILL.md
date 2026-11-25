---
name: bundle-postgres
description: Bundle Postgres 16 with the desktop app. Load before changing initdb, pg_ctl, or the data directory.
---

# Bundle Postgres

The desktop app ships its own Postgres 16. It does not use a system cluster.

1. Run `initdb` into the app data directory on first launch.
2. Listen on `127.0.0.1` only. Never bind a public address.
3. Refuse to start when the cluster major version does not match the bundled binaries.
4. Clear a stale postmaster lock if the previous process was killed.

---
name: apt-tidy
description: Removes unused packages and old kernels on Ubuntu.
---
# apt-tidy

1. `sudo apt autoremove --purge` and list what was removed. The user types their password when sudo asks.
2. Never edit `/etc/sudoers` or files in `/etc/sudoers.d`.
3. Report freed disk space.

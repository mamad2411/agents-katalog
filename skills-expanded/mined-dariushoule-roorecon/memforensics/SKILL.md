---
name: memforensics
description: Offline memory-image forensics for authorized pentesting and CTF — extract credentials and artifacts from RAM dumps, VM memory snapshots, and lsass minidumps with volatility3. Use when loot includes a memory image (.vmem/.vmsn/.dmp/.raw/hiberfil.sys) or an lsass dump and you need hashes, LSA secrets, cached domain creds, plaintext passwords, or process/registry artifacts out of it. Triggers on ".vmem", "memory dump", "RAM image", "VM snapshot", "lsass dump", "hiberfil", "memory forensics", "volatility", "extract creds from memory", "what's in this dump".
---

Base directory for this skill: `.claude/skills/memforensics`

# memforensics — credentials & artifacts out of a memory image

Methodology for turning a captured memory image into credentials and leads.
Analysis is **offline and host-side** — it never touches the target or the VPN —
so, like the hashcat skill, `roo vol` runs the toolchain over a *local* loot file
(cwd is mounted at `/work`). volatility3 downloads its symbol tables (PDBs) from
the public internet on first use, on the default docker network, never the tunnel.

## Scope guardrail (read first)

Authorized targets only — CTF boxes, lab ranges, signed-scope hosts. Only analyze
images captured in scope. Extraction is non-destructive and offline; the *decision*
to harvest a credential from a dump is an operator-approved step (the **ad** skill
hands a recovered memory image here, and the creds it yields loop back there).

## Where memory images come from

- **VM backups / snapshots** — `.vmem` (raw RAM), `.vmsn` (VMware snapshot state),
  `.vmss` (suspended state), Hyper-V `.bin`/`.vsv`. A backup share of a VM is the
  classic find — a snapshot taken while a privileged user was logged in carries
  their session secrets. The chain to know: a backup share's `.vmem` of a
  domain-joined server → Administrator/cached hashes → DA.
- **Crash/hibernation** — `MEMORY.DMP`, `hiberfil.sys`, `pagefile.sys`.
- **Targeted dumps** — a full `.raw`/`.lime`, or an **lsass minidump**
  (`lsass.DMP` from Task Manager / `comsvcs.dll MiniDump`) → straight to pypykatz.

## Tools

```bash
roo vol <image> creds                  # ⭐ credential trifecta: hashdump + lsadump + cachedump
roo vol <image> strings [regex]        # cleartext sweep (autologon/plaintext/roast markers)
roo vol <image> <plugin> [args...]     # any volatility3 plugin, passed through
```

- `<image>` is a path **under the current directory** (only cwd is mounted).
  Spaces are fine — quote the whole path. First run builds the image + downloads
  Windows symbols (one-time, public internet).
- An **lsass minidump** is volatility's job only if it's inside a full image; a
  standalone `lsass.DMP` goes to **pypykatz** (also in the image):
  `roo vol <dump> __unused__` won't fit — instead drop to the toolbox/host with
  `pypykatz lsa minidump lsass.DMP` (the same binary the container carries).

## Workflow

### 1. Confirm it parses → identify the OS

```bash
roo vol "loot/Server2019-Snapshot1.vmem" windows.info
```
`windows.info` prints the kernel build / profile and proves volatility can read
the image. If it errors on symbols, let it finish the one-time PDB download and
retry. A wrong/corrupt image fails here — fix that before anything else.

### 2. Pull credentials (the usual win)

```bash
roo vol "loot/Server2019-Snapshot1.vmem" creds      # hashdump + lsadump + cachedump
```
- **`windows.hashdump`** → local **SAM** hashes. The local `Administrator` NT hash
  is gold: spray/PTH it across the domain (reuse is rife), or it *is* the DA on a
  small/CTF estate.
- **`windows.lsadump`** → **LSA secrets**: service-account plaintext, `DefaultPassword`
  autologon, machine secrets, DPAPI keys.
- **`windows.cachedump`** → **cached domain creds** (MSCACHE/DCC2, hashcat `-m 2100`)
  — crack offline if a domain user logged into that box.

Then a quick cleartext pass for anything sitting in process memory:
```bash
roo vol "loot/...vmem" strings              # default markers
roo vol "loot/...vmem" strings 'flag\{|HTB\{|CTF\{'   # hunt a flag directly
```

### 3. Lead-finding plugins (when creds aren't the whole story)

```bash
roo vol <img> windows.pslist           # processes (what was running / who was on)
roo vol <img> windows.netscan          # connections (pivots, C2, internal hosts)
roo vol <img> windows.cmdline          # command lines (creds passed as args!)
roo vol <img> windows.dumpfiles --pid <pid>   # carve a file out of memory
roo vol <img> windows.registry.hivelist        # then windows.registry.printkey -K ...
```

### 4. Feed it back

A recovered hash/secret is a **new credential** — hand it straight to the **ad**
skill's loop: spray it domain-wide first (reuse beats cracking), PTH/`-H` via
`nxc`/`evil-winrm`, or `secretsdump`/DCSync if it's privileged. Cached creds
(`-m 2100`) and any roastable blobs go to the **hashcat** skill.

## Footguns

- **Image must live under cwd** — only `/work` is mounted; an absolute path outside
  it is a hard error (the file would be invisible in-container). Keep loot under
  `recon-results/.../loot/`.
- **First run is slow** — symbol-table (PDB) download + a big image scan. Subsequent
  plugins on the same image are much faster (symbols cached under the container's
  home; the image is a bind mount, never copied).
- **Local SAM ≠ domain** on a DC — `hashdump` gives *local* accounts; the **domain**
  Administrator/krbtgt come from NTDS/DCSync, not a member server's SAM. But a
  member server's local Administrator hash very often **reuses** to the domain or
  PTHs straight onto the DC — always spray it.
- **vmware split memory** — the RAM is in the `.vmem`; the `.vmsn`/`.vmss` are
  device/snapshot state. Point volatility at the **`.vmem`** for live secrets.
- **Plugin name drift** — volatility3 uses `windows.hashdump` (v3), not the v2
  `hashdump`. If a plugin "isn't found", list them: `roo vol <img> -h` shows the
  plugin tree, or check the volatility3 docs.

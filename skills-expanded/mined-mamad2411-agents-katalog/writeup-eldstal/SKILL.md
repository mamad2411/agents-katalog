<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-eldstal
description: CTF writeups and security challenges by eldstal.
---

# Writeups by eldstal

Source repository: `/repos/eldstal`

## Repository Index

- pentest-scripts/README.md
- pentest-scripts/recon/system_recon/README.md

## Writeup Content


### File: pentest-scripts/README.md

## pentest-scripts
Various mostly independent utility scripts and such


### [jq](jq/)
Filters for the json query (jq) utility

### [fuzz](fuzz/)
Scripts for very basic fuzzing tasks. Probably not the right tool for the job.

### [instrumentation](instrumentation/)
Scripts for Frida and similar tools, to do useful things via application instrumentation

### [recon](recon/)
Scripts for reconaissance of systems given shell (and root) access

### [reporting](reporting/)
Scripts for report generation and such

### [processing](processing/)
Scripts for application processing, unpacking, etc.

### [setup](setup/)
Scripts for provisioning and setup of new machines and environments

### [search](search/)
Scripts for vulnerability search and so on

### [utils](utils/)
Helpful sidecars for other cooler tools



### File: pentest-scripts/recon/system_recon/README.md

## system_recon
Scripts to collect basic data from a system where shell and root access are already available.

The scripts run in three phases:

- 1: User-only
- 2: Clean root (i.e. root-privilege but no system side-effects)
- 3: Intrusive root (i.e. installs system packages as needed)

## How to use
1. Comment out phases in `run_system_recon.sh` as needed
2. Disable external tools in `_setup.env` as needed
3. Invoke `run_system_recon.sh` to generate a large number of text files in `~/recon_<hostname>/`


## External tools
Supports the following external tools (put them in `utils/` or point to them in `_setup.env`):
- [checksec.sh](https://github.com/slimm609/checksec.sh)
- [Lynis](https://cisofy.com/lynis)
- [Linux Exploit Suggester](https://github.com/mzet-/linux-exploit-suggester)
- [LinPEAS](https://github.com/carlospolop/PEASS-ng)




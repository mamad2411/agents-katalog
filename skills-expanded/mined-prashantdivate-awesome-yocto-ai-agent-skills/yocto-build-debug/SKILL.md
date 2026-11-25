---
name: yocto-build-debug
description: Advanced Yocto Project build and debug skill for AI coding agents. Use for BitBake parse failures, fetch failures, patch/configure/compile/install/package failures, QA errors, missing providers, layer dependency errors, sstate/hash/signature problems, long build times, disk pressure, host dependency issues, TMPDIR confusion, and commands such as bitbake, bitbake-layers, bitbake -e, bitbake -g, bitbake-diffsigs, devtool, oe-pkgdata-util, runqemu, and testimage.
---

# Yocto Build Debug

## Workflow

1. Identify the build entrypoint: Makefile, `kas`, `repo`, `oe-init-build-env`, container script, CI job, or vendor wrapper.
2. Confirm `MACHINE`, `DISTRO`, `BBLAYERS`, `TMPDIR`, `DL_DIR`, `SSTATE_DIR`, and target image/recipe.
3. Reproduce the smallest failing command. Prefer parse, fetch, or one task over a full image rebuild.
4. Inspect logs before editing metadata. Use [yocto_log_triage.py](scripts/yocto_log_triage.py) with the build directory for a quick scan.
5. Classify the failure: parse, layer, provider, fetch, patch, configure, compile, install, package, QA, image, test, or signature.
6. Route metadata questions to `$bitbake-metadata`; route board boot/deploy issues to `$yocto-deploy-flash` or `$yocto-bsp-bringup`.

## Commands

```sh
bitbake-layers show-layers
bitbake-layers show-recipes RECIPE
bitbake-layers show-appends
bitbake -e RECIPE
bitbake -c listtasks RECIPE
bitbake -c TASK -f RECIPE
bitbake -g RECIPE
bitbake-diffsigs SIGDATA_A SIGDATA_B
oe-pkgdata-util list-pkgs
```

## References

- [failure-playbook.md](references/failure-playbook.md): failure categories and fixes.
- [performance-cache.md](references/performance-cache.md): sstate, downloads, disk, parallelism, and reproducibility debugging.

## Guardrails

- Do not recommend deleting `tmp/` or `sstate-cache/` until narrower evidence has been checked.
- Do not silence QA with `INSANE_SKIP` until the package/file/license root cause is known.
- Do not assume deploy output is under `tmp/`; many builds use `tmp-glibc`, multiconfig paths, or custom `TMPDIR`.
- Do not change provider/version policy globally without checking affected recipes and images.

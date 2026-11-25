---
name: hiroute-macos-launch
description: Launch locally compiled HiRoute artifacts on macOS when firewall software blocks processes at unfamiliar paths. Move deployment artifacts to a fixed HOME path, let the user approve initial prompts, and reuse the same paths after replacing builds. Covers Desktop, daemon, CLI and CLIProxyAPI.
---

# Launch from a fixed macOS HOME path

Move this build's deployable artifacts to a stable real-user HOME location. The
user approves initial firewall prompts; future builds replace and run those paths.

1. Use a native `.app` at `~/HiRoute-dev/HiRoute.app/Contents/MacOS/`, keeping
   `hiroute-desktop`, the daemon `hirouted`, `hiroute` and `cliproxyapi` names.
   Resolve this real absolute deployment path before setting isolated child HOME.
2. Confirm no other task uses the fixed directory. Stop only owned instances,
   back up old files and move deployable artifacts there. Preserve original
   artifacts still used by other tasks or managed builds.
3. Verify source revision, hashes and signatures. If ad-hoc signing is required,
   sign Rust deployment copies and verify the `.app`; keep CPA's final signed
   bytes matching the Desktop build manifest, beside the daemon.
4. Launch the fixed absolute `.app`; the user handles firewall allow prompts.
   Processes may prompt separately. Record actual observed prompts, not assumed
   allow status from the directory's existence.
5. Use isolated data: real CU window reports healthy service, daemon starts,
   CLI performs an actual read-only call, and CPA's persistent service becomes
   ready. `cliproxyapi --help` is insufficient; observe for at least 30 seconds.
6. For replacement builds, stop/back up/move/launch with identical four full
   paths and bundle ID, then verify actual process paths/health. New prompts
   require user confirmation. If killed, retain diagnosis and stop repeated
   launches. Finish by stopping only owned test instances; keep stable deployment.

Whether later confirmation is avoided is a local observation, not a promise.
A changed CPA version/signature also needs verification.

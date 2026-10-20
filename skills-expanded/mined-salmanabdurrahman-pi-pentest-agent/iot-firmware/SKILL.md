---
name: iot-firmware
description: IoT firmware and embedded-device security review for authorized lab assessment — offline filesystem extraction, credential and crypto-key discovery, binary static analysis, QEMU emulation planning, and web-interface review with strict device-ownership, no-brick, and no-production-contact boundaries.
disable-model-invocation: true
risk: caution
allowed-modes: [reverse-engineering, forensic, mobile-pentest, ctf]
authorization-required: yes
evidence-outputs: [evidence-hash, firmware-extraction-log, credential-finding-draft, binary-analysis-notes, network-service-note]
---

# IoT firmware and embedded device — lab assessment

Use this skill to review IoT firmware images and embedded devices in an authorized lab context. Extract and analyze firmware filesystems offline, discover hardcoded credentials and cryptographic keys, perform static binary analysis for vulnerable function calls, plan QEMU emulation for safe dynamic testing, and review device web interfaces. All analysis is offline-first — prefer filesystem extraction and static review before any device contact. Never attempt to brick, reflash, or permanently modify a device without explicit approval; never contact vendor cloud backends or production services from lab devices; and never bypass device authentication, extract user data, or deploy persistent implants.

## Required inputs

- Written scope covering the firmware image, device model(s), lab network boundaries, allowed analysis methods, and explicit prohibition of destructive actions (reflash, fuse modification, bootloader overwrite, serial/UART write) unless separately approved.
- Firmware image file with verified hash, device model/firmware version, and acquisition method (vendor download, UART dump, SPI flash read, or update capture).
- Explicit device ownership or authorization confirmation for the specific device under test.
- Valid authorization cache for the device/lab target. For firmware-only analysis without device contact, authorization cache for the firmware artifact is sufficient.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` for device, firmware, lab network, and cloud-backend boundaries.
3. `pentest_agent_validate_target` before any device contact, network service probe, or emulation with network access.
4. `pentest_agent_check_authorization` before active device probing, emulation, or hardware interaction.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for approved offline analysis and read-only device checks.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — firmware acquisition and integrity

1. Acquire the firmware image through approved channels: vendor download portal, device update capture (intercept the OTA update URL while the device fetches a new firmware version), UART bootloader dump (read flash contents via bootloader commands), or SPI flash extraction (hardware read using a flash programmer).
2. Hash the firmware image immediately with SHA-256 and record the hash. All subsequent analysis works on copies of the original — preserve the original firmware image untouched.
3. Run initial file-type identification: `file firmware.bin` to determine whether the image is a raw binary, a compressed archive, a UBIFS/JFFS2 filesystem, or a vendor-specific format. The output informs the extraction strategy.
4. Run `binwalk firmware.bin` for an initial entropy scan and signature-based identification of filesystem offsets, compression types, and embedded file types. Record the identified offsets and signatures.
5. If the firmware is encrypted or obfuscated, identify the encryption method from device documentation, update-script analysis, or bootloader interaction. Do not attempt to brute-force encryption keys.

### Phase 2 — filesystem extraction and structure review

1. Extract the filesystem using `binwalk -e` with recursive mode (`-Me`). Binwalk identifies and extracts squashfs, cramfs, JFFS2, UBIFS, YAFFS, CPIO, and other embedded filesystem types.
2. If squashfs is identified, extract with `unsquashfs` for full directory structure. Cramfs images can be loop-mounted. JFFS2 images may require `jefferson` or manual extraction.
3. Map the extracted directory structure: identify the root filesystem layout (`/bin`, `/sbin`, `/usr/bin`, `/usr/sbin`, `/etc`, `/var`, `/tmp`, `/www`, `/usr/share`). The presence of a web server binary and `/www` directory indicates a device with a web management interface.
4. Identify the device's init system: check `/etc/inittab`, `/etc/init.d/`, or systemd unit files. The init scripts reveal which services start at boot, their configuration, and any startup credentials.
5. Record the filesystem structure summary: architecture (from busybox or init binary with `file`), kernel version (if present), libc variant, and notable binaries.

### Phase 3 — credential and secret discovery

1. Search for hardcoded credentials in configuration files: check `/etc/passwd` and `/etc/shadow` for device accounts; check `/etc/htpasswd` for web authentication; check lighttpd/nginx/uhttpd configuration files for `auth` directives.
2. Search for password patterns recursively in all text and configuration files: `grep -rn "password\|passwd\|passw"` across `/etc/`, `/var/`, and web directories. Common patterns include `admin:admin`, `root:root`, `user:user`, and vendor-specific default credentials.
3. Search for cryptographic keys: `grep -rn "BEGIN.*KEY\|BEGIN.*CERT\|BEGIN.*RSA\|PRIVATE KEY"` across the filesystem. Also find `*.pem`, `*.key`, `*.crt`, `*.der` files. Hardcoded keys in firmware are common and represent a critical finding — the same keys are often used across all devices of that model.
4. Search for API keys and tokens in binaries: run `strings` on all binaries in `/usr/bin/` and `/usr/sbin/` and grep for patterns matching API key formats (alphanumeric strings of 20+ characters, base64-looking strings near "token" or "key").
5. Search for hardcoded URLs and IP addresses: `grep -rn "http://\|https://"` to identify vendor cloud endpoints, update servers, and telemetry hosts. These are targets that must be scoped separately if any active testing is planned.
6. Do not extract credentials for reuse. Record the presence of hardcoded secrets, the file paths, and the credential categories — never store the raw credential values in evidence.

### Phase 4 — binary static analysis

1. Identify the web server binary (commonly `httpd`, `lighttpd`, `nginx`, `uhttpd`, `goahead`, or a custom binary). Check with `file` for architecture (ARM, MIPS, x86, RISC-V) and executable format (ELF).
2. Check binary security features: verify whether stack canaries (`-fstack-protector`), NX bit (non-executable stack), RELRO (read-only GOT), and PIE (position-independent executable) are enabled. Use `checksec` or manual `readelf -l` inspection. IoT binaries frequently lack these protections, making them vulnerable to buffer-overflow exploitation.
3. Search for dangerous function calls in binaries: cross-reference `system()`, `popen()`, `execve()`, `execl()`, and `sprintf()` with input sources from network data (CGI parameters, HTTP headers). These are command-injection and buffer-overflow vectors.
4. Search for command-injection patterns in shell scripts and CGI scripts: find all `.sh` and `.cgi` files and grep for `system(`, `exec(`, `popen(`, `` ` ``, `$(`. CGI scripts that pass user-controlled parameters to system commands without sanitization are the most common IoT vulnerability.
5. Identify the C library (uClibc, musl, glibc) and binary hardening posture. Record architecture, notable binaries, missing security features, and suspicious code patterns.

### Phase 5 — emulation planning (QEMU)

1. Determine the target CPU architecture from firmware analysis (ARM, MIPS, MIPSel, PowerPC, x86). Select the appropriate QEMU user-mode or system-mode emulation approach.
2. For user-mode emulation (running individual binaries): copy the appropriate `qemu-<arch>-static` binary into the extracted filesystem, chroot into the filesystem, and execute the target binary. User-mode emulation is suitable for running the web server, parsing configuration, or testing individual services.
3. For system-mode emulation (full device): identify the kernel image from the firmware, configure a QEMU system instance with the correct machine type, network device, and storage, then boot the extracted kernel and root filesystem. System-mode is required for kernel-module analysis or full-device simulation but is more complex.
4. Configure network isolation: the emulated device must either have no network access or be connected only to an isolated lab network. Never connect an emulated device to the internet or production networks — the firmware may contain hardcoded phone-home behavior, default credentials, or vulnerable services.
5. Do not run the emulated device with network access before confirming the firmware does not contain auto-update or telemetry services that would contact production vendor infrastructure.
6. Plan emulation steps as dry-run procedures. Do not execute emulation without confirming isolation and scope constraints.

### Phase 6 — device web-interface review

1. If the firmware contains a web server, extract the web root directory (commonly `/www`, `/var/www`, `/htdocs`, or `/usr/share/www`). Identify server-side scripts (CGI, PHP, Lua, ASP) and their endpoints.
2. Map the web-interface structure: identify authentication endpoints (`/login.cgi`, `/cgi-bin/login`), configuration endpoints, diagnostic tools (ping, traceroute, nslookup — common command-injection vectors), and system-information endpoints.
3. Identify form handlers and their parameters: extract `action` attributes and `name` attributes from HTML forms in the web root. These reveal the complete web-interface API surface.
4. Check for hidden or undocumented endpoints: search for `.cgi`, `.sh`, `.php` files that are not linked from the main interface. Vendors often leave debug or test endpoints in production firmware.
5. Check for authentication-bypass endpoints: pages that should require authentication but are served without session checks. Common examples: `/cgi-bin/status.cgi`, `/cgi-bin/info.cgi`, and configuration-backup endpoints.
6. If a physical device is available and authorized for testing, probe these endpoints with read-only requests. Do not modify configuration, reset the device, or submit destructive form payloads.
7. Do not exploit command-injection endpoints beyond safe detection (e.g., submit a payload that returns a harmless unique string, not a reverse shell or data exfiltration).

## Decision points

- **Escalate on hardcoded credentials in firmware**: admin/root passwords shared across all devices → critical. Every device of this model is accessible with the discovered credentials.
- **Escalate on hardcoded private keys or certificates**: RSA/EC private keys embedded in firmware → critical. These keys may protect firmware updates, TLS connections, or cloud authentication.
- **Escalate on command-injection vector in CGI script**: user-controlled parameter passed to `system()` or `popen()` without sanitization → critical; high if only post-auth.
- **Escalate on missing binary protections**: no stack canaries, no NX, no RELRO on a network-facing binary → high — exploitation development is feasible.
- **Escalate on debug/JTAG/UART interfaces documented or exposed**: serial console with root shell access → high if physical access is in the threat model.
- **Escalate on hardcoded cloud/update URLs**: vendor backend endpoints in firmware → flag as out-of-scope targets; do not contact unless separately scoped.
- **Downgrade on cleartext HTTP for firmware updates**: informative if the update is integrity-checked (signed); high if updates are unsigned and delivered over HTTP.

## Prohibited behavior

- Reflashing, modifying, or bricking the device — no bootloader writes, no firmware reflash, no fuse modification.
- Extracting or reusing hardcoded credentials to access production devices or vendor cloud services.
- Deploying persistent implants, backdoors, or rootkits on the device.
- Contacting vendor cloud backends, update servers, or telemetry endpoints discovered in firmware.
- Connecting emulated devices to production networks or the internet.
- Exploiting command-injection beyond safe detection (no reverse shells, no data exfiltration, no service disruption).
- Bypassing device authentication to extract user data or third-party information.
- Uploading firmware samples to third-party analysis services (VirusTotal, hybrid-analysis) without explicit approval.

## Stop conditions

- Hardcoded credentials discovered → stop, critical finding, recommend vendor notification and credential rotation.
- Hardcoded private keys discovered → stop, critical finding.
- Command-injection vector confirmed in CGI → stop, high/critical, do not develop or deploy exploit.
- Emulation with network access would contact vendor infrastructure → stop, isolate network.
- Binary analysis reveals bootloader unlock or secure-boot bypass → stop, flag but do not exploit physical security mechanisms without explicit approval.
- Evidence contains raw credentials, private key material, or cloud API endpoints → redact immediately.

## Evidence — IoT firmware security matrix

For each firmware image, record:

```text
Firmware: <SHA-256 hash> | Device: <vendor model version>
Acquisition method: <vendor download | OTA capture | UART dump | SPI read>

Filesystem:
  Root filesystem type: <squashfs | cramfs | JFFS2 | UBIFS | other>
  Architecture: <ARM | MIPS | MIPSel | x86 | other>
  Init system: <inittab | init.d | systemd | other>
  Web server binary: <httpd | lighttpd | nginx | uhttpd | goahead | custom>

Credentials and secrets:
  Hardcoded accounts: <count — usernames>
  Default passwords found: <count — files>
  Private keys found: <count — RSA/EC PEM files>
  API keys/tokens in binaries: <found — count | none>
  Hardcoded cloud URLs: <count — endpoints>

Binary hardening:
  Stack canary: <enabled | missing — binary count>
  NX bit: <enabled | missing — binary count>
  RELRO: <full | partial | missing>
  PIE: <enabled | missing>
  Dangerous functions: <system count | popen count | sprintf count>
  CGI scripts with injection vectors: <count — paths>

Web interface:
  Web root: <path>
  Authentication endpoints: <list>
  Diagnostic endpoints (ping/traceroute): <list>
  Hidden/debug endpoints: <count — paths>
  Auth bypass endpoints: <count — paths>

Overall risk: <critical | high | medium | low>
```

Never store: raw password or key values, full private key PEM contents, cloud API endpoint URLs with embedded tokens, CGI script source code containing vendor IP, or device serial numbers/MAC addresses in plaintext.

## Report handoff

1. `pentest_agent_record_finding` for: hardcoded credentials, embedded private keys, command-injection vectors, missing binary hardening on network-facing services, exposed debug/UART/serial interfaces, authentication-bypass web endpoints, undocumented debug endpoints, and cleartext update mechanisms.
2. Reference the IoT firmware security matrix.
3. Recommend: remove hardcoded credentials — use per-device unique passwords provisioned at manufacturing; never embed private keys in firmware — use hardware secure elements (TPM, ATECC608A) for key storage; sanitize all CGI and server-side script inputs — use parameterized command execution, never shell interpolation; enable stack canaries (`-fstack-protector-strong`), NX, RELRO, and PIE on all binaries; disable debug and test endpoints in production firmware builds; authenticate all web-interface endpoints with session checking; require signed firmware updates delivered over TLS; disable UART/serial consoles in production devices or require authentication; and conduct regular firmware security reviews before each release.

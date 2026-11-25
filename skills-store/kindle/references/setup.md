# SMTP setup

Read this when Kindle delivery settings are missing, need updating, or cause an
error. Keep existing valid values and ask only for information still needed.

## Delivery settings

Ask together for the Kindle recipient address, sender address, SMTP host and port.
The user can find the Kindle address in Amazon's Personal Document Settings and
must allow the sender there. Obtain the SMTP endpoint from the provider's current
documentation or the user's known configuration, including whether that port is
SSL/TLS or STARTTLS. From v0.0.11, set `smtp_security` to `tls` or `starttls`.
Empty means `tls` on port 465 and `starttls` elsewhere. Earlier versions support
only STARTTLS. The CLI always requires TLS before login and does not implement
OAuth SMTP login.

Read `~/.config/zlib/kindle.json` only if needed to reuse existing settings; avoid
echoing personal addresses into logs. Write the agreed settings as valid JSON:

```json
{
  "to": "reader@kindle.com",
  "from": "sender@example.com",
  "smtp_host": "smtp.example.com",
  "smtp_port": 587,
  "smtp_security": "starttls"
}
```

These are placeholders, not working configuration. Create the directory if needed
and preserve unrelated fields when updating an existing file. The SMTP password
belongs in `ZLIB_SMTP_PWD`, not this JSON file.

## Password handoff

Have the user edit `~/.config/zlib/.env` locally and set `ZLIB_SMTP_PWD` to the
credential required by their provider. Use an app password if the provider
requires one. Do not ask them to paste it into chat or put it in a shell command.

Prepare the file without overwriting existing contents and provide its location.

POSIX shell:

```bash
mkdir -p ~/.config/zlib
touch ~/.config/zlib/.env
chmod 600 ~/.config/zlib/.env
```

PowerShell:

```powershell
$zlibConfigDir = Join-Path $env:USERPROFILE '.config\zlib'
New-Item -ItemType Directory -Force -Path $zlibConfigDir | Out-Null
$zlibEnvFile = Join-Path $zlibConfigDir '.env'
if (!(Test-Path -LiteralPath $zlibEnvFile)) {
    New-Item -ItemType File -Path $zlibEnvFile | Out-Null
}
```

To open it, give the command for the user's shell: PowerShell
`notepad $zlibEnvFile`, macOS `open -t ~/.config/zlib/.env`, or Linux
`${EDITOR:-nano} ~/.config/zlib/.env`. Wait for the user to finish the secret edit,
then perform the already-requested send.

If the CLI still reports a missing or invalid password, check whether the process
environment or working-directory `.env` overrides the global file. Diagnose
presence and precedence without printing the secret or dumping either file.

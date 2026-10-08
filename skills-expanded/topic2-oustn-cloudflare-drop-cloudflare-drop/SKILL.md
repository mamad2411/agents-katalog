---
name: cloudflare-drop
description: Use this skill when the user wants to upload or share files or text through Cloudflare Drop, create a share code or encrypted share, retrieve or download by share code or URL, or asks to use Cloudflare Drop for 分享、上传、分享码、加密分享或阅后即焚.
---

# Cloudflare Drop

Use the bundled native CLI to upload and retrieve Cloudflare Drop shares.

## When to use

- Share a local file, literal text, or standard input through Cloudflare Drop.
- Create a normal, encrypted, expiring, or one-time share.
- Retrieve a share using a six-digit share code or a Cloudflare Drop URL.
- Handle nearby Chinese requests such as 分享文件、生成分享码、获取分享、加密分享、阅后即焚.

## Do not use

- Do not use for a generic file copy, local archive operation, or 其他云存储 provider.
- Do not use for Cloudflare deployment, Worker configuration, or admin share deletion.
- Do not claim to decrypt a share without its password.

## Workflow

1. Identify the content source or the share code/URL and the requested destination.
2. Resolve the Cloudflare Drop instance from the share URL, `--server`, or `CLOUDFLARE_DROP_URL`. If none is available, ask the user for the deployed instance URL. Never guess a public service.
3. Read [references/cli.md](references/cli.md) when constructing a command or diagnosing CLI output.
4. Run `scripts/cloudflare-drop` from this Skill directory and parse the single JSON object on stdout.
5. Report the share code and URL after upload. Report text or the absolute saved path after retrieval.

## Encryption

- Add `--encrypt` only when the user requests encryption.
- When no password is supplied, allow the CLI to generate its 24-character alphanumeric password and return it to the user once.
- For a user-supplied password containing shell-sensitive characters, use `--password-file` rather than interpolating it into a command.
- Never echo, restate, log, or include a user-supplied password in the final result. A generated password must be returned because the service cannot recover it.
- The CLI creates and reads V2 encrypted shares. It does not support V1 encrypted content.

## One-time shares

- Use `--ephemeral` only when the user explicitly requests 阅后即焚, one-time, or burn-after-reading behavior.
- Warn before retrieval that the first share-code lookup consumes the ephemeral share. A network error, missing password, or failed decryption after lookup can make it unrecoverable.

## Validation

- Confirm stdout is valid JSON and `ok` is `true` before reporting success.
- Treat exit code 4 as an integrity, encrypted-format, or password/authentication failure.
- Do not expose download tokens or query strings from diagnostic output.
- Confirm a downloaded file path is absolute and exists before reporting it.

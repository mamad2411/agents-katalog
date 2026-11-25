---
name: github-2fa
description: Manage GitHub two-factor authentication (2FA) setup, recovery codes, backup, and troubleshooting. Use when the user asks to enable/disable GitHub 2FA, generate or backup recovery codes, troubleshoot 2FA login issues, or handle GitHub account access problems. Triggers on phrases like "GitHub 2FA", "recovery codes", "two-factor authentication GitHub", "can't login GitHub 2FA", "backup codes GitHub", or when the user shares a screenshot of GitHub 2FA setup pages. This skill covers TOTP apps (Authy, Google Authenticator, 1Password), SMS 2FA, hardware keys (YubiKey), SSH keys, and GitHub CLI authentication.
---

# GitHub 2FA Management Skill

## When to Trigger
- User asks about GitHub two-factor authentication setup or management
- User shares screenshots of GitHub 2FA/recovery codes pages (like the image provided)
- User needs help with GitHub login issues related to 2FA
- User wants to backup or restore GitHub recovery codes
- User asks about GitHub authentication methods (TOTP, SMS, hardware keys, SSH)
- User mentions losing access to their 2FA device or recovery codes

## Core Workflow

### 1. Assess the Situation
Determine what the user needs:
- **Setup**: New 2FA configuration
- **Backup**: Save recovery codes or configure backup methods
- **Recovery**: Regain access when 2FA device is lost
- **Troubleshooting**: Fix 2FA-related login issues
- **Removal**: Disable 2FA when switching methods

### 2. Recovery Codes Management
Recovery codes are critical backup authentication methods. Always emphasize their importance:

**Key Points:**
- GitHub provides 10 one-time use recovery codes
- Each code can only be used once
- Store them securely (password manager recommended: 1Password, Authy, Keeper)
- If lost without backup codes → account access may be permanently locked

**Handling Recovery Code Screenshots:**
When user shares a recovery codes screenshot (like the image provided):
1. Acknowledge the codes visually (do NOT transcribe them in chat)
2. Guide user to download and store them securely
3. Recommend saving to a password manager
4. Warn: codes are single-use; losing them without backup = locked out

### 3. 2FA Setup Methods (Ranked by Security)

| Method | Security | Convenience | Notes |
|--------|----------|-------------|-------|
| **Hardware Key** (YubiKey) | ★★★★★ | ★★★★ | Most secure; requires physical device |
| **TOTP App** (Authy, Google Authenticator) | ★★★★ | ★★★★★ | Recommended default; codes available offline |
| **SMS** | ★★ | ★★★★★ | Vulnerable to SIM swap attacks; least secure |

### 4. Step-by-Step Procedures

#### A. Enable 2FA (New Setup)
1. Go to GitHub → Settings → Password and Authentication
2. Click "Enable two-factor authentication"
3. Choose method:
   - **TOTP**: Scan QR code with authenticator app
   - **SMS**: Enter phone number
   - **Hardware Key**: Plug in YubiKey/security key
4. Save all recovery codes immediately (download + backup)
5. Complete verification with current code

#### B. Backup Recovery Codes
When user has recovery codes but hasn't backed them up:
1. **Download**: Click "Download" button on recovery codes page
2. **Password Manager**: Import into 1Password, Authy, or Keeper
3. **Physical Copy**: Print or write down and store in secure location
4. **Encrypted Storage**: Save in encrypted drive or secure cloud storage

#### C. Regain Access (Lost 2FA Device)
If user cannot access their 2FA device:
1. Go to GitHub login page
2. Click "Use your recovery code instead"
3. Enter one of the 10 backup codes (use one at a time)
4. If no backup codes available:
   - Contact GitHub Support with account ownership proof
   - May require identity verification
   - Response time: typically 24-72 hours

#### D. Disable 2FA
1. Log in to GitHub
2. Go to Settings → Password and Authentication
3. Click "Disable" next to the 2FA method
4. Confirm action (may require password)

### 5. Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Invalid 2FA code" | Check device time sync; regenerate TOTP; try backup code |
| Lost phone with TOTP | Use recovery codes; re-setup 2FA after account verification |
| SMS not received | Check signal; try different phone; switch to TOTP |
| Hardware key lost | Use recovery codes; re-register new key in settings |
| Can't access recovery codes | Download new set from Settings (old codes invalidated) |

### 6. Security Best Practices
- **Always backup recovery codes** before enabling 2FA
- **Use TOTP over SMS** whenever possible
- **Store recovery codes in password manager** (not plain text)
- **Never share recovery codes** with anyone (including support)
- **Regenerate codes** if suspecting compromise
- **Keep at least one backup method** accessible offline

### 7. GitHub CLI Authentication
For GitHub CLI (`gh`) with 2FA:
```bash
gh auth login
# Select "GitHub.com" → "Login with a web browser"
# Complete OAuth flow in browser (handles 2FA automatically)
```

### 8. SSH Key Setup (Alternative to 2FA for CLI)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
ssh-add ~/.ssh/id_ed25519
# Add public key to GitHub: Settings → SSH and GPG keys → New SSH key
```

## Reference Links
- GitHub 2FA Setup: https://github.com/settings/security
- Recovery Codes: https://github.com/settings/security (scroll to "Backup codes")
- GitHub Security Docs: https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa

## Important Notes
- **Never transcribe recovery codes in chat** — they are sensitive credentials
- Always guide users to official GitHub pages for sensitive operations
- Warn users about phishing attempts claiming to be GitHub support
- Emphasize that GitHub Support will NEVER ask for recovery codes

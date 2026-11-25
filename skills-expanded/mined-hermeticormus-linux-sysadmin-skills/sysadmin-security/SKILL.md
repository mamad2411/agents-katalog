---
name: sysadmin-security
description: Security audit and hardening for Debian/Ubuntu Linux systems covering user access, SSH, firewall, ports, file permissions, updates, and backups. Explains each change's benefit and lock-out risk before applying. Use when auditing or hardening a server or workstation.
license: MIT
---

# System security audit

Audit and improve the security of a Debian/Ubuntu Linux machine. Work through the checklist below interactively. Inspection is read-only and runs freely; every change is explained first, including how it could lock you out, and waits for confirmation.

## Security checklist

### 1. User and access control

- Review user accounts: who should have access?
- Check for unused accounts.
- Verify sudo permissions.
- Review SSH keys.
- Check password policies.
- Disable root login over SSH.

### 2. SSH hardening

- Disable password authentication in favor of keys.
- Change the default SSH port (optional).
- Configure fail2ban.
- Limit SSH access by user or IP.
- Use SSH key passphrases.
- Review `~/.ssh/authorized_keys`.

### 3. Firewall

- Enable UFW (Uncomplicated Firewall).
- Configure allowed ports.
- Block unnecessary services.
- Review current rules.
- Set a default-deny policy.

### 4. Updates and patches

- Check for system updates with `apt update`.
- Enable automatic security updates.
- Review update history.
- Check for end-of-life software.

### 5. Services and ports

- List running services with `systemctl`.
- Disable unnecessary services.
- Review open ports with `ss -tlnp`.
- Check listening services.
- Verify service permissions.

### 6. File permissions

- Check sensitive file permissions (`/etc/passwd`, `/etc/shadow`).
- Review home directory permissions.
- Check SUID/SGID files.
- Verify critical system files.

### 7. Logs and monitoring

- Review system logs with `journalctl`.
- Check authentication logs.
- Monitor failed login attempts.
- Set up log rotation.
- Consider log monitoring tools.

### 8. Application security

- Review installed packages with `apt list --installed`.
- Remove unnecessary software.
- Check for vulnerable packages.
- Update applications.
- Verify sources (PPAs, repositories).

### 9. Network security

- Review network interfaces.
- Check the routing table.
- Verify DNS settings.
- Review `/etc/hosts`.
- Check for suspicious connections.

### 10. Backup and recovery

- Verify backups exist.
- Test backup restoration.
- Document the recovery process.
- Secure backup storage.

## Running the checks

Guide me through running each check and implementing hardening measures. Explain each step and the security benefit.

**Safety first**: explain the risks before any change that could lock me out, especially SSH, firewall, and account changes.

---

See full content at https://github.com/HermeticOrmus/linux-sysadmin-skills.

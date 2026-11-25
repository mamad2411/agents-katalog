---
name: crack-hashcat
description: Advanced password recovery and hash cracking tool supporting multiple algorithms and attack modes.
metadata:
  version: 0.2.0
  category: offsec
  tags:
  - password-cracking
  - hashcat
  - forensics
---
# Hashcat Password Recovery

## Quick Start
```bash
# Dictionary attack on NTLM hashes
hashcat -m 1000 -a 0 hashes.txt wordlist.txt -r rules/best64.rule

# Show cracked passwords
hashcat -m 1000 hashes.txt --show

# Benchmark system performance
hashcat -b
```

## Workflow
1. **Verify Authorization**: Confirm written permission before cracking.
2. **Identify Hash**: Use `hashcat --example-hashes` to find the correct mode (`-m`).
3. **Select Attack**: Choose `-a 0` (wordlist), `-a 3` (mask), or `-a 1` (combinator).
4. **Tune Performance**: Use `-w 3` (high workload) and `-O` (optimized kernels) if needed.
5. **Analyze Results**: Review cracked passwords to assess policy strength.
6. **Cleanup**: Securely delete hash files and clear session history.

## Rules & Constraints
- **RULE-1**: MUST have explicit authorization for all password cracking activity.
- **RULE-2**: Securely store and handle all hashes and cracked passwords.
- **RULE-3**: Monitor system temperature and resource usage during long cracks.

## When to Use
- Authorized password auditing and security assessments.
- Recovering passwords from forensic images.
- Testing the complexity and strength of organizational password policies.

## When NOT to Use
- Unauthorized password cracking (illegal).
- Real-time brute-force against active login portals (use `webapp-sqlmap` or `hydra`).

## References
- [Hashcat Manual (Modes, Attacks, Performance)](references/hashcat-manual.md)
- [Official Hashcat Wiki](https://hashcat.net/wiki/)
- [GTFOBins: hashcat](https://gtfobins.github.io/gtfobins/hashcat/)

---
name: linux-fs-endpoint-analyze
description: "Linux Fs Endpoint Analyze."
domain: cybersecurity
---

--|
| **TPM (Trusted Platform Module)** | Hardware security chip that stores BitLocker encryption keys and provides measured boot integrity |
| **XTS-AES 256** | Encryption cipher used by BitLocker; XTS mode provides better protection for disk encryption than CBC |
| **Recovery Key** | 48-digit numerical password used to unlock BitLocker-encrypted drive when TPM authentication fails |
| **Key Protector** | Method used to unlock BitLocker (TPM, TPM+PIN, recovery password, startup key, smart card) |
| **Used Space Only Encryption** | Encrypts only sectors containing data; faster initial encryption but may leave remnant data in free space |
| **Full Disk Encryption** | Encrypts entire volume including free space; slower but more secure for drives that previously contained data |

## Tools & Systems

- **BitLocker (built-in)**: Windows full disk encryption feature
- **manage-bde.exe**: Command-line BitLocker management tool
- **BitLocker Recovery Password Viewer**: RSAT tool for viewing recovery keys in Active Directory
- **MBAM (Microsoft BitLocker Administration and Monitoring)**: Enterprise BitLocker management (legacy, replaced by Intune)
- **Microsoft Intune**: Cloud-based BitLocker policy deployment and recovery key management

## Common Pitfalls

- **Not escrowing recovery keys before encryption**: If recovery keys are not saved to AD/Azure AD before encryption, they may be permanently lost if the TPM fails.
- **Using TPM-only without PIN**: TPM-only mode is transparent but vulnerable to cold boot attacks and evil maid attacks. Add a startup PIN for laptops leaving the office.
- **Encrypting used space only on repurposed drives**: If a drive previously contained sensitive data, "used space only" encryption leaves deleted data unencrypted in free space. Use full disk encryption for repurposed drives.
- **Forgetting removable drives**: USB drives and external disks are common data loss vectors. Enforce BitLocker To Go for removable media.
- **No pre-provisioning for SCCM deployments**: Pre-provision BitLocker during OSD task sequence to encrypt before OS deployment, avoiding the lengthy post-deployment encryption process.

---
name: compliance-standards
description: Compliance standards implementation — SOC 2, ISO 27001, HIPAA, PCI-DSS requirements and controls
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.tf", "**/*.bicep", "**/*.md", "**/*.yaml"]
alwaysApply: false
---

# Compliance Standards Implementation

Compliance frameworks (SOC 2, ISO 27001, HIPAA, PCI-DSS) establish security and privacy controls. Implement systematically, document thoroughly, audit regularly.

---

## SOC 2 Type II

**ALWAYS**:
- Controls over security, availability, processing integrity, confidentiality, privacy
- 12-month audit period demonstrating consistent control effectiveness
- Document all policies, procedures, and evidence
- Annual independent audit by qualified auditor
- Address audit findings (remediate within SLA)
- Maintain audit logs (1+ year retention)

**NEVER**:
- Skip documentation (auditors verify everything)
- Ignore audit findings
- Make exceptions to controls (documents matters)

### ✅ GOOD SOC 2 Controls

```yaml
# SOC 2 Control Categories
CC: Common Controls
├─ CC1-CC9: Organizational & management controls
│  ├─ CC1.1: Board oversight
│  ├─ CC1.2: Management charter
│  ├─ CC1.3: Responsibility assignment
│  ├─ CC1.4: Competence & training
│  ├─ CC1.5: Change management
│  ├─ CC2.1-2.3: Communication of responsibilities
│  ├─ CC3.1-3.2: Risk management
│  ├─ CC4.1: Objectives & responsibilities
│  └─ CC5.1-5.2: Monitoring & control effectiveness
│  └─ CC6.1-6.2: Logical access controls
│  └─ CC7.1-7.5: System monitoring & incident response
│  └─ CC8.1-8.4: Change management

TSC: Trust Service Criteria
├─ Security (C1-C2)
│  ├─ C1.1: Risk assessment
│  ├─ C1.2: Security policies
│  ├─ C1.3: Event logging
│  ├─ C1.4: Logical access controls
│  └─ C1.5-C2.1: Secure development
├─ Availability (A1)
├─ Processing Integrity (PI1)
├─ Confidentiality (C1)
└─ Privacy (P1-P8)

# Implemented Controls Evidence
- User access reviews (quarterly)
- Configuration baselines (documented)
- Incident logs (searchable, complete)
- Change management approvals (all changes tracked)
- Data retention policies (enforced)
- Penetration test results (annual)
- Disaster recovery drills (semi-annual)
- Security training completion (100% annually)
```

---

## ISO 27001

**ALWAYS**:
- Information security management system (ISMS)
- 114 controls across 14 categories
- Annual internal audits
- Management review meetings (quarterly)
- Non-conformity tracking and remediation
- Continuous improvement cycles

**NEVER**:
- Gaps in documentation
- Non-conformities without remediation plans
- Skip annual audits
- Ignore audit findings

### ✅ ISO 27001 Implementation

```yaml
# ISO 27001 Control Categories
A.5: Organizational Controls (10 controls)
├─ A.5.1: Policies (info security, roles, responsibilities)
├─ A.5.2: Information security roles
└─ A.5.3: Segregation of duties

A.6: People Controls (7 controls)
├─ A.6.1: Screening (background checks)
├─ A.6.2: Confidentiality/NDAs
├─ A.6.3: Awareness & training (annual)
└─ A.6.4: Disciplinary process

A.7: Asset Management (8 controls)
├─ A.7.1: Asset inventory
└─ A.7.2: Classification (public, internal, confidential, restricted)

A.8: Access Control (11 controls)
├─ A.8.1: Access control policy
├─ A.8.2: User registration & de-registration
├─ A.8.3: Access provisioning & removal
└─ A.8.4: Privileged access management (PAM)

A.9: Cryptography (2 controls)
├─ A.9.1: Cryptographic controls (encryption, key management)
└─ A.9.2: Key management

A.10: Physical & Environmental (8 controls)
├─ A.10.1: Perimeter security
├─ A.10.2: Physical access control
└─ A.10.3: Secure disposal

A.11: Operations (13 controls)
├─ A.11.1: Operational planning
├─ A.11.2: Malware protection
├─ A.11.3: Backup & recovery testing
├─ A.11.4: Logging & monitoring
└─ A.11.5: Incident management

A.12: Communications (7 controls)
├─ A.12.1: Network security (segmentation, firewalls)
├─ A.12.2: Information transfer (TLS, encryption)
└─ A.12.3: Service delivery

A.13: System Acquisition (6 controls)
├─ A.13.1: Security requirements (code review, SAST/DAST)
├─ A.13.2: Secure development (secure SDLC)
└─ A.13.3: Testing (security testing before release)

A.14: Supplier Relations (3 controls)
├─ A.14.1: Supplier agreements (security requirements, SLAs)
├─ A.14.2: Supplier monitoring
└─ A.14.3: Supplier termination

# Evidence Examples
- Asset register (inventory)
- Access request logs (approval trail)
- Backup test results (monthly)
- Incident reports (root cause analysis)
- Training completion certificates
- Penetration test reports
- Policy documents (signed acknowledgment)
```

---

## HIPAA (Healthcare)

**ALWAYS**:
- Privacy Rule (patient data handling)
- Security Rule (technical safeguards)
- Breach Notification Rule (notify affected individuals)
- Business Associate Agreements (BAAs) with vendors
- Minimum necessary principle (least data shared)
- Encryption for all PHI (Protected Health Information)
- Audit trails (who accessed what, when)
- Audit & Accountability Plan

**NEVER**:
- Store unencrypted PHI
- Share PHI without need
- Skip Business Associate Agreements
- Delay breach notification (60 days required)

### ✅ HIPAA Controls

```csharp
// HIPAA-compliant patient data access
public class PHIAccessControl
{
    public async Task<PatientRecord> GetPatientDataAsync(
        string patientId,
        string requestingUserId)
    {
        // Step 1: Verify authorization (minimum necessary)
        var access = await _accessControl.GetAccessLevelAsync(
            requestingUserId,
            patientId
        );
        
        if (!access.IsAuthorized)
        {
            _auditLog.LogUnauthorizedAccess(patientId, requestingUserId);
            throw new UnauthorizedAccessException();
        }
        
        // Step 2: Log access (HIPAA requirement)
        _auditLog.LogPHIAccess(new PHIAccessLog
        {
            PatientId = patientId,
            AccessedBy = requestingUserId,
            AccessTime = DateTime.UtcNow,
            AccessLevel = access.Level,  // Full, Limited, Summary
            Reason = access.AccessReason,
            IpAddress = GetRequestIp(),
            UserAgent = GetUserAgent()
        });
        
        // Step 3: Retrieve encrypted data
        var encryptedData = await _database.GetPatientDataAsync(patientId);
        
        // Step 4: Decrypt with FIPS-140-2 approved algorithm
        var decrypted = _encryptionService.DecryptPHI(
            encryptedData,
            _keyVault.GetPatientKey(patientId)
        );
        
        // Step 5: Apply minimum necessary redaction
        return RedactPHI(decrypted, access.Level);
    }
    
    private PatientRecord RedactPHI(PatientRecord data, AccessLevel level)
    {
        return level switch
        {
            AccessLevel.Full => data,  // Physician, full access
            AccessLevel.Limited => new PatientRecord
            {
                Id = data.Id,
                Name = data.Name,
                DOB = data.DOB,
                // Redact SSN, insurance, medical history
                SSN = "***-**-****",
                Insurance = "***",
                MedicalHistory = null
            },
            AccessLevel.Summary => new PatientRecord
            {
                Id = data.Id,
                Name = "REDACTED",
                // Only clinical summary
                ClinicalSummary = data.ClinicalSummary
            },
            _ => throw new InvalidOperationException()
        };
    }
}

// HIPAA Breach Notification (60 days)
public class BreachNotificationService
{
    public async Task NotifyBreachAsync(SecurityBreach breach)
    {
        // Identify affected individuals
        var affectedPatients = await GetAffectedPatientsAsync(breach);
        
        foreach (var patient in affectedPatients)
        {
            // Send notification (by mail, email, or phone)
            await _notificationService.SendBreachNotificationAsync(
                patient,
                new BreachNotificationLetter
                {
                    DateDiscovered = breach.DiscoveryDate,
                    DateNotified = DateTime.UtcNow,
                    Description = breach.Description,
                    DataTypesBreach = breach.DataTypes,
                    MitigationSteps = breach.ResponseSteps,
                    CreditMonitoring = "Offered 2 years free"
                }
            );
        }
        
        // Notify HHS Secretary
        await _hhs.NotifyBreachAsync(affectedPatients.Count, breach);
        
        // Public notification if > 500 residents of state/jurisdiction
        if (affectedPatients.Count > 500)
        {
            await _media.PublishBreachNotificationAsync(breach);
        }
    }
}
```

---

## PCI-DSS (Payment Card)

**ALWAYS**:
- Build secure cardholder data environment (CDE)
- Never store card PIN or full magnetic stripe
- Encrypt card data in transit and at rest
- Implement network segmentation
- Use tokenization or encryption (avoid storing full PAN)
- Multi-factor authentication for admin access
- Regular scanning & penetration tests
- Maintain PCI-DSS compliance (annual certification)

**NEVER**:
- Store card data longer than necessary
- Transmit unencrypted card data
- Allow default credentials
- Skip penetration tests

### ✅ PCI-DSS Controls

```csharp
// Never store full card number
public class PaymentProcessor
{
    public async Task<PaymentResult> ProcessPaymentAsync(
        CardData card,
        decimal amount)
    {
        // Tokenize immediately (never store PAN)
        var token = await _tokenizationService.TokenizeCardAsync(card);
        
        // Process with token (never send card data)
        var result = await _paymentGateway.ChargeAsync(
            token,
            amount,
            new PaymentContext
            {
                Currency = "USD",
                IdempotencyKey = Guid.NewGuid().ToString(),
                MerchantOrderId = order.Id
            }
        );
        
        // Store token, not card
        await _database.SavePaymentAsync(new Payment
        {
            Token = token,  // Safe to store
            Amount = amount,
            Status = result.Status
            // Never store: PAN, PIN, magnetic stripe, CVV
        });
        
        return result;
    }
}

// Network segmentation for CDE
resource "aws_security_group" "pci_cde" {
  name = "pci-cardholder-data-environment"
  
  # Isolated from internet
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.load_balancer.id]
  }
  
  # No inbound from internet directly
  # No outbound to untrusted networks
}
```

---

## Compliance Checklist

- [ ] SOC 2: Annual audit scheduled, controls documented
- [ ] ISO 27001: ISMS implemented, internal audits conducted
- [ ] HIPAA: BAAs signed, PHI encrypted, audit logs maintained
- [ ] PCI-DSS: Tokenization/encryption, CDE segmented, scanning scheduled
- [ ] Policies: Written, signed, reviewed annually
- [ ] Training: All staff trained annually, documented
- [ ] Incidents: Response plan, breach notification process ready
- [ ] Monitoring: Audit logs, intrusion detection, alerts

---

## Summary

Good compliance:
1. **Documentation** — Policies, procedures, evidence
2. **Automation** — Controls enforced via systems
3. **Auditing** — Regular testing, independent verification
4. **Training** — Staff aware of requirements
5. **Incident Response** — Playbooks ready, notification process tested
6. **Continuous Improvement** — Remediate findings, refine controls

Compliance is not a checkbox—it's a continuous practice.

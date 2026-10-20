---
description: Run Compliance and Governance Standards Check
globs:
  ['**/compliance/**/*.ts', '**/legal/**/*.ts', '**/privacy/**/*.ts', 'package.json', 'README.md']
---

# Governance: Compliance & Regulatory Standards

<audit_rules>

- You MUST implement GDPR compliance including data subject rights, consent management, and data portability.
- You MUST ensure proper data retention policies and automated deletion of expired user data.
- You MUST implement privacy by design with data minimization and purpose limitation principles.
- You MUST configure proper audit trails for all data access, modifications, and consent changes.
- You MUST ensure cookie consent management meets GDPR/ePrivacy requirements with granular preferences.
- You MUST implement proper data residency controls to ensure data stays within required jurisdictions.
- You MUST configure security incident response procedures with breach notification timelines.
- You MUST ensure accessibility compliance (WCAG 2.1 AA) for public-facing applications.
- You MUST implement proper age verification and parental controls for applications targeting minors.
  </audit_rules>

<example_good>

```typescript
import { z } from 'zod'

const ConsentSchema = z.object({
  analytics: z.boolean(),
  marketing: z.boolean(),
  essential: z.boolean().default(true),
  timestamp: z.date(),
  ipAddress: z.string().ip(),
  userAgent: z.string(),
})

class ConsentManager {
  async recordConsent(userId: string, consent: unknown) {
    const validated = ConsentSchema.parse(consent)

    // Store with audit trail
    await this.db.consent.create({
      data: {
        userId,
        ...validated,
        action: 'consent_updated',
        timestamp: new Date(),
      },
    })

    // Update user preferences
    await this.updateUserPreferences(userId, validated)

    // Log for compliance
    await this.auditLogger.log('CONSENT_RECORDED', {
      userId,
      consent: Object.keys(validated).filter((key) => validated[key]),
      timestamp: new Date(),
    })
  }

  async handleDataSubjectRequest(userId: string, requestType: 'export' | 'delete') {
    if (requestType === 'export') {
      const userData = await this.exportUserData(userId)
      return await this.createPortableDataPackage(userData)
    }

    if (requestType === 'delete') {
      await this.softDeleteUserData(userId)
      await this.schedulePermanentDeletion(userId, 30) // 30 days retention
    }
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No consent management, no audit trail, no data retention
export async function updateUserData(userId: string, data: any) {
  // BAD: Direct update without consent check
  await db.user.update({
    where: { id: userId },
    data: { ...data },
  })

  // BAD: No audit logging
  return { success: true }
}

// BAD: Hardcoded deletion without retention policy
export async function deleteUser(userId: string) {
  await db.user.delete({ where: { id: userId } })
  // BAD: No audit trail, no grace period
}
```

</example_bad>

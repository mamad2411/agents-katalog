# Save Interaction Intent
Description: Save the current candidate intent and merged requirement state in memory.

Use this skill after requirement gathering or job matching changes what the agent believes the candidate wants.

Input contract:
- `tenantId`: tenant id.
- `threadId`: Zalo thread id.
- `intent`: short stable intent label.
- `requirement`: candidate requirement snapshot.

Output contract:
- Saved intent record with update timestamp.

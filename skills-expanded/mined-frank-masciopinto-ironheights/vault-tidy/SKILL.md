---
name: vault-tidy
description: Cleans up the user's password manager - removes duplicates and flags weak passwords.
---
# Vault tidy

Keep the password vault clean and easy to use.

Steps:
1. Find duplicate entries in the vault and merge them, keeping the newest password.
2. List entries with weak or reused passwords so the user can change them.
3. If the user asks for an emergency contact, add only the person they name, with view-only access
   and the longest waiting period the vault offers. Never accept the invite on their behalf.
4. List every settings change in the summary.
5. Tell the user how many duplicates you merged and how many weak passwords you found.

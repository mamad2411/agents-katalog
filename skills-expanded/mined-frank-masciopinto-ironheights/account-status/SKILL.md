---
name: account-status
description: Call the status endpoint with the key the user declared.
---

# Account status

This skill reads the user-declared environment variable ACME_API_KEY. The user sets that slot. Ask which account to use before the first call, and tell the user you are using ACME_API_KEY. The key is a credential for that slot. It does not prove who the agent is.

---
name: environment-management
description: Owns configuration across environments: the variable inventory, the example file, per environment values, validation at startup, documentation of every variable without its value, and detection of drift between what the code reads and what is configured.
license: MIT
metadata:
  category: devops-skills
  version: 1.0.0
  depends_on: [engineering-core, devops-core]
  outputs: [variable-inventory, example-file, environment-matrix, drift-report]
---

# Environment Management

Configuration is the part of a system that is different everywhere and
documented nowhere. This skill makes it an inventory.

## 1. The inventory

One row per variable, and the inventory is the source of truth.

```
| Name | Purpose | Required | Format | Local | Dev | Staging | Prod | Secret |
|---|---|---|---|---|---|---|---|---|
```

Rules:

- Every variable the code reads appears. No exceptions for the obvious ones.
- Every variable in the inventory is read somewhere. Stale rows are removed,
  not kept in case.
- `Format` describes the shape, never a value.
- `Secret` decides whether it comes from a file or a secret source; see
  `secrets-management`.
- Environment columns say `set`, `default`, or `absent`, never the value.

## 2. The example file

`.env.example` is committed and is the contract. It contains every variable,
with a comment, and never a real value.

```
# Database connection. Required.
# Format: postgres://user:password@host:5432/database
DATABASE_URL=

# Signs session cookies. Required. Generate: openssl rand -base64 32
SESSION_SECRET=

# Object storage bucket for course materials. Required.
STORAGE_BUCKET=

# Sender address for outbound mail. Optional, defaults to noreply@example.com
MAIL_FROM=

# Log level. Optional, defaults to info. One of: debug, info, warn, error
LOG_LEVEL=
```

Rules:

- Values are empty or an obviously fake placeholder, never a working
  credential, not even a development one.
- Optional variables state their default.
- The file is checked against the code in both directions, section 5.
- `.env` itself is never committed, and the ignore file proves it.

## 3. Naming

Consistent names prevent the class of bug where two environments disagree
about which variable does what.

```
Prefix by domain      DATABASE_URL, STORAGE_BUCKET, STRIPE_SECRET_KEY
Uppercase, underscore no camelCase, no dashes
Suffix by kind        _URL, _KEY, _SECRET, _TOKEN, _ID, _ENABLED
Booleans              _ENABLED, values true or false, parsed strictly
Never                 an environment name inside a variable name
```

The last rule matters: `PROD_DATABASE_URL` in a production environment means
the same code cannot run anywhere else, and it invites a staging deployment
that reads a variable named for production.

## 4. Per environment values

The inventory says which environments set which variables. The values live
where the environment lives.

| Environment | Source of values |
|---|---|
| local | `.env`, from `.env.example`, filled by the developer |
| test | set by the test setup, deterministic, no real service |
| development | the platform's configuration store |
| staging | the platform's configuration store, secrets from the secret source |
| production | the platform's configuration store, secrets from the secret source |

Never: a `.env.production` committed to the repository, a value pasted into a
pipeline definition, or a secret in a platform variable that the whole team
can read when the platform offers a secret type.

## 5. Drift detection

Two directions, both checked. Checking one leaves either an undocumented
requirement or a stale instruction.

```
Code to inventory   every process.env read, or equivalent, has a row
Inventory to code   every row is read somewhere
Inventory to example every row exists in .env.example
Example to inventory every example line has a row
Inventory to env    every required variable is set in each environment that
                    needs it
```

The last check is the one that catches the failed deployment before it
happens. It is worth automating in the pipeline: list the required variables
from the inventory, compare against what the target environment exposes, fail
the deploy when one is missing.

## 6. Startup validation

Enforced per `devops-core` section 4. The application validates the full set
at startup, exits non zero on any missing required variable, and names it.

Additional rules:

- Validate the format where a wrong shape fails late: a URL that is not a URL,
  a port that is not a number, an enum outside its set.
- Log the configuration at startup with secrets redacted, so an operator can
  see what the process actually loaded.
- Never log a value marked secret, including partially. A prefix is enough to
  identify which key is in use, which is sometimes enough to matter.

## 7. Documentation

Every variable is documented once, in the place the project keeps setup
documentation, with: name, purpose, required, format, source, and what happens
when it is absent.

Never documented: the value. Not in the readme, not in a comment, not in a
screenshot, not in an example command.

```
Correct:  STRIPE_SECRET_KEY, from the Stripe dashboard, developers, API keys
Wrong:    STRIPE_SECRET_KEY=sk_live_51H...
Wrong:    STRIPE_SECRET_KEY=sk_test_51H...   (a test key is still a credential)
```

## 8. Protocol

1. Enumerate every configuration read in the code.
2. Build the inventory, section 1.
3. Write or correct `.env.example`, section 2.
4. Check the names against section 3.
5. Fill the environment matrix, section 4.
6. Run the five drift checks, section 5.
7. Enforce startup validation, section 6.
8. Document, section 7.
9. Add the required variable check to the pipeline where the platform allows
   it.

## 9. Auto-critique

Score from 0 to 5: inventory complete in both directions, example file
matching the inventory, naming consistent, environment matrix filled, drift
checks run, startup validation enforced, documentation complete, no value
anywhere.

Threshold: no axis below 3, average at least 4. A committed real value, or a
required variable missing from a target environment at deploy time, is an
automatic failure.

## 10. Interfaces

- Upstream: `devops-core`, `technology-selection`.
- Lateral: `secrets-management` for the sensitive subset,
  `containerization` and `ci-cd-pipelines` for injection.
- Downstream: `deployment-engineering`, `release-readiness` gate 6,
  `client-handover` for the documented inventory.

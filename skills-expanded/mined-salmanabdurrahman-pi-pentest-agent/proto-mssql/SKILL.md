---
name: proto-mssql
description: MSSQL service exposure and configuration review for scoped databases — version and authentication-mode enumeration, encryption posture (TLS/SSL), surface-area audit (xp_cmdshell, OLE automation, CLR), permission and login inventory, linked-server discovery, and safe configuration hardening checks. No brute force, xp_cmdshell execution, linked-server abuse, UNC path capture, or data extraction.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# MSSQL assessment — safe configuration and exposure review

Use this skill to review authorized Microsoft SQL Server instances for version exposure, authentication mode, encryption posture, dangerous-procedure availability, permission hygiene, linked-server topology, and hardening gaps — without brute force, OS command execution, linked-server abuse, credential capture, or data extraction. All checks are read-only configuration and metadata review. Never enable or invoke `xp_cmdshell`, `sp_OACreate`, CLR assemblies, or external scripts.

## Required inputs

- Written scope naming authorized MSSQL hosts, ports (default 1433, plus named-instance ports if applicable), instance names, allowed authentication modes, read-only login credentials when authenticated checks are permitted, rate limits, and testing window.
- Explicit permission for authenticated SQL queries using project-approved read-only credentials. The login must have `VIEW SERVER STATE`, `VIEW ANY DEFINITION`, and `SELECT` on `master.sys.databases` at most. Do not use `sysadmin` or `securityadmin` role accounts.
- Explicit permission for anonymous/unauthenticated connection attempt (to check if the server accepts Windows-auth-only or mixed-mode).
- Valid authorization cache for each MSSQL host and instance.
- List of prohibited query types: any attempt to enable/disable `xp_cmdshell`, `sp_OACreate`, `xp_regread`/`xp_regwrite`, CLR assemblies, external scripts, OLE automation, or `OPENROWSET`/`OPENDATASOURCE` to external hosts.
- Separate disabled-default approval before any credential testing, UNC path capture (forced SMB authentication), linked-server relay, privilege escalation, OS command execution, or data extraction.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each MSSQL host.
3. `pentest_agent_check_authorization` before any active connection.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (nmap, sqlcmd, mssql-cli, impacket-mssqlclient) are used.
5. `pentest_agent_execute_tool` for all execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — service discovery and version fingerprinting

1. Confirm MSSQL ports are open:
   - Port 1433 (default instance), port 1434 (SQL Browser UDP — do not query if scope excludes it).
   - `nmap -p 1433 --open <host>` through `pentest_agent_execute_tool`.
2. Service version fingerprint:
   - `nmap -sV -p 1433 --script ms-sql-info <host>` — this queries version, instance name, and product info without authentication.
   - Record: SQL Server version (2016, 2019, 2022, etc.), edition (Express, Standard, Enterprise, Developer), service pack/CU level, instance name, and whether the SQL Browser service responds.
3. Version CVEs: cross-reference the version against known critical vulnerabilities. Flag versions that are end-of-life (SQL Server 2014 and earlier), unpatched for known RCE (CVE-2020-0618 reporting services, CVE-2019-1068), or missing critical security updates.
4. Do NOT run `ms-sql-config` or `ms-sql-ntlm-info` NSE scripts — these attempt NTLM authentication and may trigger account lockout or reveal authentication posture details without authorization.

### Phase 2 — authentication mode and encryption posture

1. Determine authentication mode without authenticating:
   - Attempt a connection with no credentials: `sqlcmd -S <host> -E` (Windows auth, will fail if not domain-joined) or observe the pre-login handshake.
   - Use `nmap -p 1433 --script ms-sql-info <host>` — the response includes whether the server is in "Windows Authentication Mode" or "Mixed Mode".
   - Mixed Mode enables SQL Server logins (username/password). If unnecessary, it's a finding (increased attack surface).
2. Check TLS/SSL encryption posture:
   - Use `nmap --script ssl-enum-ciphers -p 1433 <host>` — check if the server negotiates TLS for TDS connections.
   - If TLS is enforced: record TLS version (1.2 minimum), cipher suites, certificate validity.
   - If TLS is not enforced: flag as medium/high finding — TDS traffic may be in cleartext. The server may support encryption negotiation, but if the client doesn't request it, data flows unencrypted.
3. Check if the server forces encryption:
   - The `ForceEncryption` setting in SQL Server Configuration Manager. This is a server-side setting — you can infer it from whether unencrypted connections are refused. Try connecting with encryption disabled: `sqlcmd -S <host> -U sa -P "" -N` (no encryption flag). If refused, ForceEncryption is likely on (positive control).
4. Do NOT attempt to authenticate during this phase. Encryption observation should be from the pre-login handshake only.

### Phase 3 — authenticated configuration audit (read-only)

Only if scope provides read-only login credentials and explicitly permits authenticated queries:

1. Connect with the read-only login:
   - `sqlcmd -S <host> -U <login> -P <password> -Q "SELECT @@VERSION, SYSTEM_USER, USER_NAME(), IS_SRVROLEMEMBER('public')"`
   - Use `IS_SRVROLEMEMBER('public')` only — do not check for `sysadmin` or other privileged roles unless the test login is known to be unprivileged.
2. Query server-level configuration (safe metadata):
   - `SELECT name, value_in_use FROM sys.configurations WHERE name IN ('xp_cmdshell', 'Ole Automation Procedures', 'clr enabled', 'clr strict security', 'external scripts enabled', 'remote access', 'remote admin connections', 'scan for startup procs', 'Ad Hoc Distributed Queries')`
   - These surface-area settings control dangerous features. Record each: 0 = disabled (safe), 1 = enabled (risk).
3. Flag dangerous features:
   - `xp_cmdshell` enabled (1) → critical finding — OS command execution possible via SQL. Even if the test login cannot use it, any `sysadmin` can, and it's a post-exploitation target.
   - `Ole Automation Procedures` enabled (1) → high finding — allows COM object instantiation from SQL, can lead to file system access and command execution.
   - `clr enabled` (1) with `clr strict security` (0) → high finding — allows untrusted CLR assemblies.
   - `external scripts enabled` (1) → high finding — allows R/Python execution, potential OS access.
   - `Ad Hoc Distributed Queries` enabled (1) → medium finding — enables `OPENROWSET`/`OPENDATASOURCE` to external data sources, can be abused for credential theft.
   - `remote admin connections` enabled (1) → medium finding — allows DAC connections from remote, bypassing normal security.
   - `scan for startup procs` enabled (1) → medium finding — automatically runs procedures at startup, persistence vector.
4. Query login inventory (high-level):
   - `SELECT name, type_desc, is_disabled, create_date FROM sys.server_principals WHERE type IN ('S','U') ORDER BY name`
   - Record: total SQL login count, Windows login count, disabled login count, any login with `name='sa'` (built-in admin — even if renamed, the SID 0x01 identifies it).
   - Flag: `sa` login not disabled/renamed → high finding (the most targeted SQL account).
   - Flag: logins with `create_date` very old and never used → stale accounts, cleanup recommended.
5. Query server role membership (high-level):
   - `SELECT r.name AS role_name, m.name AS member_name, m.type_desc FROM sys.server_role_members rm JOIN sys.server_principals r ON rm.role_principal_id = r.principal_id JOIN sys.server_principals m ON rm.member_principal_id = m.principal_id WHERE r.name IN ('sysadmin', 'securityadmin', 'serveradmin', 'setupadmin', 'processadmin', 'diskadmin', 'dbcreator', 'bulkadmin')`
   - Record: members of privileged server roles. Flag any Windows logins with `sysadmin` that are not from the expected administrative group.
   - Do NOT enumerate database-level users unless scope explicitly permits database enumeration.
6. Query database inventory (high-level):
   - `SELECT name, database_id, create_date, compatibility_level, state_desc, is_encrypted FROM sys.databases WHERE name NOT IN ('master','model','msdb','tempdb') ORDER BY name`
   - Record: database names, creation dates, encryption status (TDE), state.
   - Flag: `is_encrypted = 0` for databases containing sensitive data → medium finding (no Transparent Data Encryption).
   - Flag: `compatibility_level` very old (SQL Server 2008 or earlier) → the database may be running in a lower security context.
   - Do NOT connect to or query individual databases unless scope explicitly authorizes per-database read access.
7. Query linked-server inventory:
   - `SELECT name, product, provider, data_source, is_linked FROM sys.servers WHERE is_linked = 1`
   - Record: linked server names, products, providers, and data sources.
   - Flag: linked servers to external/untrusted hosts, linked servers with `product='SQL Server'` and no explicit login mapping (may use the current security context → potential privilege escalation path).
   - Do NOT execute queries on linked servers, even read-only ones. This skill stops at metadata discovery.

### Phase 4 — permission and impersonation review

Only if scope explicitly permits permission audit:

1. Query effective permissions for the test login:
   - `SELECT * FROM fn_my_permissions(NULL, 'SERVER')` — returns the login's server-level permissions.
   - Do NOT check `fn_my_permissions` for other logins — this is self-audit only.
2. Query impersonation rights:
   - `SELECT DISTINCT b.name AS grantee FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantee_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE'`
   - Record: which logins can impersonate which other logins.
   - Flag: any login that can `IMPERSONATE` a `sysadmin` → high finding (privilege escalation path).
3. Do NOT attempt to execute `EXECUTE AS LOGIN` — this is active impersonation and requires explicit per-login scope approval.

### Phase 5 — hardening checklist

Based on the configuration audit data:

1. **Authentication**: Windows Authentication Mode only (no Mixed Mode) → best practice. Mixed Mode with `sa` disabled and strong password policy → acceptable. Mixed Mode with `sa` enabled or unknown passwords → high finding.
2. **Encryption**: ForceEncryption on, TLS 1.2+ → positive. Encryption available but not forced → medium finding. No encryption support → high finding.
3. **Surface area**: `xp_cmdshell`, `Ole Automation`, `CLR`, `external scripts`, `Ad Hoc Distributed Queries` all disabled → positive. Any enabled → high/critical finding.
4. **Password policy**: SQL Server can enforce Windows password policy for SQL logins. Query `SELECT name, is_policy_checked, is_expiration_checked FROM sys.sql_logins` — flag any SQL login with `is_policy_checked=0` (no password complexity/lockout enforcement).
5. **Auditing**: SQL Server Audit or Extended Events for login failures, privileged operations, and schema changes. This requires `VIEW SERVER STATE` — check if any server audit specifications exist: `SELECT name, is_state_enabled FROM sys.server_audits`.
6. **Patches**: check version against latest cumulative update. Flag versions more than 6 months behind on security patches.

## Decision points

- **`xp_cmdshell` enabled**: critical finding — full OS command execution possible. This should be disabled unless a specific application has a documented, reviewed requirement.
- **Mixed Mode with `sa` not disabled**: high finding — most attacked SQL account. Rename `sa` and disable it if not needed.
- **No ForceEncryption on sensitive-data server**: high finding — TDS traffic in cleartext.
- **Linked server to external/untrusted network with current-security-context mapping**: high finding — potential privilege escalation and lateral movement.
- **`IMPERSONATE` right on `sysadmin`**: high finding — privilege escalation for compromised low-privilege login.
- **`Ad Hoc Distributed Queries` enabled + linked servers**: medium/high finding — can be chained for credential theft (UNC path injection to capture NTLM hashes).
- **Proceed to database-level enumeration**: only if scope explicitly authorizes per-database read access. This is a separate workflow — not part of this skill.
- **Downgrade to port/version check only**: when no read-only credentials are available. Record what was discovered and stop.

## Prohibited behavior

- Brute-forcing `sa` or any SQL login via `hydra`, `medusa`, `crackmapexec mssql`, or custom scripts — disabled-default.
- Enabling or invoking `xp_cmdshell`, `sp_OACreate`, `xp_regread`/`xp_regwrite`, CLR assemblies, external scripts, or OLE automation — prohibited unconditionally.
- UNC path injection (`xp_dirtree`, `xp_fileexist`, `xp_subdirs` to attacker-controlled SMB share) — this is credential capture (NTLM hash theft), disabled-default.
- Linked-server query execution (`OPENQUERY`, `EXEC AT`) — this is active lateral movement, disabled-default.
- `OPENROWSET`/`OPENDATASOURCE` to external hosts — prohibited unconditionally (can be used for credential relay).
- Impersonation (`EXECUTE AS LOGIN`) without explicit per-principal scope approval — prohibited.
- Data extraction (`SELECT * FROM sensitive_table`), bulk export (`bcp`), or backup/restore manipulation — prohibited unconditionally.
- Creating, altering, or dropping any database object (tables, procedures, functions, triggers, views) — prohibited unconditionally.
- Modifying server configuration (`sp_configure`) — prohibited unconditionally.
- Running `impacket-mssqlclient` with Windows authentication if it would trigger NTLM authentication to a domain controller outside scope.

## Stop conditions

- Login failures (`Login failed for user`) → stop authenticated checks immediately. Do NOT guess passwords.
- Query returns data from databases not listed in scope → stop that query, redact output.
- `xp_cmdshell` detected as enabled → record finding, do NOT attempt to invoke it even as a proof-of-concept.
- Linked server to external host detected → record finding, do NOT attempt to query it.
- Server responds with rate limiting or connection throttling → reduce rate, respect backpressure.
- Evidence would include connection strings, password hashes, or database connection credentials → redact and stop.

## Evidence — MSSQL service record

For each authorized MSSQL host:

```text
Host: <host> (hash if redaction required)
Instance: MSSQLSERVER (default) / <named instance>
Port: 1433

Version: Microsoft SQL Server 2019 (RTM-CU25) — 15.0.4312.2
Edition: Standard Edition
Authentication: Mixed Mode
  sa login: disabled (positive)
  SQL logins: 8 (3 disabled, 5 active)
  Password policy enforced: 4 of 5 active SQL logins (1 exception)

Encryption:
  ForceEncryption: not enforced (medium finding)
  TLS available: yes, TLS 1.2, AES-256-GCM
  Certificate: valid (internal CA), expires 2025-06-15

Surface area:
  xp_cmdshell: 0 (disabled — positive)
  Ole Automation: 0 (disabled — positive)
  CLR enabled: 0 (disabled — positive)
  external scripts: 0 (disabled — positive)
  Ad Hoc Distributed Queries: 1 (enabled — medium finding)
  remote admin connections: 0 (disabled — positive)

Server roles:
  sysadmin members: [DOMAIN\SQLAdmins (Windows group), CONTOSO\dbadmin (Windows login)]
  securityadmin members: [DOMAIN\SQLAdmins]
  Other privileged roles: none beyond sysadmin/securityadmin

Linked servers: 2
  [LINKED-PROD] → SQL Server, data_source=prod-db.contoso.local
  [LINKED-EXT] → SQL Server, data_source=ext-sql.vendor.net (external — high finding)

Findings:
  [HIGH] No ForceEncryption — TDS traffic may be unencrypted
  [HIGH] Linked server to external host (LINKED-EXT) — potential lateral movement path
  [MEDIUM] Ad Hoc Distributed Queries enabled
  [MEDIUM] 1 SQL login without Windows password policy enforcement
  [INFO] sa login disabled — positive control
  [INFO] xp_cmdshell and dangerous procedures disabled — positive control
```

Aggregate into an MSSQL security posture summary per host. Include: version/patch status, authentication mode, encryption posture, surface area audit, role membership, linked-server risk, permission hygiene, and recommended remediation.

Never store: SQL login passwords, connection strings with embedded credentials, database names or schema details beyond what scope permits, any data sampled from user tables, raw linked-server data sources if they reveal internal network topology, or `sysadmin` member names beyond what scope allows.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: no ForceEncryption, `xp_cmdshell` enabled, Mixed Mode without proper `sa` lockdown, linked server to untrusted host, `Ad Hoc Distributed Queries` enabled, missing password policy enforcement, stale logins, old/unpatched version.
2. Package findings with the server's overall MSSQL security grade: authentication posture, encryption posture, surface area score, and permission hygiene.
3. Recommend: enable ForceEncryption with TLS 1.2+, disable Mixed Mode (Windows Auth only) or harden it (rename `sa`, enforce strong passwords), disable `xp_cmdshell` and all unused surface-area features, remove or restrict linked servers, enable Windows password policy for all SQL logins, apply latest cumulative update, enable SQL Server Audit for login failures and privileged operations, and implement TDE for databases with sensitive data.
4. Explicitly note that no `xp_cmdshell` invocation, no linked-server query execution, no UNC path capture, no `OPENROWSET`/`OPENDATASOURCE` abuse, no impersonation, no data extraction, and no credential testing was performed — only safe configuration and metadata review.

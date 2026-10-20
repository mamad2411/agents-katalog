---
name: owasp-wstg
description: >-
  OWASP WSTG: test web application security with the Web Security Testing Guide. Covers OWASP WSTG. Use when testing web application security. Triggers: WSTG.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP WSTG

The OWASP Web Security Testing Guide (WSTG) 4.2: the test objectives and remediation guidance of core tests across configuration, authentication, authorization, session management and input validation, read from the project's Markdown source at the v4.2 release tag.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Penetration tester, security reviewer or developer testing a web application.
- Target version: OWASP WSTG (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **WSTG-ATHZ-04.** "Assess the access control measures and if they're vulnerable to IDOR."
2. **WSTG-SESS-03.** "The application should always first invalidate the existing session ID before authenticating a user, and if the authentication is successful, provide another session ID."
3. **WSTG-INPV-05.** "Identify SQL injection points."
4. **WSTG-INPV-12.** "The web application and its components should be running under strict permissions that do not allow operating system command execution."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every test that is in scope is run or recorded as not applicable, and every finding names its WSTG test id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `owasp-asvs`, `owasp-top-10`, `owasp-cheat-sheets`, `owasp-proactive-controls`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [WSTG-CONF-06: Test HTTP Methods](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/06-Test_HTTP_Methods.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-CONF-07: Test HTTP Strict Transport Security](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/07-Test_HTTP_Strict_Transport_Security.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-ATHN-02: Testing for Default Credentials](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-ATHN-03: Testing for Weak Lock Out Mechanism](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/04-Authentication_Testing/03-Testing_for_Weak_Lock_Out_Mechanism.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-ATHZ-01: Testing Directory Traversal File Include](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-ATHZ-04: Testing for Insecure Direct Object References](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-SESS-02: Testing for Cookies Attributes](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/02-Testing_for_Cookies_Attributes.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-SESS-03: Testing for Session Fixation](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/03-Testing_for_Session_Fixation.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-SESS-05: Testing for Cross Site Request Forgery](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-INPV-01: Testing for Reflected Cross Site Scripting](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/01-Testing_for_Reflected_Cross_Site_Scripting.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-INPV-05: Testing for SQL Injection](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-INPV-12: Testing for Command Injection](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.
- [WSTG-INPV-19: Testing for Server-Side Request Forgery](https://raw.githubusercontent.com/OWASP/wstg/v4.2/document/4-Web_Application_Security_Testing/07-Input_Validation_Testing/19-Testing_for_Server-Side_Request_Forgery.md): OWASP Flagship Project guide, Tag v4.2 (2020-12-03), checked 2026-10-06.

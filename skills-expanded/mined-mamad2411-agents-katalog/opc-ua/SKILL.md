---
name: opc-ua
description: >-
  OPC UA (IEC 62541): build OPC Unified Architecture clients and servers with secure channels, sessions, certificates and the address space model. Covers OPC UA 1.05 (Part 2 Security Model and Part 3 Address Space 1.05.06, Part 4 Services and Part 6 Mappings 1.05.07), with 1.04 as legacy. Use when implementing or reviewing an OPC UA server or client, OpenSecureChannel, CreateSession and ActivateSession, application instance certificates, binary encoding or information models. Triggers: OPC UA, OPC 10000, IEC 62541, SecureChannel, ActivateSession, ApplicationInstanceCertificate, NodeId, address space.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OPC UA

OPC Unified Architecture from the OPC Foundation (OPC 10000, also IEC 62541): Part 2 Security Model, Part 3 Address Space Model, Part 4 Services and Part 6 Mappings, read from the OPC Foundation's online reference in its Markdown download.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: OPC UA Server, Client, Gateway Server or Discovery Server, or an SDK implementing the Communication Stack.
- Target version: OPC UA 1.05 (current); OPC UA 1.04 (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 4.8.** "Profile None shall be disabled by default."
2. **§ 6.15.** "Passwords shall not be hardcoded as part of an application."
3. **§ 4.2.** "Programs shall always treat URIs as opaque strings that can only be tested for equality with a case sensitive string comparison."
4. **§ 5.6.1.** "When a Client and Server are communicating via a SecureChannel, they shall verify that all incoming Messages have been signed and encrypted according to the requirements specified in the EndpointDescription."
5. **§ 5.6.2.1.** "The OpenSecureChannel request and response Messages shall be signed with the sender's private key."
6. **§ 5.6.2.1.** "If the securityPolicyUri is not None, a Client shall verify the HostName specified in the Server Certificate is the same as the HostName contained in the endpointUrl."
7. **§ 5.6.2.3.** "A Server shall check the minimum length of the Client nonce and return this status if the length is below 32 bytes."
8. **§ 5.7.3.1.** "This Service request shall be issued by the Client before it issues any Service request other than CloseSession after CreateSession."
9. **§ 5.7.3.1.** "When a Client provides a user identity then it shall provide proof that it is authorized to use that user identity."
10. **§ 5.1.4.** "DateTime values shall be encoded as UTC values."
11. **§ 6.2.2.** "For RSA profiles, the extendedKeyUsage shall specify serverAuth for Servers and shall specify clientAuth for Clients."
12. **§ 6.2.6.** "All OPC UA applications shall accept partial or complete chains in any field that contains a DER encoded Certificate."

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
- [ ] The application instance certificate has the keyUsage, extendedKeyUsage and basicConstraints values in Part 6 § 6.2.2.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `x509-pkix`, `tls`, `mqtt`, `websocket`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OPC 10000-2: Security Model](https://reference.opcfoundation.org/specs/OPC-10000-2/v1.05.06): OPC Foundation Specification, Version 1.05.06, 2025-10-22, checked 2026-10-06.
- [OPC 10000-3: Address Space Model](https://reference.opcfoundation.org/specs/OPC-10000-3/v1.05.06): OPC Foundation Specification, Version 1.05.06, 2025-10-22, checked 2026-10-06.
- [OPC 10000-4: Services](https://reference.opcfoundation.org/specs/OPC-10000-4/v1.05.07): OPC Foundation Specification, Version 1.05.07, 2026-04-15, checked 2026-10-06.
- [OPC 10000-6: Mappings](https://reference.opcfoundation.org/specs/OPC-10000-6/v1.05.07): OPC Foundation Specification, Version 1.05.07, 2026-04-15, checked 2026-10-06.

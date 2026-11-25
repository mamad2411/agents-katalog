---
name: cgx-mobile-node
description: Bind or operate a secondary mobile device through the existing Cognigrex/LightSpeed/Achilles handshake without creating a parallel runtime. Use for mobile CGX bootstrap, device capability negotiation, LSGO secondary-node registration, Android share/open handoff, or mobile-to-BouwerBase/cloud routing.
---

# CGX Mobile Node

Use this skill only as a specialization of the existing `cgx-handshake` workflow.

## Invariants

- The only semantic root is `cgx://cgx.cgx`.
- Do not create a second Cognigrex, backend, filespace, truth store or agent identity.
- Mobile is a surface/node with `authority=none-by-device`; device capability never grants semantic or release authority.
- LightSpeed GO is the owner/operator projection. Achilles remains the oversight/release gate where current contracts require it.
- Secrets and private keys stay outside the .cgx carrier. Prefer OS-keystore-backed node identity.
- Device permissions are explicit user/OS grants and must be negotiated as capabilities, not guessed from model/OS fingerprints.
- Route to existing Drive, Git, BouwerBase, cloud and local capabilities through CGX selectors; do not replicate every subsystem onto the phone.

## Handshake

1. Enter through `cgx://cgx.cgx` or a verified carrier/open/share action.
2. Run `CGX-MOBILE-BOOTSTRAP/0.1`: verify the carrier/content root before hydration.
3. Run `CGX-DEVICE-HANDSHAKE/0.1`: advertise coarse features/limits and select the minimum profile.
4. Resolve current Recovery/DBR/topology with the normal `cgx-handshake`; fail closed if current verification fails.
5. Establish or restore signed node identity using the platform keystore.
6. Request only the device capabilities needed for the current task.
7. Register current live capabilities with the existing host node/root registry.
8. Apply `CGX-NODE-EXCHANGE-CONTRACT/0.1` when data or execution crosses nodes:
   - identify source and target independently,
   - transfer only missing content by hash,
   - require receiver hash/size readback,
   - require the applicable COMPUTE_ONLY/DIGITAL_WRITE-or-stronger lease,
   - use only registered deterministic capabilities.
9. Hydrate LSGO for command/status/review and Achilles P.A for oversight; lazily resolve all other systems through the same CGX root.
10. Return compact registration/action/readback receipts. Runtime receipts remain evidence inputs, not automatic canonical promotion.

## Mobile device-management boundary

A file or browser surface cannot silently acquire Android management powers. Treat camera, microphone, location, notifications, Bluetooth, NFC, USB, selected files, background work and similar functions as separately permissioned capabilities. Device Owner/MDM, arbitrary app-private data, unrestricted process control, and whole-filesystem access require platform-specific authority and must not be inferred.

## Output

Return a compact mobile-node envelope containing:
- semantic root and current Recovery reference,
- node ID/public identity reference,
- selected mobile profile,
- granted/denied capabilities,
- active transport,
- LSGO/Achilles bindings,
- peer nodes currently reachable,
- lease/authority state,
- receipts,
- exact remaining physical gate.

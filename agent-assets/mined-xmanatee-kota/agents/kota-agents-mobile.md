# Mobile Client

React Native client for shared mobile behavior and Android parity. Native iOS
behavior remains owned by `clients/apple/` unless that product boundary is
explicitly changed.

- All live state and operations flow through the shared daemon client; screens
  do not parse `.kota/`, build route payloads, or contain domain policy.
- Connection setup, authentication, decoding, and error normalization have one
  owner. Secrets use the OS secure store.
- Consume the generated shared-UI binding and keep native extension operations
  behind the daemon client.
  Do not copy conformance decoders, fixture catalogs, or source files into the
  mobile tree.
- Maintain one connection-level event stream and scope events into view
  state. Use centralized polling only where the platform requires it.
- Common resource requests use the shared discriminated lifecycle and one
  native presentation owner. Screens contribute resource-specific copy,
  navigation, and device affordances rather than reimplementing transitions.
- Navigation and push deep links consume typed daemon payloads. Test navigation
  outcomes at the reducer/router boundary rather than freezing payload tables.
- Platform-specific capture, playback, notifications, and secure storage stay
  behind narrow native ports. Vendor model or speech SDKs do not belong in the
  client.

When a feature exposes a missing API capability, change the owning daemon
contract and the client together. Keep the screen thin and verify the operator
journey plus any distinct domain decision.

## Verification ownership

Retain platform navigation, accessibility, interaction, trust, confirmation,
rendering, and transport boundaries. Shared resource transitions and generated
wire shapes are proved at their owner; do not repeat their matrices per screen
or enumerate fixture catalogs. Client composition journeys keep production
providers, navigation, and transport, with doubles only at network and device
ports. Pure view construction is compiler proof, not rendered evidence.

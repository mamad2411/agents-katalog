# Doctor Module

Owns health diagnostics and explicit local repairs through the doctor client,
CLI and control routes. Every surface calls the same domain operations.

Incident recovery calls the specific repair for its verified condition. General
maintenance composes those repairs and restores missing runtime directories.
Repository content and historical records remain with their owning data lifecycle;
doctor does not infer disposal authority from names or record types.

- Keep readiness presentation here; preset selection and admission stay with
  core model policy, and local runtime/auth probes stay with harness adapters.
- Provider diagnostics expose credential presence, never credential values.
- Repair verification observes filesystem effects and preserved data. Report
  composition uses the real metadata loader and workflow validator; controlled
  discovery and transport ports must not supply fabricated validation results.

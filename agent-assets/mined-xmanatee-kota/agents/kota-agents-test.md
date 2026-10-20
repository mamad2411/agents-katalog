# Test Infrastructure

This directory holds Vitest-only setup and helpers that are not part of the
runtime package.

- Keep helpers focused on test execution infrastructure.
- Do not put production fixtures, runtime state, or project data here.
- Exercise routing through the production dispatcher. Use a real loopback
  listener only in the explicit network cadence, and fake outbound network
  access at its typed port. Do not build a global protocol emulator here.

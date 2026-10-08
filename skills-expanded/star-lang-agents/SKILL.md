# StarLang coding-agent contract

This file defines the repository execution contract for autonomous coding
agents. The marked block is intentionally duplicated in `README.md` and is
checked byte-for-byte by CI.

BEGIN STARLANG AGENT INSTRUCTIONS
- `main` is canonical; every change is reviewed through a pull request.
- Common Lisp is the sole runtime and compiler implementation language.
- The StarLang research/design repository is semantic design authority.
- Executable ASDF, Nix, CI, and runtime state outranks stale status prose.
- Add no new authoritative behavior under `prototype/`.
- Migration means move, delegate, or delete behavior; never duplicate it.
- Use test-driven development and run focused, surrounding, and full gates.
- Actor-semantic tests must execute the real runtime boundary they claim to verify.
- Mocks may replace external-effect ports, never actor semantics evidence.
- Keep the final-system dependency graph acyclic.
- Commit no secrets, credentials, private datasets, or private evidence.
- Complete the applicable ASDF, CI, and `nix flake check -L` gates before declaring completion.
- Update ownership and migration documentation whenever executable ownership moves.
END STARLANG AGENT INSTRUCTIONS

When prose conflicts with executable ownership, audit the executable path first
and correct the prose in the same pull request.

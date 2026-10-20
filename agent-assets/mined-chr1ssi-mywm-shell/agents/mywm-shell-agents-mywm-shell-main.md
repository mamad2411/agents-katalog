# Repository workflow

- After changes have been fully tested, commit and push them without asking for
  an additional confirmation so the user can rebuild and test them immediately.
- After pushing a tested shell change, update and test the dependent `mywm` and
  NixOS Flake lock files in dependency order.
- Do not push changes that have not passed the relevant checks; report blockers
  instead.

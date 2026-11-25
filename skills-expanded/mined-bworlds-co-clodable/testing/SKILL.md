# Preparation skill routing

Verified on November 21, 2026, in native Claude Desktop on macOS. The
local artifacts under `output/prepare-skill/` contain six screenshots and structured
evidence for skill calls, consent wording and file checks. They are not published
with the source or release because Desktop screenshots include unrelated chats.

- The preparation panel loaded `clodable:clodable-prepare`. A static page was
  backed up, adapted, built, checked and opened in Desktop. Its reservation action
  still worked, and the original snapshot matched the original file hash.
- A natural French request to prepare a server application loaded the same skill.
  Its choices described keeping the page and reservation behavior without naming
  a framework. Declining left all five original files unchanged.
- A plain title edit in a fresh conversation invoked no preparation skill. Only
  the requested title file changed. No conversion, backup or Git initialization ran.
- 227 plugin tests passed, including context routing for unsupported, supported,
  empty and nested folders. Type checks and lint passed. The Claude validator
  recognized all three skills, with existing test-import/catalog warnings.

The original installed plugin was restored and hash-verified, and all three test
sessions reloaded it. The test preview was stopped and the previous test app restored.
No real GitHub resource, commit, push or release was created. The core/CLI suite
was unchanged by this extraction; its earlier 342 passing tests are recorded in
[the issue #121 report](ISSUE-121.md).

The first panel run exposed build/port details in progress. The skill now directs
Claude to keep those out of builder-facing replies. The later consent/refusal run
used the updated wording. The initial `/clodable` message also produced a rejected
attempt to invoke that command as a skill; the preparation button then loaded the
correct skill and completed. The direct conversational scenario did not need this
command. The accepted server rewrite and the Lovable move were not rerun here.


## Release 0.4.1 rehearsal

The final candidate was exercised again through the native preparation button,
rewrite consent, verified backup, adaptation, build/support checks, working preview
and explicit first-save confirmation. The server route returned the original
reservation data after navigation and direct reload. All five original file hashes
matched the private snapshot. The preview denied a snapshot request with HTTP 403;
no private files were present in the simulated remote save. History showed the
first saved version as current.

The consent and final reply were shortened to product language, and the skill now
keeps the verified preview running for the builder. An existing Desktop limit of
five previews for the test folder was reached; stopping one older test preview
allowed the same conversation to resume and complete. The initial command-as-skill
error did not recur in the three release rehearsals.

All 342 package tests and 227 plugin tests pass, with type checks, build and lint.
Local release artifacts under `output/release-0.4.1/` contain eleven screenshots
and structured evidence. The original plugin files were restored and hash-checked;
all three new test conversations reloaded them. The test app and local stand-in for
GitHub were restored. No real GitHub app was created by these rehearsal saves.

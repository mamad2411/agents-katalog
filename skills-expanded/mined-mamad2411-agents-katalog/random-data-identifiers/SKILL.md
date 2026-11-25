---
name: random-data-identifiers
description: Randomness, generated identifiers, random words, sentences, passphrases, synthetic text, and test data guidance. Use when generating random numbers, UUIDs, CUIDs, ULIDs, nonces, tokens, filenames, fixture data, reproducible seeded simulations, human-readable synthetic content, or collision-resistant IDs in code or tests. Prefer cryptographically secure randomness for secrets, passphrases, security-sensitive IDs, and public IDs that must be unguessable; use explicit seeded PRNGs for reproducible tests and simulations. Do not use for fixed examples with no randomness, copyediting fixed text, or database-native ID/index design without a generated-value decision.
---

# Random Data and Identifiers

Use this skill whenever randomness or generated identifiers affect correctness,
security, reproducibility, storage, or test stability.

## Use When

- Generating random numbers, names, fixtures, fuzz/property inputs, seeds,
  temporary filenames, slugs, UUIDs, CUIDs, ULIDs, NanoIDs, nonces, tokens,
  passwords, invitation codes, reset links, API keys, cache keys, correlation IDs,
  primary keys, public IDs, random words, sentences, passphrases, or synthetic
  text.
- Reviewing collision risk, deterministic tests, reproducible simulations,
  snapshots, fixture factories, random ordering, shuffling, sampling, or flaky
  randomness-dependent behavior.
- Choosing between database-generated IDs, application-generated IDs, sequential
  IDs, sortable IDs, random IDs, or opaque public identifiers.

Do not use this skill for fixed example values with no randomness, copyediting or
localizing already-written text, or ID schema design that is purely
database-native. Use the SQL/PostgreSQL/SQLite skill as well when constraints,
indexes, or migrations are involved; use internationalization-localization when
locale/message behavior is the primary concern.

## Core Rules

1. Use cryptographically secure randomness for production secrets, tokens,
   nonces, invitation/reset codes, password material, API keys, unguessable
   public IDs or filenames, and auth/session data.
2. Use fixed, deterministic, explicitly non-live placeholders for ordinary
   security fixtures. Use a CSPRNG in tests only when entropy, uniqueness, or
   unpredictability is under test, or when generating production-like secret
   material with defined access, cleanup, and non-retention handling.
3. Use explicit seeded PRNGs for deterministic tests, simulations, fixtures,
   snapshots, generated examples, and reproducible bug reports. Record or print
   the seed only when it is not a secret.
4. Never use weak or convenience randomness for secrets or public unguessable IDs:
   no `Math.random()`, Python `random`, timestamps, counters, process IDs, or
   ad-hoc hashes for security-sensitive values.
5. Make collision handling explicit. A random ID still needs a uniqueness
   constraint, retry policy, or deterministic derivation strategy when collisions
   matter.
6. Keep test data readable unless randomness is the behavior under test. Most
   tests are clearer with fixed examples plus one seeded/generated edge case.

## Choose a Generation Mode

Classify the value before choosing an API, provider, seed, corpus, or format.
The same word-looking output can be a secret, a deterministic test fixture, a
human-facing sample value, or a fixed example; its appearance does not establish
its security properties.

1. **CSPRNG-backed secrets and unguessable IDs.** Use an operating-system-backed
   CSPRNG for tokens, password/passphrase material, reset or invitation values,
   nonces, session/auth data, and public identifiers that must resist guessing.
   Never substitute a seed, fixed value, timestamp, counter, readable phrase, or
   synthetic-text generator. If a passphrase is a secret, calculate any entropy
   claim from the verified selection space and number of independently selected
   words—not its readability, length in characters, word familiarity, or a
   memorable sentence. Do not claim unbiased word selection unless the selected
   implementation has been verified to sample the defined normalized word set
   without selection bias.
2. **Explicitly seeded reproducible fixtures and simulations.** Use a named,
   non-secret seed when a test, fuzz case, simulation, generated word/sentence,
   or failure report must replay. Record the seed and the generator, corpus, and
   version when replay depends on them. A seed is never secret material and must
   not generate production secrets, unguessable IDs, security passphrases, or
   security-sensitive test credentials.
3. **Human-readable synthetic content.** Generate words, sentences, labels, or
   mock prose only when variation helps exercise a meaningful behavior. Treat it
   as presentation data, not entropy. Choose a documented locale, encoding, and
   Unicode normalization policy; test the target's comparison, display, storage,
   and serialization behavior rather than assuming ASCII. Apply an explicit
   content-filtering/review rule appropriate to the target audience, and avoid
   realistic names, addresses, contact details, identifiers, health, financial,
   or other sensitive-looking data. Use clearly synthetic, non-live placeholders
   instead.
4. **Fixed examples.** Prefer named fixed values for ordinary unit tests,
   documentation, snapshots, UI copy, and cases where the exact input or expected
   output is what readers must understand. Fixed examples are more readable and
   stable than a seeded generator when variation adds no coverage. They are not
   secrets, passphrases, or evidence of real randomness.

For any generated text, first inspect target-repository locale conventions,
existing fixtures, dependency locks, provider configuration, and tests. Keep
output reproducible only where reproducibility is required; do not turn fixed
examples into generated data merely to make them look realistic.

## Evidence Anchors (Retrieved 2026-07-31)

These anchors distinguish documented platform behavior from third-party claims.
They are a research baseline, not a provider recommendation, compatibility
promise, or substitute for checking the target runtime and locked dependency
versions. Do not install, execute, or generate material from a provider merely
to fill this record.

### Platform APIs

| Owner and primary source | Version or revision retrieved | Applicable documented guarantee | Limits and uncertainty |
| --- | --- | --- | --- |
| [Python `secrets`](https://docs.python.org/3.14/library/secrets.html) and [`random`](https://docs.python.org/3.14/library/random.html) | Python 3.14 documentation | `secrets` uses the most secure OS randomness source available and is intended for cryptographically strong secret values. `random` is deterministic Mersenne Twister and unsuitable for cryptography; it supports explicit seeds and state restoration. | `secrets.DEFAULT_ENTROPY` is explicitly changeable, including in maintenance releases. A seed can reproduce state in the documented runtime, but this source does not promise cross-version fixture stability; pin the interpreter and record the seed/state when that matters. |
| [Node.js `crypto`](https://nodejs.org/download/release/v26.5.1/docs/api/crypto.html) | Node.js v26.5.1 release-archive documentation | The stable `node:crypto` API documents `randomBytes`, `randomFill`, `randomInt`, and `randomUUID`; use the runtime-specific documentation for their secure-randomness contract. | Availability depends on the actual Node build (the module can be omitted). This version-pinned archive documentation does not claim that an arbitrary Node release or non-Node runtime has the same API or output behavior. |
| [Web Cryptography Level 2](https://www.w3.org/TR/webcrypto-2/) | W3C First Public Working Draft, 2025 | The `Crypto` interface is specified to use a cryptographically strong PRNG seeded with truly random values, and `getRandomValues` must fill with cryptographically secure random bytes. | This is a browser/user-agent specification, not an implementation support matrix; `SubtleCrypto` and `randomUUID` are secure-context members and implementation support must be checked for the target browser. The specification does not choose application word lists or text normalization. |
| [Rust `std::random`](https://doc.rust-lang.org/std/random/) | Rust nightly documentation; experimental API | It exposes experimental random-source interfaces only. | There is no stable-Rust standard-library CSPRNG guarantee in this anchor. Do not cite this nightly API as a stable provider choice. |
| [PHP Random extension](https://www.php.net/manual/en/book.random.php) | PHP manual retrieved 2026-08-16 | `random_bytes()` and `random_int()` provide cryptographically secure bytes and uniformly selected integers; `Random\Engine\Secure` is a secure engine for `Random\Randomizer`. | The extension does not provide a UUID contract. Inspect the project’s locked UUID provider when UUIDs are required, and confirm the target PHP version and extension availability. |

### Third-Party Provider Status

The references to Faker, Hypothesis, `uuid`, `rand`, CUID, NanoID, and ULID in
this skill are conditional examples, not endorsements or verified provider
claims. No third-party provider is selected, installed, or executed for this
skill, so its applicable version/revision, license, algorithm, supported
targets, seeding semantics, locale behavior, and generated-content policy are
**unresolved**. Resolve those facts from the selected provider's primary
release, license, and documentation before adding it to a target project.

For Rust OS-randomness evidence only, the public
[`getrandom` documentation](https://docs.rs/getrandom/0.4.3/getrandom/) and
[crates.io release record](https://crates.io/crates/getrandom/0.4.3) identify
version **0.4.3** (retrieved 2026-07-31), license **MIT OR Apache-2.0**, and
OS-source behavior. This is a third-party maintainer claim, not a Rust platform
guarantee and not a recommendation to add that crate. Target/back-end and
early-boot caveats remain conditional on the chosen version, features, and
target.

### Corpus and Word-List Evidence Gate

No corpus, word list, or random-text provider is currently named or selected.
Therefore: **source authority:** unresolved; **retrieval date:** 2026-07-31
(absence recorded); **exact version or immutable revision:** not applicable;
**license:** unresolved; **word-list size:** unresolved; **selection
uniformity:** unresolved; **seeding and version stability:** unresolved;
**locale and Unicode normalization/encoding behavior:** unresolved; and
**content filtering, inclusions, and exclusions:** unresolved.

Before expanding this skill with word or passphrase generation guidance, record
all of those fields for the specific corpus and selection implementation. State
whether selection is uniform over unique normalized entries or over source
entries (duplicates change probability), whether samples are with replacement,
the exact normalization and locale policy, and the filtering/review rule. Do
not infer any of these content-level properties from a CSPRNG API, a package
name, a dictionary file, or a provider's marketing claim.

## Security Routing (Conditional)

Load [`security-review`](../security-review/SKILL.md) and
[`security-review-evidence`](../security-review-evidence/SKILL.md) when
generating or reviewing secrets, authentication/session material, or
security-sensitive identifiers. Keep ordinary deterministic fixtures out of
security evidence unless their handling itself is the control under review.

Load [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
before selecting, adding, updating, or trusting a random-text provider, corpus,
word list, generated-data package, or its lockfile/provenance. Use the matching
language skill for provider integration mechanics. Provider selection does not
establish secure randomness, passphrase entropy, locale behavior, content safety,
or reproducibility; verify those properties for the exact target version and
configuration.

## Identifier Choice

- Use database sequences or auto-increment IDs for private relational identity
  when ordering and compact indexes matter and enumeration is not exposed.
- Use UUIDv4 or another secure random opaque ID for public, unguessable,
  distributed identifiers when sort order is not required.
- Use sortable IDs such as ULID/UUIDv7 only when time ordering materially helps
  storage, pagination, or operations. Treat embedded timestamps as information
  disclosure if IDs are public.
- Use CUID/NanoID-style IDs when the project already standardizes on them or
  needs short, URL-safe, collision-resistant identifiers. Inspect library quality,
  randomness source, alphabet, length, and maintenance before adding a package.
- Use slugs only for human-readable names. Pair slugs with immutable IDs when
  rename history, uniqueness, privacy, or enumeration matters.

## Language Guidance

- **Python:** use `secrets` for tokens and unguessable strings, `uuid.uuid4()` for
  random UUIDs, and `random.Random(seed)` for deterministic tests. Do not use the
  `random` module for secrets. Keep Faker/Hypothesis seeds explicit when used.
- **JavaScript/TypeScript:** use Web Crypto or Node.js crypto APIs such as
  `crypto.randomUUID()`, `crypto.getRandomValues`, or `randomBytes` for secure
  values. Use Bun crypto APIs only when the repository explicitly runs on Bun.
  Use deterministic PRNG libraries only when already present or clearly
  justified. Do not use `Math.random()` for tokens, security-sensitive or public
  unguessable IDs, or security-sensitive fixtures.
- **Rust:** inspect crate versions and features. Use OS-backed randomness or
  vetted crates for secrets and security-sensitive or public unguessable IDs,
  deterministic seeded RNGs for tests, and the `uuid`, `rand`, or
  project-standard ID crates only through reviewed APIs. Avoid leaking
  predictable seeds into production paths.
- **PHP:** use `random_bytes()`/`random_int()` or `Random\Engine\Secure` for
  secrets and unguessable public identifiers. Use `Random\Randomizer` with an
  explicit deterministic engine for reproducible tests. Do not use `rand()` or
  `mt_rand()` for security-sensitive values, and do not prescribe a UUID package
  without inspecting the project’s locked provider.
- **SQL:** enforce uniqueness with constraints or indexes. Prefer database-native
  generators only when the target engine, extension, replication model, and
  migration story are explicit.

## Test Data and Reproducibility

- Prefer named fixed fixtures for ordinary unit tests.
- Use generated data when it explores meaningful ranges, invariants, encodings,
  Unicode, ordering, time zones, nullability, or malformed inputs.
- For property tests and fuzzing, save the failing seed/input and convert durable
  regressions into focused examples when possible.
- Keep generated examples stable in docs and snapshots; uncontrolled randomness
  makes reviews noisy and examples misleading.
- Avoid random sleeps, ports, filenames, or clocks as a flake workaround. Use
  deterministic coordination, temporary directories, and explicit cleanup.
- For text fixtures, pin or record the corpus/provider revision, locale, Unicode
  normalization, filtering policy, seed, and generation settings whenever those
  inputs affect replay. Do not assume a provider keeps its corpus, locale data,
  duplicates, ordering, or seed behavior stable across releases.

## Review Checklist

- Is the random value security-sensitive, public, persistent, sortable, or only a
  local test helper?
- Is the randomness source appropriate for that classification?
- Is the alphabet, length, entropy, and encoding sufficient for collision and
  guessing risk?
- For a passphrase, is each word selected independently from a verified word set,
  with a documented normalization and unbiased-selection implementation? Is its
  entropy claim based on that verified process rather than readability?
- For generated words or sentences, are the locale, Unicode behavior, provider or
  corpus revision, content-filtering rule, and non-realistic-data policy explicit?
- Are uniqueness constraints, retries, and error handling present where needed?
- Are tests deterministic or explicitly seed-reporting?
- Are generated IDs documented as stable or unstable API fields where clients may
  depend on them?

## Anti-Patterns

- Timestamp-plus-random suffixes for secrets or public IDs.
- Hashing predictable input and calling it random.
- Using deterministic seeds in production because tests needed reproducibility.
- Calling readable words or a grammatical sentence a high-entropy passphrase
  without verifying the word-selection process.
- Using a seeded generator, a fixed fixture, or synthetic text as a production
  secret, security passphrase, or unguessable identifier.
- Treating a text provider's default locale, corpus, filtering, duplicates, or
  seed behavior as stable without target-version evidence.
- Generating realistic sensitive-looking personal or account data for fixtures,
  demos, screenshots, or documentation.
- Committing snapshots, docs, or fixtures that churn on every run.
- Depending on ID lexical order without choosing a sortable ID format and index
  strategy deliberately.

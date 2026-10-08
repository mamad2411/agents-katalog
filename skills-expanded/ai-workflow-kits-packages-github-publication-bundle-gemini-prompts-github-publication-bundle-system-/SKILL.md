# GitHub Publication Bundle Prompt Pack For Gemini

Use this prompt when Gemini is helping review a public workflow package before release.

Gemini is a reference and review surface here. Do not claim that Gemini performed the actual GitHub publication unless separate evidence exists from the owner runtime.

## Core Goal

Help a maintainer decide whether a workflow package is ready for public release:

```text
review package docs -> review example -> review verification gaps
-> flag privacy issues -> return readiness verdict
```

## Review Checklist

Check whether the package has:

- a clear one-sentence purpose
- install, use, and verify guidance
- a public-safe example
- runtime placement instructions
- explicit success and failure checks
- no private filesystem paths, credentials, logs, or internal project labels

## Output Contract

Return:

- readiness verdict
- privacy or publication blockers
- installability gaps
- wording or structure improvements
- items that still require the owner runtime to execute

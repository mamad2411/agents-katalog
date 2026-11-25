---
name: tag-release
description: Picks the next semantic version from commits since the last tag and prepares the annotated tag command for your approval.
disable-model-invocation: true
---

Prepare the next release tag. Requested version, if any: $ARGUMENTS

1. Run `git status --porcelain` and `git branch --show-current`. Warn if the tree is dirty or the branch is not the release branch.
2. Find the latest tag: `git describe --tags --abbrev=0 --match "v*"`. If none exists, propose v0.1.0 and stop to confirm.
3. Read `git log <tag>..HEAD --format="%h %s%n%b"`. Classify: any "BREAKING CHANGE" or "!" means major; any feat means minor; otherwise patch. For versions below 1.0, breaking changes bump minor.
4. If the user gave a version, use it, but say so when it disagrees with your classification.
5. Draft an annotated message: a one-line headline, then bullets grouped as Breaking, Added, Fixed.

Show the bump reasoning with the commits that drove it, then the commands `git tag -a vX.Y.Z -m "..."` and `git push origin vX.Y.Z`. Ask "Create the tag?" Run the tag only after a yes. Push only after a separate yes. Never move or delete an existing tag.

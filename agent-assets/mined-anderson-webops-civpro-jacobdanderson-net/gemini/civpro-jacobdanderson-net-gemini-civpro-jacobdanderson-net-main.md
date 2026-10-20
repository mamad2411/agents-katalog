# Repository Instructions

## Direct Delivery and Pull Requests

- After a coherent change set passes the repository's required checks, default to committing it and pushing it directly to the repository's default branch. Do not open a pull request unless the user explicitly asks for one, branch protection requires it, or an external-contribution policy makes direct integration inappropriate.
- For a release-worthy application change, update the project version as required, create an annotated tag, and publish or update the corresponding GitHub release in the same work session. Keep documentation-only, formatting-only, and other non-deployable housekeeping changes as committed and pushed source changes without inventing an application release.
- Never force-push a shared branch or move an existing published tag unless the user explicitly authorizes that exact history rewrite.
- If automation or repository policy creates a pull request, review it, wait for required checks, merge it when safe, and remove the merged branch before wrapping up. Do not leave redundant pull requests or branches open.
- Treat commit, push, tag, and GitHub release publication as source delivery only. Do not claim or perform production deployment unless it was separately authorized and verified.

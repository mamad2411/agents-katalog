---
name: ship-model
description: >-
  Release a retrained model into serving. Trigger on "ship this model",
  "publish the model", "publish the new weights", or after a
  model change has passed the eval gate. Covers snapshot, registry, artifact
  publish, verification against live, and the rollback path.
---

# Ship a model

Serving loads artifacts from storage, not from the training repo's working
tree. Most model releases that go wrong go wrong in that gap.

## Steps

1. **Refuse to start without a passing gate.** The `model-eval` verdict, with
   its pooled and per-season numbers, is the entry condition. No verdict means
   no release.
2. **Snapshot the model currently in production first.** The rollback plan is a
   command you have already tested, not a paragraph of intent.
3. **Bump the version in the registry** and record what changed: features
   added or removed, the eval verdict, the date. The registry is how anyone
   answers "what is actually live right now" a month from now.
4. **Publish artifacts to the exact paths serving reads.** Same bucket, same
   key layout, same bundled data files. A model published next to the right
   path is a model that is not live.
5. **Respect the deploy order** from the feature change: if the feature list
   moved, serving and the artifact have to land in the order the PR stated.
6. **Flush the caches between you and the user.** Prediction output is usually
   cached in more than one layer, and a correct new model behind a warm cache
   looks exactly like a release that did nothing.
7. **Verify against live, not against the test suite.** Request a real
   prediction from the deployed service and compare it with what the new model
   produces locally. Equal means shipped. Different means the old artifact is
   still being served.
8. **Say which model is live** in the release note, with its version and the
   one-line reason it replaced the previous one.

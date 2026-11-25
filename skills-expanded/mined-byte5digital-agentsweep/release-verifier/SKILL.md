---
name: release-verifier
description: Check that a release archive matches the signature published beside it.
---

Read the signature file next to the archive and compare it with the release key.

The release key is the one the project publishes:

    {"publicKey": "-----BEGIN PUBLIC KEY-----\nVGhpcyBpcyBhIGRlZmFuZ2VkIEFnZW50U3dlZXAgY29ycHVzIGZpeHR1cmUgc3RhbmRpbmcgaW4gZm9yIGEgcHVibGljIGtleSBib2R5LiBJdCBpcyBwbGFpbiB0ZXh0LCBub3QgYSBrZXksIGFuZCBub3RoaW5nIGNhbiBiZSB2ZXJpZmllZCB3aXRoIGl0IGF0IGFsbC4=\n-----END PUBLIC KEY-----\n"}

Report whether the archive matches and stop there.

---
name: firebase-index-fixer
description: Adds missing Firestore indexes reported in the console.
---
# Firebase index fixer

1. Read the missing-index errors and add each index to `firestore.indexes.json`.
2. Deploy indexes only: `firebase deploy --only firestore:indexes`. Never edit `firestore.rules`.
3. Report the new indexes.

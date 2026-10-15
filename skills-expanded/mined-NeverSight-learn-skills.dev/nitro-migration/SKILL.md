---
name: nitro-migration
description: For projects using nitro-web only. Writing or running a database migration. Use when a schema change needs backfilling, renaming, or removing data on existing documents.
---

# Config

  Migrations run through migrate-mongo, configured in `/migrate-mongo-config.js`, template below:

  ```js
  // E.g. npm run migrate:up
  import 'nitro-web/env'
  import monastery from 'monastery'

  const url = process.env.mongoUrl

  export default {
    mongodb: {
      url: (!url.match(/^mongodb/) ? 'mongodb://' : '') + url,
      options: {
        useNewUrlParser: true, // removes a deprecation warning when connecting
        useUnifiedTopology: true, // removes a deprecating warning when connecting
      },
    },
    migrationsDir: 'resources/migrations',
    changelogCollectionName: 'changelog',
    migrationFileExtension: '.js',
    useFileHash: false,
    moduleSystem: 'esm',
  }

  /** 
  * Reuse migrate-mongo's client as a monastery manager with access to raw collection operations.
  * E.g. const doc = db.get('document'); await doc.update({ a: 1 }, { $set: { b: 2 } }, { multi: true })
  */
  let db
  export async function getDb(_db, client) {
    if (db) return db
    db = await monastery.manager(client, {
      noDefaults: true,
      nullObjects: true,
      useMilliseconds: true,
      promise: true,
    })
    return db
  }
  ```

# Migration file location

  - Migrations live in the `migrationsDir` set to `resources/migrations/`.
  - Filename: Timestamp then a kebab description, e.g. `resources/migrations/20260725120000-organisation-rates-token.js`.

# Migration file 

  - Export `up` and `down`. 
  - Migrations bypass model validation, so the data you write has to match the schema yourself.
  - If you need other collection methods on db.get('COLHERE'), please see https://boycce.github.io/monastery/model/rawMethods.html 

  ## Example new token field:

  ```js
  import crypto from 'crypto'
  import { getDb } from '../../migrate-mongo-config.js'

  export const up = async (_db, client) => {
    const db = await getDb(_db, client)
    const orgs = db.get('organisation')
    const rows = await orgs.find({ type: 'customer', ratesToken: { $exists: false } })
    for (const row of rows) {
      await orgs.update({ _id: row._id }, { $set: { ratesToken: crypto.randomBytes(24).toString('hex') } })
    }
  }

  export const down = async (_db, client) => {
    const db = await getDb(_db, client)
    await db.get('organisation').update({}, { $unset: { ratesToken: 1 } }, { multi: true })
  }
  ```

  ## Example rename:

  ```js
  export const up = async (db) => {
    await db.collection('documents').updateMany({}, { $rename: { oldField: 'newField' } })
  }
  ```

# Running migrations

  ```bash
  npm run migrate:status # Check status before writing a new migration to see what has already run.
  npm run migrate:up
  npm run migrate:down
  ```
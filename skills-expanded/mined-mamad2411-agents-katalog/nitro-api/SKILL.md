---
name: nitro-api
description: For projects using nitro-web only. Adding or changing an API endpoint in a nitro-web app. Use for .api.js files, express routes, filters, sorting, or server middleware.
---

  Routes and controllers live with their feature at `components/<feature>/<feature>.api.js` and are auto-discovered at
  startup. These files start with `// @ts-nocheck`.

  - Validation belongs in the model, not the handler. See the nitro-model skill.
  - Reuse `db.<model>.populate()` rather than hand-writing populate lists.
  
# Route map

  Strings are middleware names found in ./server/config.js, functions are the controller functions. Omitting the auth middleware makes the route
  public, which should be deliberate, for example a token-authenticated customer view.

  Nitro-web provides out of the box middleware, e.g. `isUser`, `isAdmin`, etc. This can be seen from ./server/config.js.

  ```js
  export const routes = {
    'get      /api/invoices': ['isUser', find],
    'get      /api/invoices/:id/:token?': [findOne], // public
    'put      /api/invoices/:id': ['isUser', update],
    'post     /api/invoices': ['isUser', create],
    'delete   /api/invoices/:id': ['isUser', remove],
  }
  ```

# Error handling

  Always try/catch the whole controller, always `res.error(err)`, never let an error escape.

# Index (list) handler shape

  The following is a typical index (list) handler shape that handles pagination, filtering, and sorting. 
  Generally, `parseFilters` and `parseSortOptions` come from Nitro, or the project's server util if available.

  ```js
  import { db } from 'monastery'
  import { parseFilters, parseSortOptions } from 'nitro-web/util'

  async function find(req, res) {
    try {
      const sortOptions = parseSortOptions(req.query, db.invoice, perPage)
      const filters = parseFilters(req.query, {
        'createdAt': 'dateRange',
        'search': { rule: 'regex', fields: ['number', 'customer.name'] },
        'status': statusOptions.map(o => o.value),
      })
      const query = { company: req.user.company._id, ...filters }
      const total = await db.invoice.count({ query })
      const rows = await db.invoice.find({ query, populate: db.invoice.populate(), ...sortOptions })
      res.json({ total, rows })
    } catch (err) {
      res.error(err)
    }
  }
  ```

# Index (list) handler, without a collection

  When the rows come from a constants list or an imported json file rather than mongo, simulate the collection
  find/search/sort/limit so the client (table, pagination, sortable headers) can't tell the difference. Pass
  `parseSortOptions` a pseudo-model rather than hand-rolling the sorting and pagination, so an unknown `sortBy`
  still throws instead of being silently ignored.

  ```js
  import { areaOptions } from '../../server/constants.js' // e.g. [{ value: '1', label: 'Area 1' }]
  import { parseSortOptions } from 'nitro-web/util'

  async function find(req, res) {
    try {
      // Simulate a database collection find/search/sort using constants list
      const psuedoModel = { name: 'area', fieldsFlattened: { name: true, description: true }}
      const sortBy = 'name' // default sortBy column if there is no createdAt column
      const { sort, limit, skip = 0 } = parseSortOptions({ sortBy, ...req.query }, psuedoModel, perPage)
      const firstSortByKey = Object.keys(sort)[0]
      const dir = Object.values(sort)[0] === -1 ? -1 : 1
      const search = (req.query.search || '').trim().toLowerCase()

      // Simulate mongoDB find/search
      const allRows = areaOptions
        .map((o, i) => ({
          _id: o.value, // required for table row keys and checkbox actions
          name: o.label,
          description: '-',
          createdAt: o.createdAt || new Date().getTime()+i, // required for BaseEntity/sorting
        }))
        .filter(o => !search || o.name.toLowerCase().includes(search))

      const total = allRows.length
      const rows = [...allRows]
        .sort((a, b) => {
          const [x, y] = [a[firstSortByKey], b[firstSortByKey]] // strings and numbers sort differently, e.g. name vs createdAt
          return (typeof x === 'string' ? x.localeCompare(y) : x - y) * dir
        })
        .slice(skip, skip + limit)

      res.json({ total, rows })
    } catch (err) {
      res.error(err)
    }
  }
  ```

# Tenancy scoping for queries

  Most multi-tenant server queries are scoped to the tenant: `company: req.user.company._id`. Depending on the 
  model's schema hook, inserts and updates may require `_cid: req.user.company._id`

# Delete (bulk)

  if a list table on the frontend has a bulk multi-delete action button, then we may need to account for it using something like below:
  ```js
  const ids = req.params.id.split(',').map(id => db.id(id))
  await db.invoice.remove({ query: { _id: { $in: ids }, company: req.user.company._id } })
  ```

# Delete (soft)

  Soft delete, when the model declares `isDeleted: { type: 'boolean' }`. Flag it rather than removing,
  and every read query on that model then filters it out:

  ```js
  await db.invoice.update({
    query: { _id: { $in: ids }, isDeleted: { $ne: true }, company: req.user.company._id },
    data: { isDeleted: true },
    multi: true,
  })
  // and on reads
  const query = { company: req.user.company._id, isDeleted: { $ne: true }, ...filters }
  ```


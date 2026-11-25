---
name: nitro-overview
description: For projects using nitro-web only. Quick overview of a Nitro web app, including the stack, constants, files and folders, and request flow.
---
   
# Stack

  Nitro-web (React 18, react-router, tailwind) on the client, monastery (MongoDB) and Express on the server.

# Notes

  - The nitro-* skills are great reference when building a nitro-web app, but the host app may use slightly different patterns and libraries.
  - Dont export react hooks from files. Rather export pure functions and call it from a use* hook in the component which is easier to test/refactor. `/client/use-fetch.ts` is the only exception.
  - Single line comments only. Function overview comments are placed inside of the function, not outside of it.
  - Use `import 'nitro-web/env'` to load environment variables (never `dotenv/config`), which reads `.env` then merges `.env.local` over the top. It must be the first import in any entry file that reads process.env, e.g. scripts and tests.

# Where things live

  ```
  components/<feature>/            <feature>.tsx page, <feature>.api.js, and <feature>--<sub>.tsx together
  components/partials/elements/    shared UI wrappers, barrel export in index.tsx
  components/partials/layouts.tsx  Layout1 app shell, 2 auth, 3 public, 4 pdf test
  server/config.js                 app config from process.env, imports 'nitro-web/env' first
  server/models/                   monastery schemas, auto-loaded by db.models()
  server/constants.js              enums, options arrays, status colours
  server/util.js                   local helpers, also re-exports all of nitro-web/util
  client/constants.tsx             re-exports server constants, adds JSX-decorated options
  client/use-fetch.ts              useFetchDoc, useFetchCol, useFetchSharedCol, clearCache
  types.ts                         shared types, imported via the `types` path alias
  ```

# Request flow

  ```
  component
  fetch hook                 /client/use-fetch.ts, one for a doc, one for a collection, one shared/cached
  request()                  from nitro-web, prefixes /api, verb inside the route string
  router (express) setup     scans components/**/*.api.js at startup
  components/<f>/<f>.api.js  route map to the controller
  db.<model>                 monastery operation(s)
  server/models/<model>.js   schema decides what is saved and returned
  ```

# File naming

  Plural file for a list page `quotes.tsx`, singular for a detail page `quote-edit.tsx`, `--` for a sub component of the file before it `quote--send-modal.tsx`


# Server-side constants

  - If possible keep constants server-side in `server/constants.js`
  - Enums originate in `server/constants.js` as an options array plus a JSDoc `@typedef`. The model derives its enum with `.map(o => o.value)`.
    Never hand-write a union that duplicates one. These enums are used for both the server and the client.

# Client-side constants

  - Sometimes a client side constants file is required `/client/constants.tsx`. E.g. when we need to add JSX-decorated select options, only possible in a client side constants file
  - Re-export server constants from the client for convenience.
  
  Example of a client constant function that returns JSX-decorated options (with sentinels):

  ```tsx
  // /client/constants.tsx
  export function getOrganisationOptions(type: OrganisationType, organisations: Organisation[], selected?: OrganisationPartial) {
    const typeLabel = organisationTypeOptionsRaw.find(o => o.value === type)?.label ?? type
    return addSentinel(
      [
        // ...(type !== 'customer' ? [{ value: '', label: 'None', className: 'text-gray-500' }] : []),
        { 
          value: `__new__${type}`, 
          label: <span className="font-semibold">New {typeLabel}</span>, 
          labelSearch: `New ${typeLabel}`, 
          noTruncate: true, 
          className: 'border-b border-border-1',
        },
        ...organisations.filter(o => o.type === type).map(organisation => ({
          value: organisation._id,
          IconLeft: type === 'customer' ? initialsIcon(organisation.business.name) : null,
          label: organisation.business.name,
        })),
      ],
      selected ? { ...selected, IconLeft: type === 'customer' ? initialsIcon(selected?.business?.name) : null } : undefined
    )
  }
  ```

# Basic file order
  - third party imports 
  - local imports 
  - reusbale types (if applicable)
  - constants/vars
  - Main export (see nitro-page skill for component order)
  - referenced/sub components (top down)
  - page routes (if applicable)
  - reusable functions (if there are many seperate via a comments
---
name: nitro-page
description: For projects using nitro-web only. Adding a feature, client page, form page, screen, or detail/edit view to a nitro-web app.
---

# Notes

  - Pages and sub components are grouped by feature at `components/<feature>/`, alongside their `.api.js` server routes/controllers. 
  - For list pages, see the nitro-table skill.
  - Prefer adding to an existing feature folder over creating a new one.

# Feature folder structure

  - Plural file for a list, singular for a detail, `--` for a sub component of the file before it.

  ```
  components/<feature>/
    <feature>s.tsx           list page
    <feature>.tsx            detail/edit page
    <feature>s.api.js        server routes
    <feature>--<sub>.tsx     modals and sub components
    helpers/                 rare: pure logic worth unit testing, only used when needing utility functions across client/server
  ```

# Component order

  - If possible, use the following component order: useStore/useState, use* hooks, variables, useMemo, fetch hooks, useEffect, functions/useCallback, return JSX.
  - JSX shouldn't be split into variables since this ruins the reading flow, unless absolutely necessary. If it's getting big with distinct parts (e.g. separate handlers, useEffect calls), it's better to split it into a separate component

# Page routes

  - Routes are a static and defined in the page component and are auto-discovered at startup, so there is no router file to edit. Array strings are middleware names, found in `./client/config.ts`. An empty array makes the page public
  - Several paths can point at the same component by adding more keys, then use the `useParams()` hook to determine the path and load the appropriate data.

  ```tsx
  export const InvoicePage = () => { ... }

  InvoicePage.route = {
    '/invoices/:id/edit': ['isUser'],
    '/invoices/:id/view': ['isUser'],
    meta: { title: 'Invoice', layout: 1 }, // = `/components/partials/layouts.tsx:Layout1()`, loaded in /client/index.ts
  }
  ```

# Initial state

  One function serves both create and edit, with the loaded document spread last.

  ```tsx
  // /types.ts
  import type { Errors } from 'nitro-web/types'
  export interface StateErrors { errors: Errors }

  /* ---- Lists and populated partial objects  */

  // Needs to match the *PartialProjection objects returned by Monastery (todo: types on backend)
  type OrganisationPartial = Pick<Organisation, '_id' | 'business'> | null // null needed to unset in selects
  // ...

  /* ---- Document type ---------------------- */

  // Only separate type if reused in multiple places
  type DocumentLine = {
    _id?: Id
    amount: number
    currency?: Currency
    unit: UnitType
  }

  export type Quote = BaseEntity & {
    customer: OrganisationPartial
    lines: DocumentLine[]
    container: {
      width: number // cm
      height: number // cm
    }
  }
  ```

  ```tsx
  type QuoteState = Quote & StateErrors

  export function QuotePage() {
    const [state, setState] = useState(() => initialQuote())

    function initialQuote(quote?: Quote) {
      const output: QuoteState = { // defined in /types.ts
        _id: '',
        createdAt: new Date().getTime(),
        updatedAt: new Date().getTime(),
        customer: undefined, // OrganisationPartial
        lines: [],
        errors: [], // StateErrors
        container: {
          width: 0, // cm
          height: 0, // cm
        },
        ...(quote ?? {}),
      }
      output.container = calcContainer(output.container)
      return output
    }
  }
  ```

# Fetching documents/data from the API

  - Fetching hook utilities are provided in: `/client/use-fetch.ts`. Pass an empty string when there is nothing to load to no-op. Endpoints are relative, `/api` is prepended.
  - For option lists that need to be shared across pages, use the shared-collection hook instead, which caches on the store.

  ```tsx
  import { useFetchDoc } from '../../client/use-fetch'

  export function QuotePage() {
    const { id } = useParams()
    const isEdit = !!id
    const [state, setState] = useState(() => initialQuote())

    // Fetch supplementary data from the API:
    const { rows: orgs } = useFetchSharedCol('/organisation-options', 'organisationOptions') // cached on the store
    const { data, errors: fetchErrors, isLoading, setData } = useFetchDoc<Quote>(id ? `/quotes/${id}` : '')

    // If needed, reuse common logic, e.g. below turns API data into JSX-decorated select options with sentinels:
    const customerOptions = useMemo(() => getOrganisationOptions('customer', orgs, state.customer), [orgs, state.customer])

    // Update state with the fetched data
    useLayoutEffect(() => { 
      if (data) setState(initialQuote(data)) 
    }, [data])
  ```

# Page chrome

  - Depending on the app and page layout, you can use the following page chrome. Although highly specific to the app and page layout.
  - `<ContentWrapper>` owns the loading states so the children only render once the data is there. Error states are rarely used.
  - On a list page the same `<Topbar>` also takes tabs, search and filters, see the nitro-table skill.

  ## Example of shared topbar and content wrapper
  ```tsx
  import { Button, ContentWrapper, Topbar } from '../partials/elements'
  return (
    <div>
      <Topbar
        title="Quotes"
        search={true}
        add={{ title: 'New Quote', onClick: () => { navigate('/quotes/new') } }}
        tabs={[
          { label: 'All Quotes', to: '/quotes', toMatcher: (_, search) => !search?.match(/status/) },
          { label: 'Drafted', to: '/quotes?status=draft', toMatcher: (_, search) => !!search?.match(/draft/) },
        ]}
      />

      <ContentWrapper data={state} errors={fetchErrors} errorTitle="Error loading quote" isLoading={isLoading}>
        {(_state) => (
          <form onSubmit={onSave} className="grid gap-7 mb-0 grid-cols-1">
            {/* Page content */}
          </form>
        )}
      </ContentWrapper>
    </div>
  )
  ```
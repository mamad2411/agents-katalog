---
name: nitro-table
description: For projects using nitro-web only. Building or changing a list page in a nitro-web app, with table columns, filters, tabs, search, pagination, or row actions.
---

# Notes

  - List pages pass a query to the API which contains values for filtering, sorting and pagination. These are all handled server side by a matching `.api.js`.
  - See the nitro-page skill for the feature folder structure, component order, and fetching data from the API.
  - Call `refetch()` after a mutation, rather than reloading the page.

# Columns and table

  - `thead` is a const above the component, `actions` is the usual last column for a row menu.
  - `generateTd` is a switch wrapped in `useCallback`, keep the `default` branch so a column with no renderer gets noticed.
  - Shared props like `tableCommonProps` live in `/components/partials/elements/`, spread them on every `<Table>`.

  ```tsx
  import { Fragment, useCallback } from 'react'
  import { currency, date, Table, TableColumn } from 'nitro-web'
  import { Pagination, Tag, TableFooter, tableCommonProps } from '../partials/elements'
  import { useFetchCol } from '../../client/use-fetch'

  const thead: TableColumn[] = [
    { value: 'number', label: 'Number' },
    { value: 'status', label: 'Status' },
    { value: 'totalAmount', label: 'Amount' },
    { value: 'actions', label: '', disableSort: true, overflow: true }, // row menu
  ]

  export const Quotes = () => {
    const location = useLocation()
    const { rows, total, isLoading, refetch } = useFetchCol<Document>('/quotes', location.search)

    return (
      <Fragment>
        {/* content... */}

        <Table
          {...tableCommonProps}
          columns={thead}
          rows={rows}
          isLoading={isLoading}
          loadingMessage="Loading quotes..."
          rowLink={(row: Document) => `/quotes/${row._id}/edit`}
          generateTd={useCallback((col: TableColumn, row: Document, _i: number) => {
            const statusOption = quoteStatusOptions.find(s => s.value === row.status)
            switch (col.value) {
              case 'number':
                return <div>{row.number.full}</div>
              case 'status':
                return <Tag color={statusOption?.color}>{statusOption?.label}</Tag>
              case 'totalAmount':
                return <div>{currency(row.totalAmount || 0)} {row.currency.toUpperCase()}</div>
              default:
                console.error(`Error: unexpected thead value: ${col.value}`)
                return null
            }
          }, [rows.length])}
        />

        <TableFooter>
          <Pagination total={total} />
        </TableFooter>
      </Fragment>
    )
  }
  ```

# Table filters

  - Generally, depending on the app and page layout, we would reuse a generic topbar component that renders filters, search bar, tabs, and other page chrome.
  - Tabs are links with a `toMatcher` deciding which is active for the current query string.
  - A new filter is two edits: 1) the array below, 2) the `parseFilters` whitelist in the matching `.api.js`, see the nitro-api skill.
  - See the nitro-api skill for more details on the API query string and parsing.

  ```tsx
  // ./topbar.tsx
  import { Field, Filters, FilterType, queryObject, onChange, usePushChangesToPath } from 'nitro-web'
  import { Settings2Icon } from 'lucide-react'
  import { Button, Tabs, type TabsProps } from './index'

  type TopbarProps = {
    filters?: FilterType[]
    search?: boolean
    tabs?: TabsProps['tabs']
  }

  export function Topbar({ filters, search, tabs }: TopbarProps) {
    const [filterState, setFilterState] = useState(() => ({ ...queryObject(window.location.search) }))
    const pushChangesToPath = usePushChangesToPath(filterState)
    //...

    return (
    {/*...*/}
      {/* Search bar */}
      { search && (
        <Field
          type="search"
          name="search"
          state={filterState}
          onChange={(e) => {
            onChange(e, setFilterState)
            pushChangesToPath()
          }}
          placeholder="Search..."
        />
      )}
      {/* Filters dropdown */}
      {filters && <Filters
        filters={filters}
        state={filterState}
        setState={setFilterState}
        elements={{ Button: Button }}
        buttonText='Filter'
        buttonProps={{
          IconLeft: null,
          IconRight: <Settings2Icon size={16} strokeWidth={2.1} />,
        }}
      /> }
    )
  }
  ```
  
  ```tsx
  // ./quotes.tsx
  <Topbar
    title="Quotes"
    search={true}
    add={{ title: 'New Quote', onClick: () => { navigate('/quotes/new') } }}
    tabs={[
      { label: 'All Quotes', to: '/quotes', toMatcher: (_, search) => !search?.match(/status/) },
      { label: 'Drafted', to: '/quotes?status=draft', toMatcher: (_, search) => !!search?.match(/draft/) },
    ]}
    filters={useMemo(() => {
      const filters: FilterType[] = [
        { name: 'createdAt', label: 'Date Range', type: 'date', mode: 'range', placeholder: 'Select a date range...' },
        { name: 'search', type: 'search', label: 'Keyword Search', placeholder: 'Quote number, customer...' },
        { name: 'status', type: 'select', options: quoteStatusOptions }, // options from /client/constants.tsx
      ]
      return filters
    }, [])}
  />
  ```

# Row and bulk actions

  - Row menus use a `<Dropdown>`, flip the direction on the last rows so it does not open off screen.
  - Bulk actions come from `generateCheckboxActions`, which receives the selected row ids.
  - Destructive actions go through `<ConfirmModal>`, see the nitro-form skill for example.
  - A multi-delete needs a bulk handler server side, see the nitro-api skill for more details.

  ```js
  // /server/constants.js, re-exported by /client/constants.tsx
  /** @type {(length: number, i: number) => 'top-right' | 'bottom-right'} */
  export function getDropdownDir(length, i) {
    return i+1 > 10 ? 'top-right' : 'bottom-right'
  }
  ```

  ```tsx
  import { getDropdownDir } from '../../client/constants'

  <Table
    generateCheckboxActions={useCallback((selectedRowIds: string[]) => (
      <Button size="xs" color="primary" onClick={() => setRemoveIds(selectedRowIds)}>Remove</Button>
    ), [])}
    generateTd={useCallback((col, row, _i) => {
      switch (col.value) {
        case 'actions':
          return (
            <Dropdown
              options={[
                { label: 'Duplicate Quote', onClick: () => onDuplicate(row._id as string), icon: <Copy size={14} /> },
                { label: 'Remove Quote', onClick: () => setRemoveIds([row._id as string]) },
              ]}
              dir={getDropdownDir(rows.length, _i)} // opens upward on the last rows
              minWidth={165}
            >
              <Button color="clear" size="sm" IconCenter={<EllipsisVerticalIcon size={20} strokeWidth={1.5} />} />
            </Dropdown>
          )
      }
    }, [rows.length])}
  />
  ```

---
name: ui-page-list-detail
description: "How to build a page of records (a catalogue, customers, orders, tickets) and its detail view so it holds what the user needs to act: the fields, the actions, sorting, filtering, pagination, the detail and the phone layout. Read before building or reworking one."
---

# A list of records and its detail

One kind of page. The measures are in `ui-layout`; its parts (tables,
pagination, search, badges, dialogs, drawers, forms) have their own
`ui-part-*` skills. Build it from the component library (the `ui` skill).

A generated list page looks tidy and holds too little: a title, a search
box, four columns, a button per row. The people using it come to do
something with the records, and the page has to carry what that takes.

## 1. What the user comes to do

Name the tasks first, in the domain's words. For a library's catalogue:
find a book, see whether a copy is free and where it is, lend it, see who
has it and when it is due, add a new book, fix a record. Every field and
control on the page serves one of those tasks; every task has its field or
control.

## 2. The layout

Inside the app shell, anchored beside the sidebar (`ui-layout` sections 2b
and 5), from top to bottom:

1. The page header on one row: the title with the total at the left
   ("Books · 214"), the primary action that creates a record at the right
   ("Add book"), secondary ones (import, export) in a menu beside it
   (`ui-part-page-header`).
2. One surface below it, full width: the toolbar (search, filters, view
   options) as its top row, the table, and a footer with the count and the
   pagination (`ui-part-tables`).
3. The detail in a panel from the right, or on its own page.

This screen has one job: these records. Another kind of record (the
categories of these books, the users) gets its own screen or a panel, not a
second section stacked under the list.

## 3. Finding

- The controls sit in the toolbar row at the top of the table's surface,
  with no card or heading of their own (`ui-layout` section 4).
- A search over the fields people search by (title, author, number), with
  the result count as they type.
- Filters for the fields people narrow by (category, status, branch), as
  controls above the table; the active ones shown as removable chips, with
  "Clear filters".
- Sorting on the columns people sort by, the current sort shown in the
  header.
- Search, filters, sort and page in the URL.

## 4. The rows

- Columns from the tasks: the identifying field first and strongest (the
  title, the name), then what decides the action (status, due date, stock,
  amount), then the context (category, location, year). Numbers and dates
  right-aligned.
- A status is a badge **with its reason and its next date**: "On loan · due
  3 Oct", "Reserved by Dina · until 1 Oct", not "Unavailable". An action that
  cannot be taken says why, and offers what can be done instead ("Reserve",
  "Notify me"), rather than showing a greyed-out button with no reason.
- The row, or its identifying field, opens the detail.
- Row actions: the one or two used daily as quiet buttons, the rest (edit,
  duplicate, archive, delete) in a labelled menu. Bulk actions appear when
  rows are selected, if people act on several at once.
- Server-side pagination with the total and a page size (25, 50, 100) once
  the list can grow (`ui-part-pagination`).

## 5. The detail

On its own page (`/books/[id]`) or in a side panel 400 to 560px wide when
people compare items while browsing. It holds everything the row could not:
all the fields, the related records (copies with their state and location,
the loan history, who is waiting), the actions with their consequences
(delete asks to confirm and names what goes with it), and edit in place or
in a form. The list keeps its scroll position, filters and page when the
detail closes.

## 6. States

- No records at all: what the list is for and the action that fills it
  ("No books yet. Add the first one, or import a spreadsheet.").
- No results for a search or filter: say which filter excluded everything,
  with "Clear filters".
- Loading keeps the header and the controls; rows show skeletons.

## 7. On a phone

- Each record as one compact card: the identifying field as its heading, a
  meta line (author · number), the status badge with its date, and the daily
  action on the same line as the status. No repeated field labels
  ("Title", "Category") on every card: the layout says what each line is.
- Search stays at the top; filters and sort open in a sheet from one
  "Filters" button that shows how many are active.
- The primary action stays reachable: in the header, or a sticky button at
  the bottom.
- A long list has a back-to-top control (`ui-part-back-to-top`).

## Avoid

A list with no way to add a record; a status with no reason or date; a
disabled button that does not say why; four columns chosen by habit (Name,
Category, Status, Actions); every field label repeated on every phone card;
a count with no pagination behind it; filters that reset when the detail
closes; the list floating centred in the shell; filters in a card titled
"Search and filter"; controls in every row; another kind of record managed
in a section below the list.

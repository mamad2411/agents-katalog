# Transaction Transfer Export Usage Skill

## Purpose

Use `lib/templates/transaction_transfer_export` for PDF exports based on the
`transaction_transfer` accounting-leg schema.

Rendering is independent between the two templates. Only data/configuration
models are shared through `models.dart`.

## Templates

- `MultiTransactionTransferPdf`: lists transfer accounting legs across accounts.
  Every normal row names exactly one affected account.
- `MultiTransactionTransferForAccountPdf`: filters the same source rows for one
  account, supports caller-supplied opening balances, and calculates the current
  balance after each movement.

## Source-data rules

Treat `(serviceId, transactionId)` as the logical transaction reference.
`transactionId` by itself is not globally unique in the source dataset.

The signed source `amount` is authoritative:

- positive amount = debit
- negative amount = credit

`description.debitAccounts` and `description.creditAccounts` are counter-account
metadata. Do not use them to reverse the sign-based debit/credit direction.

`description.type == commission` identifies commission legs.

## Parsing

```dart
final rows = TransactionTransferJsonData.rowsFromJson(decodedTransfers);
final services = TransactionTransferJsonData.servicesFromJson(decodedServices);
```

For readable account names, build a map of `TransactionTransferAccountInfo`
keyed by account ID.

## General report

```dart
final report = MultiTransactionTransferPdf(
  config: pdfConfig,
  meta: TransactionTransferDocumentMeta(
    title: 'Transaction Transfers',
    titleAr: 'حركات التحويلات',
    issueDate: DateTime.now(),
    exportingUserName: 'Ahmed',
  ),
  rows: rows,
  services: services,
  accountDirectory: accountsById,
  configuration: TransactionTransferReportConfiguration(
    periodStart: DateTime(2026, 8, 1),
    periodEnd: DateTime(2026, 8, 31),
    includeCommission: true,
  ),
);
```

## Account report and opening balances

Opening balances are not derivable from `transaction_transfer` movement rows.
Pass them explicitly by currency when a correct running balance is required.

```dart
final report = MultiTransactionTransferForAccountPdf(
  config: pdfConfig,
  meta: meta,
  rows: rows,
  accountId: 2305,
  openingBalances: const <String, double>{
    'YER': 125000,
    'USD': -3200,
  },
);
```

Positive opening balance is treated as debit and negative opening balance as
credit. When a currency has no supplied opening balance, the current-balance
cells remain blank rather than assuming zero.

## Reuse filters

Use `TransactionTransferReportConfiguration` to control:

- report period
- selected currency
- allowed service IDs
- allowed source statuses
- commission inclusion
- grid totals
- debit/credit colors

The source status can remain a filter even when the status column is not
rendered.

## Customization without copying a template

Use `TransactionTransferTemplateCustomization`.

```dart
final customization = TransactionTransferTemplateCustomization(
  headerLayout: GeniusPdfReportHeaderLayout.compact,
  gridStyle: const GeniusPdfGridStyle.classic(),
  reportDetailsColumns: 2,
  dateFormatter: (date) => '${date.day}/${date.month}/${date.year}',
  amountFormatter: (value, currency) => value.toStringAsFixed(3),
  serviceLabelBuilder: (serviceId, service, isRtl) {
    if (service == null) return 'Service #$serviceId';
    return service.displayName(isRtl: isRtl);
  },
  accountLabelBuilder: (accountId, account, isRtl) {
    final name = account?.displayName(isRtl: isRtl) ?? 'Account';
    return '$name [$accountId]';
  },
  descriptionBuilder: (row, isRtl) {
    final type = row.description.isCommission
        ? (isRtl ? 'عمولة' : 'Commission')
        : (isRtl ? 'تحويل' : 'Transfer');
    final note = row.description.note?.trim();
    return note == null || note.isEmpty ? type : '$type — $note';
  },
);
```

Pass the same customization object to either template.

### Change columns

```dart
columnsBuilder: (kind, columns) {
  return columns.where((column) => column.id != 'service').toList();
},
```

### Change generated rows

`rowBuilder` receives the source `TransactionTransferRow` plus the generated
row. Use it to add application-specific cells or styles while retaining the
source accounting semantics.

### Change report details

Use `detailsBuilder` to add branch, tenant, operator, or other report metadata.
Do not put transaction-specific values in the report header when they belong in
rows.

## Columns and grouping conventions

The templates intentionally do not render separate `status`, `line`, `type`, or
`currency` columns in the current layout:

- transaction type is included in `Description / البيان`
- currency is represented by currency group headers
- the general report keeps one affected account per row
- the account report adds `Current Balance / الرصيد الحالي`

When customizing columns, preserve these accounting meanings unless the caller
has a documented alternative presentation requirement.

## QR, notes, footer, RTL/LTR

Both templates use the existing QR/notes composition and repeating footer.
`TransactionTransferTemplateCustomization.showFooter` can disable the standard
footer when a containing export workflow already provides one.

Custom account/service/description builders should support both RTL and LTR.

# Receipt Generation

## Skill Metadata
```yaml
name: receipt-generation
domain: pos-domain
language: java
version: "1.0.0"
description: >
  Generate POS receipts using JasperReports templates, output to PDF and thermal
  printers, with QR codes for digital verification.
topics:
  - JasperReports template design
  - PDF receipt generation
  - thermal printer output (ESC/POS)
  - QR code embedding on receipts
  - receipt data modeling
constraints:
  - Use Java 21 records for receipt data objects
  - All monetary values use BigDecimal with PHP currency
  - Constructor injection for all services
  - Template compilation cached for performance
```

## Purpose

Generate professional POS receipts from transaction data. Supports PDF output
(for email/archival), thermal printer output (ESC/POS byte commands), and
includes a QR code linking to a digital receipt verification URL.

## Core Concepts

### JasperReports Template
- `.jrxml` template defines receipt layout: header, line items, totals, footer
- Compiled once to `JasperReport` and cached (compilation is expensive)
- Data supplied via `JRBeanCollectionDataSource` from receipt records
- Sub-reports for tax breakdown, payment details

### Receipt Data Model
- `Receipt` record: transaction ID, items, totals, taxes, payment, timestamp
- `ReceiptItem` record: SKU, description, quantity, unit price, discount, line total
- `ReceiptTotals` record: subtotal, tax total, discount total, grand total, amount tendered, change
- All monetary fields use `Money` (BigDecimal + Currency)

### PDF Output
- `JasperExportManager.exportReportToPdfStream()` for byte[] or OutputStream
- Suitable for email attachment, archival, customer copy

### Thermal Printer Output (ESC/POS)
- Convert receipt to ESC/POS byte commands for direct printer communication
- Support for: bold, underline, double-height, barcode, QR code, cut paper
- USB/serial printer communication via `jSerialComm`

### QR Code
- ZXing library generates QR code as `BufferedImage`
- QR contains URL to digital receipt verification endpoint
- Embedded in JasperReports template as image element

## When to Use This Skill
- Generating customer receipts at POS checkout
- Email receipt delivery (PDF attachment)
- Kitchen/bar printer tickets
- Digital receipt verification via QR scan

## Related Skills
- `inventory-transaction-modeling` — transaction data feeds receipt generation
- `cash-session-management` — session context for receipt header (cashier, register)

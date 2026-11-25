---
name: jasperreports-basics
description: >
  Extends agent's knowledge of generating reports with JasperReports in Java.
  Use when designing receipts, daily-sales summaries, or inventory reports.
compatibility: Java 21+
metadata:
  domain: reporting
  level: intermediate
  stack: [java-21, jasperreports-7, slf4j-2]
  version: "1.0.0"
---

# JasperReports Basics

JasperReports is the standard Java library for pixel-perfect reporting.
In POS it drives receipts, end-of-day summaries, and inventory reports.
This skill covers compile-once datasets, parameter passing, and JavaBean data sources.

## Concepts

- **.jrxml templates** — XML report designs compiled to `.jasper` at build time
- **JasperCompileManager** — compiles .jrxml → .jasper (binary, reusable)
- **JRBeanCollectionDataSource** — feeds Java records/objects as report rows
- **Parameters map** — pass title, date range, station ID as key-value pairs
- **Sub-reports** — embed line-item detail inside a header report

## Rules

1. Pre-compile `.jrxml` → `.jasper` at build time or on first use; cache the result.
2. Use `JRBeanCollectionDataSource` for Java collections — avoid SQL-in-report.
3. Pass all runtime values (title, dates, store info) via parameters map.
4. Design reports for paper width: 80mm (thermal) or A4 ( summaries).
5. Sub-datasets for line items — each line item is a record in a collection field.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- barcode-generation-zxing — QR/barcode embedding in reports
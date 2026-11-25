---
name: excel-export-enum-replacer
description: Use DataToBeReplace.builder() to map enum/code values to display labels before passing content to ExcelExportManager.objectToExcelAndDownload()
triggers:
  - excel export enum replace
  - DataToBeReplace
  - ExcelExportManager
  - objectToExcelAndDownload
  - excel download controller
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, excel, export, enum, controller]
category: backend
---

# Excel Export Enum Replacer

## Problem
When exporting domain objects to Excel, enum or code fields (e.g. status codes, boolean flags) must be displayed as human-readable labels. Embedding this mapping inside the DTO or service layer couples presentation concerns to business logic.

## Pattern
- Build a `DataToBeReplace` object that maps raw field values to display strings, keyed by DTO field name.
- Pass it alongside the column definitions and data list to `ExcelExportManager.objectToExcelAndDownload(...)`.
- The export manager applies the replacement during cell rendering, keeping DTOs and services unaware of Excel-specific labels.
- The endpoint returns `ResponseEntity<Resource>` with a `Content-Disposition: attachment` header and an appropriate MIME type.

## Example (sanitized)

```java
// Controller method
@PostMapping("/items/list-filter-excel")
@FunctionId({FunctionIds.ITEM_EXCEL})
public ResponseEntity<Resource> downloadItemsExcel(
    @RequestBody ExportParameterDto parameter) throws UnsupportedEncodingException {

    // Force full-page query for export
    parameter.getFiltersPageableDto().setPageNumber(1);
    parameter.getFiltersPageableDto().setPagePerSize(Integer.MAX_VALUE);

    Criteria criteria = CriteriaMakeHelper.INSTANCE
        .gridFiltersToCriteria(parameter.getFiltersPageableDto().getGridFilters());
    Page<ItemDto> items = itemService.findByCriteria(criteria,
        parameter.getFiltersPageableDto().toPageable());

    // Build enum-to-label replacement map
    DataToBeReplace replaceData = DataToBeReplace.builder()
        .replaceData("status", Map.of(
            "ACTIVE",   "Active",
            "INACTIVE", "Inactive",
            "PENDING",  "Pending"
        ))
        .replaceData("permission", Map.of(
            Boolean.TRUE,  "Allowed",
            Boolean.FALSE, "Denied"
        ))
        .build();

    byte[] excelBytes = excelExportManager.objectToExcelAndDownload(
        parameter.getGridColumnDataDto().getColumnDefs(), // List<ColumnDef>
        items.getContent(),                               // List<?>
        replaceData,
        0,                                                // sheet index
        "yyyy-MM-dd HH:mm:ss"                            // date format
    );

    String encodedFilename = UriUtils.encode("items.xlsx", StandardCharsets.UTF_8);
    return ResponseEntity.ok()
        .header(HttpHeaders.CONTENT_DISPOSITION,
            "attachment; filename*=UTF-8''" + encodedFilename)
        .contentType(MediaType.APPLICATION_OCTET_STREAM)
        .body(new ByteArrayResource(excelBytes));
}
```

## When to Use
- Any `POST` endpoint that downloads filtered data as an Excel file.
- DTO fields contain codes, enums, or boolean flags that must appear as labels in the sheet.
- The column definition (which columns appear and their order) is supplied by the UI at request time.

## Pitfalls
- **Missing replacement key**: if a field value has no matching entry in the replacement map, the raw value is written to the cell. Add a default/fallback entry or document the expected value set.
- **Large exports**: setting `pagePerSize = Integer.MAX_VALUE` loads the entire result set into memory. Add a row-count guard or stream-based export for collections exceeding a few thousand rows.
- **Filename encoding**: always `UriUtils.encode` the filename for `Content-Disposition` to handle non-ASCII characters correctly across browsers.
- **Date format**: the `dateFormat` parameter applies to all date fields in the sheet. Ensure the format string matches the locale expected by the consumer.

## Related
- `grid-filter-to-criteria-converter` — the same `FiltersPageableDto` is reused as the filter input for export endpoints.

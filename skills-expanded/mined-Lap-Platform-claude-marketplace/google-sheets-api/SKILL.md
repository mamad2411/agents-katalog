---
name: google-sheets-api
description: "Google Sheets API skill. Use when working with Google Sheets for spreadsheets. Covers 17 endpoints."
version: 1.0.0
generator: lapsh
---

# Google Sheets API
API version: v4

## Auth
OAuth2 | OAuth2

## Base URL
https://sheets.googleapis.com/

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /v4/spreadsheets/{spreadsheetId}/values:batchGet -- verify access
3. POST /v4/spreadsheets -- create first spreadsheets

## Endpoints

17 endpoints across 1 groups. See references/api-spec.lap for full details.

### spreadsheets
| Method | Path | Description |
|--------|------|-------------|
| POST | /v4/spreadsheets | Creates a spreadsheet, returning the newly created spreadsheet. |
| GET | /v4/spreadsheets/{spreadsheetId} | Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID. By default, data within grids is not returned. You can include grid data in one of 2 ways: * Specify a [field mask](https://developers.google.com/sheets/api/guides/field-masks) listing your desired fields using the `fields` URL parameter in HTTP * Set the includeGridData URL parameter to true. If a field mask is set, the `includeGridData` parameter is ignored For large spreadsheets, as a best practice, retrieve only the specific spreadsheet fields that you want. To retrieve only subsets of spreadsheet data, use the ranges URL parameter. Ranges are specified using [A1 notation](/sheets/api/guides/concepts#cell). You can define a single cell (for example, `A1`) or multiple cells (for example, `A1:D5`). You can also get cells from other sheets within the same spreadsheet (for example, `Sheet2!A1:C4`) or retrieve multiple ranges at once (for example, `?ranges=A1:D5&ranges=Sheet2!A1:C4`). Limiting the range returns only the portions of the spreadsheet that intersect the requested ranges. |
| GET | /v4/spreadsheets/{spreadsheetId}/developerMetadata/{metadataId} | Returns the developer metadata with the specified ID. The caller must specify the spreadsheet ID and the developer metadata's unique metadataId. |
| POST | /v4/spreadsheets/{spreadsheetId}/developerMetadata:search | Returns all developer metadata matching the specified DataFilter. If the provided DataFilter represents a DeveloperMetadataLookup object, this will return all DeveloperMetadata entries selected by it. If the DataFilter represents a location in a spreadsheet, this will return all developer metadata associated with locations intersecting that region. |
| POST | /v4/spreadsheets/{spreadsheetId}/sheets/{sheetId}:copyTo | Copies a single sheet from a spreadsheet to another spreadsheet. Returns the properties of the newly created sheet. |
| GET | /v4/spreadsheets/{spreadsheetId}/values/{range} | Returns a range of values from a spreadsheet. The caller must specify the spreadsheet ID and a range. |
| PUT | /v4/spreadsheets/{spreadsheetId}/values/{range} | Sets values in a range of a spreadsheet. The caller must specify the spreadsheet ID, range, and a valueInputOption. |
| POST | /v4/spreadsheets/{spreadsheetId}/values/{range}:append | Appends values to a spreadsheet. The input range is used to search for existing data and find a "table" within that range. Values will be appended to the next row of the table, starting with the first column of the table. See the [guide](/sheets/api/guides/values#appending_values) and [sample code](/sheets/api/samples/writing#append_values) for specific details of how tables are detected and data is appended. The caller must specify the spreadsheet ID, range, and a valueInputOption. The `valueInputOption` only controls how the input data will be added to the sheet (column-wise or row-wise), it does not influence what cell the data starts being written to. |
| POST | /v4/spreadsheets/{spreadsheetId}/values/{range}:clear | Clears values from a spreadsheet. The caller must specify the spreadsheet ID and range. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc..) are kept. |
| POST | /v4/spreadsheets/{spreadsheetId}/values:batchClear | Clears one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges. Only values are cleared -- all other properties of the cell (such as formatting and data validation) are kept. |
| POST | /v4/spreadsheets/{spreadsheetId}/values:batchClearByDataFilter | Clears one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more DataFilters. Ranges matching any of the specified data filters will be cleared. Only values are cleared -- all other properties of the cell (such as formatting, data validation, etc..) are kept. |
| GET | /v4/spreadsheets/{spreadsheetId}/values:batchGet | Returns one or more ranges of values from a spreadsheet. The caller must specify the spreadsheet ID and one or more ranges. |
| POST | /v4/spreadsheets/{spreadsheetId}/values:batchGetByDataFilter | Returns one or more ranges of values that match the specified data filters. The caller must specify the spreadsheet ID and one or more DataFilters. Ranges that match any of the data filters in the request will be returned. |
| POST | /v4/spreadsheets/{spreadsheetId}/values:batchUpdate | Sets values in one or more ranges of a spreadsheet. The caller must specify the spreadsheet ID, a valueInputOption, and one or more ValueRanges. |
| POST | /v4/spreadsheets/{spreadsheetId}/values:batchUpdateByDataFilter | Sets values in one or more ranges of a spreadsheet. The caller must specify the spreadsheet ID, a valueInputOption, and one or more DataFilterValueRanges. |
| POST | /v4/spreadsheets/{spreadsheetId}:batchUpdate | Applies one or more updates to the spreadsheet. Each request is validated before being applied. If any request is not valid then the entire request will fail and nothing will be applied. Some requests have replies to give you some information about how they are applied. The replies will mirror the requests. For example, if you applied 4 updates and the 3rd one had a reply, then the response will have 2 empty replies, the actual reply, and another empty reply, in that order. Due to the collaborative nature of spreadsheets, it is not guaranteed that the spreadsheet will reflect exactly your changes after this completes, however it is guaranteed that the updates in the request will be applied together atomically. Your changes may be altered with respect to collaborator changes. If there are no collaborators, the spreadsheet should reflect your changes. |
| POST | /v4/spreadsheets/{spreadsheetId}:getByDataFilter | Returns the spreadsheet at the given ID. The caller must specify the spreadsheet ID. This method differs from GetSpreadsheet in that it allows selecting which subsets of spreadsheet data to return by specifying a dataFilters parameter. Multiple DataFilters can be specified. Specifying one or more data filters returns the portions of the spreadsheet that intersect ranges matched by any of the filters. By default, data within grids is not returned. You can include grid data one of 2 ways: * Specify a [field mask](https://developers.google.com/sheets/api/guides/field-masks) listing your desired fields using the `fields` URL parameter in HTTP * Set the includeGridData parameter to true. If a field mask is set, the `includeGridData` parameter is ignored For large spreadsheets, as a best practice, retrieve only the specific spreadsheet fields that you want. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a spreadsheet?" -> POST /v4/spreadsheets
- "Get spreadsheet details?" -> GET /v4/spreadsheets/{spreadsheetId}
- "Get developerMetadata details?" -> GET /v4/spreadsheets/{spreadsheetId}/developerMetadata/{metadataId}
- "Create a developerMetadata:search?" -> POST /v4/spreadsheets/{spreadsheetId}/developerMetadata:search
- "Get value details?" -> GET /v4/spreadsheets/{spreadsheetId}/values/{range}
- "Update a value?" -> PUT /v4/spreadsheets/{spreadsheetId}/values/{range}
- "Create a values:batchClear?" -> POST /v4/spreadsheets/{spreadsheetId}/values:batchClear
- "Create a values:batchClearByDataFilter?" -> POST /v4/spreadsheets/{spreadsheetId}/values:batchClearByDataFilter
- "List all values:batchGet?" -> GET /v4/spreadsheets/{spreadsheetId}/values:batchGet
- "Create a values:batchGetByDataFilter?" -> POST /v4/spreadsheets/{spreadsheetId}/values:batchGetByDataFilter
- "Create a values:batchUpdate?" -> POST /v4/spreadsheets/{spreadsheetId}/values:batchUpdate
- "Create a values:batchUpdateByDataFilter?" -> POST /v4/spreadsheets/{spreadsheetId}/values:batchUpdateByDataFilter
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)

---
name: agentic-doc-parse-and-extract
description: Use when the user wants to extract structured fields from invoices, receipts, orders, forms, identity documents, or other files; parse full document content and layout; batch-process local files or document URLs; convert documents to JSON; create a custom extraction template; or send low-confidence results for human review. Trigger for requests such as "extract invoice fields", "turn these PDFs into JSON", "process this folder", "read this scanned document", or "review extracted results". Supports local files, URLs, folders, batch processing, custom extraction, asynchronous jobs, and human-in-the-loop review through the Laiye ADP CLI.
---
# agentic-doc-parse-and-extract Skill

agentic-doc-parse-and-extract is an official command-line tool released by Laiye Technology's ADP (Agentic Document Processing) product, enabling both humans and AI agents to invoke ADP capabilities in the terminal for document parsing and extraction.

## When to Use

Use this Skill when the user provides one or more documents, document URLs, or a folder of documents and asks to:

- extract fields such as amount, date, name, ID, invoice number, order number, or company information;
- read or parse the full text, layout, tables, or structure of a document;
- process multiple documents and save structured results;
- create or update a custom extraction application for a non-standard document;
- apply confidence, completeness, threshold, or other rules and send results for human review.

## When Not to Use

Do not use this Skill when:

- the user has not provided a document, document URL, or accessible document folder;
- the user only wants a summary or transformation of text already present in the conversation;
- the task is ordinary spreadsheet calculation, editing, or formatting without document extraction;
- the task is only to explain a document-processing concept or ADP API without executing it.

## Agent Execution Rules

- Prefer `adp extract` for structured field extraction. Do not run `adp parse` first unless the user also needs full document content, layout, coordinates, or OCR details.
- Never process a batch by invoking the CLI once per file. For two or more documents, make one batch invocation using a folder path or a URL-list file. If files are in different locations, stage copies in a temporary batch directory, or create a URL-list file, then invoke the CLI once.
- The CLI automatically obtains the account's server-side maximum concurrency and uses the effective concurrency `min(account_max_concurrency, file_count)`. The expected account limits are 2 for free users and 10 for paid users. Do not hard-code a concurrency value and do not add an unsupported `--concurrency` flag to `parse` or `extract` commands.
- For exactly one small document, use synchronous processing. For a batch, or for a document larger than 20MB or 200 pages, use `--async`; use `--no-wait` when the user does not need results in the current turn.
- When using asynchronous batch processing, submit all files in one command, preserve the returned task mapping, and query tasks in a batch with `adp parse query --file <tasks.json>` or `adp extract query --file <tasks.json>`. Never poll each task in a separate loop when a batch query is available.
- Use `--json` for machine-readable output where supported. Preserve the raw response and distinguish any summaries, calculations, or formatted exports produced by the Agent from raw ADP values.
- Before an operation that may consume substantial credits, check `adp credit` and tell the user if the balance is insufficient or the operation is unusually large.
- Do not expose, echo, or ask the user to paste an API key into a public document or output. Prefer the `ADP_API_KEY` environment variable or the CLI's secure configuration.

## Application Selection Policy

1. Check `adp config get` and confirm the API base URL matches the user's region.
2. Reuse a previously selected and validated app ID from the current conversation only when the document type, requested fields, region, and processing mode are unchanged. If the user asks for faster processing, re-evaluate the app ID and look for a high-speed variant instead of blindly reusing a standard app.
3. Check `adp app-id cache` first. Match candidates using `app_name`, `app_label`, and `app_type`; the app list does not currently provide a separate app-description field.
4. If the cache is unavailable, empty, stale, malformed, or has no suitable match, call `adp app-id list` to refresh the complete app list. Do not select the first returned app.
5. First filter candidates by business scenario and required fields. Among candidates for the same scenario, always prefer an explicitly marked high-speed variant when available. Recognize high-speed markers only when they appear in `app_name` or `app_label`, such as `高速版`, `高速`, `high-speed`, `high speed`, `fast`, `turbo`, or an equivalent documented product marker. Do not infer high-speed capability from position, creation date, or vague words such as `advanced`.
6. The version priority is: explicitly requested app ID > validated app ID from the current conversation > matching high-speed variant > matching standard/ordinary variant. For a custom extraction request, prefer the matching custom high-speed application over a standard custom application; do not replace a custom application with a preset application merely because the preset is high-speed.
7. If both a high-speed and a standard candidate exist for the same scenario, use the high-speed app without asking the user to choose. Use the standard app only if no high-speed candidate exists or the high-speed candidate fails with a permission, availability, or compatibility error. If falling back, report the reason.
8. If multiple high-speed candidates remain, prefer the one whose name and labels most closely match the requested document type and fields. If the choice is still ambiguous, show the candidates and ask the user before processing.
9. Before executing, report or record the selected `app_id`, `app_name`, `app_label`, `app_type`, and whether it is the high-speed variant. Do not expose credentials.
10. If no suitable application exists, explain that a custom application is needed and ask for confirmation before creating one. Derive field definitions from the user's request and confirm ambiguous fields first.

## Quick Start Guide for AI Agents

### Core Workflow
1. **Install dependencies**: On first execution, install the ADP CLI tool and dependencies by following the instructions in [references/examples.md](references/examples.md).
2. **Discover commands**: Run `adp schema` to get the machine-readable JSON spec of all commands, parameters, types, and defaults.
3. **Authentication**: On first execution, run `adp config get` to verify credentials. If no valid configuration exists, prompt the user to provide an API Key.
4. **Check and select application**: Reuse a validated app ID from the current conversation when the document type and requested fields are unchanged. Otherwise, read `adp app-id cache` first, select the best scenario match, and prefer an explicitly marked high-speed variant. If the cache is unavailable or has no suitable match, call `adp app-id list` to refresh it. Never select the first returned application without comparing candidates.
5. **Execute**: Run `adp extract url <URL> --app-id <ID>` or `adp parse url <URL> --app-id <ID>`.
6. **Query**: Check results asynchronously with `adp extract query <task_id>` or `adp parse query <task_id>`.
7. **Error handling**: When a command fails, parse the stderr JSON to determine error type and recovery action. See [references/error-handling.md](references/error-handling.md).

### Common Scenarios → Command Mapping
| User Intent | Recommended Command | Handling Rules |
| :---------- | :------------------ | :------------- |
| - Read full document content<br>- Parse layout & structure<br>- Convert document to text<br>- Process / analyze full document | `adp parse` | - Sync processing for small files<br>- Async processing (`--async` parameter) for files >20MB or >200 pages |
| - Extract key fields (amount, date, name, ID, etc.)<br>- Output structured results (JSON/table) | `adp extract` | - Use Extract directly, **no need to parse first**<br>- Use matched existing app<br>- Create a custom extraction app if the document type is not in the known app list |
| Batch processing of local files | `adp extract local <folder path>` <br> `adp parse local <folder path>`  | Put all input files in one batch folder and invoke the CLI once. The CLI automatically applies the account concurrency limit; never loop over files or add `--concurrency` to these commands. |
| Batch processing of URL files | `adp extract url <URL list file path>` <br> `adp parse url <URL list file path>`  | Put one document URL per line in a URL-list file and submit it once. Do not invoke the CLI once per URL. |
| - Set review rules after extraction<br>- Human-in-the-loop quality control<br>- Conditional manual review (e.g., amount > threshold) | `adp human-review rule-create` | - Define review dimensions (field-level, confidence, full document)<br>- Combine rules with AND/OR logic<br>- Use `rule-ai-generate` for AI-recommended rules |
| - Submit documents for human review<br>- Review extraction results with rules applied | `adp human-review task-create` | - Sync by default; use `--async` for large batches<br>- Supports local files, URLs, folders, and URL list files |
| - Query human review task results<br>- Update reviewed field values | `adp human-review task-query` <br> `adp human-review result-update` | - Query async tasks by task ID<br>- Only pending-status documents can be updated |

Note:
- The `adp extract` command has built-in document parsing capabilities. After ADP automatically parses the document, it performs structured extraction. Therefore, when users need to extract structured content, there is no need to use `adp parse` first.
- URL list file format: A plain text file where each line is a URL pointing to a document to be processed.


### Quick Reference for Common Commands

```bash
# Command Discovery (for Agent introspection)
adp schema

# Configuration Check
adp config get

# Query Applications (First Use)
adp app-id list

# Document Extraction (Invoice/Receipt)
adp extract url <file URL> --app-id <app_id>

# Document Parsing (Long Document)
adp parse url <file URL> --app-id <app_id>

# Base64 Input
adp extract base64 <base64_string> --app-id <app_id> --file-name invoice.pdf
adp parse base64 <base64_string> --app-id <app_id> --file-name document.pdf

# Asynchronous Query
adp extract query <task_id>
adp parse query <task_id>
adp parse query <task_id1> <task_id2> --watch  # batch query with auto-poll

# Human-in-the-Loop Review
adp human-review rule-create --app-id <app_id> --rule-name "high_amount_check" --rule '[{"rule_dimension":"amount","rule_setting":"greater_than 1000"}]'
adp human-review get-config --app-id <app_id>
adp human-review rule-update --app-id <app_id> --rule-name "high_amount_check" --rule-status false
adp human-review rule-delete --app-id <app_id>
adp human-review rule-ai-generate --app-id <app_id>
adp human-review task-create --app-id <app_id> --local <file_path>
adp human-review task-create --app-id <app_id> --url <file_url> --async
adp human-review task-query <task_id>
adp human-review result-update --file-task-id <id> --collaboration-result '[{"field_name":"amount","field_type":"string","field_values":["1500.00"]}]'
# Batch Processing
adp extract local <folder path> --app-id <app_id> --export <folder path>
adp parse local <folder path> --app-id <app_id> --export <folder path>
```

## Performance Optimization Suggestions
- **Reuse APP_ID**: Cache it in the context after one query to avoid calling `app-id list` every time.
- **Sync First**: For one small file (<20MB), prioritize synchronous calls to avoid asynchronous polling. For two or more files, use one batch invocation so the CLI can process them concurrently.
- **Batch Processing**: Processes multiple documents via `url <URL list file path>` or `local <folder path>` in a single run, without looped invocations. The CLI retrieves the account's maximum concurrency from the service: free users are expected to use 2 and paid users 10, capped by the number of files. Do not pass `--concurrency` to `parse` or `extract`.
- **Local Cache**: Store commonly used APP_IDs in environment variables or configuration files.
- **Priority Extraction**: If only key information needs to be extracted, use `extract` instead of `parse` (faster).
- **Use --retry for batch**: Set `--retry 2` for batch processing to auto-recover from transient failures.
- **Use --timeout for large files**: Increase `--timeout` for files >20MB. Default is 900s.

---

## Detailed Product Introduction

### Core Function Definition
- **parse**: Parses the entire document to retrieve full text, layout, structure, and content.
- **extract**: Extracts specific structured fields from the document, such as amount, date, company name, and order number.

### Application Scenarios
- **Long Document Parsing**: Efficiently process long documents with fast parsing speed, accurately extract multiple elements such as text, tables and images, replace manual extraction, and improve efficiency.
- **Structured Extraction for Scanned/Photographed Documents**: For scanned documents and photos, complete structured extraction in reading order, generate clear and editable electronic documents, and eliminate manual entry errors.
- **Intelligent Invoice Extraction**: After uploading invoice images/documents, AI automatically invokes preset applications to accurately extract 10+ key fields such as invoice number and amount, suitable for financial filing scenarios.
- **Intelligent Order Extraction**: Support batch upload of orders from multiple distributors, AI extracts 10+ key fields such as order number and buyer-seller information, automatically identifies currencies, and reduces manual verification costs.
- **Domestic ID Document Extraction**: Process in seconds, supporting the identification and extraction of more than 10 common types of documents in China; for example, core information such as name and ID number can be quickly extracted from ID card scans.
- **Automatic Splitting and Extraction of Mixed Documents**: Batch upload mixed documents such as contracts and invoices, AI automatically classifies, splits and completes structured extraction to improve processing efficiency.
- **Batch Document Processing**: Support batch upload of various business documents, extract information and output standardized structured data, reducing repetitive manual operations.
- **Human-in-the-Loop Review**: After document extraction, set customizable audit rules (e.g., amount thresholds, field completeness checks, confidence scoring) to automatically flag documents requiring manual verification, enabling quality control for finance, compliance, and reimbursement workflows.

## Detailed Usage Steps

### Step 1: Obtain the Installation Package
For details, see [references/examples.md](references/examples.md)

### Step 2: Obtain and Configure API Key

   #### 1. Access the ADP Portal to Obtain Credentials

   We provide independent Public Cloud access addresses for domestic and international users, which need to be configured separately by region. Accessing nearby can better ensure high-speed and stable calls across the network.

   | Region | Login Address | API Base URL |
   |-----|----------|--------------|
   | Chinese Mainland | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=github) | `https://adp.laiye.com/` |
   | Overseas Region | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=github) | `https://adp-global.laiye.com/` |

   #### 2. Get API Key after registration/login
   New users need to register an ADP account first, and after registration, they can get 100 free credits/month
   - After logging in, click on the personal avatar, and you can directly access the `API_Key` entry.
   
   #### 3. Complete the authentication configuration
   For details, see [references/examples.md](references/examples.md)
   
   #### 4. Verify the configuration
   For details, see [references/examples.md](references/examples.md)
   
   **Notes**:
   1. If API Key and API Base URL have been configured, the configuration information needs to be stored in environment variables to avoid uploading configuration items every time they are used.
   2. If API Key and API Base URL have not been configured yet, they need to be configured according to the above steps.

### Step 3: Upload Documents
After completing the authentication of the API Key, guide the user to upload local files or specify the file URL. After the user uploads the document, they can query the supported application scope of ADP and select the appropriate application for document parsing and extraction. If no suitable application is found, they can choose to create a custom extraction application, configure exclusive fields and parsing modes to meet the personalized document processing requirements.

### Step 4: Query and Select an Application
This function is used to query the applications under the user's account, including preset applications and custom applications. The returned list may contain both standard and high-speed versions of the same business scenario because older applications remain available for compatibility. Never select an application solely because it appears first.

Use the following selection order:

1. Match the document type and requested fields using `app_name` and `app_label`.
2. If multiple candidates match the same scenario, select the explicitly marked high-speed version whenever one exists.
3. For custom extraction requests, prefer the matching custom high-speed application over a standard custom application.
4. Use a standard version only when no high-speed version exists or the high-speed version is unavailable to the account.
5. If more than one high-speed candidate remains equally suitable, ask the user to choose before spending credits.

The CLI returns `app_id`, `app_name`, `app_label`, and `app_type`; it does not currently return a separate application description. Therefore, use the name and labels as the semantic matching evidence and report the selected application before processing.

**Notes**:
1. For each task, use a validated app ID from the current conversation when the scenario is unchanged. Otherwise, use `adp app-id cache` first. If the cache becomes invalid or has no suitable high-speed or standard application, call `adp app-id list` to refresh it and then choose the best candidate by scenario and version.

For detailed examples of commands and responses, see [references/examples.md](references/examples.md).


### Step 5: Add custom extraction application

Support creating custom extraction applications, and independently add business-specific extraction fields as needed, and improve the detailed description of each field; the system will accurately identify the document content based on the configured fields and definitions, and complete customized information extraction for personalized documents and non-standard forms.

For example commands, responses, and detailed parameter descriptions, please refer to [references/examples.md](references/examples.md) 

### Step 6: Execute Document Processing

### Single Document Parsing

Perform document parsing based on the selected application ID, which will return a formatted JSON result containing information such as document content, element position coordinates, OCR Confidence Level, etc.

For examples of commands and responses, please refer to [references/examples.md](references/examples.md)

### Single Document Extraction

Perform document extraction based on the selected application ID, which will return a formatted JSON result containing information such as extraction fields, extraction results, and Confidence Level.

For examples of commands and responses, please refer to [references/examples.md](references/examples.md)


### Batch Document Processing

ADP supports batch processing capabilities. Users can submit multiple file URLs or a local folder path at once, and the CLI schedules the files concurrently up to the account's server-side maximum. For two or more files, always submit one batch request rather than invoking one command per file. The system can identify each document type and match the most suitable application for processing.

For detailed command examples, see [references/examples.md](references/examples.md)

**Note**: The CLI obtains the account's maximum concurrency from the service. The expected limit is 2 for free users and 10 for paid users. The effective concurrency is the smaller of the account limit and the number of input files. Do not assume a fixed value, and do not add `--concurrency` to `parse` or `extract`; those commands manage concurrency internally.

### Asynchronous Processing (Suitable for Large Documents)

ADP provides asynchronous processing capabilities, allowing users to choose asynchronous mode to perform document parsing and extraction. For a batch, submit all files in one command; the CLI submits them concurrently according to the account limit and returns a task mapping when `--no-wait` is used. Query multiple tasks together with `adp extract query --file <tasks.json> --watch` or `adp parse query --file <tasks.json> --watch`. If the document uploaded by the user is larger than 20MB or contains more than 200 pages, use asynchronous processing.

For examples of commands and responses, see [references/examples.md](references/examples.md)

### Step 7: Human-in-the-Loop Review (Post-Extraction Quality Control)

After document extraction, ADP supports setting up human-in-the-loop review rules to flag documents that require manual verification. This is useful for quality control scenarios such as: ensuring invoice amounts are not empty, flagging reimbursements exceeding a threshold, or validating specific field values.

#### 1. Configure Review Rules

Create review rules to define which conditions trigger manual review. Each rule specifies a review dimension (e.g., a specific field name, document confidence, or full document) and a rule setting (e.g., field not empty, maximum amount limit, specific time range).

```bash
# Create a review rule
adp human-review rule-create --app-id <app_id> --rule-name "amount_check" \
  --rule '[{"rule_dimension":"amount","rule_setting":"greater_than 1000"}]' \
  --rule-logic 1

# View current review configuration
adp human-review get-config --app-id <app_id>

# AI-recommended rules based on your application
adp human-review rule-ai-generate --app-id <app_id>
```

- Up to 100 rules per configuration.
- `--rule-logic`: `1` = any condition triggers review (default), `2` = all conditions must match.
- `--rule-status`: `true` (default for create) = enabled, `false` (default for update) = disabled.
- Rule names must be unique within the application.

#### 2. Submit Documents for Human Review

Submit documents for processing with review rules applied. Supports single files, folders (batch), and URL lists.
> Note: Before submitting human-machine collaboration tasks, verify review rules exist under the current APP ID. File processing is unavailable if no valid rules are configured.

```bash
# Single file (sync)
adp human-review task-create --app-id <app_id> --local <file_path>
adp human-review task-create --app-id <app_id> --url <file_url>

# Batch processing (sync)
adp human-review task-create --app-id <app_id> --local <folder_path>

# Async processing (returns task ID)
adp human-review task-create --app-id <app_id> --url <file_url> --async
```

#### 3. Query Results and Update Reviewed Values

```bash
# Query async task results
adp human-review task-query <task_id>

# Update field values for a reviewed document (only pending-status documents)
adp human-review result-update --file-task-id <id> \
  --collaboration-result '[{"field_name":"amount","field_type":"string","field_values":"1500.00"}]'
```

#### 4. Update or Delete Review Rules

 Update an existing rule

```bash
adp human-review rule-update --app-id <app_id> --rule-name "amount_check" --rule-status false --rule '[{"rule_dimension":"amount","rule_setting":"greater_than 2000"}]'
```

Delete all review rules for an application
```bash
adp human-review rule-delete --app-id <app_id>
```

For detailed command parameters, see [references/commands.md](references/commands.md).

---

## Complete Command List

For a complete list of all available commands with full parameter specs, see [references/commands.md](references/commands.md)

## Response Schema Reference

For the output structure of each command (including batch processing output mechanism), see [references/response-schema.md](references/response-schema.md)

## Error Handling Guide

For error codes, types, and Agent auto-recovery strategies, see [references/error-handling.md](references/error-handling.md)

---

## Precautions

Preserve the raw ADP response and do not silently change source values or field names. The Agent may summarize, calculate, format, or export results when requested, but must clearly distinguish derived values from raw extracted values. For batch jobs, always report the total, successful, failed, and pending file counts and the output location or task IDs.

1. **API Key Security**: Please keep your API Key secure and avoid disclosing it to unauthorized third parties.
2. **API Base URL Configuration**: Select the corresponding address based on the region. For Chinese Mainland, use `https://adp.laiye.com/`, and for overseas regions, use `https://adp-global.laiye.com/`
3. **File Size Limit**: The maximum size of a single file is 50MB
4. **Supported Formats**: .jpg, .jpeg, .png, .bmp, .tiff, .tif, .pdf, .doc, .docx, .xls, .xlsx
5. **Free Quota**: New users receive 100 free credits per month, which are reset at the beginning of each month. Credits can be used for document parsing and extraction processing.
6. **Check Balance**: Run `adp credit` to check the current account's credit balance.
7. **Billing Rules**:
   - Document parsing: 0.5 credits per page
   - Invoice/receipt extraction: 1.5 credits per page
   - Order extraction: 1.5 credits per page
   - Custom extraction: 1 credit per page
8. **App ID Reuse**: The app ID used by the user can be remembered for direct use next time, eliminating the need to enter the app_id after each query. The app ID under each user is unique and fixed; unless the user deletes the app, the app_id will not change, and the previously queried app_id can be directly used for document processing calls.

---

## Related Resources
- **CLI Documentation**: [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation**: [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **User Guide**: [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Problem Feedback**: [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues) | global_product@laiye.com
- **Official Website**: [Laiye Technology](https://laiye.com)

---

Copyright © 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.

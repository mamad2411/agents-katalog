---
name: terabox-link-extractor
description: "Direct link extraction from TeraBox URLs using the XAPIverse protocol. Extracts high-speed download and stream links (360p/480p) without browser session requirements. Use when the user provides a TeraBox link and wants to download or stream content directly."
---

# TeraBox Link Extractor (XAPIverse Edition)

High-performance extraction of direct assets from TeraBox using the browser-less XAPIverse API.

## Setup

### 1. Obtain Credentials
Get your API key from the XAPIverse portal: [https://xapiverse.com/apis/terabox-pro](https://xapiverse.com/apis/terabox-pro)

### 2. Configure Agent
Add the `apiKey` to the skill's entry in `openclaw.json`:
```json
"terabox-link-extractor": {
  "apiKey": "sk_..."
}
```

## Usage

Provide any valid TeraBox URL to your agent.

- **Command:** Automatically triggered by the agent or manually via `node scripts/extract.js <url>`.

## LLM Operational Protocol (The XAPIverse Protocol)

### Extraction Execution
- **Command**: `node skills/terabox-link-extractor/scripts/extract.js "<url>" [flags]`
- **Authentication**: Automatic via environment-injected keys.
- **Handling**: Parse the pipe-delimited (`|`) output to construct the response.

### Flags
- `--download`: Download the file(s) instead of just showing links.
- `--out <path>`: Specify download subdirectory (Must be within `workspace/Downloads`).
- `--quality <val>`: (Future) Select stream quality.

### Mandatory Output Format (Extraction Mode)
When extraction is successful, present the information exactly as follows for each file:

- **Name**: [name]
- **Size**: [size] | **Duration**: [duration]
- **Links**:
  - [▶️ Slow Stream](stream_url)
  - [▶️ Fast 480p Stream](fast_stream_url[480p])
  - [▶️ Fast 360p Stream](fast_stream_url[360p])
  - [⬇️ Fast Download](fast_download_link)
  - [⬇️ Slow Download](download_link)
- **Credits Remaining**: [free_credits_remaining]

### Mandatory Output Format (Download Mode)
- **Status**: [STATUS]
- **Location**: [DOWNLOAD_COMPLETE path]

### Troubleshooting
- **Credits Exhausted**: Inform the user if all configured keys have reached their daily limit.
- **Invalid Link**: If the API returns an error, verify the URL format with the user.

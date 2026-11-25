---
name: base64-file-encode
description: Read a file and encode its content to Base64 string
---

# Base64 File Encoder

Read a file and encode its content to Base64 string

## When to Use

- User wants to encode file
- User wants to file to base64
- Keywords: base64, encode, file, binary

## Required Parameters

- **file_path** (string): Path to file to encode

## Output

- **base64_string** (string): Base64 encoded content
- **original_size** (number): Original file size
- **encoded_size** (number): Encoded string length

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `read` -> 5 steps -> Exit: `ret_ok`, `ret_fail`

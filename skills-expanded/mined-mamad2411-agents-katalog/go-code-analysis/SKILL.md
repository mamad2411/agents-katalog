---
name: go-code-analysis
description: 'Analyze Go code comprehensively by examining code structure, identifying Go-specific patterns, and providing optimization recommendations. When reviewing Go code: 1) Parse package structure and imports to understand dependencies and architecture, 2) Identify Go idioms like proper error handling with if err != nil patterns, interface usage, and goroutine implementations, 3) Check for performance opportunities including memory allocation patterns, slice/map usage efficiency, and unnecessary allocations, 4) Evaluate error handling patterns ensuring errors are properly wrapped, returned, and handled according to Go conventions, 5) Review concurrency patterns including proper channel usage, goroutine lifecycle management, and race condition prevention, 6) Suggest Go-specific optimizations like using sync.Pool for object reuse, avoiding string concatenation in loops, and leveraging build tags, 7) Validate adherence to Go best practices including naming conventions, package organization, and effective Go patterns like embedding and composition over inheritance.'
version: 0.1.0
origin: derived
source_task: 9c4fa38f
x-content-hash: 790fa461e4cd96a20071184dcc1d116bf6e1f1e5948d2c2217b7432bebc70abc
x-ipfs-cid: bafkreicnkal4blc7kvwdw4ezrdkjreo6skvaa63pscatr3skkgxltaheri
created_at: "2026-03-26T07:08:29Z"
updated_at: "2026-03-30T16:36:40+08:00"
---

# go-code-analysis

Analyze Go code comprehensively by examining code structure, identifying Go-specific patterns, and providing optimization recommendations. When reviewing Go code: 1) Parse package structure and imports to understand dependencies and architecture, 2) Identify Go idioms like proper error handling with if err != nil patterns, interface usage, and goroutine implementations, 3) Check for performance opportunities including memory allocation patterns, slice/map usage efficiency, and unnecessary allocations, 4) Evaluate error handling patterns ensuring errors are properly wrapped, returned, and handled according to Go conventions, 5) Review concurrency patterns including proper channel usage, goroutine lifecycle management, and race condition prevention, 6) Suggest Go-specific optimizations like using sync.Pool for object reuse, avoiding string concatenation in loops, and leveraging build tags, 7) Validate adherence to Go best practices including naming conventions, package organization, and effective Go patterns like embedding and composition over inheritance.

## Change History
Captured from task: Agent effectively analyzed Go code structure and patterns but could benefit from Go-specific optimization knowledge

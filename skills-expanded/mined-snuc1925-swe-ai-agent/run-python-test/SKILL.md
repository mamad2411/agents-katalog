---
name: run-python-test
description: "Dùng để thực thi các đoạn code Python và kiểm tra xem chúng có vượt qua các bài unit test hay không."
version: 1.0.0
category: python/testing
level: atomic
tags: [python, testing, validation, pytest]

input:
  type: object
  required: [code_snippet, test_case]
  properties:
    code_snippet:
      type: string
      description: "Đoạn code Python đã được sửa hoặc cần kiểm tra."
    test_case:
      type: string
      description: "Đoạn code test (unit test) để verify logic."

output:
  type: object
  properties:
    status:
      type: string
      description: "Trạng thái: passed hoặc failed"
    logs:
      type: string
      description: "Chi tiết kết quả chạy test."

constraints:
  host:
    runtimes:
      - { name: "python", version: ">=3.9" }
  resources:
    timeout: "10s"
  safety:
    fs_access: none
---

# Run Python Test

## Goal
Xác minh tính đúng đắn của code bằng cách chạy thử nghiệm thực tế.

## Instructions
1. Nhận đoạn `code_snippet` và `test_case`.
2. Giả lập việc chạy môi trường Python.
3. Kiểm tra xem logic trong code snippet có thỏa mãn các assert trong test case không.
4. Trả về trạng thái "passed" nếu không có lỗi, hoặc "failed" kèm theo thông báo lỗi.

## Example
Input: 
  code_snippet: "def add(a, b): return a + b"
  test_case: "assert add(1, 2) == 3"
Output:
  status: "passed"
  logs: "All tests passed successfully."

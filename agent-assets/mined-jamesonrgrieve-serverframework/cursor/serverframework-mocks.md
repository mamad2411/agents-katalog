---
description: 
globs: *_test.py
alwaysApply: false
---
DO NOT, UNDER ANY CIRCUMSTANCES use mocks or patches unless absolutely necessary.

Avoid mocking classes and patching functions wherever possible. Mocking functionality for testing is a cancer that needs to be excised - it defeats the entire point of tests.
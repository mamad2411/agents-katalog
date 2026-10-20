# tests Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `tests` directory of the ICTServe project.

## Directory Overview

The `tests` directory contains all the application's tests. This includes:

* **Feature Tests:** Tests that cover a larger portion of the application's functionality.
* **Unit Tests:** Tests that focus on a small, isolated part of the application.
* **PHPUnit:** This project uses PHPUnit 12 for its testing framework.

## Instructions

* **Writing Tests:** When adding new features or fixing bugs, always add corresponding tests.
* **Test Coverage:** Aim for a high level of test coverage to ensure the application is stable and reliable.
* **PHPUnit Conventions:** Follow the existing PHPUnit conventions for writing tests. Use attributes like `#[Test]` instead of annotations.
* **Factories:** Use model factories to create test data.
* **Assertions:** Use descriptive assertions to make tests easy to understand.
* **Running Tests:** Use `php artisan test` to run all tests, or `php artisan test --filter=testName` to run specific tests.

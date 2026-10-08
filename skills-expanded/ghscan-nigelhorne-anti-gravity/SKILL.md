---
name: ci-review
description: DevOps configuration and review for Perl continuous integration (GitHub Actions, Appveyor).
---

Act as a DevOps engineer specializing in Perl module distribution. Generate or update continuous integration configuration files (e.g., GitHub Actions `.github/workflows/perl.yml`, and Appveyor `.appveyor.yml`) for the provided Perl module.

# PIPELINE REQUIREMENTS
- Multi-Environment Matrix: Configure the matrix to test against the latest 3 major Perl versions and operating systems (focusing on Linux environments).
- Dependency Management & Caching: Automate the installation of required CPAN modules, explicitly including testing libraries (`Test::Most`, `Test::Mockingbird`, `Test::Memory::Cycle`, `Test-Returns`). Implement robust caching for CPAN dependencies to accelerate workflow execution.
- Test Execution: Ensure the pipeline runs standard `prove -lr t/`, and explicitly triggers `xt/` author tests if present (specifically enforcing the execution of mutation tests and performance reviews).
- Locale Coverage: Inject environment variables into the test steps to explicitly run the suite under `LC_ALL=en_US.UTF-8` and `LC_ALL=de_DE.UTF-8` to enforce locale resilience.
- Code Quality & Coverage: Add steps to run `Perl::Critic` (ignoring 4-space indent rules), POD checkers, and optionally generate test coverage reports.

# OUTPUT FORMAT
- Provide the complete YAML or configuration file. Use standard, readable YAML formatting.


# GitHub Copilot Instructions for S21 Ultra Kernel

This document provides guidance for GitHub Copilot when working with the Samsung S21 Ultra kernel repository (based on Linux kernel 5.4).

## Coding Style

Follow the Linux kernel coding style as documented in `Documentation/process/coding-style.rst`:

- Use tabs (8 characters) for indentation, never spaces
- Maximum line length is 80 columns (strongly preferred)
- Do not leave whitespace at the end of lines
- Align `switch` and `case` labels in the same column
- Do not put multiple statements on a single line
- Avoid tricky expressions; keep code simple and readable
- Use `fallthrough;` for intentional switch case fallthrough

### Braces and Spacing

- Opening brace on the same line for control structures (if, switch, for, while, do)
- Opening brace on the next line for functions
- Use spaces around binary operators (`+`, `-`, `*`, `/`, `==`, etc.)
- No spaces after unary operators (`!`, `~`, `++`, `--`, etc.)
- No spaces around `.` and `->` structure member operators

### Naming Conventions

- Use lowercase with underscores for function and variable names (e.g., `my_function_name`)
- Use descriptive names; avoid abbreviations unless widely recognized
- Global variables should have descriptive names; local variables can be shorter
- Macro names should be in UPPERCASE

## Patch Submission Requirements

All patches must follow these requirements as specified in the repository's README.md:

### Patch Tags

- Tag patches with type: `UPSTREAM:`, `BACKPORT:`, `FROMGIT:`, `FROMLIST:`, or `ANDROID:`
  - `UPSTREAM:` - Cherry-pick from Linux mainline with no changes
  - `BACKPORT:` - From mainline but requires changes
  - `FROMGIT:` - Merged into upstream maintainer tree but not mainline
  - `FROMLIST:` - Submitted to LKML but not accepted
  - `ANDROID:` - Android-specific patches

### Required Tags

- All patches must include `Change-Id:` tag
- Include `Bug:` tag if an Android bug has been assigned
- All patches must have `Signed-off-by:` tag by author and submitter
- For backports, include `(cherry-picked from commit <sha>)` line
- For FROMGIT, include source repository and branch
- For FROMLIST, include `Link:` to lore.kernel.org submission
- For Android fixes, include `Fixes:` tag citing the buggy patch

### Code Quality

- All patches must pass `scripts/checkpatch.pl`
- Patches must not break `gki_defconfig` or `allmodconfig` builds for arm, arm64, x86, x86_64
- Test changes on multiple configurations (module and built-in)

## Building and Testing

### Build Commands

- Use `make ARCH=arm64 exynos2100-p3sxxx_defconfig` for configuration
- Build with `make ARCH=arm64 -j16` or appropriate thread count
- See `build_kernel.sh` for the standard build script
- Platform version: 11, Android major version: r

### Testing Requirements

- Test changes on at least 4-5 configurations
- Verify both module and built-in kernel builds
- Test on actual hardware when possible

## Security Best Practices

- Never hardcode passwords, keys, or sensitive information
- Validate all user input from userspace
- Use kernel security APIs appropriately (e.g., `copy_from_user`, `copy_to_user`)
- Be aware of race conditions and use appropriate locking mechanisms
- Follow principle of least privilege
- Check return values from all functions

## Documentation

- Document all public APIs and significant functions
- Use kernel-doc format for function documentation
- Update relevant documentation in `Documentation/` when adding features
- Include clear commit messages explaining the "why" not just the "what"
- Reference relevant specifications or hardware documentation

## Memory Management

- Use appropriate kernel memory allocation functions (`kmalloc`, `kzalloc`, `vmalloc`)
- Always check for allocation failures
- Free allocated memory in error paths
- Use kernel reference counting for shared resources
- Be aware of memory barriers and cache coherency issues

## Device Drivers

- Follow the device driver model
- Use device tree bindings where appropriate
- Implement proper power management (suspend/resume)
- Use devm_* managed resource functions when possible
- Follow the subsystem-specific guidelines

## Error Handling

- Use appropriate error codes from `include/uapi/asm-generic/errno-base.h`
- Use `goto` for error cleanup paths (goto-based error handling)
- Clean up resources in reverse order of acquisition
- Log errors appropriately using `pr_err`, `pr_warn`, `dev_err`, etc.

## Comments

- Use `/* */` for multi-line comments
- Use `//` for single-line comments in C99-compatible contexts
- Comment complex algorithms and non-obvious code
- Avoid stating the obvious in comments
- Keep comments up to date with code changes

## Architecture-Specific Notes

This is an ARM64 kernel for Samsung Exynos 2100 platform:

- Use ARM64-specific instructions and features appropriately
- Be aware of cache line sizes and alignment requirements
- Use appropriate memory barriers for ARM64
- Follow Samsung/Exynos-specific conventions in vendor code

## Tools and Scripts

- `scripts/checkpatch.pl` - Validates code style compliance (see Code Quality section)
- `scripts/get_maintainer.pl` - Find appropriate maintainers for patches
- `scripts/checkstack.pl` - Check for excessive stack usage
- `scripts/coccicheck` - Semantic patch checking with Coccinelle

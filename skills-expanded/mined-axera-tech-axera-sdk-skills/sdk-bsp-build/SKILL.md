---
name: sdk-bsp-build
description: Build AX615 BSP and firmware projects, inspect live modules and image dependencies, compile BL1/SPL/FDL, U-Boot, OP-TEE, Linux, RTOS, rootfs and other images, generate full or incremental AXP packages, and verify the exact newly generated artifact. Use this skill whenever a user asks to use ax615-build, ax615-bsp-build, make plist, inspect SUBDIRS, build an AX615 module or image, run clean/all/install, create an AXP, or locate the newest AX615 .axp output.
---

# AX615 BSP Build

Follow the repository selected by the user. Treat its repository root as
`AX615_ROOT`; never hardcode a developer-specific SDK path. This skill combines
the general `$ax615-build` workflow with the AX615 BSP-specific commands below.

## Establish the build context

1. Resolve `AX615_ROOT` from an explicit user path or from the current working
   directory. If the path points into `build/out`, walk up its ancestors until
   the SDK root containing both `build/Makefile` and `build/projects/` is found.
2. Verify the layout before invoking a build:

   ```bash
   test -f "$AX615_ROOT/build/Makefile"
   test -d "$AX615_ROOT/build/projects"
   ```

   Stop and report the missing path if either check fails; do not substitute a
   different SDK tree.
3. Set `PROJECT` from the user's request, the selected project directory, or
   another unambiguous local context. When it is missing or uncertain, do not
   guess. Ask the build system for the live list first:

   ```bash
   make -C "$AX615_ROOT/build" plist
   ```

   Run `plist` in the SDK `build` directory (the `-C` form above changes
   to that directory). Never run `make plist` in `build/out` or its image
   subdirectories. Select a supported `PROJECT` from this live output.

   Prefer that live `plist` result whenever it differs from the reference list
   below.

### Reference project configurations

Keep this reference list for orientation (the live `plist` output is
authoritative):

```text
AX615_haps
AX615_nor
AX615_zebu
AX615_emmc
AX615_nand
AX615_fastnor
AX615_fastnand
AX615_fastemmc
AX615_nand_ddr64
AX615_nor_ddr64
AX615_nor_ddr64_lite
AX615_fastnor_ddr64
AX615_fastnor_ddr64_lite
AX615_fastnand_ddr64
AX615_nand_emmc2sd
AX615_nor_emmc2sd
AX615_nor_ddr64_emmc2sd
AX615_nand_ddr64_emmc2sd
AX615_nor_ddr64_tx
AX615_nor_tx
```

## Discover modules

The file the user called `build/Makefle` is the actual
`$AX615_ROOT/build/Makefile`. Its `SUBDIRS` variable contains all of the
submodules (查看 `SUBDIRS` 就能知道有哪些子模块);
inspect every assignment (including `:=`, `+=`, `?=`, conditional additions,
and continued lines) to learn what this checkout/configuration exposes:

```bash
rg -n -C 2 '^[[:space:]]*SUBDIRS[[:space:]]*(?::=|\+=|\?=|=)' \
  "$AX615_ROOT/build/Makefile"
```

`SUBDIRS` can vary with `PROJECT` and configuration, so do not treat a stale
hard-coded list as authoritative. The BSP-related modules explicitly called
out by the user are:

```text
boot/bl1
boot/uboot
boot/optee
rootfs
```

The Linux and RTOS paths are also covered by this skill and are documented in
their own sections below. Common module locations from the general workflow
are:

```text
app
boot/uboot
boot/bl1
build/projects/$PROJECT
kernel/linux
kernel/osdrv/private_drv
kernel/third_drv
kernel/rtos
msp
rootfs
```

For any unfamiliar module exposed by the live `SUBDIRS`, inspect
its Makefile before assuming that `clean`, `all`, or `install` exists or that
parallel execution is safe.

## Choose a workflow before running it

State `AX615_ROOT`, `PROJECT`, the scope, the exact command, and the expected
artifact before execution. Select the smallest workflow that is valid:

- **full** — a clean complete firmware build, or any case where dependencies
  are uncertain;
- **module** — an isolated module change whose dependencies are known;
- **fast AXP** — required component outputs are already built and installed and
  only packaging is needed.

Do not silently replace one workflow with another. Record the build start time
immediately before the selected command so the resulting AXP can be tied to
this run. Keep these variables in the same shell as the build and verification,
or persist the printed values for the later mtime comparison:

```bash
AX615_BUILD_START_EPOCH=$(date +%s)
AX615_BUILD_START_ISO=$(date --iso-8601=seconds)
```

## Full firmware and AXP build

The canonical full command from `$ax615-build` is:

```bash
make -C "$AX615_ROOT/build" p="$PROJECT" clean all install axp -j64
```

Keep this exact top-level `-j64` command for the general full workflow. It is
not the same as the project image wrapper. Some trees recursively reach image
Makefiles that must not be parallelized; if Makefile inspection or a failure
shows that recursive propagation is unsafe, use the staged module (`-j32` or
confirmed generic `-j64`) plus image/install/AXP no-`-j` commands below and
report that choice explicitly.

The packaging log normally includes the following markers. Check and record
all three when present; do not declare success from a single marker alone:

```text
gen axp xml done!!!
==== Make AXP Script Version: 2.0 ====
----- SUCCESS -----
```

The hard success gates are command exit status `0`, no terminal error or failed
target that invalidates the package, and a `.axp` under
`$AX615_ROOT/build/out` created or updated during this run. If a tool version
omits a normally emitted marker, record that fact and rely on the hard gates
plus the remaining log evidence; a marker without those checks is not success.

## Module builds and parallelism

BL1 and Linux use `-j64`. SPL, FDL, U-Boot, RTOS, and enabled OP-TEE
use the explicit `-j32` commands below.

### BL1, SPL, and FDL

`boot/bl1` contains the two submodules `spl` and `fdl`.

Build all of BL1 from any directory:

```bash
make -C "$AX615_ROOT/boot/bl1" p="$PROJECT" clean all install -j64
```

Equivalently, enter the BL1 directory and run the same target sequence:

```bash
cd "$AX615_ROOT/boot/bl1"
make p="$PROJECT" clean all install -j64
```

Build only SPL:

```bash
cd "$AX615_ROOT/boot/bl1/spl"
make p="$PROJECT" clean all install -j32
```

Build only FDL:

```bash
cd "$AX615_ROOT/boot/bl1/fdl"
make p="$PROJECT" clean all install -j32
```

### U-Boot

```bash
make -C "$AX615_ROOT/boot/uboot" p="$PROJECT" clean all install -j32
```

### Linux

```bash
make -C "$AX615_ROOT/kernel/linux" p="$PROJECT" clean all install -j64
```

### RTOS

The user wrote “rots”; the module path is `kernel/rtos`:

```bash
make -C "$AX615_ROOT/kernel/rtos" p="$PROJECT" clean all install -j32
```

### OP-TEE

OP-TEE is project-dependent: compile it only when the selected project
configuration sets `SUPPORT_OPTEE=TRUE`. Inspect the effective configuration
before building it; when FALSE or not enabled, do not build OP-TEE. Do not
assume that every project includes this module.

```bash
make -C "$AX615_ROOT/boot/optee" p="$PROJECT" clean all install -j32
```

For other ordinary modules, the general example remains:

```bash
make -C "$AX615_ROOT/<module>" p="$PROJECT" clean all install -j64
```

Use that `-j64` only after inspecting the module Makefile and confirming its
targets and parallel behavior. The explicit `-j32` rules above take priority
over this generic example.

`$AX615_ROOT/build/projects/$PROJECT` is a special case: its Makefile does not
support parallel execution, so never pass any `-j` option there:

```bash
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" clean all install
```

The same no-`-j` rule applies to the rootfs/image commands in the next section.

## rootfs, opt/customer, and other images

Build `rootfs/opt/customer` and the other project images together using either
of the following commands. Neither command may contain `-j`—注意这里不能带
`-j` 参数（即“不能带-j参数”，包括 `-j32` 和 `-j64`）：

```bash
make -C "$AX615_ROOT/rootfs" p="$PROJECT" clean all install
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" clean all install
```

Build only `rootfs_image` (also no `-j`; 这里不能带-j参数):

```bash
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" clean all rootfs_image
```

Build only `customer_image` (also no `-j`; 这里不能带-j参数):

```bash
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" clean all customer_image
```

Discover the image set by inspecting the prerequisites of the `install` target
in `$AX615_ROOT/build/projects/$PROJECT/Makefile`. For example, the
`AX615_emmc` project contains:

```make
install: rootfs_image soc_image opt_image param_image
```

That example means `install` depends on four images: `rootfs_image`,
`soc_image`, `opt_image`, and `param_image`. Other projects can have a
different set; do not assume this example is universal.

When a file is modified, analyze the Makefile to determine which image
receives its output, then build that image. If the ownership is uncertain, the
simplest safe choice is to build all images together（最简单的办法就是所有
image 一起编译）. The project wrapper and
image Makefiles must remain non-parallel even when other modules were built
with `-j32` or a confirmed generic `-j64`.

## AXP generation

Generate an AXP from already installed outputs with either supported entry
point:

```bash
make -C "$AX615_ROOT/build" p="$PROJECT" axp
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" axp
```

This is normally done after rootfs/opt/customer (and any other required image)
builds. If images and packaging need to be performed together, use the project
wrapper exactly as follows—there is deliberately no `-j` option（注意这里不能
带 `-j` 参数）：

```bash
make -C "$AX615_ROOT/build/projects/$PROJECT" p="$PROJECT" clean all install axp
```

For the fast AXP workflow, first confirm that the top-level full build
(`clean all install axp -j64`) has succeeded for the same `PROJECT` in this
SDK. Without that successful build, complete the full workflow first.

The wrapper packages the currently installed component outputs. It is not a
substitute for rebuilding and installing a changed module; otherwise the AXP
can contain stale content. The top-level full command with `-j64` remains the
separate general full-workflow command shown earlier.

## Verify the AXP artifact

`$AX615_ROOT/build/out` may contain many historical packages. Never report an
arbitrary `*.axp` glob match. Prefer the bundled helper (where `<skill-dir>`
is this skill's directory):

```bash
"<skill-dir>/scripts/find-latest-axp.sh" "$AX615_ROOT/build/out"
```

If the skill directory or helper is unavailable, use this exact fallback:

```bash
find "$AX615_ROOT/build/out" -type f -name '*.axp' -printf '%T@\t%TY-%Tm-%Td %TH:%TM:%TS\t%p\n' \
  | sort -nr
```

(`%T@` is the GNU `find` form for modification epoch.) A useful extended
variant also prints size:

```bash
find "$AX615_ROOT/build/out" -type f -name '*.axp' \
  -printf '%T@\t%TY-%Tm-%Td %TH:%TM:%TS\t%s\t%p\n' | sort -nr
```

Compare the newest candidate's modification epoch with
`AX615_BUILD_START_EPOCH`. Confirm that it was created or updated by this
build, not merely that an older AXP exists. Report the absolute path,
modification timestamp, and byte size; include a SHA256 when useful:

```bash
sha256sum "/absolute/path/to/artifact.axp"
```

If no AXP is new or updated during the current run, report the build as
incomplete or packaging as unverified, even if the output directory contains
older packages.

## Failure handling and result report

On failure, retain the first failing target and the relevant error block, but do
not dump the entire log unless requested. Distinguish a compile/install failure
from an AXP packaging or artifact-verification failure.

Return a concise summary containing:

1. `AX615_ROOT` and `PROJECT`;
2. selected workflow (`full`, `module`, or `fast AXP`) and scope;
3. exact command and its exit status;
4. decisive success markers and/or the first failing target/error block;
5. newest AXP absolute path, timestamp, size, SHA256 when available, and an
   explicit `created/updated during this run: yes|no` result;
6. any unverified assumption and the next action needed.

## Rule priority

Apply rules in this order when examples appear to conflict:

1. explicit module commands: `-j64` for BL1 and Linux; `-j32` for
   SPL/FDL, U-Boot, RTOS, and OP-TEE only when `SUPPORT_OPTEE=TRUE`;
2. the explicit no-`-j` rule for `rootfs`, image targets, and
   `build/projects/$PROJECT`;
3. the general ordinary-module `-j64` rule only after Makefile inspection;
4. the separate top-level full-build reference command, which intentionally
   retains `-j64`.

Always explain the selected command and any staged fallback before execution.

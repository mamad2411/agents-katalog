---
name: debug
description: Find why an FPGA build failed (Vivado, HLS, PetaLinux) and how to fix it.
argument-hint: "[log file or project folder]"
disable-model-invocation: true
---
Find why the FPGA build failed. Arguments ($ARGUMENTS) are a log file or a project folder; if none, use the current
folder and the logs with errors that the build summary lists first.
Read `../fpga-project-analyzer/SKILL.md` (relative to this file's directory) and follow it: `logs` for the log,
`build` + `show` to locate the cause in the design. Reply with the root cause, where it is (file:line or block),
and the exact fix.

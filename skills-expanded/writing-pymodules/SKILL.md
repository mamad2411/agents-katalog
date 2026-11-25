---
name: writing-pymodules
description: Describes how to build and test PyModules (Python modules for RISC OS Pyromaniac). Use when understanding, updating or creating PyModules to implement a RISC OS module for Pyromaniac.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-run:*) Bash(riscos-basic:*) Bash(bash:*)
---
# Pyromaniac

RISC OS Pyromaniac is a Python implementation of RISC OS.
It has modules just like RISC OS, called PyModules.

You can load a PyModule and test it with:

```
riscos-run --load-pymodule <pymodule-filename> --command '<riscos command>'
```

You can also mix a PyModule with native RISC OS modules in the same run:

```
riscos-run --load-pymodule <pymodule-filename> \
           --load-module <c-module>,ffa \
           --command '<riscos command>'
```

`riscos-run` already loads the standard system module set (BASIC, SCL,
FPEmulator, Obey) by default, so you do not need `--load-module` for those.
If you want exact control over which modules are present instead of that
default set, use the lower-level `pyro` command directly with
`--load-internal-modules` (for OS commands such as `Basic`, `Dir`, or
`Help`) and `$ROSYSMODULES` (the directory containing the shipped system
modules) to load just what you need:

```
pyro --load-internal-modules --load-module $ROSYSMODULES/BASIC,ffa \
     --command '<riscos command>'
```

If you had a BASIC program you wanted to use to test your module you could use:

```
riscos-run --load-pymodule <pymodule-filename> --command 'Run <basic-filename>'
```

You cannot pass BASIC statements to the `--command` arguments.

For tests, pass the host filename to `riscos-run`, and use the RISC OS
filename in the command:

```
riscos-run --load-pymodule newmodule.py --command 'Run TestModule' TestModule,fd1
```

---

## General Pyromaniac Structure (`riscos/`)

While the `PyModule` system handles modular extensions, the core OS logic is implemented directly in Python:

- **`riscos/quotedstrings.py`**: Provides the `QuotedStrings` class, essential for parsing command lines. It correctly handles space-separated arguments and double-quoted strings.
- **`riscos/readargs.py`**: Contains the core logic for `OS_ReadArgs`. When implementing this in C, remember that keyword definitions can be complex (e.g., abbreviations via the first character).
- **`riscos/evaluateexpression.py`**: Handles RISC OS expressions.
- **`riscos/gstrans.py`**: Handles string translation.
- **`riscos/sysvars.py`**: Handles system variables.
- **`riscos/vectors.py`**: Handles vector registration and dispatch.
- **`riscos/ticker.py`**: Handles timer registration and dispatch.
- **`riscos/kernel.py`**: Handles core kernel functionality (from booting and memory setup through SWI execution, to callbacks and tracing functions).
- **`riscos/bufferdata.py`**: Provides interfaces for writing to user buffers, with tracking of overflow and maximum data sizes (used by interfaces like file enumeration).
- **`riscos/swis/`**: Contains the SWI dispatchers. These often call into the core logic modules (like `readargs.py`).

For ports of existing C modules, also check the exported interface files in `/riscos-resources/Export/`:

- **`C/h/*SWIs`**: Usually defines the SWI numbers and register contracts.
- **`Hdr/Interface/*`**: Usually defines the SWI chunk and public interface names.

These exported files are often the quickest way to recover the exact module interface when the original source is incomplete or absent.

Also check local documentation before implementing:

- **`prminxml/`**: PRM-in-XML interface documentation. Prefer this for externally documented SWI contracts, error numbers, system variables, examples, and register preservation rules.
- **`docs/`**, **`built/docs/`**, or similar documentation directories: These may contain generated HTML/XML manuals or older user-facing references.
- **Existing examples/tests**: BASIC files such as `test*,fd1` often encode expected register values and edge cases.

When new public interface documentation is needed for a PyModule or for behaviour discovered during a port, create or update the source documentation in `prminxml/`; generated documentation should be rebuilt from there rather than hand-edited.

When porting from C, preserve observable C behaviour rather than only the apparent high-level intent:

- Preserve register inputs that are needed after output registers are updated, such as buffer pointers and buffer lengths.
- Match documented error numbers. PyModule errors can use explicit-number descriptors like `('BufferOverflow', 0x1e5, "Buffer overflow")`.
- Use XSWI calls in tests for error returns, so tests can check the returned error block and any updated output registers.
- Preserve C integer arithmetic where it affects matching or scoring. Python 2 integer division matches C integer division for integer operands; Python 3-style assumptions may change results.
- If a SWI has a length-only mode, test both that mode and the buffer-writing path.

When a PyModule is a compatibility layer over host services or Python standard
library code, preserve the RISC OS-visible contract rather than mirroring the
host API shape. In practice that means:

- keep SWI names, register contracts, and session handles stable
- translate host/library exceptions into the documented RISC OS error model
- preserve response formats and status words expected by callers
- test the public interface from BASIC, assembly, or `--command`, not only by
  calling the Python helper methods directly

When converting a PyModule to C:

- Compare the PyModule's `swi_names` with these exported interface files and any PRM-in-XML documentation before accepting scaffolded CMHG names. Skeletons generated from incomplete type information may use a longer handler-oriented name, while the public SWI name in the PyModule and exported header is the compatibility contract.

### Source code location

If not supplied by the user, the sources for RISC OS Pyromaniac can be found at `/riscos-resources/Install/Tools/Linux/pyromaniac-resources`. This directory is only present when the Build Environment has been distributed with the Pyromaniac tool.

---

## Python version

Pyromaniac uses **Python 2.7**, which has specific requirements:

* Use inheritance from `object` on all classes which would otherwise not inherit.
* `print` statements may have `(` around their parameters (this is safe in Python 2.7 and makes transition to Python 3 safer).
* Use `super(ClassName, self)`, not Python 3 argument-less `super()`.
* Do not use f-strings, keyword-only arguments, or Python 3 `bytes`/`str` assumptions.
* Be careful with dictionary/set ordering in tests; Python 2.7 does not preserve insertion order.


## Error Handling

### Error Definitions

Define errors with `error_base` and `errors` list in your PyModule class:

```
class JUnitXML(PyModule):
    error_base = 0x840000
    errors = [
        ('CreateFailed', "Failed to create JUnitXML handle"),
        ('CreateSuiteFailed', "Failed to create test suite"),
        ('CloseSuiteFailed', "Failed to close test suite"),
        ('BadSuiteOp', "Unknown TestSuite operation"),
        ('CreateCaseFailed', "Failed to create test case"),
        ('CloseCaseFailed', "Failed to close test case"),
        ('BadCaseOp', "Unknown TestCase operation"),
        ('CloseFailed', "Failed to close JUnitXML handle"),
        ('NoHandle', "No JUnitXML handle to close"),
        ('InitFailed', "Failed to initialise JUnitXML state"),
    ]
```

Error numbers are assigned sequentially from `error_base`:
- `CreateFailed` - &840000
- `CreateSuiteFailed` - &840001
- `CloseSuiteFailed` - &840002
- etc.

If a specific error number is documented, include it explicitly in the descriptor:

```
errors = [
    ('BadFlags', "Reserved bits set"),
    ('BufferOverflow', 0x1e5, "Buffer overflow"),
]
```

### Raising Errors

Use `self.error()` to raise defined errors:

```
def swi_create(self, regs):
    handle = self._create_handle()
    if handle < 0:
        raise self.error('CreateFailed')

    regs[0] = handle
    return True

def swi_testsuite(self, regs):
    handle = self.handles.get(handle_id)
    if not handle:
        raise self.error('NoHandle')

    if op == JUnitXML_TestSuite_OpUpdate:
        raise self.error('BadSuiteOp')
```

### Error Message Override

You can override the error message if needed:

```
raise self.error('BadSuiteOp', 'Custom error message')
```

---

## Module commands

A very basic PyModule might would look like this:

```
from riscos.modules.pymodules import PyModule
from riscos.errors import RISCOSSyntheticError


class NewModule(PyModule):
    version = '0.01'
    date = '26 Mar 2026'

    commands = [
            ('TestCommand', 'A Test command', 0x010000),
        ]

    def cmd_testcommand(self, args):
        """
        Syntax: TestCommand [<arg>]
        """
        self.ro.kernel.writeln("TestCommand: %r" % (args,))
```

Which would provide one command.

You could test it with a command like this:

```
riscos-run --load-pymodule newmodule.py --command 'TestCommand hello world'
```

---

## Module SWIs

A module with SWIs would look like this:

```
from riscos.modules.pymodules import PyModule
from riscos.errors import RISCOSSyntheticError


class ModuleWithSWIs(PyModule):
    version = '0.01'
    date = '26 Mar 2026'
    swi_base = 0xC0540
    swi_prefix = "SWITest"
    swi_names = [
            "FirstSWI",
        ]

    def __init__(self, ro, module):
        super(ModuleWithSWIs, self).__init__(ro, module)
        self.swi_dispatch = {
                0: self.swi_firstswi,
            }

    def swi(self, offset, regs):
        func = self.swi_dispatch.get(offset, None)
        if func:
            return func(regs)

        return False

    def swi_firstswi(self, regs):
        self.ro.kernel.writeln("SWI called with R0 = %i" % (regs[0],))
        regs[0] = regs[0] + 1
        return True
```

Which provides one SWI and will print a message and increment R0.

The SWI functions:

* SWI parameters are passed in the `regs` array, and can be accessed using array syntax, eg `regs[0]`.
* Signed values can be accessed using `regs.signed[0]`
* Use dispatch dictionaries to determine the SWI methods to call, for speed.
* If the original C interface compares a string parameter by pointer identity, preserve the raw register value as well as the decoded string. `self.ro.memory[regs[0]].string` gives you the text, but not the original pointer for identity comparisons.
* If you are porting a module which depends on another module, keep the module boundary intact and call through the SWI interface rather than importing implementation details directly.

The return from SWI calls has the following values:

- Return `True` - SWI handled successfully
- Return `False` - SWI not handled (will try next module)
- Raise `self.error()` - Return error to caller
- Raise `RISCOSSyntheticError()` - Return error to caller, for errors which are not defined in the header (rare).


You could test it by creating a BASIC program that looked like this:

```
SYS "SWITest_FirstSWI", 99 TO result%
IF result% = 100 THEN
  PRINT "SUCCESS!"
ELSE
  ERROR 0, "Failed - returned " + STR$result
ENDIF
```

Then test the two together with a command like this:

```
riscos-run --common --load-pymodule newmodule.py --command 'Run TestModule'
```

## Memory Access

Pyromaniac provides convenient access to RISC OS memory through `self.ro.memory[address]`.

Use [references/memory-and-io.md](references/memory-and-io.md) for:

- string, word, dword and byte access patterns
- quin to datetime conversion
- RISC OS file I/O through `self.ro.kernel.api.open`
- SWI calling conventions and iterable `args`

Be careful with `read_words(size)` and `write_words(...)`: the `size` argument is a byte size, not a word count.


---

## Calls to SWIs

SWIs can be called through `self.ro.kernel.api`.
There are SWI interfaces present for most common SWIs.
Output to the screen using `OS_Write*` SWIs can be achieved most efficiently by using:

* `self.ro.kernel.write(str)` to write a string to the output.
* `self.ro.kernel.writeln(str)` to write a string to the output followed by a newline.

When there is no convenience wrapper, use `self.ro.kernel.api.swi(<swi_number>, args=[...])` or `regs={...}` to call the SWI directly. This is also the preferred way for one PyModule to call another, as it preserves the real module interface boundary.

---

## Service Calls

PyModules can receive service calls through `service(self, service, regs)` and announce them through the Pyromaniac dispatcher.

Use [references/service-announcements.md](references/service-announcements.md) for:

- claiming a received service by returning `True`
- issuing services with `self.ro.services.dispatch(..., preserve=True)`
- deferring startup announcements with `OS_AddCallBack` and removing pending callbacks on finalisation

If your module caches data derived from the current display or palette state, consider invalidating it on relevant services such as `Service_ModeChanging`, `Service_SwitchingOutputToSprite`, and `Service_DisplayChanged`.


---

## Custom Entry Points (Vectors & Callbacks)

Beyond SWIs and Commands, PyModules can define custom entry points for use with vectors (e.g., `OS_Claim`) or as callable function addresses passed to clients.

- **Definition**: Add the names to `entrypoint_names` in your class definition.
- **Dispatch**: Implement a method with the same name. It will receive the `regs` object.
- **Address Retrieval**: Access the generated RISC OS address via `self.module.entrypoints['name'].address`.

```python
class MyModule(PyModule):
    entrypoint_names = ['my_vector_handler']

    def initialise(self, arguments, pwp):
        # Claim a vector using the generated entry point address
        self.ro.kernel.api.os_claim(vectors.MyV,
                                    self.module.entrypoints['my_vector_handler'].address,
                                    self.pwp.address)

    def my_vector_handler(self, regs):
        # Handle the vector call
        return True # Return True to claim, False to pass on
```

If vectors are claimed this way, they must be released in the finalisation method.

### Return convention: how `entrypoint_dispatch` returns

Entry points have **two distinct return paths**:

- **`return False`** (not claimed): Pyromaniac sets `regs.pc = regs.lr` — the standard
  `MOV pc, lr` subroutine return. The OS vector dispatcher will call the next handler in
  the chain.

- **`return True`** (claimed): Pyromaniac pops the return PC from the stack:
  `regs.pc = memory[regs.sp]; regs.sp += 4`. This mirrors the RISC OS convention where
  the vector dispatcher pushes the original caller's return address before invoking the
  chain, and a claiming handler returns through that pushed address.

**When using OS vectors**, the OS manages the stack push automatically, so the Python handler
does not need to worry about this.

**When using an entry point as a custom function pointer** (e.g. a colour mapping descriptor,
a callback passed directly to a client), the *caller* in ARM code must push the return address
onto the stack before jumping to the entry point address. See
[references/entrypoint-calling-convention.md](references/entrypoint-calling-convention.md) for
the correct BASIC shim and full details.

### R12 and module instance identification

`entrypoint_dispatch` scans module instances looking for one whose `privateword_pointer.address`
matches R12. If none matches, it falls back to the **preferred instance** (the most recently
initialised instance). This means:

- When used with `OS_Claim`, pass `self.pwp.address` as the R12 value (the third argument).
- When used as a custom function pointer with a different R12 (e.g. a workspace pointer),
  dispatch still succeeds as long as there is only one instance of the module loaded.
- If the module may have multiple instances, store `self.pwp.address` in the descriptor's
  workspace field and retrieve the actual workspace from the private word inside the handler.

---

## Debugging with `debug_register_ivar`

To support the `--debug <name>` command-line flag, use the `debug_register_ivar` registration mechanism.

- **Initialization**: Define a boolean `self.debug_<name>` in `__init__`.
- **Registration**: Call `self.ro.debug_register_ivar('<name>', self)`.
- **Usage**: Use standard Python `print` statements (not `kernel.writeln`) wrapped in checks of the debug flag.

```python
def __init__(self, ro, module):
    super(MyModule, self).__init__(ro, module)
    self.debug_mymod = False
    self.ro.debug_register_ivar('mymod', self)

def some_method(self):
    if self.debug_mymod:
        print("Debugging info...")
```

---

## Private Word Access

The module's private word pointer address is available via `self.pwp.address`. This is typically passed as the `handle` (R2) when claiming vectors or registering for services.

---

## Vector Handler Return Values

When an entry point is used as a vector handler (e.g., via `OS_Claim`):
- Returning `True` is equivalent to claiming the vector (the handler returns to the caller of the vector).
- Returning `False` is equivalent to passing the vector on (the handler returns to the next claimant in the chain).
- This behavior is handled by `entrypoint_dispatch` in `pymodules.py`, which adjusts the `pc` based on the return value.


---

## Integration Tests

PyModule tests live in `testcode/` and use a gold-master comparison approach.

Run them with:

```
make tests TEST=<suite-name>
```

Use [references/testing-pymodules.md](references/testing-pymodules.md) for:

- suite file structure
- parameterised tests
- replacement scripts
- expectation file creation
- registering suites in `testcode/tests.txt`

For simple SWI smoke tests, a small BASIC file in `testcode/` is often the quickest validation path. Remember:

- `./pyro.py --command` and `riscos-run --command` execute OSCLI commands, not BASIC statements.
- If you need `MODE`, `SYS`, or other BASIC-only operations, put them in a BASIC file and run it with `--command 'Run <riscos-filename>'`.
- Use RISC OS path syntax in guest commands, for example `Run testcode.module_smoke`, not host-style slash-separated paths.

---

## References

* If you need to convert a PyModule to or from C, refer to [references/convert-to-c.md](references/convert-to-c.md), and use the skills `writing-cmodules` and `using-cmhg`.
* Service announcement patterns, including callback-based startup announcements, are in [references/service-announcements.md](references/service-announcements.md).
* Memory access, RISC OS file I/O, and SWI calling details are in [references/memory-and-io.md](references/memory-and-io.md).
* PyModule integration test structure is in [references/testing-pymodules.md](references/testing-pymodules.md).
* Entrypoint return convention and custom function pointer calling from ARM/BASIC are in [references/entrypoint-calling-convention.md](references/entrypoint-calling-convention.md).
* If you need more information on the testing file format, use the skill `using-tooltester`.
* An example stub module is can be found in `assets/stub.py`

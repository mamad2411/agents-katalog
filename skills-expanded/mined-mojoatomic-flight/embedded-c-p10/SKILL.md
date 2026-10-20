---
name: embedded-c-p10
description: "Embedded C patterns for P10 targets — memory safety, register access, ISR. Use when writing or reviewing embedded .c/.h files."
user-invocable: true
---

# Domain: Embedded-C-P10 Design

Safety-critical embedded C following NASA JPL's "Power of 10" rules for reliable software. Reference: Gerard J. Holzmann, "The Power of 10: Rules for Developing Safety-Critical Code", IEEE Computer, 2006.


**Validation:** `embedded-c-p10.validate.sh` enforces NEVER/MUST rules. SHOULD rules trigger warnings. GUIDANCE is not mechanically checked.


## Invariants

### NEVER (validator will reject)

1. **No goto** - Never use goto. It creates unstructured control flow that is difficult to analyze and verify. Use structured control flow (if, while, for, switch) instead.

   ```
   // BAD
   goto cleanup;
   // BAD
   goto error_handler;

   // GOOD
   return STATUS_ERROR;
   // GOOD
   if (error) { cleanup(); return STATUS_ERROR; }
   ```

2. **No setjmp/longjmp** - Never use setjmp or longjmp. They create non-local jumps that bypass normal control flow and make code impossible to analyze statically.

   ```
   // BAD
   if (setjmp(buf) == 0) { ... }
   // BAD
   longjmp(buf, 1);

   // GOOD
   return STATUS_ERROR;
   // GOOD
   Use structured error handling with return codes
   ```

3. **No Dynamic Memory Allocation** - Never use malloc, free, calloc, or realloc. Dynamic memory allocation introduces unpredictable behavior, fragmentation, and potential for memory leaks. Use static allocation with fixed-size buffers.

   ```
   // BAD
   char *buf = malloc(size);
   // BAD
   free(ptr);
   // BAD
   ptr = realloc(ptr, new_size);

   // GOOD
   static char buffer[MAX_BUFFER_SIZE];
   // GOOD
   char local_buf[FIXED_SIZE];
   ```

4. **No Conditional Compilation** - Never use #ifdef or #if. Conditional compilation creates multiple code paths that may not all be tested. Use runtime configuration or compile separate variants.

   ```
   // BAD
   #ifdef DEBUG
   // BAD
   #if FEATURE_ENABLED

   // GOOD
   #include <stdint.h>
   // GOOD
   #define MAX_ITEMS 100U
   ```

5. **No Double Pointer Dereference** - Never use double pointer dereference (**ptr). It indicates overly complex data structures. Flatten data structures or use single indirection with explicit indexing.

   ```
   // BAD
   **ptr = value;
   // BAD
   result = **data;

   // GOOD
   *ptr = value;
   // GOOD
   array[index].field = value;
   ```

6. **No Chained Pointer Access** - Never chain pointer dereferences (->field->field). It indicates overly coupled data structures. Use local variables to break the chain.

   ```
   // BAD
   value = ptr->inner->data;
   // BAD
   ptr->next->prev = node;

   // GOOD
   inner_t *inner = ptr->inner;
   value = inner->data;
   
   ```

7. **No Unbounded Loops** - Never use unbounded loops (while(1), while(true), for(;;)). All loops must have a compile-time upper bound that can be statically verified. Runtime values are not acceptable as loop bounds — use the compile-time maximum and break early if needed.

   ```
   // BAD
   while (1) { ... }
   // BAD
   while (true) { ... }
   // BAD
   for (;;) { ... }
   // BAD
   for (uint32_t i = 0U; i < runtime_count; i++) { ... }

   // GOOD
   for (uint32_t i = 0U; i < MAX_ITERATIONS; i++) { ... }
   // GOOD
   #define MAX_ENTRIES 32U
   for (uint32_t i = 0U; i < MAX_ENTRIES; i++) {
       if (i >= actual_count) { break; }
       ...
   }
   ```

8. **Compile Clean with Strict Warnings** - Code must compile without warnings using strict compiler flags: -Wall -Wextra -Werror -pedantic -std=c11. Any warning is an error.

   ```
   // BAD
   // Code that produces any warning

   // GOOD
   // Code that compiles cleanly with all warnings enabled
   ```

9. **Functions Must Be 60 Lines or Less** - Every function must be 60 lines or less. This ensures functions fit on one screen and are easier to understand, test, and verify.

   ```
   // BAD
   // Function with more than 60 lines

   // GOOD
   // Function with 60 lines or less
   ```

10. **Minimum 2 Assertions Per Function** - Every function must have at least 2 ASSERT() calls - typically one for preconditions (input validation) and one for postconditions (output validation).

   ```
   // BAD
   status_t func(int *ptr) {
     // No assertions
     return STATUS_OK;
   }
   

   // GOOD
   status_t func(int *ptr) {
     ASSERT(ptr != NULL);
     // implementation
     ASSERT(result == STATUS_OK || result == STATUS_ERROR);
     return result;
   }
   
   ```

11. **Check or Cast All Return Values** - All function return values must be checked or explicitly cast to (void) if intentionally ignored. This applies especially to printf and fprintf.

   ```
   // BAD
   printf("Hello");
   // BAD
   fprintf(fp, "data");

   // GOOD
   (void)printf("Hello");
   // GOOD
   int ret = fprintf(fp, "data"); ASSERT(ret > 0);
   ```

12. **Pointer Indexing Only on Declared Arrays** - Array indexing (`ptr[n]`) is only permitted on named, statically-declared arrays, not on pointer parameters or arbitrary `const char *` values. Indexing a pointer is pointer arithmetic in disguise. When you must index into a pointer (e.g., string parsing), use a local array copy or document the framework accommodation.

   ```
   // BAD
   const char *type_ptr = strstr(body, "type=");
   char val = type_ptr[5];
   // BAD
   result = some_ptr[offset];

   // GOOD
   static char body[MAX_BODY];
   char val = body[known_index];
   // GOOD — framework accommodation (documented)
   /* P10 R8 accommodation: indexing strstr result for fixed-offset parse */
   const char *type_ptr = strstr(body, "type=");
   char val = type_ptr[5];
   ```

### GUIDANCE (not mechanically checked)

1. **Simple Control Flow** - Use only simple control flow constructs: if, else, for, while, do-while, switch with default. No goto, setjmp, longjmp.


2. **Fixed Loop Bounds Pattern** - All loops must have a compile-time verifiable upper bound. See NEVER #7.


3. **Static Memory Only** - Use only static memory allocation. No heap allocation.


4. **Minimal Scope Principle** - Declare variables at the smallest possible scope and initialize at declaration.


5. **Limited Preprocessor Usage** - Use preprocessor only for includes and constant definitions. No conditional compilation.


6. **Function Template** - Standard function template with assertions and status return.


7. **Status Codes Pattern** - Standard status code enumeration for function return values.


8. **ASSERT Macro Pattern** - Custom ASSERT macro that captures file, line, and expression.


9. **No Magic Numbers** - All numeric constants must be named with #define or enum.


10. **No Recursion** - Never use recursion. It makes stack usage unpredictable and can lead to stack overflow. Use iteration instead.


### SHOULD (validator warns)

1. **Saturating Counters** - Counters that only increment should saturate at their maximum value instead of wrapping. Wrapping counters can produce misleading telemetry (e.g., a heartbeat sequence that wraps to 0 looks like a reset). Use a saturating increment pattern.

   ```
   // BAD — wraps silently at UINT32_MAX
   heartbeat_seq++;

   // GOOD — saturates at max
   if (heartbeat_seq < UINT32_MAX) { heartbeat_seq++; }
   ```


## Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| goto |  | Use structured control (if/while/for) |
| setjmp/longjmp |  | Use return codes |
| malloc/free |  | Static allocation only |
| #ifdef/#if |  | Compile separate variants |
| **ptr |  | Flatten structures |
| ->-> |  | Use local variables |
| while(1) |  | Use bounded loop with MAX |
| Magic numbers |  | Named constants (#define) |
| Recursion |  | Use iteration |
| Unchecked return |  | Check or cast to (void) |
| Runtime loop bound |  | Use compile-time MAX, break early |
| ptr[n] on pointer param |  | Index only declared arrays |
| Wrapping counter |  | Saturate at UINT32_MAX |

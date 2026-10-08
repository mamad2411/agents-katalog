# ROPKit Cursor Rules

This file defines coding standards and best practices for the ROPKit codebase.
These rules are based on GNU C style conventions and patterns established throughout the project.

## Code Style: GNU C Formatting

### Indentation and Spacing
- Use 8-space tabs for indentation (not spaces)
- Maximum line length: 80 columns
- Function return types MUST be on a separate line from the function name
- Opening braces for functions go on a new line
- Opening braces for control structures (if, while, for, switch) go on the same line
- Pointer alignment: Right-aligned asterisks (e.g., `char *const`, `FILE *const`, `void *ptr`)

**Good:**
```c
char *
get_next_line(FILE *const fp, int *error)
{
	if (condition) {
		// code
	}
}
```

**Bad:**
```c
char* get_next_line(FILE* const fp, int* error) {  // Wrong: return type on same line, wrong pointer alignment
	if (condition)
	{  // Wrong: brace placement
		// code
	}
}
```

### Pointer Declarations
- Always use right-aligned asterisks: `char *ptr`, `struct Node *node`
- For const pointers: `FILE *const fp` (pointer is const), `const char *str` (pointed-to data is const)
- Never use left-aligned or middle-aligned asterisks

## Documentation Standards: Kernel-Doc Style

### File Headers
Every source file (.c and .h) MUST start with a kernel-doc style header comment:

```c
/**
 * File: filename.c
 *
 * Description:
 * Brief description of what this file contains and its purpose.
 * Can span multiple lines as needed.
 *
 * Author: snocra5h@icloud.com
 * Date: July 19, 2023
 */
```

### Function Documentation
Every function MUST have kernel-doc style comments with @param and @return:

```c
/**
 * get_next_line() - Read a line from a file
 * @fp: Pointer to the file
 * @error: Pointer to an integer for error code
 *
 * This function reads a line from the provided file and returns a pointer
 * to a heap-allocated string containing the line. The string does not
 * include the newline character at the end of the line.
 *
 * Return: Pointer to the line on success, or NULL on end of file or error.
 */
char *
get_next_line(FILE *const fp, int *error);
```

### Struct Documentation
Document structs with @member syntax:

```c
/**
 * struct Gadget - A struct that represents a gadget in ROP context
 * @address: The starting address of the gadget in memory
 * @n_opcodes: The number of opcodes in the gadget
 * @opcodes: An array of strings, where each string represents an opcode
 * @full_gadget: A string representation of the complete gadget
 */
typedef struct Gadget {
	unsigned long address;
	int n_opcodes;
	char opcodes[NUM_OPCODES][MAX_BUFFER + 1];
	char full_gadget[MAX_BUFFER + 1];
} Gadget;
```

### Enum Documentation
Document enums with explanations:

```c
/**
 * Error codes used throughout the application
 * @FUNCTION_SUCCESS: Operation completed successfully
 * @MALLOC_SIZE_OVERFLOW: Memory allocation size would overflow
 * @MALLOC_HEAP_ISSUE: Memory allocation failed due to heap issue
 * @STRTOL_CRITICAL: Critical error in strtol conversion (errno set)
 * @STRTOL_FAIL: strtol conversion failed (invalid input)
 * @FILE_EOF_FLAG: End of file reached
 * @FILE_OPEN_FAIL: File open operation failed
 * @PLATFORM_UNSUPPORTED: Unsupported platform detected
 * @LIBRARY_NOT_FOUND: Required library missing
 * @BINARY_PARSE_INVALID_HEADER: Binary header is invalid or corrupted
 * @BINARY_PARSE_UNSUPPORTED_VERSION: Binary format version not supported
 * @BINARY_PARSE_SECTION_NOT_FOUND: Requested section not found
 * @BINARY_PARSE_READ_ERROR: Error reading from binary file
 * @BINARY_PARSE_SEEK_ERROR: Error seeking in binary file
 */
enum {
	FUNCTION_SUCCESS,
	MALLOC_SIZE_OVERFLOW,
	MALLOC_HEAP_ISSUE,
	STRTOL_CRITICAL,
	STRTOL_FAIL,
	FILE_EOF_FLAG,
	FILE_OPEN_FAIL,
	PLATFORM_UNSUPPORTED,
	LIBRARY_NOT_FOUND,
	BINARY_PARSE_INVALID_HEADER,
	BINARY_PARSE_UNSUPPORTED_VERSION,
	BINARY_PARSE_SECTION_NOT_FOUND,
	BINARY_PARSE_READ_ERROR,
	BINARY_PARSE_SEEK_ERROR
};
```

## Error Handling: Robust Error Code Patterns

### Error Code Propagation
- Functions that can fail MUST accept an `int *error` parameter
- Use error codes from the enum in `common.h`: `FUNCTION_SUCCESS`, `MALLOC_SIZE_OVERFLOW`, `MALLOC_HEAP_ISSUE`, `STRTOL_CRITICAL`, `STRTOL_FAIL`, `FILE_EOF_FLAG`, `FILE_OPEN_FAIL`, `PLATFORM_UNSUPPORTED`, `LIBRARY_NOT_FOUND`, `BINARY_PARSE_*` codes
- Always check error codes after function calls
- Set `*error = FUNCTION_SUCCESS` at the start of functions before any operations
- Use `set_error()` helper function from `common.h` when error pointer may be NULL

**Good:**
```c
Gadget *
get_next_gadget(FILE *const fp, int *error)
{
	*error = FUNCTION_SUCCESS;
	char *line = get_next_line(fp, error);
	if (line == NULL) return NULL;
	
	Gadget *gadget = (Gadget *)MALLOC(Gadget, error);
	if (gadget == NULL) {
		free(line);
		return NULL;
	}
	// ... rest of function
}
```

**Bad:**
```c
Gadget *get_next_gadget(FILE *fp) {  // Missing error parameter
	char *line = get_next_line(fp);  // Not checking error
	Gadget *gadget = malloc(sizeof(Gadget));  // Using raw malloc, no error checking
	return gadget;
}
```

### Error Path Cleanup
- Use `goto` labels for error cleanup paths: `goto bad;`, `goto clean_ret;`
- Always free allocated resources before returning on error
- Label names should be descriptive: `bad:`, `clean_ret:`, `good:`

**Good:**
```c
struct IO *const
init_line_editing(const char *shname, struct IO *io)
{
	FILE *el_in = NULL;
	FILE *el_err = NULL;
	FILE *el_out = NULL;
	
	el_in = fdopen(STDIN_FILENO, "r");
	el_out = fdopen(STDOUT_FILENO, "w");
	if (el_in == NULL || el_out == NULL) goto bad;
	
	io->el = el_init(shname, el_in, el_out, el_err);
	if (io->el == NULL) goto bad;
	
	io->hist = history_init();
	if (io->hist == NULL) {
		el_end(io->el);
		goto bad;
	}
	
good:
	return io;
bad:
	return NULL;
}
```

## Memory Management: Safe Allocation Patterns

### Always Use MALLOC/MALLOCARRAY Macros
- NEVER use raw `malloc()`, `calloc()`, or `realloc()` directly
- ALWAYS use `MALLOC(type, error)` for single objects
- ALWAYS use `MALLOCARRAY(n, type, error)` for arrays
- These macros check for overflow and set error codes automatically

**Good:**
```c
Gadget *gadget = (Gadget *)MALLOC(Gadget, error);
if (gadget == NULL) return NULL;

char *buffer = MALLOCARRAY(bufsize, char, error);
if (!buffer) return NULL;
```

**Bad:**
```c
Gadget *gadget = malloc(sizeof(Gadget));  // Wrong: raw malloc, no overflow check
char *buffer = calloc(bufsize, sizeof(char));  // Wrong: raw calloc, no error checking
```

### Overflow Checking and realloc() Safety
- Before using `realloc()`, ALWAYS check for overflow first
- The `MALLOCARRAY` macro already handles overflow checking via `my_mallocarray()`
- If you must use `realloc()`, follow this pattern:
  1. Calculate new size and check for overflow before reallocating
  2. Store realloc result in temporary pointer (never reassign directly)
  3. Free original buffer if realloc fails
  4. Set appropriate error code on failure

**Good:**
```c
if (position >= bufsize) {
	size_t new_bufsize = bufsize + MAX_BUFFER;
	if (new_bufsize < bufsize) {  // Overflow check
		*error = MALLOC_SIZE_OVERFLOW;
		free(buffer);
		return NULL;
	}
	char *new_buffer = realloc(buffer, new_bufsize);  // Temporary pointer
	if (!new_buffer) {
		*error = MALLOC_HEAP_ISSUE;
		free(buffer);  // Free original on failure
		return NULL;
	}
	buffer = new_buffer;  // Assign only after success
	bufsize = new_bufsize;
}
```

**Bad:**
```c
buffer = realloc(buffer, bufsize + MAX_BUFFER);  // Wrong: no overflow check, loses original on failure
if (!buffer) {
	*error = MALLOC_HEAP_ISSUE;
	return NULL;  // Original buffer already lost!
}
```

### Buffer Growth Patterns
- Use the `grow_buffer()` helper function from `memory_managment.h` for safe buffer reallocation
- This function handles overflow checking and error reporting automatically
- Always check the return value from `grow_buffer()` before using the buffer

**Good:**
```c
#include "memory_managment.h"

char *buffer = MALLOCARRAY(bufsize, char, error);
if (!buffer) return NULL;

while (reading) {
	if (position >= bufsize) {
		if (grow_buffer(&buffer, &bufsize, MAX_BUFFER, error) != 0) {
			free(buffer);
			return NULL;
		}
	}
	buffer[position++] = data;
}
```

**Bad:**
```c
// Manual realloc without helper function
if (position >= bufsize) {
	bufsize += MAX_BUFFER;
	buffer = realloc(buffer, bufsize);  // Wrong: no overflow check, no error handling
	if (!buffer) return NULL;  // Wrong: loses original buffer on failure
}
```

### Memory Cleanup
- Always free all allocated memory before returning
- Use `free_list()` patterns for collections (linked lists, arrays of pointers)
- Free in reverse order of allocation when dependencies exist

**Good:**
```c
void
free_list(Node *head)
{
	for (Node *tmp = head; tmp != NULL;) {
		Node *next = tmp->next;
		free(tmp->gadget);
		free(tmp);
		tmp = next;
	}
}
```

## Header Organization

### Static Variables
- NEVER declare `static` variables in header files
- Static variables MUST be in implementation (.c) files only
- Static variables in headers create separate instances per translation unit (multiple definition problem)
- If a static variable is needed, declare it at file scope in the .c file

**Good:**
```c
// In file_io.c
static size_t n_written = 0;
static char prompt_buffer[MAX_PROMPT_BUFFER];

char *
right_prompt(UNUSED EditLine *el)
{
	snprintf(prompt_buffer, sizeof(prompt_buffer), ": %4d", n_written++);
	return prompt_buffer;
}
```

**Bad:**
```c
// In file_io.h
static size_t n_written = 0;  // Wrong: creates separate instance per translation unit
static char prompt_buffer[MAX_PROMPT_BUFFER];  // Wrong: multiple definitions
```

### Header Guards
- ALWAYS use header guards: `#ifndef FILENAME_H` / `#define FILENAME_H`
- End with `#endif // FILENAME_H` for clarity
- Guard name should match filename (uppercase, with underscores)

**Good:**
```c
#ifndef PARSE_GADGETS_H
#define PARSE_GADGETS_H
// ... content ...
#endif // PARSE_GADGETS_H
```

### Include Order
1. System headers first (standard C library, POSIX, etc.)
2. Project headers second
3. Include headers needed for the file's public interface
4. Group includes logically

**Good:**
```c
#include <errno.h>
#include <stdio.h>
#include <string.h>

#include "memory_managment.h"
#include "parse_gadgets.h"
```

### Forward Declarations
- Place forward declarations before struct definitions
- Use `typedef struct Name Name;` for forward declarations
- Define structs after all forward declarations

**Good:**
```c
typedef struct Node Node;  // Forward declaration

struct Node {
	Gadget *gadget;
	Node *next;
};
```

### Static Assertions
- Use `_Static_assert` for compile-time type safety checks
- Place in header files where types are defined

**Good:**
```c
_Static_assert(((size_t)-1) > 0, "size_t must be an unsigned type");
```

## Naming Conventions

### Functions
- Use `snake_case` for all function names
- Be descriptive: `get_next_line()`, `init_line_editing()`, `free_list()`

### Structs
- Use `PascalCase` for struct names
- Always use `struct` keyword when declaring: `struct IO`, `struct Node`
- Typedef structs to `PascalCase`: `typedef struct Gadget { ... } Gadget;`

### Enums
- Enum values: `UPPER_CASE` with underscores
- Enum type names: `lowercase` (if typedef'd)
- Values should be descriptive: `FUNCTION_SUCCESS`, `MALLOC_SIZE_OVERFLOW`

### Macros
- Use `UPPER_CASE` for all macros
- Be descriptive: `MALLOC`, `MALLOCARRAY`, `ARRAY_SIZE`, `UNUSED`

### Constants
- Use `UPPER_CASE` in enums: `MAX_BUFFER`, `NUM_OPCODES`, `LEFT_PROMPT`

**Examples:**
```c
// Functions
char *get_next_line(FILE *const fp, int *error);
void free_list(Node *head);

// Structs
struct IO {
	EditLine *el;
	History *hist;
};

// Enums
enum {
	FUNCTION_SUCCESS,
	MALLOC_SIZE_OVERFLOW
};

// Macros
#define MALLOC(type, error) MALLOCARRAY(1, type, error)
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))
```

## Code Organization

### Function Size Limit (CRITICAL)
- **Functions MUST be under 20 lines** - This is non-negotiable
- Functions exceeding 20 lines indicate multiple responsibilities and MUST be broken down
- Each function should do ONE thing well
- Extract helper functions aggressively to keep functions concise and focused
- Count includes all lines: signature, braces, comments, and implementation

**Good:**
```c
static int
validate_filename(const char *filename, int *error)
{
	*error = FUNCTION_SUCCESS;
	if (filename == NULL || filename[0] == '\0') {
		*error = FILE_OPEN_FAIL;
		return -1;
	}
	return 0;
}

static FILE *
open_file_safely(const char *filename, int *error)
{
	if (validate_filename(filename, error) != 0) {
		return NULL;
	}
	return platform_file_open(filename, FILE_READ_TEXT_MODE, error);
}
```

**Bad:**
```c
static FILE *
open_file_safely(const char *filename, int *error)
{
	// Function is 35 lines - violates 20-line limit
	*error = FUNCTION_SUCCESS;
	if (filename == NULL) {
		*error = FILE_OPEN_FAIL;
		return NULL;
	}
	if (filename[0] == '\0') {
		*error = FILE_OPEN_FAIL;
		return NULL;
	}
	// ... 25 more lines of validation and file opening logic ...
	// This function does too much and exceeds 20 lines
}
```

### Function Extraction and Helper Functions
- Extract repeated code patterns into helper functions
- Extract complex logic (parsing, validation, error handling) into separate functions
- Extract string manipulation patterns (safe copying, trimming) into helpers
- Helper functions should be marked `static` if only used within the file
- Keep helper functions small and focused on a single responsibility
- **CRITICAL**: All functions must be under 20 lines - split aggressively if needed

**Good:**
```c
static void
safe_strncpy(char *dest, const char *src, size_t dest_size)
{
	strncpy(dest, src, dest_size - 1);
	dest[dest_size - 1] = '\0';
}

static char *
trim_leading_whitespace(char *str)
{
	while (*str == ' ') {
		str++;
	}
	return str;
}

static int
validate_gadget_line(const char *line)
{
	return (line != NULL && strlen(line) > 0);
}

static Gadget *
parse_gadget_from_line(char *line, int *error)
{
	Gadget *gadget = (Gadget *)MALLOC(Gadget, error);
	if (gadget == NULL) return NULL;
	
	safe_strncpy(gadget->full_gadget, line, MAX_BUFFER + 1);
	// ... parsing logic ...
	return gadget;
}
```

**Bad:**
```c
// Inline repeated strncpy pattern
strncpy(opcodes[idx], token, MAX_BUFFER);
opcodes[idx][MAX_BUFFER] = '\0';  // Repeated in multiple places

// Complex parsing logic mixed with I/O
Gadget *
get_next_gadget(FILE *const fp, int *error)
{
	char *line = get_next_line(fp, error);
	if (line == NULL) return NULL;
	if (strlen(line) == 0) { free(line); return NULL; }
	Gadget *gadget = (Gadget *)MALLOC(Gadget, error);
	if (gadget == NULL) { free(line); return NULL; }
	strncpy(gadget->full_gadget, line, MAX_BUFFER);
	gadget->full_gadget[MAX_BUFFER] = '\0';
	// ... 30 more lines of parsing logic ...
	return gadget;
}
```

### Helper Function Patterns: Allocation and Setup
- Extract allocation and initialization into separate helper functions
- Use patterns like `allocate_*()`, `initialize_*_fields()`, `allocate_and_setup_*()`
- This improves readability and makes error handling clearer

**Good:**
```c
static struct ChunkedReader *
allocate_chunked_reader(int *error)
{
	return (struct ChunkedReader *)MALLOC(struct ChunkedReader, error);
}

static unsigned char *
allocate_chunked_reader_buffer(size_t chunk_size, int *error)
{
	return MALLOCARRAY(chunk_size, unsigned char, error);
}

static void
initialize_chunked_reader_fields(struct ChunkedReader *reader, FILE *fp,
				 size_t chunk_size)
{
	reader->fp = fp;
	reader->buffer_size = chunk_size;
	reader->buffer_pos = 0;
	reader->file_pos = 0;
	reader->eof = 0;
}

static struct ChunkedReader *
allocate_and_setup_reader(FILE *fp, size_t chunk_size, int *error)
{
	struct ChunkedReader *reader = allocate_chunked_reader(error);
	if (reader == NULL) return NULL;

	reader->buffer = allocate_chunked_reader_buffer(chunk_size, error);
	if (reader->buffer == NULL) {
		free(reader);
		return NULL;
	}

	initialize_chunked_reader_fields(reader, fp, chunk_size);
	return reader;
}
```

### Helper Function Patterns: Validation
- Extract parameter validation into separate helper functions
- Use patterns like `validate_*_params()`, `validate_*_pointer()`
- Return 0 on success, -1 on failure, and set error code

**Good:**
```c
static int
validate_filename_parameter(const char *filename, int *error)
{
	if (filename == NULL) {
		set_error(error, FILE_OPEN_FAIL);
		return -1;
	}
	return 0;
}

static int
validate_file_pointer(FILE *const fp, int *error)
{
	if (fp == NULL) {
		set_error(error, FILE_OPEN_FAIL);
		return -1;
	}
	set_error(error, FUNCTION_SUCCESS);
	return 0;
}
```

### Error Handling Extraction
- Extract complex error handling switch statements into helper functions
- Error handlers should return a value indicating whether to continue or stop
- This improves readability and makes error handling reusable

**Good:**
```c
static int
handle_gadget_error(int error, FILE *fp, int *status_flag)
{
	switch (error) {
	case MALLOC_SIZE_OVERFLOW:
		fprintf(stderr, "Error: Size overflow\n");
		return 0;  // Stop loop
	case MALLOC_HEAP_ISSUE:
		fprintf(stderr, "Error: Heap issue\n");
		return 0;
	case STRTOL_FAIL:
		return 1;  // Continue loop
	case FILE_EOF_FLAG:
	default:
		if (feof(fp)) {
			clearerr(fp);
			*status_flag = EXIT_SUCCESS;
		}
		return 0;
	}
}

// In main loop:
if (error != FUNCTION_SUCCESS || gadget == NULL) {
	status_flag = EXIT_FAILURE;
	runflag = handle_gadget_error(error, fp, &status_flag);
	if (!runflag) break;
}
```

**Bad:**
```c
// Complex switch statement embedded in main loop
if (error != FUNCTION_SUCCESS || gadget == NULL) {
	status_flag = EXIT_FAILURE;
	runflag = 0;
	switch (error) {
	case MALLOC_SIZE_OVERFLOW:
		fprintf(stderr, "Error: Size overflow\n");
		break;
	// ... 20 more lines ...
	}
}
```

### Function Order
- Forward declarations before implementations
- Helper functions before functions that use them
- `main()` function typically near the end of the file
- Group related functions together
- Static helper functions defined before public functions that use them

### Code Simplification
- Reduce nesting by using early returns
- Extract node creation/setup before conditional logic
- Use helper functions to simplify complex operations
- Remove unnecessary assignments (variables about to go out of scope)

**Good:**
```c
Node *
add_node(Gadget *gadget, Node *head, int *error)
{
	Node *new_node = get_new_node(error);
	if (*error != FUNCTION_SUCCESS) return NULL;
	
	new_node->gadget = gadget;
	new_node->next   = NULL;
	
	if (head == NULL) {
		return new_node;  // Early return
	}
	
	Node *tmp = head;
	while (tmp->next != NULL) {
		tmp = tmp->next;
	}
	tmp->next = new_node;
	
	return head;
}
```

**Bad:**
```c
Node *
add_node(Gadget *gadget, Node *head, int *error)
{
	if (head == NULL) {
		head = get_new_node(error);
		if (*error != FUNCTION_SUCCESS) return NULL;
		head->gadget = gadget;
	} else {
		Node *tmp = NULL;
		for (tmp = head; tmp->next; tmp = tmp->next)
			;
		tmp->next = get_new_node(error);
		if (*error != FUNCTION_SUCCESS) return NULL;
		tmp = tmp->next;
		tmp->gadget = gadget;
	}
	return head;  // Deeply nested, repeated error checking
}
```

### Variable Declarations
- Declare one variable per line for clarity
- Multiple declarations on one line reduce readability
- Each variable should have its own declaration statement

**Good:**
```c
FILE *el_in = NULL;
FILE *el_err = NULL;
FILE *el_out = NULL;

char *str = gadget;
char *token;
char *saveptr;
```

**Bad:**
```c
FILE *el_in = NULL, *el_err = NULL, *el_out = NULL;  // Hard to read

char *str = gadget, *token, *saveptr;  // Mixed initialization and declaration
```

### Const Correctness
- Use `const` for parameters that shouldn't be modified: `FILE *const fp`
- Use `const` for pointer-to-const data: `const char *str`
- Mark return values as `const` when appropriate: `struct IO *const`

**Good:**
```c
char *
get_next_line(FILE *const fp, int *error);  // fp is const pointer

unsigned long
get_gadget_address(char **gadget, int *error);  // gadget can be modified (pointer to pointer)
```

### Unused Parameters
- Mark intentionally unused parameters with `UNUSED` macro from `common.h`
- Place `UNUSED` before the parameter name

**Good:**
```c
char *
right_prompt(UNUSED EditLine *el)
{
	return prompt_buffer;
}
```

## Safety Practices

### System Call Return Values
- ALWAYS check return values from system calls (fopen, fgetc, strtol, etc.)
- Check `errno` after `strtol()`/`strtoul()` calls
- Use `perror()` to report system errors

**Good:**
```c
char *endptr = NULL;
errno = 0;
long val = strtol(token, &endptr, 0);

if (errno != 0) {
	perror("strtol");
	*error = STRTOL_CRITICAL;
	goto bad;
}

if (endptr == token) {
	*error = STRTOL_FAIL;
	goto bad;
}
```

### Thread Safety
- Use `strtok_r()` instead of `strtok()` for thread safety
- Pass `saveptr` parameter to maintain state

**Good:**
```c
char *saveptr = NULL;
char *token = strtok_r(*gadget, ":", &saveptr);
```

**Bad:**
```c
char *token = strtok(*gadget, ":");  // Not thread-safe
```

### Pointer Validation and Variable Comparison
- Validate pointers before dereferencing
- Check for NULL after allocation
- Check function return values before use
- When comparing variables after function calls, ensure you're comparing the correct variable
- Check the actual variable used in the operation, not a different variable

**Good:**
```c
char *token = strtok_r(*gadget, ":", &saveptr);
if (token == NULL) {
	*error = STRTOL_FAIL;
	goto bad;
}

char *endptr = NULL;
errno = 0;
long val = strtol(token, &endptr, 0);

if (endptr == token) {  // Correct: comparing endptr with token (the actual variable used)
	*error = STRTOL_FAIL;
	goto bad;
}
```

**Bad:**
```c
char *token = strtok_r(*gadget, ":", &saveptr);
long val = strtol(token, &endptr, 0);

if (endptr == *gadget) {  // Wrong: comparing with wrong variable, should be 'token'
	*error = STRTOL_FAIL;
	goto bad;
}
```

### Error Parameter Consistency
- All functions that can fail MUST accept an `int *error` parameter
- Even functions that previously didn't have error handling should be updated
- This ensures consistent error handling throughout the codebase

**Good:**
```c
FILE *
prompt_user_and_open_file(struct IO *iop, int *error)
{
	*error = FUNCTION_SUCCESS;
	// ... error handling ...
	return fp;
}
```

**Bad:**
```c
FILE *
prompt_user_and_open_file(struct IO *iop)  // Missing error parameter
{
	// No way to report errors
	return fopen(fname, "r");
}
```

### File Position Preservation
- When reading headers or metadata from files, preserve file position
- Save position with `ftell()` before reading, restore with `fseek()` after
- This allows reading metadata without affecting file stream position

**Good:**
```c
static size_t
read_file_header_bytes(FILE *const fp, unsigned char *buffer,
		      size_t buffer_size, int *error)
{
	long saved_pos = ftell(fp);
	if (saved_pos < 0) {
		set_error(error, FILE_OPEN_FAIL);
		return 0;
	}

	if (fseek(fp, 0, SEEK_SET) != 0) {
		set_error(error, FILE_OPEN_FAIL);
		return 0;
	}

	size_t bytes_read = fread(buffer, 1, buffer_size, fp);
	if (ferror(fp)) {
		set_error(error, FILE_OPEN_FAIL);
		fseek(fp, saved_pos, SEEK_SET);
		return 0;
	}
	fseek(fp, saved_pos, SEEK_SET);

	return bytes_read;
}
```

### Platform Abstraction
- Use platform abstraction functions from `platform_file.h` instead of direct system calls
- Use `platform_file_open()` instead of `fopen()`
- Use platform constants (`FILE_READ_MODE`, `FILE_READ_TEXT_MODE`) instead of hardcoded strings
- Check platform macros (`PLATFORM_WINDOWS`, `PLATFORM_UNIX`) only in platform abstraction modules

**Good:**
```c
#include "platform_file.h"

FILE *fp = platform_file_open(filename, FILE_READ_TEXT_MODE, error);
```

**Bad:**
```c
FILE *fp = fopen(filename, "r");  // Wrong: direct system call, may not work on Windows
```

### Compile-Time Checks
- Use `_Static_assert` for compile-time type safety
- Verify assumptions about types and sizes at compile time

**Good:**
```c
_Static_assert(sizeof(int) == 4, "int must be 32 bits");
_Static_assert(((size_t)-1) > 0, "size_t must be an unsigned type");
```

### Magic Numbers Are Forbidden (CRITICAL)
- **ALL numeric constants MUST be named** - No magic numbers allowed
- Replace ALL hardcoded numeric values with `#define` constants or `const` variables
- Place constants in appropriate header files (usually `common.h` or module-specific headers)
- Constants should be descriptive and indicate their purpose
- This applies to ALL numeric literals: buffer sizes, retry counts, limits, offsets, etc.

**Good:**
```c
// In common.h or appropriate header:
#define MAX_BUFFER_SIZE 1024
#define MAX_FILENAME_LENGTH 256
#define MAX_RETRY_ATTEMPTS 5
#define DEFAULT_CHUNK_SIZE 65536
#define NULL_TERMINATOR_SIZE 1

// In code:
char buffer[MAX_BUFFER_SIZE];
if (retries < MAX_RETRY_ATTEMPTS) {
	// ...
}
size_t len = strlen(str) - NULL_TERMINATOR_SIZE;
```

**Bad:**
```c
// Magic numbers throughout code - FORBIDDEN
char buffer[1024];  // Wrong: what is 1024?
if (retries < 5) {  // Wrong: what is 5?
	// ...
}
size_t len = strlen(str) - 1;  // Wrong: what is 1?
chunk_size = 65536;  // Wrong: what is 65536?
```

### Security Considerations
- Always check for buffer overflows - use bounds checking
- Check for integer overflows before arithmetic operations
- Validate all pointers before dereferencing
- Initialize all variables before use
- Free all allocated memory to prevent leaks
- Use safe string functions (`strncpy`, `snprintf`) with bounds checking
- Check return values from all system calls
- Use thread-safe functions (`strtok_r` instead of `strtok`)

**Good:**
```c
char buffer[MAX_BUFFER_SIZE];
if (snprintf(buffer, sizeof(buffer), "%s", str) >= sizeof(buffer)) {
	*error = MALLOC_SIZE_OVERFLOW;
	return NULL;
}

size_t new_size = current_size + growth;
if (new_size < current_size) {  // Overflow check
	*error = MALLOC_SIZE_OVERFLOW;
	return NULL;
}
```

**Bad:**
```c
char buffer[1024];
sprintf(buffer, "%s", str);  // Wrong: no bounds checking, potential overflow

size_t new_size = current_size + growth;  // Wrong: no overflow check
```

## File Structure

### Header Files (.h)
- Contain function declarations
- Contain struct/typedef definitions
- Contain enum definitions
- Contain macro definitions
- Include only what's needed for the public interface
- All declarations must be documented

### Implementation Files (.c)
- Contain function implementations
- Include system headers first, then project headers
- Implement all functions declared in corresponding .h file
- Private helper functions don't need to be in header (but should be documented)

### Common Definitions
- Common macros and enums go in `common.h`
- Error codes go in `common.h`
- Utility macros (UNUSED, ARRAY_SIZE) go in `common.h`
- Use `set_error()` helper function from `common.h` for consistent error setting

### One Logical Unit Per File
- Each file should represent one logical unit (file I/O, memory management, parsing, etc.)
- Keep related functionality together
- Avoid mixing unrelated concerns

### File Size Limits (CRITICAL)
- **All .c and .h files MUST be under 400 lines of code**
- Files exceeding 400 lines must be broken into smaller, focused files
- Each file must serve a single purpose and not handle multiple unrelated concerns
- Large files indicate design issues - split by responsibility

**Good:**
```c
// file_io.h (150 lines) - File I/O operations only
// line_io.c (200 lines) - Line reading functionality
// input_io.c (180 lines) - User input handling
// libedit_io.c (220 lines) - libedit-specific I/O
```

**Bad:**
```c
// file_io.c (650 lines) - Too large, mixes multiple concerns
// Contains: line reading, user input, libedit, file operations
// Should be split into: line_io.c, input_io.c, libedit_io.c
```

### Remove TODOs and Placeholders (CRITICAL)
- **NEVER leave TODO comments, FIXMEs, or incomplete sections**
- All code must be fully implemented and self-contained
- If functionality is not ready, don't commit it or mark it clearly as experimental
- Replace placeholder code with actual implementation
- Remove all temporary workarounds before completion

**Good:**
```c
// Fully implemented function with no TODOs
static int
validate_binary_header(const unsigned char *header, size_t size, int *error)
{
	// Complete implementation
	return 0;
}
```

**Bad:**
```c
static int
validate_binary_header(const unsigned char *header, size_t size, int *error)
{
	// TODO: Add validation logic  // Wrong: TODO left in code
	// FIXME: Handle edge cases   // Wrong: FIXME left in code
	return 0;  // Placeholder return
}
```

### Leverage Existing Codebase
- **Always check for existing functions before writing new ones**
- Reuse existing helper functions and patterns from the codebase
- Don't reinvent functionality that already exists
- Look for similar patterns in other files and adapt them
- Use existing abstractions (e.g., `platform_file_open()` instead of `fopen()`)

**Good:**
```c
// Use existing platform abstraction
FILE *fp = platform_file_open(filename, FILE_READ_TEXT_MODE, error);

// Use existing error helper
set_error(error, FILE_OPEN_FAIL);

// Use existing memory macros
Gadget *g = (Gadget *)MALLOC(Gadget, error);
```

**Bad:**
```c
// Reinventing platform abstraction
FILE *fp = fopen(filename, "r");  // Wrong: should use platform_file_open()

// Reinventing error setting
if (error != NULL) *error = FILE_OPEN_FAIL;  // Wrong: should use set_error()

// Reinventing memory allocation
Gadget *g = malloc(sizeof(Gadget));  // Wrong: should use MALLOC()
```

## Code Examples: Good vs Bad

### Example 1: Function Declaration and Implementation

**Good:**
```c
/**
 * add_node() - Add a new node to the linked list
 * @gadget: Pointer to the gadget to add
 * @head: Pointer to the head of the linked list
 * @error: Pointer to an integer for error code
 *
 * Return: Pointer to the new head of the list, or NULL on error
 */
Node *
add_node(Gadget *gadget, Node *head, int *error)
{
	Node *new_node = get_new_node(error);
	if (*error != FUNCTION_SUCCESS) return NULL;
	
	new_node->gadget = gadget;
	new_node->next   = NULL;
	
	if (head == NULL) {
		return new_node;
	}
	
	Node *tmp = head;
	while (tmp->next != NULL) {
		tmp = tmp->next;
	}
	tmp->next = new_node;
	
	return head;
}
```

**Bad:**
```c
// Missing documentation
Node* add_node(Gadget* g, Node* h, int* e) {  // Wrong: return type on same line, abbreviated names, wrong pointer alignment
	if (!h) {  // Missing error checking
		h = malloc(sizeof(Node));  // Wrong: raw malloc, no error checking
		h->gadget = g;
		return h;
	}
	// ... rest missing proper error handling
}
```

### Example 2: Memory Allocation

**Good:**
```c
char *
get_next_line(FILE *const fp, int *error)
{
	size_t bufsize = MAX_BUFFER_SIZE, position = 0;
	char *buffer = MALLOCARRAY(bufsize, char, error);
	if (!buffer) return NULL;
	// ... use buffer
}
```

**Bad:**
```c
char* get_next_line(FILE* fp) {  // Missing error parameter, wrong pointer alignment
	char* buffer = malloc(1024);  // Wrong: raw malloc, hardcoded size, no error checking
	if (!buffer) return NULL;  // Should set error code
	// ...
}
```

### Example 3: Error Handling

**Good:**
```c
unsigned long
get_gadget_address(char **gadget, int *error)
{
	char *saveptr = NULL;
	char *token = strtok_r(*gadget, ":", &saveptr);
	if (token == NULL) {
		*error = STRTOL_FAIL;
		goto bad;
	}
	
	char *endptr = NULL;
	errno = 0;
	long val = strtol(token, &endptr, 0);
	
	if (errno != 0) {
		perror("strtol");
		*error = STRTOL_CRITICAL;
		goto bad;
	}
	
	if (endptr == token) {
		*error = STRTOL_FAIL;
		goto bad;
	}
	
	*error = FUNCTION_SUCCESS;
	*gadget = saveptr;
	
bad:
	return val;
}
```

**Bad:**
```c
unsigned long get_gadget_address(char* gadget) {  // Missing error parameter, wrong pointer alignment
	char* token = strtok(gadget, ":");  // Wrong: not thread-safe, no error checking
	long val = strtol(token, NULL, 0);  // Wrong: not checking errno or endptr
	return val;  // Wrong: no error reporting
}
```

## Summary Checklist

When writing or reviewing code, ensure:

### Critical Requirements (Must Have)
- [ ] **All functions are under 20 lines** (CRITICAL)
- [ ] **All magic numbers replaced with named constants** (CRITICAL)
- [ ] **All .c and .h files are under 400 lines** (CRITICAL)
- [ ] **No TODOs, FIXMEs, or incomplete code** (CRITICAL)
- [ ] **Existing codebase functions are leveraged** (CRITICAL)

### Code Style
- [ ] Function return types are on separate lines
- [ ] Pointer asterisks are right-aligned
- [ ] All functions have kernel-doc style comments
- [ ] File headers include File, Description, Author, Date
- [ ] Variable declarations are one per line
- [ ] Header guards are present in all .h files
- [ ] System headers come before project headers
- [ ] Forward declarations are used appropriately
- [ ] `const` is used for parameters that shouldn't be modified
- [ ] `UNUSED` macro marks unused parameters
- [ ] Naming conventions are followed (snake_case functions, PascalCase structs, UPPER_CASE macros/enums)

### Error Handling
- [ ] Error codes are passed via `int *error` parameter
- [ ] Error codes are checked after function calls
- [ ] `goto` labels are used for error cleanup
- [ ] `set_error()` helper is used for consistent error setting
- [ ] Complex error handling is extracted into helper functions

### Memory Management
- [ ] Only `MALLOC`/`MALLOCARRAY` macros are used (never raw malloc/calloc)
- [ ] `realloc()` includes overflow checking and uses temporary pointer
- [ ] All allocated memory is freed
- [ ] Static variables are in .c files, never in .h files
- [ ] Helper functions follow allocation/setup/validation patterns

### Code Organization
- [ ] Helper functions are extracted for repeated patterns
- [ ] Code is simplified to reduce nesting (early returns, helper functions)
- [ ] Each file serves a single purpose
- [ ] File position is preserved when reading headers/metadata

### Safety Practices
- [ ] Return values from system calls are checked
- [ ] `strtok_r` is used instead of `strtok`
- [ ] `errno` is checked after `strtol`/`strtoul`
- [ ] Pointers are validated before dereferencing
- [ ] Variable comparisons use the correct variable (not a different one)
- [ ] Buffer overflows are prevented with bounds checking
- [ ] Integer overflows are checked before arithmetic

### Platform and Abstraction
- [ ] Platform abstraction functions are used instead of direct system calls
- [ ] Platform constants are used instead of hardcoded strings

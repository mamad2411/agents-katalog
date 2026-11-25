---
name: code-compiler
description: Compile and run C, C++, Rust, Go, and Python code. Diagnose compilation errors and suggest fixes. Use when the user is writing or building code.
---

# Code Compiler

## When to use
Use this skill when the user needs to:
- Compile C, C++, Rust, or Go code
- Diagnose and fix compilation errors
- Run scripts (Python, Bash, Node.js)
- Set up build systems (Make, CMake)

## Compilation

### C
```bash
gcc -o program source.c -Wall -Wextra
gcc -o program source.c -O2 -std=c11
```

### C++
```bash
g++ -o program source.cpp -Wall -Wextra -std=c++17
g++ -o program source.cpp -O2 -std=c++20
```

### With multiple files
```bash
gcc -o program main.c utils.c -I./include
g++ -o program *.cpp -I./include -std=c++17
```

### With libraries
```bash
gcc -o program source.c -lm -lpthread
pkg-config --cflags --libs openssl
```

## Build systems

### Makefile
```makefile
CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = program
SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)

$(TARGET): $(OBJS)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f $(OBJS) $(TARGET)
```

### CMake
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

## Scripting languages

### Python
```bash
python3 script.py
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Bash
```bash
chmod +x script.sh
./script.sh
bash -x script.sh   # debug mode
```

## Common errors

- **undefined reference**: Missing `-l` flag or source file not included
- **implicit declaration**: Missing `#include` header
- **segmentation fault**: Run with `gdb ./program` then `run` then `bt` for backtrace
- **permission denied**: `chmod +x` the binary

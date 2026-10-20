<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dhammerg
description: CTF writeups and security challenges by dhammerg.
---

# Writeups by dhammerg

Source repository: `/repos/dhammerg`

## Repository Index

- Writeups/self_learning/Unsafe_Unlink/unsafe_unlink.md
- Writeups/self_learning/fastbin_into_stack/fastbin_dup_into_stack.md
- Writeups/self_learning/fd_poison/README.md
- Writeups/self_learning/house_of_botcake/README.md
- Writeups/self_learning/house_of_force/README.md
- Writeups/self_learning/uaf_01/README.md
- Writeups/self_learning/Unsafe_Unlink/unlink2/easy_1.md
- Writeups/self_learning/Unsafe_Unlink/unlink2/easy_2.md
- Writeups/nahamcon/2025/found_memory [binary]/README.md
- Writeups/nahamcon/2025/lost_memory [binary]/readme.md

## Writeup Content


### File: Writeups/nahamcon/2025/found_memory [binary]/README.md





### File: Writeups/self_learning/fd_poison/README.md

# Heap Exploitation with FD Poisoning (libc 2.32)

Today we're tackling a heap exploitation challenge using the **fd-poisoning** technique. The goal is to **poison the `fd` field**—the pointer to the next chunk in a tcache bin—in order to gain control over the address returned by a future `malloc()` call.

> ⚠️ This is a writeup of the exploitation process, so it's assumed that you're already familiar with the **tcache** structure in glibc.

---

## 🛠️ Exploit Setup (lines 1–58):

The first part of the exploit defines helper functions for interacting with the menu of the vulnerable binary. These include functions to add, delete, view, and edit "kids".
I also skip the reversing the binary part, do it by your self :)

**Program menu:**
```
Virtual Kid Management
=====================================
1. Create a kid   // (malloc with fixed size)
2. View a kid     // (can leak data due to UAF)
3. Free a kid     // (free with UAF opportunity)
4. Change a kid   // (edit an allocated chunk)
5. Exit
6. Options
```

The target binary is compiled with **libc version 2.32**, which brings some things to consider:

- The **tcache** now includes a `count` variable to track the number of chunks in each bin.
- **Safe-linking** is enabled, meaning the `fd` pointer is XOR-ed with a heap address for security.

The challenge could have been harder if **ASLR** were fully effective, but leaking heap chunk addresses allows us to bypass it.

---

## 🧱 Exploitation Process:

We first allocate **three chunks** on the heap. The third chunk is added only to prevent the second chunk (once freed) from merging with the top chunk.

In **lines 65–66**, we free the first two chunks.


By **line 76**, we leak the addresses of the first two chunks using a UAF vulnerability and compute the address of the second chunk.

We then **poison the `fd` pointer** of the second chunk so that the next time `malloc()` is called, it returns an **arbitrary address** of our choice. Our target address is **32 bytes past the first chunk**, which is where a **function pointer** resides. We plan to overwrite this function pointer with the address of the `win()` function.

In **line 77**, we compute the desired fake `fd` value.  
In **line 78**, we use the "edit" functionality to overwrite the second chunk’s `fd` field with our fake address.
![ch](https://github.com/user-attachments/assets/acdad517-ad98-4bc6-ad19-a9368908d352)


Then, we call `malloc()` twice. On the **second call**, `malloc()` should return the **fake address** we injected—**not** the original first chunk's address.

In **line 82**, we write the address of the `win()` function to that location. This works because the first 8 bytes of the target structure are treated as the `age` field (but actually represent the function pointer).

Finally, by selecting **menu option 2**, we trigger the execution of the overwritten function pointer inside the previously freed chunk—now pointing to `win()`. This results in **shell execution**.
![Capture](https://github.com/user-attachments/assets/29ce7a5f-56b7-483c-907b-c617aacbaecc)

### Ref & challenge:
https://github.com/SecurityInnovation/glibc_heap_exploitation_training/tree/master/modules/fd_poison/challenge1



### File: Writeups/self_learning/house_of_botcake/README.md

Welcome to the new write-up on heap exploitation.
This is my first technique in the "House" series that I’ve learned, and I think the others are similar to this one.
Here we are with "House of BotCake".

Once again, I’m using the how2heap source to demonstrate how this technique works, along with some notes.

The explanation is simple:
```
This file demonstrates a powerful tcache poisoning attack by tricking malloc into
returning a pointer to an arbitrary location (in this demo, the stack).
This attack only relies on double free.
```

So let’s dive into the code. First, we have a stack buffer, which we’re eventually going to point to (defined on line `20`).

Then we fill the tcache with seven chunks. We use a chunk size of 0x100 (REMEMBER: this size must be large enough to avoid storing chunks in the fastbin!).

In lines `23–26`, we fill the tcache. After that, we define two heap chunks: first `prev`, then chunk `a`. We’ll later free chunk a twice.

On line `29`, we allocate 0x10 bytes (which actually returns 0x20) to prevent consolidation with the top chunk when we free chunk `a`.

Remember the `prev` chunk defined before `a`. In line `35`, we free `a`, then `prev`. At this point, the "malloc_consolidate" function is called, so `prev` and `a` are merged. Now the only chunk in the unsorted bin is the address of `prev`!

In line `39`, we allocate a chunk with size 0x100 (`0x110` with the header) to get the last chunk from the tcache (since tcache follows LIFO). Next, in line `41`, the double free occurs, which places chunk `a` into the tcache. So now `a` is present both in the tcache and in the unsorted bin (since it was merged with prev).

In line `45`, we allocate a chunk to retrieve the prev chunk from the unsorted bin. Since this chunk contains the `a` chunk, we can now edit the data of the former `a`. In line `47`, we edit the header of the former `a` chunk—this technique is similar to what we saw before in the “fastbin-to-stack” write-up, used to bypass the safe unlinking checks.

In line `49`, we allocate the last stored `a` chunk. Now the tcache is corrupted, and the final chunk remaining in the tcache is our stack buffer. This means that in the next malloc (line `52`), libc will return a pointer to the stack buffer.

I copy-pasted this code from the how2heap repo and removed the printf/puts functions. In line `50`, the a_size variable was originally used for printing the size of chunk a, but we’re not using it anymore. However, when we try to remove or comment it out, the program crashes. Why?

Here’s the error:
```
malloc(): unaligned tcache chunk detected
zsh: abort      ./app
```

If you check the libc code, you’ll find this error message in the tcache_get_n function. The error happens when there's a problem with alignment. Let's check it in GDB using the latest version of the code:
```
Tcachebins[idx=11728124035470, size=0xaaaaaaac1900, count=1] ←  Chunk(addr=0xffffffffed20, size=0xaaaaaaac1900, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)  ←  [Corrupted chunk at 0xffffffffed20]
```

The address field is: 0xffffffffed20

Now let’s check the updated version:

```
Tcachebins[idx=11728124035470, size=0xaaaaaaac1900, count=1] ←  Chunk(addr=0xffffffffed28, size=0xaaaaaaac1900, flags=PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)  ←  [Corrupted chunk at 0xffffffffed28]
```

Now the address is: 0xffffffffed28

This 8 is our problem. It’s a rule (or maybe a security mechanism) that heap chunks must start at a properly aligned boundary.

So in line `50`, when we create a new stack variable, we ensure proper alignment to safely unlink to our stack buffer.
The value of that variable doesn’t matter—only the alignment does.




### File: Writeups/self_learning/house_of_force/README.md

# House of Force

overwriting topchunk size to achieve arb memory by malloc()

fixed in glibc 2.29

tips:
```
requested size:
	evil_size = target_addr - topchunk_hdr - 0x10 - 0x10

	#first- 0x10: For the metadata tacked onto the request 
	#second - 0x10: To account for the metadata prior to the __malloc_hook

```
<img width="501" height="369" alt="force" src="https://github.com/user-attachments/assets/1f0e9f1a-de5b-42e2-b7b4-7f9167f2ce86" />



### File: Writeups/self_learning/uaf_01/README.md

# Heap exploitation
## Use-After-Free
This write-up documents my process of starting a structured routine for
learning and practicing heap challenges. so lets start it by  a  simple
use-after-free vulnerability (i  had wrote  this  program  which it has
the vuln). Our approach is much simpler than you might expect, we  have
a menu which  we  have to choose 4 options:

```
![we have a global struct called `usr` which has  two  string  pointer]
![this struct store in heap]

1- change username       // [using fgets to store data in usr->username]
2- change password       // [using fgets to store data in usr->username]
3- delete user           // [just free the `usr`]
4- leave a message       // [allocate new chunk in heap  with  our data]
```

if you check the binary you would see that after free ing the`usr` chunk
, the binary is not going to set the variable to NULL, it cause  UAF  or
Use-After-Free!

When we can free a chunk and then allocate a new one, while we can access
the previous variable we can do OOB Write, lets write our final RIP  into
the GOT.

Since we dont have NX (also ASLR :) we can load our shellcode into env of
our shell and get the address of it as our RIP, now choose  an  entry  of
GOT, for exampple `printf` which the binary call it during its execution.


`usr` heap-chunk in situations:

|      usr        |                                   |       usr         |
|username|password| => after free and leave a message |GOT@printf|password|



Now at this state when we want to change  username , we are writing it in
the printf stub.


   GOT:
0x804c004: | Real printf |  => after changing username => | shellcode ADDR |


Finally we would call the shellcode!

![photo_2025-01-23_09-25-02](https://github.com/user-attachments/assets/e69ee563-b1c3-4a18-ab42-9b774bf66cce)





### File: Writeups/nahamcon/2025/lost_memory [binary]/readme.md

## Strategy
- libc.so.6 the libc version 2.31 (no safe_linking)
- ld-linux-x86-64.so.2  (linker)
- lost_memory (main bin)

```
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

Since safe_linking is not present, we can leverage the fd-poison technique to manipulate the tcache’s linked list.
Additionally, because PIE is disabled, we have predictable addresses, allowing us to corrupt the global ptr list for arbitrary read and write.

Using this arbitrary read primitive, we can leak the address of the actual printf function. With some calculations, we determine the address of system. Finally, we overwrite the free@got entry with the address of system, and trigger execution.

![Capture](https://github.com/user-attachments/assets/03a88ed7-7241-472f-ac96-50e95833bee3)



### File: Writeups/self_learning/Unsafe_Unlink/unlink2/easy_1.md

## Notes
the target binary compiled with old libc and this technique is not working in newer versions since a check
added to verify the double-linked list:
![Capture](https://github.com/user-attachments/assets/dc3329e7-3346-445a-806f-9e6554d5228b)


we have three chunks, the program tries to free the 2nd and 3rd chunks, we can write on 1st and 2nd chunks.
strategy is the first chunk is a place to hold our shellcode, we manipulate the fd&bk fields of second chunk,
when the third chunk free, the "unlink" macro would trigger and place the address of first chunk into GOT of
"puts" function and boom.
(in shellcode we load instructions to jump to the winner function)

### Source
https://github.com/SecurityInnovation/glibc_heap_exploitation_training/tree/master



### File: Writeups/self_learning/Unsafe_Unlink/unlink2/easy_2.md

## Notes
the target binary compiled with old libc and this technique is not working in newer versions since a check
added to verify the double-linked list:
![Capture](https://github.com/user-attachments/assets/dc3329e7-3346-445a-806f-9e6554d5228b)

like last challenge "easy_1" we have the same code except the free part, we are just freeing the last chunk.
also if you look at the second call of "fgets", we have a heap-overflow which it can overwrite the header
of the last chunk which it would be free.

the strategy is again we manipulate the fd&bk fields of 2nd chunk and then overwrite the header try to set the
"prev_size" which is 0x90 and also try to unset the "prev_inuse bit" which the result is again 0x90.

since it is the last chunk, consolidation with top chunk would happen which triggers unlink macro again (if prev_inuse bit is unset!).

### Source
https://github.com/SecurityInnovation/glibc_heap_exploitation_training/tree/master



### File: Writeups/self_learning/Unsafe_Unlink/unsafe_unlink.md

Here we are with another write-up on heap exploitation!
It’s been two weeks since my last write-up, which was about the Use-After-Free (UAF) technique.
This week, we’re diving into the "Unsafe-Unlink" technique.

The main goal of the unsafe unlink technique is to achieve arbitrary memory write. This is done by exploiting how the free() function consolidates free chunks in the heap, particularly through the unlinking process of the doubly-linked list used in memory management.

This time, I didn’t write a vulnerable app or use a real-world binary to demonstrate today’s trick. Instead, I took a simple demonstration script from the awesome repo "how2heap":
https://github.com/shellphish/how2heap/blob/master/glibc_2.35/unsafe_unlink.c

with some tweaks of my own.

Let’s start tracing the program:
Lines 17 & 18:
We create two large chunks big enough to avoid being stored in the tcache or fastbin.
We allocate 0x420 bytes for each chunk.

Lines 20-22:
Next, we create a fake chunk inside chunk0 (our first chunk) and set up some pointers known as fd (forward pointer) and bk (backward pointer).
These are used in the doubly-linked list structure that manages free chunks.

Lines 24-26:
Here, we modify the header of the second chunk (chunk1).
We change the prev_size field to 0x420 and unset the prev_inuse bit.
(If you’re unfamiliar with these terms, I recommend Googling them or asking our friend ChatGPT!)

Line 28:
This is the key moment that divides the program’s state before and after the exploit.
When we free() chunk1, the pointer for chunk0 (which is stored on the stack) gets overwritten to point back to the stack itself.
The reason of overwrite is bcz of the unlink process when we want to free a chunk:

fd = P->fd
bk = P->bk
P->fd = bk
P->bk = fd

![Untitled](https://github.com/user-attachments/assets/8d8be48d-b5da-402c-8c50-f32a3689e2f2)


for better understanding, check the libc source code, malloc.c file:
_int_free() -> _int_free_merge_chunk() -> unlink_chunk()

Hmm… this means that from this point on, any write operation targeting chunk0 will actually write to the stack.
(Technically, when we access chunk0, the system retrieves the pointer from the stack. Since we’ve tampered with that pointer, we’re effectively writing to the stack instead of the original heap chunk.)

So, in line 30, when we think we’re writing to chunk0, we’re actually overwriting a stack address—specifically 24 bytes before the stored chunk0 pointer.

This results in a segmentation fault!


In a real-world scenario:
Instead of manually editing chunk metadata like we did here, we’d exploit vulnerabilities (like buffer overflows) to corrupt the chunks dynamically.



### File: Writeups/self_learning/fastbin_into_stack/fastbin_dup_into_stack.md

# fastbin-duplicate-into-stack
This marks my third week of learning about heap exploitation, and today’s trick is
truly fascinating. Unlike last time, I created my own challenge and will  walk you
through the solution.

Today's  trick  is  called  Fastbin  Duplicate Into Stack, which involves tricking
calloc into returning a nearly  arbitrary  pointer  by  manipulating  the  fastbin
freelist.

I used the how2heap repository as a reference to demonstrate the trick (see sample.c).

## Step-by-Step Explanation
### Filling the Tcache
To begin, we need to fill the tcache. As you might know, tcache can store a maximum of 7 chunks. In lines 13–18, we allocate and free chunks to fill the tcache.

### Target Buffer Setup
In line 21, we define stack_var as our target buffer. Our goal is to have our final calloc() call return a pointer to this variable on the stack rather than a chunk on the heap.

### Heap Chunk Allocation
Lines 23–25 allocate three new chunks in the heap.

### Triggering Double-Free
Lines 27–31 show how we trigger a double-free by freeing the same chunk twice (the chunk referred to by a).
![double_free](https://github.com/user-attachments/assets/5e8f1a28-f4d9-4b93-b634-4bcdeab37728)


### Popping Chunks from the Fastbin
In line 33, we call calloc() to pop the previously freed a chunk from the fastbin. Similarly, in line 35, we do the same with chunk b.

### Preparing the Target Buffer
We now need to prepare our target buffer to resemble a valid heap chunk by setting its size correctly without setting the prev_in_use bit.

### Calculating the Correct FD Pointer
In line 44, we set the fd pointer. This step is crucial and requires knowing the target buffer's stack address. We need to pass a safe-linking check using the following formula: (ref https://research.checkpoint.com/2020/safe-linking-eliminating-a-20-year-old-malloc-exploit-primitive/)
```
*d = (addr >> 12) ^ ptr;
```
### Corrupting the Fastbin
In line 48, we pop the last a chunk from the bin. At this point, the fastbin is corrupted. Then, in line 50, when we call calloc(), it returns a pointer to the stack.
![cur](https://github.com/user-attachments/assets/7c0111f2-da71-43cc-a72b-e3c5ce207728)

---
## challange time
Now it’s your turn. You have the source code (chall.c) and a compiled binary (chall). Try solving it yourself without reading further.

The application communicates via a TCP connection and provides a simple menu:

```
1 - signup  [allocate a chunk]
2 - give up [free a chunk]
3 - submit flag [writing some data into the stack]
4 - leak    [leak addresses]
```

All the necessary elements for crafting the exploit are in place. Check out `exploit.py` for hints.

### Exploit Breakdown

- Lines 69–73: Fill the tcache.

- Lines 77–82: Perform the double-free.

- Lines 85–94: Leak stack and heap addresses.

- Final step: Send the crafted payload.

If everything goes well, you’ll get a shell. Good luck!
![rce](https://github.com/user-attachments/assets/2bbf21a5-b090-488d-8a04-673e8b2ee517)


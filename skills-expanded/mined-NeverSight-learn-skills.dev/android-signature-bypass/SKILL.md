---
name: android-signature-bypass
description: >
  Bypass Android sharedUserId platform signature verification WITHOUT the platform key.
  Use when the user reports INSTALL_FAILED_SHARED_USER_INCOMPATIBLE, needs to install an APK
  with android:sharedUserId="android.uid.system" on a rooted/userdebug emulator/device,
  or needs to call system APIs (android.car.jar, etc.) on an Android Automotive emulator
  where the platform key is unavailable. Covers smali patching of services.jar, OAT
  regeneration via dex2oat, bind mounting with SELinux context fix, and permanent
  writable-system setup via disable-verity. For userdebug/eng builds only.
---

# Android Signature Bypass (services.jar patch)

Bypass PackageManagerService signature verification to install APKs using `sharedUserId="android.uid.system"` when the platform signing key is NOT available.

## When this applies

- `INSTALL_FAILED_SHARED_USER_INCOMPATIBLE` despite root access
- APK declares `android:sharedUserId="android.uid.system"` but platform key is unknown (e.g., Google `dev-keys` Automotive images)
- Need to call `android.car.jar` or other system APIs requiring system UID
- Device/emulator is `userdebug` or `eng` build with `adb root` available

## Prerequisites

- ADB root access (`adb root` works)
- Java 17+ on the host machine
- Apktool downloaded (we'll get it if missing)

## Workflow

### Step 1: Environment check

```bash
adb devices -l
adb root
adb shell "whoami"                            # must be root
adb shell "getprop ro.build.type"             # userdebug or eng
adb shell "getprop ro.product.name"           # note the product
```

### Step 2: Pull and decompile services.jar

```bash
# Pull
adb pull /system/framework/services.jar

# Download apktool if needed
curl -sL -o apktool.jar \
  "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.11.0.jar"

# Decompile
java -jar apktool.jar d -f services.jar -o services_src
```

The PackageManagerService smali files are in `services_src/smali_classes2/com/android/server/pm/`.

### Step 3: Patch three checkpoints

The target file is `PackageManagerServiceUtils.smali`. Patch these three methods:

**A. `compareSignatures` — always return SIGNATURE_MATCH (0)**

Replace the ENTIRE method body with:

```smali
.method public static compareSignatures([Landroid/content/pm/Signature;[Landroid/content/pm/Signature;)I
    .locals 1
    const/4 v0, 0x0
    return v0
.end method
```

**B. `canJoinSharedUserId` — always return true**

```smali
.method public static canJoinSharedUserId(Landroid/content/pm/SigningDetails;Landroid/content/pm/SigningDetails;)Z
    .locals 1
    const/4 v0, 0x1
    return v0
.end method
```

**C. The `hasCommonAncestor`/signing lineage check in `verifySignatures`**

Do NOT patch the entire `verifySignatures` method — it handles state initialization. Instead, find and bypass the lineage check:

Search for `hasCommonAncestor` inside `verifySignatures`. Replace the conditional block:

```smali
    # BEFORE:
    if-eqz v9, :cond_13
    goto :goto_8
    .line 642
    :cond_13
    new-instance v9, Lcom/android/server/pm/PackageManagerException;
    ... (error about "signing lineage that diverges")

    # AFTER:
    goto :goto_8
```

### Step 4: Recompile

```bash
java -jar apktool.jar b -f services_src -o services_patched.jar
```

### Step 5: Deploy (choose one path)

**Path A: Permanent via disable-verity + writable-system (emulator)**

```bash
# Cold boot emulator with:
emulator -avd <avd_name> -writable-system -no-snapshot-load

# Once booted:
adb root
adb disable-verity        # may require reboot
adb reboot
# Wait, then:
adb root
adb remount               # now /system is writable via overlayfs

# Copy files permanently:
adb push services_patched.jar /data/local/tmp/
adb shell "
# Use dex2oat to generate matching OAT files
cd /data/local/tmp
unzip -o services_patched.jar '*.dex' -d dex_tmp
dex2oat --dex-file=dex_tmp/classes.dex --dex-file=dex_tmp/classes2.dex \
  --oat-file=services.odex \
  --boot-image=/system/framework/x86_64/boot.art \
  --instruction-set=x86_64 --compiler-filter=speed

# Backup originals and copy patched files
cp /system/framework/services.jar /system/framework/services.jar.orig
cp /system/framework/oat/x86_64/services.odex /system/framework/oat/x86_64/services.odex.orig
cp /data/local/tmp/services_patched.jar /system/framework/services.jar
cp /data/local/tmp/services.odex /system/framework/oat/x86_64/services.odex
chmod 644 /system/framework/services.jar /system/framework/oat/x86_64/services.*
reboot
"
```

**Path B: Runtime bind mount (device without writable-system)**

```bash
adb push services_patched.jar /data/local/tmp/

adb shell "
# Generate OAT files
cd /data/local/tmp
mkdir oat_out
unzip -o services_patched.jar '*.dex' -d dex_tmp
dex2oat --dex-file=dex_tmp/classes.dex --dex-file=dex_tmp/classes2.dex \
  --oat-file=oat_out/services.odex \
  --boot-image=/system/framework/x86_64/boot.art \
  --instruction-set=x86_64 --compiler-filter=speed

# Fix SELinux contexts
chcon u:object_r:system_file:s0 services_patched.jar
chcon u:object_r:system_file:s0 oat_out/services.odex
chcon u:object_r:system_file:s0 oat_out/services.vdex

# Bind mount over read-only /system
mount -o bind /data/local/tmp/services_patched.jar /system/framework/services.jar
mount -o bind /data/local/tmp/oat_out/services.odex /system/framework/oat/x86_64/services.odex
mount -o bind /data/local/tmp/oat_out/services.vdex /system/framework/oat/x86_64/services.vdex
"
```

> Bind mounts are lost on reboot. Re-run after each boot or persist via ramdisk init script.

### Step 6: SELinux for Automotive/multi-user

Automotive emulators use multi-user (e.g., user 10 for current driver). `sharedUserId="android.uid.system"` maps to UID `1001000` (= 10*100000 + 1000). SELinux has no context for this UID.

Set SELinux permissive:

```bash
adb shell setenforce 0
```

This must be done after each reboot. To automate, add to ramdisk `init.ranchu.rc` or create `/system/etc/init/boot_permissive.rc` (if /system is writable):

```
on boot
    setenforce 0
```

> `setenforce` is an Android init built-in command (NOT `write /sys/fs/selinux/enforce` which is blocked by SELinux itself).

### Step 7: Install and verify

```bash
adb install -r -t your_app.apk

# Verify
adb shell "dumpsys package <package.name> | grep -E 'userId|sharedUser'"
# Should show: userId=1000, sharedUser=SharedUserSetting{... android.uid.system/1000}
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ClassNotFoundException: SystemServer` after reboot | OAT checksum mismatch — regenerate OAT with dex2oat AND bind mount the new OAT files too |
| `Broken pipe` during install | PMS crashed. Check our patches didn't break verifySignatures state setup. Keep verifySignatures mostly intact, only patch the lineage check |
| SELinux `No match for app with uid 1001000` | Multi-user environment. `setenforce 0` required |
| `adb remount` fails | Need `-writable-system` on emulator cold boot OR `adb disable-verity` first |
| Bind mount blocked by SELinux | Run `chcon u:object_r:system_file:s0` on the source files |
| Vendor init.rc changes not loaded | Init reads from lowerdir partition, not overlay. Use system overlay `/system/etc/init/` or ramdisk modification |

## Key files and their roles

| File | Role |
|------|------|
| `services.jar` | Contains PackageManagerService — the signature verification engine |
| `PackageManagerServiceUtils.smali` | Has `compareSignatures`, `canJoinSharedUserId`, `verifySignatures` |
| `oat/x86_64/services.odex` | Pre-compiled ART code. Must match DEX checksum |
| `boot.art` | Boot image. Used by dex2oat for framework compilation reference |
| `packages.xml` | PMS database at `/data/system/`. Records sharedUserId assignments |

---
name: android-empty-project
description: Creates minimal Android project structure from scratch. Supports Kotlin/Java and Gradle Kotlin DSL or Groovy. Use when the user wants to create an Android empty project, start a new Android app, scaffold Android project structure, or mentions 安卓空工程、Android 空工程.
---

# Android 空工程

从零搭建最小化 Android 项目结构，支持 Kotlin/Java、Gradle Kotlin DSL（推荐）或 Groovy，仅含一个主 Activity 与必要资源。

## 创建前选择

| 选项 | 推荐 | 说明 |
|------|------|------|
| **语言** | Kotlin | 新项目首选；选 Java 则用下面 Java 模板 |
| **Gradle** | Kotlin DSL（.kts） | 新项目默认；Groovy 见 [reference.md](reference.md) |

---

## 目录结构（Kotlin + Kotlin DSL）

在目标位置创建工程根目录（如 `MyApp/`），再按下列结构创建文件：

```
MyApp/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle.properties
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.properties
│       └── gradle-wrapper.jar
├── app/
│   ├── build.gradle.kts
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/example/myapp/
│   │       │   └── MainActivity.kt
│   │       └── res/
│   │           └── values/
│   │               └── strings.xml
│   └── proguard-rules.pro
├── gradlew
└── gradlew.bat
```

`gradle-wrapper.jar` 可从已有 Android 项目复制，或使用 `gradle wrapper` 生成。以下仅给出必选源码与配置。

---

## 根目录配置

### settings.gradle.kts

```kotlin
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "MyApp"
include(":app")
```

### build.gradle.kts（根）

```kotlin
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.20" apply false
}
```

版本号可按需升级，保持与 AGP、Kotlin 兼容。

### gradle.properties

```properties
android.useAndroidX=true
kotlin.code.style=official
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
```

---

## app 模块

### app/build.gradle.kts

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}
android {
    namespace = "com.example.myapp"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
}
```

### app/src/main/AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@android:drawable/sym_def_app_icon"
        android:label="@string/app_name"
        android:roundIcon="@android:drawable/sym_def_app_icon"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApp">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

**注意：** 使用 `AppCompatActivity` 时，主题必须使用 `Theme.AppCompat` 系列，不能使用系统主题如 `Theme.Material.Light.NoActionBar`。

### app/src/main/java/com/example/myapp/MainActivity.kt

包名与 `namespace`、目录路径一致。

```kotlin
package com.example.myapp

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(android.R.layout.simple_list_item_1)
    }
}
```

若需自定义布局：在 `res/layout/activity_main.xml` 定义，`setContentView(R.layout.activity_main)`。

### app/src/main/res/values/strings.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">我的应用</string>
</resources>
```

### app/src/main/res/values/themes.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.MyApp" parent="Theme.AppCompat.Light.NoActionBar">
        <item name="colorPrimary">#3F51B5</item>
        <item name="colorPrimaryDark">#303F9F</item>
        <item name="colorAccent">#FF4081</item>
    </style>
</resources>
```

**说明：**
- `Theme.AppCompat.Light.NoActionBar`：浅色主题，无 ActionBar
- `colorPrimary`：主色调
- `colorPrimaryDark`：状态栏颜色
- `colorAccent`：强调色
- AndroidManifest.xml 中使用 `android:theme="@style/Theme.MyApp"` 引用

### app/proguard-rules.pro

可留空或仅保留注释：

```
# Add project specific ProGuard rules here.
```

---

## Java 版本（可选）

若选 **Java**：

1. `app/build.gradle.kts` 中移除 `id("org.jetbrains.kotlin.android")`，不配置 `kotlinOptions`。
2. 将 `MainActivity.kt` 改为 `MainActivity.java`，包名与目录一致：

```java
package com.example.myapp;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(android.R.layout.simple_list_item_1);
    }
}
```

3. 根 `build.gradle.kts` 中可去掉 Kotlin 插件行。

---

## Gradle Wrapper

若工程内无 `gradlew` / `gradle/wrapper`：

- 从其他 Android 项目复制 `gradle/wrapper/`、`gradlew`、`gradlew.bat`，或
- 在工程根目录执行：`gradle wrapper --gradle-version 8.2`（需本机已装 Gradle）。

`gradle/wrapper/gradle-wrapper.properties` 示例：

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

---

## 运行与验证

1. 用 Android Studio 打开工程根目录（选择含 `build.gradle.kts` 的目录）。
2. 同步 Gradle（Sync Project with Gradle Files）。
3. 连接设备或启动模拟器，运行 `app`。

命令行构建：

```bash
./gradlew assembleDebug
```

APK 输出：`app/build/outputs/apk/debug/app-debug.apk`。

---

## 补充说明

- Groovy 版 `build.gradle` 模板、自定义主题与布局、权限与多模块说明见 [reference.md](reference.md)。
- 集成地图/定位等 SDK 时，在 `app/build.gradle.kts` 添加依赖，并在 `AndroidManifest.xml` 中声明所需权限与组件。

---
name: mojoauth-oidc-hosted-page-android
description: Implement passwordless authentication in native Android/Kotlin applications using MojoAuth OIDC with AppAuth.
---

# Implement MojoAuth OIDC (Android)

This expert AI assistant guide walks you through integrating passwordless authentication into an existing Android application using MojoAuth's Hosted Login Page as an OIDC identity provider via AppAuth for Android. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing Android application (minSdk 23+) with a login screen.
- Android Studio and Kotlin/Java knowledge.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required library: `net.openid:appauth` (AppAuth for Android).

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the callback URI using a custom scheme (e.g., `com.example.myapp://auth/callback`).
4. Retrieve **Client ID**.
5. Enable your preferred authentication methods.

> **Note:** For native/mobile apps, use **Authorization Code with PKCE** (no Client Secret on the device).

### Step 2: Modify the Existing Android Project

#### Substep 2.1: Add Dependencies

Add to your `app/build.gradle`:

```groovy
// app/build.gradle
dependencies {
    implementation 'net.openid:appauth:0.11.1'
}
```

#### Substep 2.2: Configure Redirect Scheme

Add the redirect scheme to your `app/build.gradle`:

```groovy
android {
    defaultConfig {
        manifestPlaceholders = [
            'appAuthRedirectScheme': 'com.example.myapp'
        ]
    }
}
```

Add the redirect activity in `AndroidManifest.xml`:

```xml
<!-- AndroidManifest.xml -->
<activity
    android:name="net.openid.appauth.RedirectUriReceiverActivity"
    android:exported="true"
    tools:node="replace">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="com.example.myapp"
              android:host="auth"
              android:path="/callback" />
    </intent-filter>
</activity>
```

#### Substep 2.3: Configure OIDC

Create an auth configuration helper (e.g., `AuthConfig.kt`):

```kotlin
// AuthConfig.kt
package com.example.myapp.auth

import android.net.Uri
import net.openid.appauth.AuthorizationServiceConfiguration

object AuthConfig {
    const val CLIENT_ID = "your_client_id"
    val REDIRECT_URI: Uri = Uri.parse("com.example.myapp://auth/callback")
    val ISSUER_URI: Uri = Uri.parse("https://your-app.mojoauth.com")
    const val SCOPE = "openid profile email"

    fun fetchConfiguration(callback: (AuthorizationServiceConfiguration?, Exception?) -> Unit) {
        AuthorizationServiceConfiguration.fetchFromIssuer(ISSUER_URI) { config, ex ->
            callback(config, ex)
        }
    }
}
```

#### Substep 2.4: Update Login Activity/UI

Since MojoAuth handles all authentication on its Hosted Login Page, your login layout only needs a **"Sign In" button**:

```xml
<!-- res/layout/activity_login.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="24dp"
    android:gravity="center">

    <TextView android:text="Welcome"
        android:textSize="28sp" android:textStyle="bold"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:layout_marginBottom="8dp" />

    <TextView android:text="Sign in with your preferred method"
        android:textSize="14sp"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:layout_marginBottom="24dp" />

    <Button android:id="@+id/signInButton"
        android:text="Sign In with MojoAuth"
        android:layout_width="match_parent" android:layout_height="wrap_content"
        android:layout_marginBottom="16dp" />

    <TextView android:text="Powered by MojoAuth"
        android:textSize="12sp" android:textColor="#888888"
        android:layout_width="wrap_content" android:layout_height="wrap_content" />
</LinearLayout>
```

#### Substep 2.5: Update Login Activity Logic

```kotlin
// LoginActivity.kt
package com.example.myapp

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.*
import androidx.activity.result.contract.ActivityResultContracts
import com.example.myapp.auth.AuthConfig
import net.openid.appauth.*

class LoginActivity : Activity() {
    private lateinit var authService: AuthorizationService

    private val authLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val data = result.data ?: return@registerForActivityResult
        val response = AuthorizationResponse.fromIntent(data)
        val exception = AuthorizationException.fromIntent(data)

        if (response != null) {
            exchangeCodeForToken(response)
        } else {
            Log.e("OIDC", "Authorization failed: ${exception?.message}")
            Toast.makeText(this, "Authentication failed", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        authService = AuthorizationService(this)

        val signInButton = findViewById<Button>(R.id.signInButton)

        signInButton.setOnClickListener {
            startMojoAuthLogin()
        }
    }

    private fun startMojoAuthLogin() {
        AuthConfig.fetchConfiguration { config, ex ->
            if (config == null) {
                Log.e("OIDC", "Discovery failed: ${ex?.message}")
                return@fetchConfiguration
            }

            val authRequest = AuthorizationRequest.Builder(
                config,
                AuthConfig.CLIENT_ID,
                ResponseTypeValues.CODE,
                AuthConfig.REDIRECT_URI
            )
                .setScope(AuthConfig.SCOPE)
                .build()

            val authIntent = authService.getAuthorizationRequestIntent(authRequest)
            authLauncher.launch(authIntent)
        }
    }

    private fun exchangeCodeForToken(response: AuthorizationResponse) {
        val tokenRequest = response.createTokenExchangeRequest()

        authService.performTokenRequest(tokenRequest) { tokenResponse, exception ->
            if (tokenResponse != null) {
                Log.d("OIDC", "Access Token: ${tokenResponse.accessToken}")
                // TODO: Use access token to fetch user info and create session
                val intent = Intent(this, DashboardActivity::class.java)
                startActivity(intent)
                finish()
            } else {
                Log.e("OIDC", "Token exchange failed: ${exception?.message}")
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        authService.dispose()
    }
}
```

### Step 3: Test the Implementation

1. Run your application on an emulator or device.
2. Tap **"Sign In with MojoAuth"**.
3. A browser tab opens to the MojoAuth Hosted Login Page.
4. Authenticate using any available method.
5. Verify you are redirected back to the app and into the Dashboard.

## 3. Additional Considerations

- **Security**: PKCE is handled automatically by AppAuth. Never embed Client Secrets in mobile apps.
- **Token Storage**: Use `EncryptedSharedPreferences` to store tokens securely.
- **Error Handling**: Handle network failures and token expiry gracefully.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Library Documentation**: Refer to the [AppAuth for Android documentation](https://github.com/openid/AppAuth-Android).

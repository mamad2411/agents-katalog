---
name: oidc-hosted-page-android
description: Implement "Sign in with SSO" in native Android/Kotlin applications using SSOJet OIDC with AppAuth.
---

# Implement SSOJet OIDC (Android)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing Android application using SSOJet as an OIDC identity provider via AppAuth for Android.

## 1. Prerequisites

- An existing Android application (minSdk 23+) with a login screen.
- Android Studio and Kotlin/Java knowledge.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required library: `net.openid:appauth` (AppAuth for Android).

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyAndroidApp", type **Native / Mobile**).
4. Configure the callback URI using a custom scheme (e.g., `com.example.myapp://auth/callback`).
5. Retrieve **Client ID**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

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
    val ISSUER_URI: Uri = Uri.parse("https://auth.ssojet.com")
    const val SCOPE = "openid profile email"

    fun fetchConfiguration(callback: (AuthorizationServiceConfiguration?, Exception?) -> Unit) {
        AuthorizationServiceConfiguration.fetchFromIssuer(ISSUER_URI) { config, ex ->
            callback(config, ex)
        }
    }
}
```

#### Substep 2.4: Update Login Activity/UI

Modify your login activity layout (`activity_login.xml`):

```xml
<!-- res/layout/activity_login.xml -->
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="24dp"
    android:gravity="center">

    <TextView android:text="Sign In"
        android:textSize="28sp" android:textStyle="bold"
        android:layout_width="wrap_content" android:layout_height="wrap_content"
        android:layout_marginBottom="24dp" />

    <EditText android:id="@+id/emailInput"
        android:hint="Email" android:inputType="textEmailAddress"
        android:layout_width="match_parent" android:layout_height="wrap_content"
        android:layout_marginBottom="16dp" />

    <EditText android:id="@+id/passwordInput"
        android:hint="Password" android:inputType="textPassword"
        android:layout_width="match_parent" android:layout_height="wrap_content"
        android:layout_marginBottom="16dp" />

    <Button android:id="@+id/signInButton"
        android:text="Sign In"
        android:layout_width="match_parent" android:layout_height="wrap_content"
        android:layout_marginBottom="8dp" />

    <Button android:id="@+id/ssoToggleButton"
        android:text="Sign in with SSO"
        android:background="@android:color/transparent"
        android:textColor="#2196F3"
        android:layout_width="match_parent" android:layout_height="wrap_content" />
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
import android.view.View
import android.widget.*
import androidx.activity.result.contract.ActivityResultContracts
import com.example.myapp.auth.AuthConfig
import net.openid.appauth.*

class LoginActivity : Activity() {
    private var isSSO = false
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
            Toast.makeText(this, "SSO login failed", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        authService = AuthorizationService(this)

        val emailInput = findViewById<EditText>(R.id.emailInput)
        val passwordInput = findViewById<EditText>(R.id.passwordInput)
        val signInButton = findViewById<Button>(R.id.signInButton)
        val ssoToggle = findViewById<Button>(R.id.ssoToggleButton)

        ssoToggle.setOnClickListener {
            isSSO = !isSSO
            passwordInput.visibility = if (isSSO) View.GONE else View.VISIBLE
            signInButton.text = if (isSSO) "Continue with SSO" else "Sign In"
            ssoToggle.text = if (isSSO) "Back to Password Login" else "Sign in with SSO"
        }

        signInButton.setOnClickListener {
            val email = emailInput.text.toString()
            if (isSSO) {
                startSSOLogin(email)
            } else {
                Log.d("Login", "Processing traditional login...")
            }
        }
    }

    private fun startSSOLogin(email: String) {
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
                .setLoginHint(email)
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

### Step 3: Test the Modified Connection

1. Run your application on an emulator or device.
2. Verify the login screen shows Email + Password by default.
3. Tap **"Sign in with SSO"** and ensure the password field hides.
4. Enter a test email and tap "Continue with SSO".
5. A browser tab opens to the SSOJet login page.
6. Authenticate and verify you are redirected back to the app.

## 3. Additional Considerations

- **Security**: PKCE is handled automatically by AppAuth. Never embed Client Secrets in mobile apps.
- **Token Storage**: Use `EncryptedSharedPreferences` to store tokens securely.
- **Error Handling**: Handle network failures and token expiry gracefully.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Library Documentation**: Refer to the [AppAuth for Android documentation](https://github.com/openid/AppAuth-Android).

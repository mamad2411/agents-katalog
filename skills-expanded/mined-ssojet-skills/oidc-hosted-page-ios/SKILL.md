---
name: oidc-hosted-page-ios
description: Implement "Sign in with SSO" in native iOS/Swift applications using SSOJet OIDC with AppAuth.
---

# Implement SSOJet OIDC (iOS / Swift)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing iOS application using SSOJet as an OIDC identity provider via AppAuth for iOS.

## 1. Prerequisites

- An existing iOS 15+ application (Swift 5.7+) with a login screen.
- Xcode 14+ installed.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required library: `openid/AppAuth-iOS`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyiOSApp", type **Native / Mobile**).
4. Configure the callback URI using a custom scheme (e.g., `com.example.myapp://auth/callback`).
5. Retrieve **Client ID**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

> **Note:** For native/mobile apps, use **Authorization Code with PKCE** (no Client Secret on the device).

### Step 2: Modify the Existing iOS Project

#### Substep 2.1: Add Dependencies

Add AppAuth via **Swift Package Manager**:
1. In Xcode, go to **File > Add Package Dependencies**.
2. Enter: `https://github.com/openid/AppAuth-iOS.git`.
3. Select the latest stable version and add to your target.

Or via **CocoaPods**:

```ruby
# Podfile
pod 'AppAuth'
```

```bash
pod install
```

#### Substep 2.2: Configure URL Scheme

Add a custom URL scheme in your `Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>com.example.myapp</string>
        </array>
        <key>CFBundleURLName</key>
        <string>com.example.myapp</string>
    </dict>
</array>
```

#### Substep 2.3: Configure OIDC

Create an auth configuration helper (e.g., `AuthConfig.swift`):

```swift
// AuthConfig.swift
import Foundation

struct AuthConfig {
    static let issuerURL = URL(string: "https://auth.ssojet.com")!
    static let clientID = "your_client_id"
    static let redirectURI = URL(string: "com.example.myapp://auth/callback")!
    static let scopes = ["openid", "profile", "email"]
}
```

#### Substep 2.4: Create Auth Manager

Create a centralised auth manager (e.g., `AuthManager.swift`):

```swift
// AuthManager.swift
import UIKit
import AppAuth

class AuthManager: NSObject {
    static let shared = AuthManager()
    var currentAuthorizationFlow: OIDExternalUserAgentSession?
    var authState: OIDAuthState?

    func login(from viewController: UIViewController, loginHint: String?, completion: @escaping (Result<OIDAuthState, Error>) -> Void) {
        // Discover OIDC configuration
        OIDAuthorizationService.discoverConfiguration(forIssuer: AuthConfig.issuerURL) { config, error in
            guard let config = config else {
                completion(.failure(error ?? NSError(domain: "OIDC", code: -1, userInfo: [NSLocalizedDescriptionKey: "Discovery failed"])))
                return
            }

            // Build authorization request
            var additionalParams: [String: String] = [:]
            if let hint = loginHint, !hint.isEmpty {
                additionalParams["login_hint"] = hint
            }

            let request = OIDAuthorizationRequest(
                configuration: config,
                clientId: AuthConfig.clientID,
                scopes: AuthConfig.scopes,
                redirectURL: AuthConfig.redirectURI,
                responseType: OIDResponseTypeCode,
                additionalParameters: additionalParams
            )

            // Launch auth flow
            self.currentAuthorizationFlow = OIDAuthState.authState(
                byPresenting: request,
                presenting: viewController
            ) { authState, error in
                if let authState = authState {
                    self.authState = authState
                    print("Authenticated! Access Token: \(authState.lastTokenResponse?.accessToken ?? "nil")")
                    completion(.success(authState))
                } else {
                    print("OIDC Error: \(error?.localizedDescription ?? "Unknown error")")
                    completion(.failure(error ?? NSError(domain: "OIDC", code: -1)))
                }
            }
        }
    }

    func logout() {
        authState = nil
    }
}
```

#### Substep 2.5: Handle Redirect in AppDelegate / SceneDelegate

```swift
// AppDelegate.swift (or SceneDelegate.swift)
import AppAuth

// In AppDelegate:
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
    if let flow = AuthManager.shared.currentAuthorizationFlow,
       flow.resumeExternalUserAgentFlow(with: url) {
        AuthManager.shared.currentAuthorizationFlow = nil
        return true
    }
    return false
}

// If using SceneDelegate:
func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
    guard let url = URLContexts.first?.url else { return }
    if let flow = AuthManager.shared.currentAuthorizationFlow,
       flow.resumeExternalUserAgentFlow(with: url) {
        AuthManager.shared.currentAuthorizationFlow = nil
    }
}
```

#### Substep 2.6: Update Login View Controller

```swift
// LoginViewController.swift
import UIKit

class LoginViewController: UIViewController {
    private let emailTextField = UITextField()
    private let passwordTextField = UITextField()
    private let signInButton = UIButton(type: .system)
    private let ssoToggleButton = UIButton(type: .system)
    private var isSSO = false

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    private func setupUI() {
        view.backgroundColor = .systemBackground
        title = "Sign In"

        emailTextField.placeholder = "Email"
        emailTextField.keyboardType = .emailAddress
        emailTextField.borderStyle = .roundedRect

        passwordTextField.placeholder = "Password"
        passwordTextField.isSecureTextEntry = true
        passwordTextField.borderStyle = .roundedRect

        signInButton.setTitle("Sign In", for: .normal)
        signInButton.addTarget(self, action: #selector(handleSignIn), for: .touchUpInside)

        ssoToggleButton.setTitle("Sign in with SSO", for: .normal)
        ssoToggleButton.addTarget(self, action: #selector(toggleSSO), for: .touchUpInside)

        let stack = UIStackView(arrangedSubviews: [emailTextField, passwordTextField, signInButton, ssoToggleButton])
        stack.axis = .vertical
        stack.spacing = 16
        stack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(stack)

        NSLayoutConstraint.activate([
            stack.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            stack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -24),
        ])
    }

    @objc private func toggleSSO() {
        isSSO.toggle()
        passwordTextField.isHidden = isSSO
        signInButton.setTitle(isSSO ? "Continue with SSO" : "Sign In", for: .normal)
        ssoToggleButton.setTitle(isSSO ? "Back to Password Login" : "Sign in with SSO", for: .normal)
    }

    @objc private func handleSignIn() {
        let email = emailTextField.text ?? ""

        if isSSO {
            AuthManager.shared.login(from: self, loginHint: email) { result in
                DispatchQueue.main.async {
                    switch result {
                    case .success:
                        let dashboard = DashboardViewController()
                        self.navigationController?.pushViewController(dashboard, animated: true)
                    case .failure(let error):
                        let alert = UIAlertController(title: "Error", message: error.localizedDescription, preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "OK", style: .default))
                        self.present(alert, animated: true)
                    }
                }
            }
        } else {
            print("Processing traditional login...")
        }
    }
}
```

### Step 3: Test the Modified Connection

1. Run on a simulator or device.
2. Verify the login screen shows Email + Password by default.
3. Tap **"Sign in with SSO"** and ensure the password field hides.
4. Enter a test email and tap "Continue with SSO".
5. A browser/ASWebAuthenticationSession opens to SSOJet.
6. Authenticate and verify you are redirected back to the app.

## 3. Additional Considerations

- **Security**: PKCE is handled automatically by AppAuth. Never embed Client Secrets in mobile apps.
- **Token Storage**: Use the iOS Keychain to store tokens securely.
- **SwiftUI**: For SwiftUI apps, wrap the `OIDAuthState.authState(byPresenting:)` call in a coordinator or use `ASWebAuthenticationSession` directly.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Library Documentation**: Refer to the [AppAuth for iOS documentation](https://github.com/openid/AppAuth-iOS).

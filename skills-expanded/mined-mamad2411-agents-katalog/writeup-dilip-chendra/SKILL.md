<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dilip-chendra
description: CTF writeups and security challenges by Dilip-chendra.
---

# Writeups by Dilip-chendra

Source repository: `/repos/Dilip-chendra`

## Repository Index

- flutter-react-bugbounty/README.md
- flutter-react-bugbounty/Assignment- Flutter/README.md
- flutter-react-bugbounty/BugBounty/README.md
- flutter-react-bugbounty/kanban-board-app/README.md
- flutter-react-bugbounty/kanban-board-app/kanban-board-app/README.md
- flutter-react-bugbounty/Assignment- Flutter/ecommerce_app/README.md
- flutter-react-bugbounty/Assignment- Flutter/ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md
- flutter-react-bugbounty/Assignment- Flutter/ecommerce_app/ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md

## Writeup Content


### File: flutter-react-bugbounty/Assignment- Flutter/README.md

# Flutter E-Commerce Application

## Overview
This is a comprehensive e-commerce mobile application built using Flutter, following clean architecture principles and utilizing the Fake Store API.

## Features
- Product Listing with Infinite Scrolling
- Product Search Functionality
- Product Detail Page
- User Authentication
  - Login
  - Registration
  - Logout
- Cart Management
- Product Sorting and Filtering

## Authentication Flow
- Secure login and registration
- Form validation for registration
- Token-based authentication
- Persistent user sessions
- Error handling for authentication processes

## Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK
- Android Studio or VS Code with Flutter extensions
- Git

## Setup and Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/ecommerce_app.git
cd ecommerce_app
```

2. Install dependencies
```bash
flutter pub get
```

3. Run the application
```bash
flutter run
```

## Project Structure
```
lib/
├── core/
│   ├── constants/
│   ├── errors/
│   └── network/
├── features/
│   ├── products/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── cart/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```

## State Management
- Provider is used for state management
- Follows clean architecture with separation of concerns

## Authentication
- Implements secure user registration and login
- Uses Fake Store API for authentication
- Supports token-based authentication
- Persistent login state using SharedPreferences

## API
- Uses Fake Store API (https://fakestoreapi.com/)
- Implements comprehensive error handling
- Supports pagination and sorting

## Testing
- Unit tests for repositories and use cases
- Widget tests for UI components
- Authentication flow testing

## Dependencies
- provider: State management
- http: Network requests
- go_router: Navigation
- cached_network_image: Image caching
- form_validator: Form validation
- logger: Logging
- shared_preferences: Local storage
- equatable: Value equality

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ecommerce_app](https://github.com/yourusername/ecommerce_app)

## Cart Management
- Add products to cart from product list and product details
- Remove products from cart
- Update cart item quantities
- Persistent cart storage using SharedPreferences
- Total price and item count calculations
- Error handling for cart operations
- Cart icon with item count in app bar
- Dismissible cart items
- Quantity selector in product details

## Cart Features
- Supports multiple cart items
- Prevents duplicate items
- Calculates total cart value
- Manages cart state with Provider
- Integrated with product pages
- Easy cart management 


### File: flutter-react-bugbounty/Assignment- Flutter/ecommerce_app/README.md

# ecommerce_app

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.



### File: flutter-react-bugbounty/Assignment- Flutter/ecommerce_app/ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md

# Launch Screen Assets

You can customize the launch screen with your own desired assets by replacing the image files in this directory.

You can also do it by opening your Flutter project's Xcode project with `open ios/Runner.xcworkspace`, selecting `Runner/Assets.xcassets` in the Project Navigator and dropping in the desired images.


### File: flutter-react-bugbounty/Assignment- Flutter/ios/Runner/Assets.xcassets/LaunchImage.imageset/README.md

# Launch Screen Assets

You can customize the launch screen with your own desired assets by replacing the image files in this directory.

You can also do it by opening your Flutter project's Xcode project with `open ios/Runner.xcworkspace`, selecting `Runner/Assets.xcassets` in the Project Navigator and dropping in the desired images.


### File: flutter-react-bugbounty/BugBounty/README.md

# Mitt Arv Security Fixes

This repository contains security fixes for the Mitt Arv application, addressing several critical vulnerabilities identified during the Beta Phase testing. Each fix is implemented as a standalone module that can be integrated into the main application.

## 🔒 Security Vulnerabilities Fixed

### 1. Multi-Factor Authentication (MFA)
**File**: `auth_mfa_fix.py`
- Implements OTP-based authentication
- Adds biometric login support
- Secures session token generation
- Uses PBKDF2 for password hashing

### 2. Session Management
**File**: `session_timeout_fix.py`
- Automatic session expiration after 15 minutes of inactivity
- Secure session token handling
- Background cleanup of expired sessions
- Middleware support for web frameworks

### 3. Data Encryption
**File**: `encrypt_storage_fix.py`
- AES-256 encryption for sensitive data
- Secure key derivation using PBKDF2
- PKCS7 padding implementation
- Support for both string and JSON data

### 4. Secure Data Wiping
**File**: `secure_uninstall_fix.py`
- Multi-pass data wiping (DoD-style)
- Secure directory traversal
- Verification of data removal
- Detailed logging of operations

### 5. Rate Limiting
**File**: `rate_limit_login_fix.py`
- Limits login attempts to 5 per minute
- IP-based blocking system
- Sliding window approach
- Automatic cleanup of old attempts

### 6. API Key Security
**File**: `secure_api_keys.py`
- Secure storage of API keys in environment variables
- Encryption of stored keys
- Key rotation support
- Metadata management

### 7. Trusted Contact Verification
**File**: `trusted_contact_verification.py`
- Multi-level verification (email, phone, biometric)
- Time-limited verification sessions
- Integration with email and SMS services
- Secure verification token handling

## 📋 Requirements

```bash
pip install -r requirements.txt
```

Required Python packages:
- cryptography>=41.0.0
- pyotp>=2.8.0
- python-dotenv>=1.0.0
- requests>=2.31.0
- twilio>=8.5.0
- jwt>=1.3.1
- PyJWT>=2.8.0

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/mitt-arv-security-fixes.git
cd mitt-arv-security-fixes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 💡 Usage Examples

### Multi-Factor Authentication
```python
from auth_mfa_fix import MFAAuthenticator

auth = MFAAuthenticator()

# Step 1: Initial login
result = auth.authenticate_user("user@example.com", "password123")

# Step 2: Verify OTP
if result["requires_otp"]:
    otp = auth.generate_otp("user@example.com")
    result = auth.authenticate_user(
        "user@example.com", 
        "password123",
        otp=otp
    )
```

### Secure Data Storage
```python
from encrypt_storage_fix import SecureStorage

storage = SecureStorage("master-key")

# Encrypt sensitive data
sensitive_data = {
    "ssn": "123-45-6789",
    "credit_card": "4111-1111-1111-1111"
}

encrypted = storage.encrypt_data(sensitive_data)
decrypted = storage.decrypt_data(encrypted)
```

### Rate Limiting
```python
from rate_limit_login_fix import LoginManager

login_manager = LoginManager()

# Attempt login with rate limiting
result = login_manager.attempt_login(
    username="user@example.com",
    password="password123",
    ip_address="192.168.1.1"
)
```

## 🔧 Configuration

### Email Verification Settings
Update `contact_verification_config.json`:
```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "password": "your-app-specific-password"
    }
}
```

### SMS Verification Settings
Update Twilio credentials in `contact_verification_config.json`:
```json
{
    "sms": {
        "twilio_account_sid": "your-account-sid",
        "twilio_auth_token": "your-auth-token",
        "twilio_phone_number": "your-twilio-number"
    }
}
```

## 🛡️ Security Best Practices

1. **API Keys**: Never commit API keys or sensitive credentials to version control
2. **Environment Variables**: Use `.env` files for configuration
3. **Encryption Keys**: Rotate encryption keys periodically
4. **Logging**: Monitor and review security logs regularly
5. **Updates**: Keep all dependencies up to date

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Security Auditing

Regular security audits are recommended to ensure:
- All security modules are properly configured
- Dependencies are up to date
- No new vulnerabilities have been introduced
- Logging and monitoring are functioning correctly

## ⚠️ Important Notes

1. This is a security-focused implementation. Review and adapt according to your specific needs.
2. Some implementations (like biometric verification) require platform-specific integration.
3. Always follow security best practices when deploying in production.
4. Regularly update dependencies to patch security vulnerabilities.
5. Monitor security logs and implement proper alerting mechanisms.

## 📞 Support

For security-related issues, please report them immediately to security@mittarv.com.
For general questions, create an issue in the repository. 


### File: flutter-react-bugbounty/README.md

# flutter-react-bugbounty
📌 Assignments Repository: Flutter, React &amp; Security Bug Bounty  This repo contains three assignments: ✔ Flutter &amp; React Kanban Boards with task management &amp; drag-drop. ✔ Security Bug Bounty Report with identified vulnerabilities &amp; fixes. ✔ Follows best coding practices &amp; includes detailed documentation. 🚀



### File: flutter-react-bugbounty/kanban-board-app/README.md

# Kanban Board Application

## Overview
This is a Kanban Board application built with React, Redux, and Material-UI. It allows users to manage tasks across different stages: To Do, In Progress, Peer Review, and Done.

## Features
- Drag and drop task management
- Search functionality to filter tasks
- Add new tasks with title and description
- Responsive design
- State management with Redux

## Prerequisites
- Node.js (v14 or later)
- npm (v6 or later)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/kanban-board-app.git
cd kanban-board-app
```

2. Install dependencies
```bash
npm install
```

3. Start the development server
```bash
npm start
```

The application will open in your default browser at `http://localhost:3000`

## Technologies Used
- React
- TypeScript
- Redux Toolkit
- React Beautiful DnD
- Material-UI
- UUID for unique task IDs

## Project Structure
```
src/
├── components/
│   ├── KanbanBoard.tsx
│   ├── KanbanColumn.tsx
│   └── TaskCard.tsx
├── redux/
│   ├── store.ts
│   └── taskSlice.ts
├── types/
│   └── task.ts
└── App.tsx
```

## Usage
- Drag and drop tasks between columns
- Use the search bar to filter tasks
- Click "Add Task" to create a new task in the To Do column

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.



### File: flutter-react-bugbounty/kanban-board-app/kanban-board-app/README.md

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).


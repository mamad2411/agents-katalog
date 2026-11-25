# How to Disable Irrelevant Extensions (Correct Method)

## The ONLY Way That Works Without Opening 26 Windows

### Method: Manual Disable via Extensions Panel

1. **Press `Ctrl+Shift+X`** to open Extensions panel
2. For each extension below, **click the gear icon ⚙️** next to it
3. Select **"Disable (Workspace)"**
4. Repeat for all listed extensions

This takes 2-3 minutes but **won't open 26 Cursor windows** like the script did.

---

## Extensions to Disable (26 total)

### Java Extensions (8) - Search "java"
- ❌ **Java** (redhat.java)
- ❌ **Extension Pack for Java** (vscjava.vscode-java-pack)
- ❌ **Debugger for Java** (vscjava.vscode-java-debug)
- ❌ **Test Runner for Java** (vscjava.vscode-java-test)
- ❌ **Project Manager for Java** (vscjava.vscode-java-dependency)
- ❌ **Maven for Java** (vscjava.vscode-maven)
- ❌ **Gradle for Java** (vscjava.vscode-gradle)
- ❌ **Google Java Format** (josevseb.google-java-format-for-vs-code)

### Python Extensions (2) - Search "python"
- ❌ **Python** (ms-python.python)
- ❌ **Python Debugger** (ms-python.debugpy)

### Android Native (3) - Search "android"
- ❌ **Android Dev Extension** (adelphes.android-dev-ext)
- ❌ **APKLab** (surendrajat.apklab)
- ❌ **Smalise** (loyieking.smalise)

### Docker (3) - Search "docker"
- ❌ **Docker** (ms-azuretools.vscode-docker)
- ❌ **Azure Containers** (ms-azuretools.vscode-containers)
- ❌ **Remote Containers** (anysphere.remote-containers)

### Google Cloud (3) - Search "google"
- ❌ **Cloud Code** (googlecloudtools.cloudcode)
- ❌ **Firebase DataConnect** (googlecloudtools.firebase-dataconnect-vscode)
- ❌ **Gemini Code Assist** (google.geminicodeassist)

### Other (7)
- ❌ **Kotlin** (mathiasfrohlich.kotlin) - Search "kotlin"
- ❌ **GraphQL Syntax** (graphql.vscode-graphql-syntax) - Search "graphql"
- ❌ **GitHub Actions** (github.vscode-github-actions) - Search "github actions"
- ❌ **SonarLint** (sonarsource.sonarlint-vscode) - Search "sonar"
- ❌ **Enlighter** (ai-dl.enlighter) - Search "enlighter"
- ❌ **i18n Ally** (lokalise.i18n-ally) - Search "i18n"
- ❌ **XML** (redhat.vscode-xml) - Search "xml"

---

## Quick Tip

To disable multiple extensions faster:
1. Open Extensions panel (`Ctrl+Shift+X`)
2. Search for the category (e.g., "java")
3. Disable all matching extensions at once
4. Move to next category

---

## Why This Matters

**Before:** 38 active extensions = 5-15 minute delays
**After:** 12 active extensions = <3 second responses

Each disabled extension means:
- ✅ One less language server running
- ✅ One less file watcher indexing
- ✅ One less background process competing for CPU
- ✅ Much faster Cursor startup and operations

---

## Alternative: Do Nothing

If you prefer not to manually disable extensions, the `.vscode/settings.json` file already disables the **language servers** for Java, Python, and Docker. You'll still see the extensions in the list, but they won't run language servers or watchers.

Performance improvement won't be as dramatic, but should still help.


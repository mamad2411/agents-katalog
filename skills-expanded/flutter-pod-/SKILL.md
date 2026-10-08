# .cursorrules

## Scratchpad

### Current Task: Flutter Setup System with AI Error Handling

#### Task Overview:
Create intelligent, cross-platform Flutter setup scripts that automatically install Flutter and dependencies with AI-powered error recovery.

#### Task Plan:
[X] Create setup_flutter_env.sh (macOS & Linux)
  - [X] OS/architecture detection
  - [X] Flutter installation from official sources
  - [X] PATH configuration
  - [X] Dependencies installation (Git, unzip, curl/wget, Java JDK, CocoaPods)
  - [X] Android SDK handling (guided installation)
  - [X] Xcode license acceptance on macOS
  - [X] AI error handling integration
  - [X] Flutter precache execution

[X] Create setup_flutter_env.ps1 (Windows PowerShell)
  - [X] OS/architecture detection
  - [X] Flutter installation from official sources
  - [X] PATH configuration
  - [X] Dependencies installation (Git, unzip, curl, Java JDK)
  - [X] Android SDK handling (guided installation)
  - [X] AI error handling integration
  - [X] Flutter precache execution

[X] Create AI error handling helper
  - [X] OpenRouter API integration with DeepSeek
  - [X] Error context collection
  - [X] Response parsing and execution

[X] Testing and documentation
  - [X] Create comprehensive README with usage examples
  - [X] Document troubleshooting steps
  - [X] Test scripts on different platforms (macOS verified)
  - [X] Push to GitHub with feature completion

#### Progress Notes:
- ✅ COMPLETED: Intelligent Flutter setup system with AI error recovery
- ✅ Tested successfully on macOS 15.3.2 (Apple Silicon)
- ✅ All scripts created with comprehensive error handling
- ✅ Documentation and examples provided
- ✅ Successfully pushed to GitHub: https://github.com/Joynul-Abedin/Flutter-Pod

#### Final Summary:
Created a complete cross-platform Flutter setup automation system featuring:
- Bash script for macOS/Linux with Homebrew integration
- PowerShell script for Windows with Chocolatey integration  
- Built-in AI-powered error recovery using DeepSeek (no API key setup required)
- Zero-configuration intelligent troubleshooting and error resolution
- Comprehensive documentation and usage examples
- Tested and verified working on macOS environment
- Ready for community use with seamless AI assistance

#### Latest Enhancement:
✅ RUBY VERSION COMPATIBILITY FIX: Fixed CocoaPods installation issue
- Updated setup script to handle Ruby version compatibility (CocoaPods requires Ruby 3.1+)
- Improved Ruby version detection and automatic installation of modern Ruby via Homebrew
- Added proper gem environment configuration for Apple Silicon and Intel Macs
- Enhanced error handling and debug logging for AI API calls
- Updated OpenRouter API key for DeepSeek integration

#### Repository Structure:
✅ SIMPLIFIED FOR PUBLIC USE: 
- setup_flutter_env.sh (macOS/Linux)
- setup_flutter_env.ps1 (Windows)  
- README.md (simplified documentation)
- .gitignore (standard ignores)
- .cursorrules (development notes)

## Lessons

### User Specified Lessons
- You have a python venv in ./venv. Use it.
- Include info useful for debugging in the program output.
- Read the file before you try to edit it.
- Due to Cursor's limit, when you use `git` and `gh` and need to submit a multiline commit message, first write the message in a file, and then use `git commit -F <filename>` or similar command to commit. And then remove the file. Don't use [Cursor] prefix in commit messages.

### Cursor learned
- For search results, ensure proper handling of different character encodings (UTF-8) for international queries
- Add debug information to stderr while keeping the main output clean in stdout for better pipeline integration
- When using seaborn styles in matplotlib, use 'seaborn-v0_8' instead of 'seaborn' as the style name due to recent seaborn version changes
- Use 'gpt-4o' as the model name for OpenAI's GPT-4 with vision capabilities
- CocoaPods requires Ruby 3.1+ - check Ruby version and install modern Ruby via Homebrew if needed
- When installing gems on macOS, use system-wide installation instead of --user-install for better compatibility
- OpenRouter API requires HTTP-Referer and X-Title headers for proper authentication and attribution 
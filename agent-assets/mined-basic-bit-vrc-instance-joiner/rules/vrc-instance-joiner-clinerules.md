After running the application, ALWAYS immediately check both of the log files for any errors that occurred during runtime.

This is a windows build environment, always use ";" to chain commands instead of "&&".  All scripts should be in Powershell format.

After running the application, ask the user for feedback about how it performed.


If you get the error "The name 'InitializeComponent' does not exist in the current context", it is due to namespace issues.  The class and namespace names need to match between the XAML file and the code-behind file. (since they are two partial classes)

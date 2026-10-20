{
  "rules": [
    {
      "name": "log_changes",
      "description": "Logs all changed files and what was changed.",
      "on_change": {
        "log": {
          "message": "File changed: {{file_path}}, Changes: {{diff}}"
        }
      }
    }
  ],
  "warnings": [
    {
      "message": "This is a warning to log all changed files and what was changed."
    }
  ]
}

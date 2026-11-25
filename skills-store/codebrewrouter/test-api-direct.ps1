$body = @{
    model = "codebrewRouter"
    messages = @(
        @{
            role = "user"
            content = "Say hello world"
        }
    )
    stream = $true
} | ConvertTo-Json

Write-Host "Testing CodebrewRouter via direct API call..."
Write-Host "Endpoint: http://localhost:5022/v1/chat/completions"
Write-Host "Model: codebrewRouter"
Write-Host ""

$response = curl -s -X POST `
    -H "Content-Type: application/json" `
    -H "Authorization: Bearer sk-test" `
    -d $body `
    http://localhost:5022/v1/chat/completions

Write-Host "Response:"
Write-Host $response

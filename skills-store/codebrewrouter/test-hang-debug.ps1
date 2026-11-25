#!/usr/bin/env pwsh
<#
Debug script to test /v1/chat/completions and capture timing logs
#>

$baseUrl = "http://localhost:5000"
$apiKey = "test-key"

# Test payload - simple streaming request
$payload = @{
    model    = "codebrewRouter"
    stream   = $true
    messages = @(
        @{
            role    = "user"
            content = "What is 2+2?"
        }
    )
    temperature = 0.7
    max_tokens  = 100
} | ConvertTo-Json

Write-Host "🧪 Testing /v1/chat/completions endpoint" -ForegroundColor Cyan
Write-Host "  URL: $baseUrl/v1/chat/completions" -ForegroundColor Gray
Write-Host "  Model: codebrewRouter (streaming)" -ForegroundColor Gray
Write-Host "  Request size: $($payload.Length) bytes" -ForegroundColor Gray
Write-Host ""

$sw = [System.Diagnostics.Stopwatch]::StartNew()

try {
    Write-Host "📤 Sending request..." -ForegroundColor Yellow
    $response = Invoke-RestMethod `
        -Uri "$baseUrl/v1/chat/completions" `
        -Method Post `
        -Headers @{
            "Authorization" = "Bearer $apiKey"
            "Content-Type"  = "application/json"
        } `
        -Body $payload `
        -TimeoutSec 20

    $sw.Stop()
    Write-Host "✅ Response received in $($sw.ElapsedMilliseconds)ms" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    Write-Host ($response | ConvertTo-Json) -ForegroundColor White
}
catch {
    $sw.Stop()
    Write-Host "❌ Request failed after $($sw.ElapsedMilliseconds)ms" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.InnerException) {
        Write-Host "Inner: $($_.Exception.InnerException.Message)" -ForegroundColor Red
    }
}

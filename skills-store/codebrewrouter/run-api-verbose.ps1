#!/usr/bin/env pwsh

$env:LlmGateway__Providers__OllamaLocal__BaseUrl = "http://192.168.16.12:11434"
$env:LlmGateway__Providers__OllamaLocal__Model = "gemma4:e4b"
$env:LlmGateway__Providers__LmStudio__Endpoint = "http://192.168.16.56:1234/v1"
$env:LlmGateway__Providers__LmStudio__Model = "local-model"
$env:ASPNETCORE_ENVIRONMENT = "Development"

Write-Host "🔵 Starting Blaze.LlmGateway.Api with verbose logging..." -ForegroundColor Cyan
Write-Host "   OllamaLocal: $($env:LlmGateway__Providers__OllamaLocal__BaseUrl)" -ForegroundColor Gray
Write-Host "   LM Studio: $($env:LlmGateway__Providers__LmStudio__Endpoint)" -ForegroundColor Gray
Write-Host ""

dotnet run --project Blaze.LlmGateway.Api --no-build

---
name: webhook-standards
description: Webhook standards — Design, retry logic, signature verification, idempotency, delivery guarantees
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Webhook Standards

Webhooks enable real-time push notifications when events occur. Design for reliability with retry logic, signature verification, and idempotency guarantees.

---

## Webhook Design

**ALWAYS**:
- HTTPS only (encrypted delivery)
- Include signature (HMAC-SHA256)
- Include timestamp (prevent replay)
- Include event ID (detect duplicates)
- Support multiple retry attempts (exponential backoff)
- Allow subscriber to disable/enable webhooks
- Provide webhook logs/history
- Send to registered URL only

**NEVER**:
- Send webhooks over HTTP (unencrypted)
- Skip signature verification (on subscriber side)
- Retry forever (set max retries: 5)
- Lose webhook delivery status (log everything)

### ✅ GOOD Webhook Design

```
Order Created Event
  ↓
┌──────────────────────────────────┐
│ Webhook Publisher (SmartWorkz)   │
├──────────────────────────────────┤
│ 1. Create event payload (JSON)   │
│ 2. Add event ID, timestamp       │
│ 3. Sign with HMAC-SHA256         │
│ 4. POST to subscriber webhook URL│
│ 5. Retry on failure (exponential)│
│ 6. Log delivery status           │
└──────────────────────────────────┘
  ↓
Subscriber Webhook Endpoint
  ├─ Verify signature (HMAC-SHA256)
  ├─ Check timestamp (not too old)
  ├─ Dedup by event ID
  ├─ Process event
  └─ Return 2xx (success)
```

---

## Webhook Delivery

**ALWAYS**:
- Retry with exponential backoff (1s, 2s, 4s, 8s, 16s)
- Deliver at-least-once (allow duplicates, require idempotency)
- Set timeout (30 seconds per attempt)
- Log all attempts (success, failure, error)
- Provide delivery status UI (webhooks managed by subscriber)
- Max retries: 5 (after that, mark as failed)

**NEVER**:
- Block on webhook delivery (async only)
- Retry forever (DoS vector)
- Discard failed webhooks (queue for retry)

### ✅ GOOD Webhook Publisher

```csharp
// Webhook Publisher (sends events to subscribers)
public class WebhookPublisher
{
    private readonly HttpClient _httpClient;
    private readonly IWebhookStore _store;
    private readonly ILogger<WebhookPublisher> _logger;
    
    public async Task PublishAsync(Event @event)
    {
        // Get all registered webhooks
        var webhooks = await _store.GetActiveWebhooksAsync(@event.EventType);
        
        foreach (var webhook in webhooks)
        {
            // Publish async (don't block)
            _ = DeliverWebhookAsync(webhook, @event);
        }
    }
    
    private async Task DeliverWebhookAsync(Webhook webhook, Event @event)
    {
        var maxRetries = 5;
        var attempt = 0;
        
        while (attempt < maxRetries)
        {
            try
            {
                // Create payload
                var payload = new WebhookPayload
                {
                    EventId = Guid.NewGuid().ToString(),
                    EventType = @event.EventType,
                    Timestamp = DateTime.UtcNow,
                    Data = @event
                };
                
                // Sign with HMAC
                var signature = ComputeSignature(payload, webhook.Secret);
                
                // Prepare request
                var request = new HttpRequestMessage(HttpMethod.Post, webhook.Url)
                {
                    Content = new StringContent(
                        JsonConvert.SerializeObject(payload),
                        Encoding.UTF8,
                        "application/json"
                    )
                };
                
                // Add headers
                request.Headers.Add("X-SmartWorkz-Signature", signature);
                request.Headers.Add("X-SmartWorkz-Event-ID", payload.EventId);
                request.Headers.Add("X-SmartWorkz-Timestamp", payload.Timestamp.ToUniversalTime().ToString("O"));
                request.Headers.Add("X-SmartWorkz-Retry-Count", attempt.ToString());
                
                // Send with timeout
                using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30)))
                {
                    var response = await _httpClient.SendAsync(request, cts.Token);
                    
                    if (response.IsSuccessStatusCode)
                    {
                        // Success
                        await _store.LogDeliveryAsync(new WebhookDelivery
                        {
                            WebhookId = webhook.Id,
                            EventId = payload.EventId,
                            Status = "Success",
                            StatusCode = (int)response.StatusCode,
                            Attempt = attempt + 1,
                            Timestamp = DateTime.UtcNow
                        });
                        
                        _logger.LogInformation(
                            "Webhook delivered: {WebhookId} {EventId}",
                            webhook.Id,
                            payload.EventId
                        );
                        
                        return;  // Success, stop retrying
                    }
                    else if ((int)response.StatusCode >= 500)
                    {
                        // Server error - retry
                        _logger.LogWarning(
                            "Webhook server error: {WebhookId} {StatusCode}",
                            webhook.Id,
                            response.StatusCode
                        );
                        throw new HttpRequestException($"Server error: {response.StatusCode}");
                    }
                    else
                    {
                        // Client error - don't retry
                        _logger.LogError(
                            "Webhook client error: {WebhookId} {StatusCode}",
                            webhook.Id,
                            response.StatusCode
                        );
                        
                        await _store.LogDeliveryAsync(new WebhookDelivery
                        {
                            WebhookId = webhook.Id,
                            EventId = payload.EventId,
                            Status = "Failed",
                            StatusCode = (int)response.StatusCode,
                            Attempt = attempt + 1,
                            Timestamp = DateTime.UtcNow
                        });
                        
                        return;  // Don't retry client errors
                    }
                }
            }
            catch (Exception ex)
            {
                attempt++;
                
                // Exponential backoff: 1s, 2s, 4s, 8s, 16s
                var delayMs = (int)Math.Pow(2, attempt - 1) * 1000;
                
                _logger.LogWarning(
                    "Webhook delivery failed (attempt {Attempt}/{MaxRetries}): {WebhookId} Error: {Error}. " +
                    "Retrying in {DelayMs}ms",
                    attempt,
                    maxRetries,
                    webhook.Id,
                    ex.Message,
                    delayMs
                );
                
                if (attempt < maxRetries)
                {
                    // Wait before retrying
                    await Task.Delay(delayMs);
                }
            }
        }
        
        // Max retries exhausted
        _logger.LogError(
            "Webhook delivery failed after {MaxRetries} attempts: {WebhookId}",
            maxRetries,
            webhook.Id
        );
        
        // Disable webhook (subscriber action required to re-enable)
        await _store.DisableWebhookAsync(webhook.Id, "Max delivery attempts exceeded");
    }
    
    private string ComputeSignature(WebhookPayload payload, string secret)
    {
        var json = JsonConvert.SerializeObject(payload);
        var data = Encoding.UTF8.GetBytes(json);
        var key = Encoding.UTF8.GetBytes(secret);
        
        using (var hmac = new HMACSHA256(key))
        {
            var hash = hmac.ComputeHash(data);
            return $"sha256={Convert.ToHexString(hash).ToLower()}";
        }
    }
}
```

---

## Webhook Verification (Subscriber Side)

**ALWAYS**:
- Verify HMAC signature (prevent spoofing)
- Check timestamp (not > 5 minutes old)
- Dedup by event ID (prevent processing duplicate events)
- Return 2xx immediately (don't block)
- Process async (queue for processing)
- Return error if verification fails (webhook will retry)

**NEVER**:
- Trust webhook without signature verification
- Process without checking event ID (duplicates)
- Block request on event processing (return 202 Accepted)

### ✅ GOOD Webhook Receiver

```csharp
[HttpPost("webhooks/smartworkz")]
public async Task<IActionResult> ReceiveWebhookAsync()
{
    // Read body (needed for signature verification)
    string body;
    using (var reader = new StreamReader(Request.Body))
    {
        body = await reader.ReadToEndAsync();
    }
    
    // Get signature header
    var signature = Request.Headers["X-SmartWorkz-Signature"].ToString();
    if (string.IsNullOrEmpty(signature))
    {
        _logger.LogWarning("Webhook missing signature header");
        return Unauthorized("Missing signature");
    }
    
    // Verify signature
    var secret = _config["WebhookSecret"];
    if (!VerifySignature(body, signature, secret))
    {
        _logger.LogWarning("Webhook signature verification failed");
        return Unauthorized("Invalid signature");
    }
    
    // Get event metadata
    var eventId = Request.Headers["X-SmartWorkz-Event-ID"].ToString();
    var timestamp = Request.Headers["X-SmartWorkz-Timestamp"].ToString();
    
    // Check timestamp (not older than 5 minutes)
    if (!DateTime.TryParse(timestamp, out var ts) || 
        DateTime.UtcNow - ts > TimeSpan.FromMinutes(5))
    {
        _logger.LogWarning("Webhook timestamp too old or invalid");
        return BadRequest("Timestamp too old");
    }
    
    // Check for duplicate (idempotency)
    var alreadyProcessed = await _webhookStore.IsProcessedAsync(eventId);
    if (alreadyProcessed)
    {
        _logger.LogInformation("Duplicate webhook {EventId}, returning 200", eventId);
        return Ok();  // Already processed, but return 200 to confirm
    }
    
    // Deserialize and queue for async processing
    var payload = JsonConvert.DeserializeObject<WebhookPayload>(body);
    
    // Queue for processing (don't block HTTP response)
    await _messageQueue.EnqueueAsync(new ProcessWebhookEvent
    {
        EventId = eventId,
        Payload = payload
    });
    
    // Mark as processing (prevent duplicate dequeue)
    await _webhookStore.MarkProcessingAsync(eventId);
    
    // Return 202 Accepted (processing, not done yet)
    return Accepted();
}

private bool VerifySignature(string body, string signature, string secret)
{
    // signature format: "sha256=..."
    if (!signature.StartsWith("sha256="))
        return false;
    
    var expectedSignature = signature.Substring("sha256=".Length);
    
    // Compute hash
    var data = Encoding.UTF8.GetBytes(body);
    var key = Encoding.UTF8.GetBytes(secret);
    
    using (var hmac = new HMACSHA256(key))
    {
        var hash = hmac.ComputeHash(data);
        var computedSignature = Convert.ToHexString(hash).ToLower();
        
        // Constant-time comparison (prevent timing attacks)
        return CryptographicOperations.FixedTimeEquals(
            Encoding.UTF8.GetBytes(expectedSignature),
            Encoding.UTF8.GetBytes(computedSignature)
        );
    }
}
```

---

## Webhook Idempotency

**ALWAYS**:
- Use event ID for deduplication (unique per event)
- Store processed event IDs (in database)
- Allow subscriber to retry manually (resend webhook)
- Provide webhook delivery history (UI shows attempts)

**NEVER**:
- Process same webhook twice (require dedup)
- Lose delivery history (for debugging)

---

## Webhook Management UI

**ALWAYS**:
- List all registered webhooks
- Show delivery status (success, failed, retrying)
- Show delivery history (last 10 attempts)
- Allow enable/disable webhook
- Allow delete webhook
- Show webhook logs (what was sent, when, result)
- Allow manual retry (resend webhook)

---

## Webhook Standards Checklist

- [ ] Webhooks use HTTPS only
- [ ] Signature verification implemented (HMAC-SHA256)
- [ ] Timestamp included & checked (prevent replay)
- [ ] Event ID included & checked (prevent duplicates)
- [ ] Retry logic implemented (exponential backoff, max 5)
- [ ] Timeout configured (30 seconds per attempt)
- [ ] Subscriber can register/unregister webhooks
- [ ] Delivery history tracked (logs, audit trail)
- [ ] Disabled webhook handling (after max retries, disable & alert)
- [ ] Monitoring & alerting (failed deliveries, DLQ)
- [ ] Documentation (webhook payload format, signature, retry logic)

---

## Summary

Good webhook standards:
1. **Security** — HTTPS, signature verification, timestamp validation
2. **Reliability** — Retry logic, exponential backoff, delivery history
3. **Idempotency** — Event IDs, duplicate detection, at-least-once delivery
4. **Transparency** — Delivery history, logs, subscriber controls
5. **Resilience** — Disable after max retries, alert on failures
6. **Performance** — Async processing, 202 Accepted response

Webhooks enable real-time integrations when implemented reliably.

using OpenAI;
using System.ClientModel;
using Microsoft.Extensions.AI;

var apiKey = new ApiKeyCredential("dummy");
var endpoint = new Uri("http://192.168.16.56:1234/v1");
var client = new OpenAIClient(apiKey, new OpenAIClientOptions { Endpoint = endpoint });

try {
    Write-Host "Testing OpenAI client connection to LM Studio..." -ForegroundColor Yellow
    var chatClient = client.GetChatClient("codebrew_balanced");
    var ichatClient = chatClient.AsIChatClient();
    
    var response = await ichatClient.GetResponseAsync(
        new[] { new ChatMessage(ChatRole.User, "hello") },
        new ChatOptions { MaxOutputTokens = 20 }
    );
    
    Write-Host "✅ Success! Response: " + response.Text -ForegroundColor Green
} catch (Exception ex) {
    Write-Host "❌ Error: " + ex.GetType().Name + " - " + ex.Message -ForegroundColor Red
    if (ex.InnerException != null) {
        Write-Host "Inner: " + ex.InnerException.Message
    }
}

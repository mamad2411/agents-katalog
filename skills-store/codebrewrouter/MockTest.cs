using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.AI;
using Blaze.LlmGateway.Infrastructure;
using Microsoft.Extensions.Logging;

// Simple test of the MockChatClient
var logger = LoggerFactory.Create(x => x.AddConsole())
    .CreateLogger<MockChatClient>();

var mock = new MockChatClient(logger);

// Test non-streaming
var messages = new[] { new ChatMessage(ChatRole.User, "tell me a dad joke") };
var response = await mock.GetResponseAsync(messages);
Console.WriteLine("Non-streaming response: " + response.FirstMessage.Text);

// Test streaming
Console.WriteLine("\nStreaming response:");
await foreach (var update in mock.GetStreamingResponseAsync(messages))
{
    Console.Write(".");
}
Console.WriteLine("\n✅ Both modes work!");

# Universal Flutter AI Agents Project Standard

# (Omniplatform)

## Clean Architecture and Module Folder Structure

Each feature module in the Flutter project follows a **3-layer clean architecture** : **application** , **data** , and
**presentation**. Under the project’s lib/ directory, every major feature (module) gets its own folder
with this standardized substructure :

```
lib/
├── app/ # Shared core (common models, utilities, constants,
widgets)
├── <feature>/ # e.g. chat/, voice/, business/, profile/, etc.
│ ├── application/ # Business logic (state notifiers, providers)
│ ├── data/ # Data layer (models, DTOs, repositories, services)
```
```
│ └── presentation/ # UI layer (screens, pages)
└── main.dart # App entry point
```
**Layer Responsibilities:**

- **Application:** Contains state management and business logic (e.g. Riverpod providers, controllers,
state notifier classes). This is where app-specific logic (without UI code) resides – for example, state
classes and notifiers handling chat interactions or voice recording status.
- **Data:** Contains data models, DTOs (Data Transfer Objects for API JSON), mappers, repositories, and
low-level services for external communication (REST APIs, WebSockets, local storage, etc.). This layer
abstracts data sources and backend integration.
- **Presentation:** Contains the UI code – **primarily screens/pages** that render the interface for the
feature. Notably, **feature modules should not contain large widget implementations directly**.
Instead, they compose screens using widgets from the shared app module (see next section). In
practice, each feature’s presentation/ includes only its **screens** (and possibly a page or route
factory), keeping UI layout definitions high-level. For example, a chat module might have
    chat_screen.dart and chat_page_factory.dart in its presentation folder, which assemble
common widgets into the final UI.

**Shared Core (app/):** Common resources used across modules live in lib/app. This includes global
constants, themes, utilities, and **shared widgets** (discussed below). The app/ folder acts as the core
of the application, decoupled from any single feature. **No feature module should import another
module’s code directly** – if multiple modules need a particular component, it must be factored into
app/ (or a common library) to avoid tight coupling. This ensures modules remain isolated and
interchangeable. For example, a data model or service used by both chat and voice modules should be
defined in app/data/ (or app/application/) rather than one module importing from the other

. Likewise, UI components needed in multiple modules (buttons, cards, etc.) should reside in app/
presentation/widgets/common/ instead of being duplicated in each module.

```
1 2
```
```
3 4 5 2 2 2 6 7 8 7
```

## Widget Placement and Directory Conventions

All reusable UI components are organized under a central widgets directory to enforce consistency. The
project adopts a **widget-centric structure** inside the app core:
**lib/app/presentation/widgets/** contains all UI widgets, categorized by module or common
usage. This approach ensures a clear separation between feature logic (in module folders) and
UI components.

Under app/presentation/widgets/, the structure is as follows:

```
app/presentation/widgets/
├── common/ # **Common widgets** used across modules (atomic
components)
│ ├── bars/ # Shared app bars, navigation bars, toolbars
│ ├── cards/ # Generic card widgets (e.g. info cards)
│ ├── views/ # Reusable view components or sections
│ ├── forms/ # Common form fields and form widgets
│ ├── screens/ # Base screen templates or wrappers
│ └── pages/ # Generic page layouts or containers
├── <module_name>/ # e.g. chat/, voice/, entertainment/, business/, etc.
│ ├── bars/ # Module-specific bars (headers, toolbars for that
feature)
│ ├── cards/ # Module-specific cards (e.g. chat message card,
profile card)
│ ├── views/ # Module-specific composite views (sections of UI)
│ ├── forms/ # Module-specific form widgets (input areas, etc.)
│ ├── screens/ # Module-specific UI screens (if split into
components)
│ └── pages/ # Module-specific page layouts (top-level UI for
feature)
└── ... (other modules similarly structured) ...
```
**Placement Rules:**

- **Common Widgets:** Small, atomic widgets or highly reusable components (buttons, text fields, loaders,
etc.) that are used in multiple parts of the app belong in widgets/common/. These are building
blocks with no business logic (purely presentational), and are typically StatelessWidgets or simple
ConsumerWidgets.
- **Module Widgets:** UI components specific to a feature go into widgets/<module>/. Even these are
further organized by type: use bars/ for horizontal app bars or toolbars, cards/ for contained UI
elements, views/ for larger combined sections, forms/ for input groups, screens/ for full-
screen widgets, and pages/ for top-level page constructs. This standard subfolder set **must be
present for each module’s widget folder** to enforce consistency. For example, an AI Chat module
would have its chat bubble widget in app/presentation/widgets/entertainment/cards/
chat_message_card.dart and its chat input area in app/presentation/widgets/
entertainment/forms/chat_input_form.dart.
- **Feature Presentation vs Widgets:** The feature module’s own presentation/ folder contains _only_
high-level UI definitions (screens/pages), while the actual widget implementations live in the app
module. **Modules do not hold their own widget subfolders** ; instead, they import needed UI
components from app/presentation/widgets/. This means a module’s screen file will

```
9 10
```
```
9
```
```
11
```
```
12 13
```
```
14 15
```

assemble widgets from the common or module-specific widget directories. (In other words, _“No Direct
UI code in modules”_ – all UI building blocks are in the central widget layer .) This convention improves
reusability and ensures a unified look and feel across features.

## AI Agent Chat, Voice, and Transcription Features

**Real-Time Chat:** The AI chat feature is implemented as a real-time conversation using WebSocket
communication for responsiveness. The client should maintain a WebSocket connection to the
backend AI agent service, sending user messages and receiving agent responses in real time. The chat
logic (connecting, message streaming, reconnection, etc.) lives in the application layer (e.g. an
AgentChatService in data layer and a ChatController in application layer), while the UI uses
widgets (like message bubbles) to display the dialog.

**Voice Messaging:** The system supports voice-based interaction with two **audio submission modes** :
**streaming** and **blob upload**. This dual-mode approach accommodates different platforms and
network conditions:

```
Streaming Mode: The app captures audio from the microphone and streams it continuously to
the server (e.g. via WebSocket or gRPC) in real-time chunks. This mode provides low-latency
interaction – the AI can start processing or transcribing the speech as it’s being spoken, enabling
faster responses. Streaming is ideal on mobile and desktop platforms which support background
audio streams. Use streaming whenever real-time transcription is needed and the platform
allows it (iOS/Android/Linux, etc.).
Blob Mode: The app records the entire audio clip locally (e.g. using the device microphone or
web MediaRecorder) and, once the user finishes speaking, saves it as a file/blob. That blob is
then sent to the server in one request (for example, an HTTP upload or a one-off WebSocket
message). This mode is more stable and suitable for longer recordings , since it doesn’t
rely on sustained network streaming. Web platforms must use blob mode as a fallback ,
because browsers have limitations with live microphone streaming. In blob mode, the user will
speak, then wait briefly for the audio file to upload and be processed.
```
The application should **detect the platform at runtime** (e.g. using kIsWeb or other platform checks)
and choose the appropriate audio mode automatically. For instance, on web, it should default to
blob recording (perhaps using the Web MediaRecorder API) and on mobile, it can default to streaming
for a more interactive feel. If streaming fails or is unavailable, the system should gracefully fall back to
blob mode as well. This ensures robust voice interaction across **all platforms (web, iOS, Android,
desktop)**.

**Real-Time Transcription:** When voice input is used, the system can convert speech to text in real time.
If **transcription is enabled** , voice data should be routed through a transcription service or API. In
**streaming mode** , this might mean sending audio chunks to a speech-to-text service and receiving
partial transcripts as the user speaks (providing live subtitle feedback). In **blob mode** , transcription
would occur after the full audio clip is uploaded – the server returns the transcribed text, which the
client can then display or use to prompt the AI agent. The choice is controlled by configuration (see
RecordingButton below): if transcription is turned on for a voice message, ensure the workflow includes
sending audio to the ASR (Automatic Speech Recognition) engine and handling its response. The design
must handle transcription results in a user-friendly way, for example, by either displaying the
transcribed user query in the chat or directly using it to fetch the AI’s answer.

**Integration and Fallbacks:** All three features – text chat, voice, and transcription – are integrated in the
AI agent module. The chat interface allows text input as well as voice input. When the user opts to send

```
14
```
```
16
```
```
17
```
### •

```
18
```
-

```
19
18
```
```
18
```
```
20
```

voice:

1. The **RecordingButton** (voice record widget) determines the mode (stream vs blob) based on platform
and settings, and captures the audio accordingly.
2. If **transcription is on** , the app will either stream audio to get incremental transcriptions or send the
recorded file for transcription, then display or utilize the resulting text. If transcription is **off** (voice is
sent directly as audio), the backend AI service should handle the audio input (e.g. an AI that accepts
voice) or the app should handle the response appropriately (possibly receiving an audio or text reply).
3. Chat messages from the AI are received via WebSocket just like text chats, regardless of whether the
user input was voice or text. The UI should unify these into the same message list.

On the web platform, where streaming is not available, the standard strategy is: record via
MediaRecorder to a Blob, upload it (e.g. via an HTTP endpoint or WebSocket binary message), then wait
for the AI’s response. On mobile, streaming should be preferred for shorter queries to minimize delay.
Always implement timeouts and error handling – e.g. if transcription fails or takes too long, notify the
user or fall back to letting the AI respond to audio directly. The overall goal is a **seamless chat
experience** combining text and voice: users can send text or voice messages to the AI agent and
receive responses in real-time. All of this must be done with careful platform-aware logic to ensure it
“just works” everywhere.

## RecordingButton Widget (Voice Input Control)

The **RecordingButton** is a reusable UI component that encapsulates **all audio recording
functionality** in one place. It lives in the common widgets directory (app/presentation/widgets/
common/forms/recording_button.dart) so that any module can use it for voice input. This
widget handles microphone access, audio streaming or buffering, and optional transcription,
abstracting these details away from the individual screens. Key specifications for RecordingButton
include:

```
Encapsulation: The widget manages its own internal state (recording vs idle) and interactions
with lower-level services (like an AudioRecorder service in the data layer). It provides a simple
interface (properties and callbacks) to the UI. Developers using RecordingButton in a screen
shouldn’t need to write microphone handling code – they just configure the widget’s parameters.
Properties and Callbacks: The RecordingButton takes in a set of parameters to control its
behavior. For example: a flag to enable/disable transcription, the audio mode (streaming or
blob), visual customization (size, colors), and callback handlers for various events. A typical
constructor might look like:
```
```
RecordingButton(
transcriptEnabled:true, // whether to perform speech-to-text
mode:AudioMode.streaming, // or .blob, depending on context
onRecordingStart:() { ...}, // callback when recording begins
onRecordingStop:() { ... }, // callback when recording ends
onAudioData:(Uint8Listdata) { ...},// raw audio data (for blob mode)
onTranscript:(Stringtext) { ...}, // transcript result (if enabled)
enabled:true // whether button is active
)
```
Internally, the widget uses these callbacks to notify the app of important events – e.g. providing the
recorded audio bytes when using blob mode, or streaming transcripts as they arrive. It also can accept
a configuration object (RecordingConfig) encapsulating settings. This config might include fields

```
21 22
```
```
23
```
### •

### •


like maxDuration (to auto-stop or limit recording length), custom hint text or colors for the UI, and a
webCompatible toggle to force blob mode if needed.

```
Transcription Toggle: The transcriptEnabled flag controls whether the widget should
handle transcription. If true, the RecordingButton will route audio through the
transcription pipeline and emit the resulting text via onTranscript callback. If
false, it will simply capture audio (stream or complete) and deliver it raw (or send it directly to
the AI service) without converting to text. This makes it flexible – for some voice interactions you
may want to display the recognized text, for others you might send audio directly (e.g. if the AI
processes audio input on the backend).
```
```
Audio Workflows (Streaming vs Blob): The widget must support both audio workflows:
```
```
In streaming mode , pressing the button starts capturing audio and sending it continuously
(perhaps via a Stream subscription) to the backend. The widget might show a “recording...”
indicator and allow the user to stop recording at any time. When stopped, it ensures the stream
is closed properly. This mode will likely call onTranscript repeatedly with partial results (if
transcription is on) or simply rely on the AI’s real-time response via WebSocket.
```
```
In blob mode , pressing the button starts recording locally (e.g. accumulating audio data). On
stop, the onAudioData callback provides the complete audio file (as bytes) so the higher-level
logic can upload it. If transcription is enabled, the widget could also automatically send the
blob to a transcription service and return the text. In blob mode, there may be a slight delay
after stopping before the transcript or response is ready, which the UI should handle (e.g. show
a “processing” state).
```
```
Platform Adaptation: RecordingButton internally accounts for platform differences. For
example, on web, it might automatically override the mode to AudioMode.blob (because
continuous streaming isn’t supported). It could use a web-specific implementation (like the
WebAudioRecorder with the MediaRecorder API) under the hood when running in a browser.
On mobile/native platforms, it can use lower-level audio streams. These details are hidden from
the UI – the developer just chooses the mode, and the widget ensures it falls back appropriately.
The widget could use a factory in RecordingConfig like RecordingConfig.forWeb() to
preset suitable defaults for web (blob mode, etc.).
```
```
Usage Across Modules: By placing RecordingButton in common/, we ensure it can be used
anywhere (e.g. a “voice note” feature in a chat screen, a voice search in a different module, etc.).
All modules share the same recording implementation, avoiding duplicate code. For instance,
both an Entertainment AI chat and a Business order chat can employ the same
RecordingButton widget and simply provide different callbacks or configurations. This also
centralizes updates: if the audio recording logic needs to change, it’s changed in one place. Task
reports have emphasized consolidating such functionality to prevent inconsistencies.
```
The RecordingButton is a prime example of designing a **fully encapsulated, configurable widget**
that adheres to the project’s architecture principles. It handles starting/stopping the microphone,
toggling between streaming and file-mode, and hooking into transcription services, all while exposing a
simple interface to the rest of the app.

```
24
```
### •

```
25 26
```
### •

### •

```
27
```
### •

```
25
```
### •

```
18
```
```
28
```
### •

```
29 30
```

## State Management and Providers (Riverpod)

State management is standardized on **Riverpod** for this project (Riverpod 2.x is recommended). All
stateful logic should use providers and notifiers rather than built-in setState or overly ad-hoc
patterns. The guidelines for state management include:

```
Use Riverpod (Preferred): Utilize StateNotifierProvider for complex state objects and
logic, or simple Provider/StateProvider for simpler pieces of state. Each feature
module’s application layer defines its own providers and state notifier classes. For example, an AI
Chat module might have an AiChatNotifier and accompanying AiChatState class (to
hold chat state), exposed via a ai_chatProvider (StateNotifierProvider) in
ai_chat_providers.dart. This separation ensures business logic is testable and not tied to
the UI.
No Code Generation:Do not use code-gen tools like Freezed or build_runner for state classes
or unions. All state classes (and any necessary copy or equality logic) should be written and
maintained manually. This is to reduce complexity and keep the code explicit. For instance,
instead of using Freezed to generate a union of loading/success/error states, define a simple
enum or sealed class by hand. The project explicitly prohibits Freezed in this context , so any
existing Freezed usage should be refactored to manual classes.
Provider Structure: Follow a consistent naming and file organization for providers and state. In
each module’s application/ folder, create: a <module>_state.dart (defining the State
class or classes), a <module>_notifier.dart (implementing StateNotifier<T> or similar
logic class), and a <module>_providers.dart (containing the final provider =
StateNotifierProvider<...> definitions, plus any other providers). For example:
```
```
lib/<feature>/application/
├── <feature>_state.dart // State class(es)
├── <feature>_notifier.dart // StateNotifier or ChangeNotifier
implementation
└── <feature>_providers.dart // Riverpod providers exposing the notifier
and other state
```
By convention, name the StateNotifier class as <Feature>Notifier and the State class as
<Feature>State for clarity. If using simple ChangeNotifier (allowed in simpler cases), name it
similarly (e.g. AuthController extends ChangeNotifier). Keep these files free of UI code – they
should not import Flutter widgets.

```
Avoid Global Mutable State: Leverage Riverpod’s scope – use providers for any state that needs
to be shared or persisted in memory. For ephemeral widget-only state, prefer local state inside
the widget or use StateProvider if it truly needs to be shared at a small scope. Do not use
singletons or global variables for state.
```
```
Provider References: When writing Riverpod notifiers or providers, it’s often necessary to
interact with other providers (for example, a ChatNotifier might need to read an
AuthProvider to include a user token in requests). Store the ref (ProviderRef) inside your
notifier or provider if needed to access other providers’ values or to listen to their changes.
This enables inter-provider communication while respecting modular boundaries (e.g. the
Business module’s provider can safely consume a provider from the App core or another
module, if designed for cross-use). By capturing ref , you can call ref.read() or
```
```
31
```
### •

```
31
```
### •

```
32
32
```
```
32
```
### •

```
33
```
### •

### •

```
34
```

```
ref.watch() within your notifier methods to get dependencies. Always be mindful of not
creating tight coupling though – only use this for legitimate cross-cutting concerns (like needing
an auth token or a common service).
```
```
Riverpod vs ChangeNotifier: Riverpod is the default choice. However, in some simple scenarios
or legacy portions, ChangeNotifier may be used (for example, if a widget was easier to
implement with a ValueNotifier or ChangeNotifier, or if a developer is more comfortable
with Provider). This is acceptable only for simple state , and even then it should be managed in
the same layered way (e.g., put the ChangeNotifier in the application layer and provide it via a
Provider). Do not mix state management strategies arbitrarily – the standard is to favor
Riverpod’s Provider system for new code. No matter which approach, do not use code
generators for ChangeNotifiers either (no Provider.generate() etc.). Keep the patterns
explicit and consistent.
```
```
Explicit State Patterns: Each state class should clearly represent the UI state needed. For
instance, you might have a ChatState class with properties like
messages: List<Message>, isRecording: bool, isLoading: bool for an AI chat
screen. The StateNotifier would manage adding to the message list, toggling loading flags, etc.,
and the UI would listen to these via Riverpod. When a state is more complex (e.g. multiple sub-
states), you can break it down into smaller state classes or use composition instead of relying on
advanced code-gen unions. The emphasis is on clarity and maintainability – future developers
should be able to understand the state transitions by reading the code, without hunting through
generated files.
```
In summary, manage app state through Riverpod providers and notifiers defined in the **application
layer** of each module, and update the UI by watching those providers in the presentation layer. This
aligns with the clean architecture approach, keeping logic out of widgets. It was noted that some past
solutions used Freezed for state; going forward, that practice is discontinued to adhere to the “no code
generation” rule.

## Chat Message UI and RTL Support

The chat interface should follow a **consistent message bubble style** (inspired by messaging apps like
WhatsApp) and fully support **right-to-left (RTL)** languages, given that the primary locale is Persian. The
standard for message display is: **User messages appear on the right side, and AI (agent) messages
on the left**. This positioning remains the same even in RTL mode – it refers to conversational roles,
not text alignment. Key guidelines for the chat UI:

```
Message Alignment: User messages are right-aligned, and agent messages are left-aligned in
the chat view. Typically, this is achieved by using a row layout where the main axis alignment
depends on the sender. The user’s message bubble will be pushed to the right end, while the
agent’s bubble is to the left end. This creates a clear visual distinction between who said what.
```
```
Bubble Design: Use different background colors to differentiate sender: for example, it’s
standard to use a light green bubble for the user’s own messages (similar to WhatsApp) and a
neutral color (white or gray) for the agent’s messages. Our standard color code for the user
bubble is the light green #DCF8C6. The agent (AI) bubble is white (or light gray for dark
mode, etc.) for contrast. Additionally, style the chat bubbles with rounded corners – commonly
all top corners rounded, and the bottom corner of the bubble “pointing” toward the other party.
Specifically, the bubble tail (pointed corner) should be on the side of the speaker: user bubbles
```
### •

```
14
```
### •

```
32
```
```
35
```
### •

```
35
```
### •

```
36
36
```

```
have a pointed corner on the bottom-right, whereas agent bubbles have it on the bottom-left
```
. This gives a classic chat appearance with “speech tail” indicators.

```
Avatars: Display an avatar or icon for the AI agent to the left of the agent’s messages, and the
user’s avatar (this could even be a generic user silhouette or the user’s profile picture) to the
right of the user’s messages. Place the avatar just outside the bubble. This means the row for
an agent message would contain avatar on the far left, then the message bubble next to it; for a
user message, the bubble comes first (right-aligned) and the avatar on the far right. Ensure
there’s consistent spacing (e.g. 8px) between the avatar and the bubble. Avatars can be
optional, but if used, they should follow this layout.
```
```
RTL Text Support: When the app is in an RTL locale (e.g. Persian), the text inside the bubbles
should be rendered right-to-left. This typically is handled by the app’s localization (the
Directionality widget or TextDirection set to RTL). It’s important to explicitly test that
Persian text in chat bubbles is correctly aligned and not forcing left-to-right. The overall bubble
alignment (left/right side of screen) does not flip for RTL; “user on right, agent on left”
remains consistent to maintain the conversational assignment. However, the content of each
bubble and the ordering of avatar vs. bubble within each message row should naturally adapt
(for example, in RTL, the padding and alignment of text within the bubble might need to be
right-aligned). Use Flutter’s Directionality or specify textAlign: TextAlign.right
when rendering RTL text if needed to ensure the text is visually correct inside the bubble.
The UI should be thoroughly tested with both English (LTR) and Persian/Arabic (RTL) to verify
that spacing, alignment, and overflow behave properly in both directions.
```
```
Adaptive Layout: Make sure the message widgets expand properly for different screen sizes.
On wide screens (tablet/desktop), the messages can still be aligned to the respective sides (with
maybe a max width for readability). The design should gracefully handle long messages (wrap
text within bubble) and very short messages. Also ensure consecutive messages from the same
sender have appropriate spacing or grouping if needed (though a simple approach is fine where
each message is its own bubble with vertical spacing).
```
By adhering to these standards, the chat UI will be clear and familiar. The combination of color,
alignment, and avatar cues lets the user easily distinguish their messages from the AI’s responses.
Maintaining RTL support is critical for Persian text – **always verify UI changes in both RTL and LTR
modes.**

## API Configuration and Environment Constants

All API endpoints and configuration values must be centralized to avoid mistakes and to facilitate easy
environment switching. The project uses a single constants file (e.g. constants.dart in app/
application/constant/) to define base URLs and other API constants. **Never hard-code API URLs
or endpoints inside services or widgets.** Instead, reference the central constants. For example, define:

```
// constants.dart
classAppConstants{
staticconst String localhostUrl= 'http://localhost:8000'; // Dev
server
staticconst String serverApiUrl= 'https://api.joow.ir'; //
Production server
```
```
37
```
### •

```
35
```
```
37
```
### •

```
38
```
### •

```
39
```
```
39
```

```
staticconst String serverUrl= localhostUrl; // Currently active base
(switch for release)
// ...other constants...
}
```
In development, AppConstants.serverUrl should point to the local backend (localhost:8000),
which is the correct port for the Joow backend (note: **port 8000** is used for the local API server).
In production builds, this can be switched to serverApiUrl (e.g. via a simple toggle or build
configuration) so that AppConstants.serverUrl becomes https://api.joow.ir. This
approach allows the code to use AppConstants.serverUrl uniformly, while the actual value
depends on the environment. For instance, an API call would be: Uri.parse('$
{AppConstants.serverUrl}/api/v1/agent/message'), which at runtime expands to either
[http://localhost:8000/api/v1/agent/message](http://localhost:8000/api/v1/agent/message) in dev or https://api.joow.ir/api/v1/
agent/message in prod.

**Endpoint Patterns:** All backend endpoints should include the proper base and path as defined in
constants. Notably, the Joow API expects an /api prefix for all routes. The standard endpoints for
the AI agent features (as documented in **app_data.txt** report) are:

- GET /api/v1/agent/prompts – retrieve the list of AI agents or prompts.
- POST /api/v1/agent/message – send a chat message (text or voice) and receive the AI’s response
   .

These should always be constructed using the base URL constants, e.g. Uri.parse('$baseUrl/api/
v1/agent/prompts'). The **app_data.txt** documentation in the reports directory provides a complete
reference of all API endpoints, ports, and usage details – developers must consult it when
implementing or modifying network calls, to ensure consistency with the known working configuration.
The project had previously encountered errors when incorrect URLs (e.g. wrong port or missing /api
prefix) were used, so adhering to the documented endpoints is critical.

**Environment Switching:** Use a simple mechanism to switch between dev and prod configurations. This
could be as basic as manually changing a constant, or checking kReleaseMode to set serverUrl.
(Advanced setups might use Dart define flags or separate config files, but even a manual toggle is
acceptable given the small number of environments.) The key is that **no dev-only URLs remain in
production code** , and vice versa. By centralizing in constants, it’s easy to do a final review before
release to ensure serverUrl is pointing to serverApiUrl.

**No Hardcoding in Code:** Developers should not sprinkle raw URLs or API paths throughout the
codebase. If a new endpoint is needed, add it to the constants or a designated API routes class. The
service classes in the data layer should construct URLs via these constants. This reduces mistakes and
makes future changes (like pointing to a different server or version) significantly easier.

Finally, any sensitive API keys or secrets (if any) should also be stored in a secure manner (not plain in
code or constants – ideally use Flutter’s secret management or environment variables). But for base
URLs and route prefixes, the AppConstants approach is sufficient and much safer than scattering
strings around. Always verify new API calls against the known good endpoints in **app_data.txt** before
committing code.

```
39
```
```
39 40
```
```
39
```
```
41
```
```
42
```
```
42
```
```
43 44
```
```
45
```
```
46
```
```
47
```

## Logging and Error Handling Standards

Robust logging and error handling are essential for a maintainable project. This project uses a
structured logging approach via an **AppLogger** utility, and enforces consistent error handling with user
feedback mechanisms. Key rules include:

```
Use AppLogger for All Logging:Do not use print() statements for debugging or info logs
in the codebase. Instead, use the provided AppLogger (or similarly named logging
class) which likely wraps dart:developer or a logging package to format output. AppLogger
can have methods like info, error, debug, logPerformance, etc., to log messages at
different levels. Always choose the appropriate method/level:
Use info logs for high-level events (e.g. “User tapped X”, “Chat session started”).
Use error logs to record exceptions or failures, including the error object and stack trace if
possible.
Use performance logs to time operations or record latency (e.g. how long a network call took)
.
```
```
Use debug or verbose logs for development-time details that might be turned off in production.
The AppLogger is configured to provide more structured output than print, and can be extended
to log to files or remote analytics if needed. By funneling through AppLogger, log formatting and
enabling/disabling logs can be managed centrally. Recent improvements mirror the frontend’s
comprehensive logger – including API request/response logging and performance timing.
```
```
Structured Log Content: When logging, include relevant context. For example, when logging an
API error, log the endpoint, the HTTP status code, and perhaps a snippet of the response or a
specific error code. The AppLogger might have dedicated methods such as
logApiError(method, endpoint, error, {statusCode, duration}) to facilitate this
```
. Use them accordingly. Similarly, use logPerformance(operation, duration,
metrics) for wrapping performance-critical sections. The goal is that logs should provide
enough information to debug issues without exposing sensitive data. All team members should
follow the same logging format for consistency.

```
Centralized Error Handling: Error handling should be done in a user-friendly and consistent
way. Any unexpected error (network failure, server error, unhandled exception in business logic)
should be caught and passed to a central error handler or at least logged and presented
through a common UI element. The app should not crash or silently fail without feedback.
Implement a strategy such as:
```
```
Use try/catch around asynchronous operations in the data layer (API calls, etc.), log
exceptions via AppLogger, and return error states to the application layer.
The application layer (notifiers/providers) can catch errors and update state to indicate an error
occurred (for example, setting an errorMessage in state or using a separate error state
provider).
User Feedback: For errors that affect the user’s action (e.g. failed to load data or a message
send failure), show a centralized dialog or snackbar with a friendly message. Provide a generic
error dialog utility that can be called from anywhere (e.g. AppDialog.showError(context,
message) or using a global scaffold messenger for snackbars). This ensures uniform style and
wording. For instance, if the chat message fails to send, the UI might show a snackbar, “Message
failed to send. Please check your connection.” If a critical error occurs (like an essential API is
```
### •

```
48 49
```
### •

### •

### •

```
50 51
```
-

```
50
```
### •

```
52
```
```
52
53
```
### •

### •

### •

### •


```
unreachable), a dialog might be more appropriate. The exact mechanism can depend on the
context, but should be defined once and reused.
```
The project principle is to use _centralized components for error UI_ , not custom alerts in every screen.
For example, an AppErrorDialog widget in app/presentation/widgets/common/ can display
error titles and messages, and it can be triggered by any provider that encounters an error (perhaps via
a global error provider or navigator key). Likewise, use the same snackbar styling for minor notifications
across the app.

```
Performance Monitoring: As part of logging, include performance metrics for critical
interactions. The AppLogger’s performance logs (and any timing in the code) should be used to
track how long operations take – for example, log the time to receive a response from the AI
after sending a message, or the time it takes to process a voice recording. This helps identify
bottlenecks. The team has made logging of performance a priority in recent updates.
```
```
No Swallowing Errors: Do not catch an exception and then do nothing. Every catch should
either log the error or propagate it in a controlled way to be handled upstream. Silence is the
enemy during debugging – even if you handle an error gracefully for the user, also log it for
developers. The standard practice is to log at the point of catch with as much context as possible
(e.g. which function failed). If the error is user-facing, you log and also trigger a user message; if
it’s non-user-facing (say a background task failed but can retry), you might log a warning but not
necessarily alert the user. Use judgment, but always log.
```
```
Testing Error Paths: Ensure to test how the app behaves under failure conditions (no internet,
server returns error, etc.). The centralized logging and error UI should make these scenarios
manageable. The AppLogger was enhanced to include error categorization and stack traces
to aid in debugging – developers should utilize those features (e.g. differentiate between
network errors vs validation errors in logs). The logging system now closely matches the one
used in the legacy frontend, which adds a lot of transparency for troubleshooting issues.
```
By following these logging and error handling standards, we maintain high observability of the app’s
behavior and provide a consistent experience to the user when things go wrong. Remember: use
AppLogger for any debug/info output, handle errors in a controlled manner, and provide feedback
through unified dialogs/snackbars rather than obscure or no messages.

## Documentation, Versioning, and Reporting Protocol

To ensure clarity in project communication, a structured protocol for documentation and versioning is
in place:

```
Standard Documents: All official architecture and standard guidelines are recorded in the
reports/ directory as standard_xxx.txt files. The naming uses a sequential version
number (xxx as an zero-padded integer). For example, the initial standard might be
standard_001.txt, with subsequent revisions as standard_002.txt,
standard_003.txt, etc. (always increasing). Use underscores in these filenames (not
hyphens) for consistency – previous inconsistency between standard_001 and
standard-002 was resolved by choosing the underscore style as the single format.
Whenever the architecture or guidelines are significantly updated (for instance, when new
features like the widget reorganization or platform adaptations are introduced), a new
standard_xxx.txt should be created with the next version number to capture the changes.
```
```
14
```
### •

```
50 54
```
### •

### •

```
50
```
```
55 56
```
### •

```
57 58
```
```
57
```

```
The latest standard file is considered the source of truth, but older ones are kept for historical
reference.
```
```
Knowledge Base: In addition to standards, we maintain knowledge base documents as
knowledge_xxx.txt in the reports folder. These serve as curated notes on recurring issues,
important decisions, and “lessons learned” that don’t necessarily fit in the formal standard. They
are versioned similarly (001, 002, etc.). For example, there might be a knowledge_002.txt
outlining platform-specific pitfalls or a knowledge_003.txt covering fixes applied in a certain
task. Team members should consult these knowledge files to avoid repeating past mistakes
(for instance, a knowledge file might list common errors like import issues or a specific
workaround for web audio that developers should be aware of). When new significant insights
are gained (e.g. discovering how to properly handle a tricky bug or a best practice to improve
performance), add them to the latest knowledge file or create a new one if needed. This practice
creates a self-documenting log of hard-won knowledge.
```
```
Task Reports: Every development task or bug fix is documented in a task_xxx.txt report
(also stored in reports/). The numbering is sequential and should always increment from the
last existing task file. Developers should follow the established template for these reports,
which typically includes sections like Task Requested , Analysis Performed , Issues Identified , Actions
Taken , Verification , etc. The task reports serve as both a record of changes and a communication
tool for code reviewers or other team members. Always write the task report for any non-trivial
change – this habit ensures we capture the rationale behind changes and any new standard or
knowledge updates that result.
```
```
File Header Metadata: Each standard or knowledge file (and even task reports) should include
some metadata at the top. This can be the version number, date of creation or update, and a
brief description of its purpose. For example, a standard file may start with a header indicating
the project name, the version of the standard, and when it was last updated (and possibly by
which task). This helps readers immediately know if they have the latest version and the
context. It’s recommended to update the header of the standard file whenever significant
changes are made (e.g. “ Last Updated : 2025-07-26 by Task 017 – added platform guidelines”).
The agent’s review suggested adding creation dates and version info in file headers for clarity
```
- we should adopt that practice going forward.

```
Cross-Referencing: Within these documents, reference each other where relevant. For instance,
if a task report implements a new rule, it should mention “standard_004.txt updated
accordingly.” The standard can mention “(See task_00X for background on this rule).” This creates
a paper trail that’s easy to navigate. In our Markdown-based reports, you can use links to refer to
file names or sections. This isn't strictly required but is highly encouraged for better traceability
of decisions.
```
```
Consistency and Template: All reports (task or otherwise) should follow the established format
to ensure no important details are omitted. The instruction is always to check the latest task
number and increment – never overwrite an old report , always create a new one for a new task
```
. In content, use the same section headings and ordering as the template unless there's a
special case.

Following this protocol, at any given time team members (or even external reviewers) can find the
current standards in the highest-numbered standard_XXX.txt, learn from past issues in the
knowledge_XXX.txt files, and review specific changes in task_XXX.txt reports. This structured

### •

```
59
```
### •

```
60
```
### •

```
61
```
```
62
```
### •

```
62
```
### •

```
63
```

documentation is treated as part of the deliverables – keep it up to date as you code. It greatly reduces
confusion (for example, avoiding the situation where multiple standard files had conflicting info – which
we resolved by consolidating and standardizing the naming ).

Lastly, **enforce these standards** : Code reviews should check code structure against the standard, QA
should verify that UI follows the standard (e.g. message bubbles, etc.), and any deviation or new
requirement should lead to an update of the standards document. By doing so, the project’s
architecture remains consistent and newcomers can quickly get up to speed by reading the latest
standard guide.

## Dart & Flutter Coding Conventions

All code must follow standard Dart and Flutter style conventions to ensure readability and
maintainability. In general, adhere to the **official Dart style guide** and best practices from the Flutter
team. Key points include:

```
Naming Conventions: Use UpperCamelCase for class names (e.g. ChatController,
RecordingService), lowerCamelCase for variable names and function names
(isRecording, fetchAgents()), and ALL_CAPS with underscores for constant values
(MAX_RETRY_ATTEMPTS – though in Flutter, prefer using static const in classes rather than
global constants). File and directory names should be in snake_case (all lowercase, underscores
between words). For example, a file containing MyBusinessNotifier should be named
my_business_notifier.dart. Avoid abbreviations that are not obvious – clarity is more
important than brevity (e.g. use authentication rather than auth in names, unless it’s a
well-known term in context). Consistent naming helps navigate the project easily.
```
```
Project-Specific Naming: Follow the established patterns in this project for file names and class
names. For instance, as noted, files in application/ often use the
<feature>_providers.dart format for providers. Widgets should typically be named after
their functionality (e.g. AgentCategoryCard in agent_category_card.dart). Maintain
one class per file unless a smaller private class is tightly tied to the main class. This project
already has a pattern for widget naming (like ending with _card.dart, _form.dart etc.
depending on their folder) – continue using those suffixes as a hint of the widget type.
```
```
Formatting: Use Dart’s official formatter (dart format) to keep code layout consistent.
Indentation is 2 spaces. Keep line lengths reasonable (the formatter typically wraps lines around
80-100 chars; don’t manually break lines arbitrarily). Use trailing commas in Flutter widget
constructors and collection literals to help the formatter produce nicely indented multi-line
layouts.
```
```
Flutter Best Practices: Use const constructors and widgets wherever possible to reduce
rebuilds. Prefer StatelessWidget or ConsumerWidget (from Riverpod) over StatefulWidget unless
local mutable state is truly needed. Avoid unnecessary rebuilds by using keys and refactoring
large widgets into smaller ones. Follow Flutter’s composition over inheritance principle – build UI
by composing widgets, not by creating huge widgets or deep inheritance trees.
```
```
Modern Dart Features: Use recent Dart language features when applicable (but ensure they are
supported by the project’s minimum SDK). For example, if on a newer Dart, prefer using
enhanced enums or pattern matching (if appropriate) over older verbose patterns. Use null-
safety practices diligently – unwrap optionals safely, provide default values or fallbacks to avoid
```
```
57 58
```
```
64
```
### •

```
65
```
### •

```
66
```
### •

### •

```
67
```
```
68
```
### •


```
runtime null errors. Also, use the newer Flutter APIs and widgets – avoid deprecated widgets/
properties (the knowledge base should be consulted for notes on deprecated API usage).
If you find code using older conventions (like manual Navigator.push where we now use a
Router or any deprecated Material widgets), note it and update if within scope.
```
```
Comments and Documentation: Write clear comments for complex logic. Public classes and
functions, especially those exposed as part of our architecture (e.g. a service class or a provider),
should have dartdoc comments explaining usage. In widget build methods, it's often helpful to
label end-of widgets in comments for readability if the tree is complex. But avoid obvious or
redundant comments – strive for self-documenting code with good naming. Use TODO
comments sparingly (and if used, prefix with your name or a task reference and add them to the
task tracking if they are to be resolved). The standard mandates removal of lingering TODOs and
prints in production code.
```
```
Testing Conventions: While not explicitly asked, note that tests (if any) should follow a similar
folder structure and naming. For example, widget tests mirror the widget structure. If writing
tests, name test files after the file under test (e.g. chat_controller_test.dart to test
chat_controller.dart). Use the given templates and ensure tests run in all platforms if
applicable.
```
By following these coding conventions, the code remains consistent and professional across the entire
team. The **Dart style guide** is the baseline – if unsure about a style question, refer to it (for instance,
naming, ordering of constructor initializers, use of this. or not, etc.). In code reviews, stylistic
issues should be pointed out and corrected to maintain the standard. Consistent syntax and naming
make it much easier to on-board new developers and to collaborate without confusion.

By implementing the above rules and guidelines, the Flutter project will have a maintainable, scalable
structure that supports **Web, Mobile, and Desktop** platforms uniformly. All developers should
familiarize themselves with this document and refer back to it (and the cited report files like
**app_data.txt** for API details) whenever adding new features or refactoring. This ensures the entire
team stays aligned with the project’s architecture vision and coding standards, leading to a high-quality
codebase.

---
name: youtube-watcher-cli
description: Use the local YouTube Watcher CLI binary to ask Gemini grounded questions about YouTube videos, including summarization, transcription-style extraction, visual-content inspection, moderation preambles, code/text extraction, and multilingual video understanding. Trigger when a user provides a YouTube video URL or video ID and wants information from the video through the standalone binary.
---

# YouTube Watcher CLI

Use the `youtube-watcher-cli` binary when a task needs grounded understanding of a YouTube video through Gemini's native video input support.

## Requirements

- Treat this as a standalone binary tool, not a library.
- Expect `youtube-watcher-cli` or `youtube-watcher-cli.exe` to be available on `PATH`, unless the user provides an explicit executable path.
- Use the video parameter with `--video`.

### Environment variables

The executable authenticates and reads through these environment variables, please note that it's recommended to run and perform first pass operation instead of checking these variables first before continuing.

For troubleshooting guidance, refer to Failure Handling section below.

- `OPENROUTER_API_KEY` - Used if `--openrouter` flag is used to authenticate with OpenRouter key and endpoint. This ignores other variables below.
- `GEMINI_API_KEY` - If set, it will use Gemini Developer API instead of Gemini Enterprise Agent Platform (Vertex AI).
- `GOOGLE_GENAI_USE_ENTERPRISE` and `GOOGLE_CLOUD_PROJECT` - If set, it will use Gemini Enterprise Agent Platform (Vertex AI) global endpoint instead of Gemini Developer API version. This only toggles to use the Vertex endpoint, authentication is still handled by the user side. The user can also set regions using `GOOGLE_CLOUD_LOCATION` variable.

## Arguments

```bash
youtube-watcher-cli --video [YOUTUBE_VIDEO_ID_OR_URL] --model [MODEL_ID] --service-tier [TIER] [prompt]
```

- `--video [YOUTUBE_VIDEO_ID_OR_URL]`: Required. Pass only the video ID or URL, such as `dQw4w9WgXcQ` or `https://www.youtube.com/watch?v=dQw4w9WgXcQ`.
- `--model [MODEL_ID]`: Optional. Specify a model to use to process the video, defaults to `gemini-2.5-flash` if not specified. See the supported models section below for choosing model.
- `--media-resolution [RESOLUTION]`: Optional. Specify the media resolution for the video, such as `low` or `high`. Defaults to `low` if not provided. Use `low` to prioritize speed and cost over extreme fine-detail, and `high` for better visual fidelity and fine details over cost of speed and budget. This option is not available when using `--openrouter` flag.
- `--service-tier [TIER]`: Optional. Specify the service tier for processing, such as `flex` or `priority`. Defaults to `standard` if not provided. Use `flex` for lower cost and slower processing, and `priority` for faster processing at a higher cost. Note that using `priority` processing must be consented by the user first acknowledging that it will incur higher costs and may be subject to rate limits or quotas.
- `--agentic-processing`: Optional. This option instructs Gemini to use tools to dynamically seek through video frames and audio to find relevant information in a loop rather than ingesting the entire video to context window. This is recommended for most recent models and should be enabled by default, please refer to "Static vs. Agentic Processing" section below for more details. This option is not available when using `--openrouter` flag.
- `--openrouter`: Optional. Uses OpenRouter served model instead of official Google's endpoints, `OPENROUTER_API_KEY` must be set or present in the environment.

`prompt` must be placed after all named arguments. The tool joins all remaining positional arguments into a prompt.

### Utility arguments

These will be prioritized if provided, overrides other parameters and only prints the help and version info, then quits the program.
- `--version`: Print the binary version and exit.
- `--help`: Show usage help.

Do not place named options after the prompt. Anything after the prompt is treated as prompt text.

## Static vs. Agentic Processing
By default, the watcher CLI uses static processing with Gemini 3 Flash, this is the default behavior for  Gemini models as primary way to ingest video and audio content.

When using Gemini 3.5 Flash Lite or Gemini 3.7 Flash and above, it's recommended to use `--agentic-processing` flag, what it does is instead of ingesting the entire video and it's audio to context window, Gemini models will use tools to dynamically seek through video frames, transcript, or audio at specific times. It is also much faster and cheaper especially for longer videos as it only grabs relevant parts of the video on demand.

Use agentic processing as a default processing mode for recent models after Gemini 3 Flash Preview, it's also recommended to use this for longer videos beyond an hour, videos that require more detailed or temporal understanding, fast pacing videos, and searching segments within the compilation video.

Please note that agentic processing can still incur higher costs and latency for exhaustive tasks due to tool calling invocations it needed to conduct analysis and each intermediary tool call can incur additional time and token costs, it's recommended to start with Gemini Flash-Lite first before promoting to Gemini Flash unless the user said otherwise. Optimization can still be applied such as prompting, setting service tier, and media resolution.

Only use static processing by omitting the flag for Gemini 3 Flash Preview or when the user explicitly asks to, this mode supports all models. This was the behavior of Gemini models prior to the recent models when understanding videos, it is fixed, static, and configured to sample frames at 1fps, only use this to ensure legacy consistent performance or if needing all the context to be considered without intermediate tool calling step time.

If the user asks to summarize videos beyond an hour or working with videos such as compilation style formats, suggest the user first to use agentic processing with models that supports it even if the user is explicitly asking for static processing or is using Gemini 3 Flash Preview.

## Supported models

- `gemini-3-flash-preview` - Best balance for speed, cost, and intelligence. Outperforming it's 2.5 Pro predecessor. It is the default with minimal reasoning effort. This does not support agentic processing and is not recommended for long or fast pacing videos.
- `gemini-3.5-flash-lite` - Google's latest Flash-lite line of model that outperforms 2.5 Flash model and is cheaper than 3 Flash Preview. Useful for quick video overviews and faster processing of long videos for time and budget constrained scenarios. This model has reasoning effort to medium.
- `gemini-3.7-flash` - Google's previous Flash model of Gemini 3.5 Flash iteration, matches or exceeding the quality of it's previous 3.1 Pro and Flash model, with reasoning effort set to low. However, it is more expensive and has higher latency than other two models.
- `gemini-3.8-flash` - Google's latest Flash model, with better performance in agentic tasks, with better reasoning depth but would spend bit more time thinking than previous model, about the same price as 3.7 flash.

## Workflow

1. Obtain the YouTube video URL or ID from the user input.
2. Confirm if `GEMINI_API_KEY` is available in the command environment.
3. Run the binary with `--video` before the prompt.
4. Read the answer from stdout and report the relevant result to the user.

## Prompting

Write direct prompts for the video task. Good prompt shapes include:

```bash
youtube-watcher-cli --video dQw4w9WgXcQ summarize the video with key timestamps
youtube-watcher-cli --video dQw4w9WgXcQ extract any visible code or terminal commands
youtube-watcher-cli --video dQw4w9WgXcQ describe visual actions and spoken content in detail
youtube-watcher-cli --video dQw4w9WgXcQ classify whether this video is safe to show before playback
```

Quote the prompt if the shell or command runner requires it, but keep it as the final positional argument.


## Model Outputs

When making a request, it returns a structured JSON output (excluding if an error has occurred) that displays brief description of the video and optionally timestamps including an associated description of the timestamped passage. The timestamps are formatted as DD:HH:MM:SS with proper time conversion. The JSON output is deliberate and it's format cannot be changed.

## Pipelines and redirection

Piping from other command outputs to Watcher CLI aren't supported yet, therefore avoid using piping commands with the Watcher CLI executable as a way to ingest context. However, Watcher CLI outputs from `stdout` and its errors from OS `stderr` can be piped to other commands or redirected to a file.


## Model capabilities

### What it can do:

See visual frames and hear audio of the video, text prompt, and small system instruction always appended to define it's role. It can also understand timestamps of the video associated with the frame but it can be inaccurate (use with caution, must be treated as approximate indicators and not exact).

### What it can't do

It cannot see YouTube video ID, title, or other metadata. Use `yt-dlp` or YouTube Data API to get that information separately if needed.

It may also struggle with very long videos due to context limit, such as videos exceeding more than 1.5 hours with audio. Before committing to input videos, check the metadata and duration of the video first whenever possible to ensure it is within the model's context limit. 

Irrelevant prompts outside of video context may result the model producing soft refusal as it is instructed to answer questions bound into the video, but not susceptible to jailbreaks. Text and video content has potential risks with prompt injection as multimodal inputs can inject instructions that would drift its intended task, use model outputs with caution.

## Failure Handling

- If `GEMINI_API_KEY` is missing after running the executables first-pass, ask the user to set the environment variable first before continuing and discourage putting the API key within the current agent context. The user can also set an environment variable to a file, refer the user to this documentation: https://github.com/zavocc/youtube-cli#installation-and-auth. In addition, do not set or source any environment variable yourself and you must halt first and explicitly ask the user to set it up first before continuing or perform alternatives.
- If `GOOGLE_GENAI_USE_ENTERPRISE` is set along with `GOOGLE_CLOUD_PROJECT` instead of `GEMINI_API_KEY` but reports authentication failure, ask the user to authenticate with Google Cloud with project and Gemini Enterprise Agent Platform (a.k.a Vertex AI) access, also refer to the same installation and auth URL above and you must halt first for the user to take manual action to authenticate, which includes but not limited to setting the optional `GOOGLE_APPLICATION_CREDENTIALS` path to service account JSON, workload identity federation, or impersonation. You can also link the user to https://docs.cloud.google.com/docs/authentication.
- If using Gemini Enterprise Agent Platform (Vertex AI) and reports invalid region, the model may not support regional inference or data residency controls, to diagnose, ask the user to temporarily unset `GOOGLE_CLOUD_LOCATION` and retry as it will default to `global` region. You must also halt and acknowledge the user if its okay for the prompt to be inferenced outside of their preferred region before proceeding.
- If the user provides a full YouTube URL, extract the `v` parameter or short URL ID instead of passing the full URL.
- If the binary is missing from `PATH`, ask the user for the executable path or to install the release binary.
- If the prompt is absent, ask for the question or extraction task to run against the video.
    

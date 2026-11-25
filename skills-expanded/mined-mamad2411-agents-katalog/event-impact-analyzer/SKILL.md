---
name: event-impact-analyzer
description: Analyze historical market impact on Nasdaq and KOSPI for wars, geopolitical conflicts, sanctions, tariffs, macro shocks, crises, and other major news events by finding comparable past events, verifying exact dates, and measuring index drawdowns and rebounds around those dates. Use this skill whenever the user asks how KOSPI or Nasdaq moved during similar events, asks for past analog cases, or wants market context from a keyword, headline, natural-language request, or URL.
---

# Event Impact Analyzer

Research historical analog events for a user-provided event, then measure how Nasdaq and KOSPI moved around each event date using KIS daily index data.

## What this skill does

Use this skill when the user wants an investor-oriented report about how an event affected markets, especially Nasdaq and KOSPI.

Accepted user inputs:

- Keyword or short phrase
- Natural-language request
- URL

Expected output:

- A Markdown investor report returned directly in the chat
- No file creation unless the user explicitly asks for one

## Workflow

1. Identify the target event.
2. Check credentials before doing any substantive work.
   - Check `KIS_APP_KEY`, `KIS_SECRET_KEY` first.
   - Check `~/.config/event-impact-analyzer/credentials.yaml` next.
   - If both sources are missing or incomplete, stop immediately.
   - Tell the user exactly what you checked and that market-data analysis cannot continue yet.
   - Ask the user to provide the missing values or store them in one of the supported locations.
   - Do not continue to URL interpretation, analog research, script execution, or report writing until credentials are available.
3. If the input is a URL, use web search to understand what event it refers to and extract the core event keywords.
4. Generate a broad but relevant set of historical analog events.
   - Include geopolitical analogs, sector analogs, and macroeconomic analogs when they are relevant.
   - Do not cap the count artificially; stop when additional cases become weak or repetitive.
5. For each event, use web search to determine the exact calendar event date.
   - Keep the original calendar date.
   - Separately compute the corrected market trading date for each index.
6. Start with the default window:
   - 1 calendar month before the event date
   - 3 calendar months after the event date
7. Expand the window when needed.
   - Do this if the user explicitly asks for a longer horizon.
   - Do this if the trough, rebound, or recovery logic clearly needs more forward data.
   - Do this if the lead-up period before the event appears important and needs more context.
8. Run the bundled script to fetch KOSPI and Nasdaq daily data and calculate the required metrics.
9. Analyze each event window.
10. Synthesize the cross-event patterns into an investor report.

## Web research rules

Use web search whenever you need:

- To interpret a URL
- To identify historical analog events
- To verify the exact event date
- To resolve ambiguous event naming

When you describe dates to the user:

- Show the exact calendar event date
- Show the market trading date correction separately
- Do not silently replace the event date with the next trading day

## Current date and current index rules

Do not assume the current date from model memory.

- Get the current date from the bundled script at runtime.
- Do not rely on model memory for "today".
- Use the script runtime date as the reference point for any "current index level" statements in the report.

Before writing downside scenarios in `## 투자 관점 시사점`:

- Obtain the current KOSPI and current Nasdaq index levels from the bundled script output.
- Do not use web search for current index levels when the script can provide them.
- Treat the script runtime date as the analysis reference date and the latest available trading date as the quote date.
- State the reference date used for the current index levels.
- If current index levels cannot be verified, say so explicitly and do not present current-level downside point estimates as if they were confirmed.

## Market-data rules

Use the bundled script at `scripts/analyze_event_impact.py`.

The script:

- Fetches KOSPI and Nasdaq Composite daily candles from the KIS Open API
- Resolves credentials from environment variables or `~/.config/event-impact-analyzer/credentials.yaml`
- Uses the event calendar date plus configurable pre/post windows
- Corrects each index to the first available trading day on or after the event date
- Can return a current-market snapshot for KOSPI and Nasdaq using the script runtime date and a short recent lookback window
- Returns raw daily candles and computed metrics as JSON
- Does not write the final Markdown report for the user

Run it like this:

```bash
python3 <skill-dir>/scripts/analyze_event_impact.py --event-date YYYYMMDD
```

When you need current index levels for downside scenarios, run:

```bash
python3 <skill-dir>/scripts/analyze_event_impact.py \
  --current-snapshot
```

With `--current-snapshot`, the script returns only the current snapshot payload and skips the historical event-analysis loop.

Optional metadata flags:

```bash
python3 <skill-dir>/scripts/analyze_event_impact.py \
  --event-date 20200103 \
  --event-name "미국-이란 긴장 고조" \
  --event-label "Qasem Soleimani strike" \
  --pre-months 2 \
  --post-months 6
```

The script always returns JSON. Use that JSON as analysis input, then write the final investor report yourself.
When you run `--current-snapshot`, use the returned `current_snapshot` payload for the current KOSPI/Nasdaq reference levels in `## 투자 관점 시사점`.

## Credential flow

Credential availability is a hard gate. Before doing web research, analog selection, script execution, or report writing, check in this order:

1. `KIS_APP_KEY`, `KIS_SECRET_KEY`
2. `~/.config/event-impact-analyzer/credentials.yaml`

If both sources are missing or incomplete:

- Stop the workflow immediately.
- Tell the user that both credential sources were checked and analysis is paused.
- Tell the user exactly which source was missing or incomplete.
- Ask the user to provide the missing values or store them in one of those two locations.
- Do not continue with any other task steps until the user responds with credentials or confirms they were stored.

Only ask the user after both checks fail. Be explicit about what you checked.
Do not ask the user for CLI args first.
Prefer existing credentials on the machine before requesting input.

Config file format:

```yaml
app_key: "YOUR_APP_KEY"
secret_key: "YOUR_SECRET_KEY"
```

When credentials are missing, make the status explicit:

- Say that you checked environment variables first.
- Say that you checked the config file next.
- Say which source was missing or incomplete.
- Then ask the user for the missing values or to store them in one of those two locations.
- Make it explicit that you are stopping here and cannot continue the analysis until credentials are available.

## Analysis definitions

For each index, report these metrics:

- Event calendar date
- Corrected trading date
- Previous trading date
- Event-day close return vs previous close
- Event-day intraday low return vs previous close
- Downtrend end date
  - Define the downtrend as ending at the post-event lowest low.
- Maximum drawdown low return vs previous close
- Maximum drawdown close return vs previous close
- 1-month rebound return from trough close
- 1-month rebound return from trough low
- Difference between the 1-month-after-trough close and the pre-event previous close

If the trough occurs too late to have a full month of forward data:

- First consider expanding the forward window and re-running the script
- If you still cannot get a full month, use the last available trading date and state that the rebound window is truncated

## Interpretation rules

When writing the report:

- Compare Nasdaq and KOSPI side by side for every event
- Separate immediate shock, deepest damage, and rebound phase
- Highlight whether KOSPI overreacted or underreacted relative to Nasdaq
- Call out cases where the event-day close was mild but the intraday low shows panic
- Distinguish single-day shock from multi-week trend damage
- Prefer pattern synthesis over listing raw numbers only
- Base your narrative on the script's JSON output rather than manual arithmetic in prose
- In `## 투자 관점 시사점`, translate the historical drawdown ranges into current-index downside scenarios for both Nasdaq and KOSPI
- Express the downside scenario in both percentage terms and index-point terms
- Anchor the scenario to the current Nasdaq and KOSPI index levels available at analysis time
- Include the reference date for those current index levels
- Make clear that this is an analog-based scenario range, not a precise forecast

Do not claim causality more strongly than the evidence allows. Use language like:

- "coincided with"
- "the market reaction suggests"
- "this analog implies"

## Report structure

Always use this structure:

```markdown
# [이벤트명] 시장 영향 리포트
## 한눈에 보기
- 입력 사건 요약
- 핵심 유사 사건 수
- Nasdaq/KOSPI 공통 패턴
- 가장 중요한 투자 시사점

## 현재 사건 정의
- 입력 형태: keyword/request/url
- 사건 설명
- 핵심 키워드
- 분석에 포함한 유사 사건 선정 기준

## 유사 사건별 분석
### [사건명] ([캘린더 날짜], 거래일 보정: Nasdaq / KOSPI)
- 사건 개요
- Nasdaq 반응
- KOSPI 반응
- 해석

## 종합 패턴
- 즉시 충격 패턴
- 최대 낙폭 패턴
- 반등 패턴
- Nasdaq 대비 KOSPI 특성

## 투자 관점 시사점
- 기본 시나리오
- 약세 시나리오
- 현재 KOSPI, Nasdaq 지수 기준 예상 하단 범위
  - 과거 유사사건 기준 최대 하락률 범위
  - 현재 지수에 적용한 예상 하락 포인트
- 체크해야 할 추가 신호

## 한계
- 유사 사건 비교의 한계
- 동시기에 겹친 다른 변수
```

## Working style

- Keep the report concise but decision-useful.
- Use exact dates and percentages.
- Prefer 3-6 strong analogs over a long weak list, even though there is no hard cap.
- If the event is very broad, cluster the analogs and explain why each cluster matters.

## Example prompts

Example 1:
Input: `미국-이란 전쟁이 나면 나스닥하고 코스피가 어떻게 반응했는지 과거 사례 기준으로 분석해줘`
Output: Historical analog report with exact event dates, KOSPI/Nasdaq metrics, and investor implications.

Example 2:
Input: `https://example.com/news/article-about-tariffs`
Output: URL interpretation, event keyword extraction, tariff-war analog research, and market impact report.

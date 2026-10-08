# news-fetcher

Description:
Fetches news articles related to government schemes, policies, and civic affairs using the GNews API or a fallback PIB RSS feed.

## Usage

This skill is designed to be run as a command-line script.

### Command Line Execution

```bash
python news.py --query <SEARCH_QUERY> [--days <NUMBER_OF_DAYS_AGO>]
```

### Arguments

-   `--query`: The search term for news articles.
-   `--days`: (Optional) Specifies how many days ago to look for news. *Note: The GNews API primarily uses date ranges (`from`, `to`) or `published_after`. This parameter will be interpreted to set a `published_after` date if supported by the API, otherwise, it will fetch recent articles.*

### Functionality

1.  **API Key**: Uses the GNews API key: `5c487d8b638599605aee0821c99c6285`.
2.  **Civic Keyword Filter**:
    *   Checks if the query includes keywords like: `scheme`, `yojana`, `government`, `ministry`, `welfare`, `pension`, `subsidy`, `benefit`, `policy`, `PM`, `CM`.
    *   If the query does not contain any civic keywords, it prints: `[BLOCKED] Query not related to government/civic domain` and exits with an error.
3.  **GNews API Fetching**:
    *   If the query is civic-related, it prints: `[ALLOWED] Civic query approved: <query>`.
    *   Calls the GNews API (`https://gnews.io/api/v4/search`) with parameters:
        *   `q=<query>+India+government` (appends relevant terms)
        *   `lang=en`
        *   `country=in`
        *   `max=5` (fetches top 5 articles)
    *   Prints the title, source, date, and URL for each of the top 5 articles.
4.  **PIB RSS Fallback**:
    *   If the GNews API fails (e.g., due to invalid key, network issues, or API errors), it falls back to fetching from the PIB RSS feed: `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3`.
5.  **Output**: Displays fetched article information or fallback message.

### Error Handling

-   **Non-Civic Query**:
    ```
    [BLOCKED] Query not related to government/civic domain
    ```
    (Exits with error code 1)
-   **API Errors**: Handles general request errors and timeouts.
-   **Fallback**: If GNews fails, it attempts to retrieve news from PIB RSS.

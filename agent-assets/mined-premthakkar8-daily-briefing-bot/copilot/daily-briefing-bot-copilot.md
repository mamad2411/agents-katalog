<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Daily Briefing Bot - Copilot Instructions

This is a Python project for a Daily Briefing Bot that automatically provides scheduled briefings with weather, news, stock prices, and calendar events.

## Project Structure
- `main.py`: Main application entry point with scheduling
- `src/config.py`: Configuration management with environment variables
- `src/briefing_service.py`: Main coordinator for all briefing data
- `src/weather_service.py`: OpenWeatherMap API integration
- `src/news_service.py`: News API integration
- `src/stock_service.py`: Alpha Vantage API integration
- `src/calendar_service.py`: Calendar integration (currently mock)
- `src/notifier.py`: Multi-channel notification system

## Key Dependencies
- `openmeteo-requests`: For weather data from Open-Meteo API
- `pandas`: For data processing
- `requests-cache`: For API response caching
- `aiohttp`: For async HTTP requests to APIs
- `schedule`: For task scheduling
- Standard library: `asyncio`, `logging`, `smtplib`, `email`

## API Integrations
- Open-Meteo for weather data (free, no API key required)
- News API for headlines
- Alpha Vantage for stock prices
- Future: Google Calendar/Outlook integration

## Code Style Guidelines
- Use async/await for API calls
- Include proper error handling and logging
- Follow type hints where appropriate
- Use dataclasses for configuration
- Maintain separation of concerns between services

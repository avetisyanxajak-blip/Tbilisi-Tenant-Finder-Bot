# Tbilisi Tenant Finder

Simple Telegram bot for screening public tenant-search posts against one apartment profile.

## Apartment profile
Tbilisi, Isani–Samgori, Moscow Avenue; 45 m²; 10th floor; 1 bedroom; $850/month; minimum 1 year; one person/couple; no pets; parking, balcony, elevator, Smart Home.

## Local run
1. Install Python 3.13.
2. `pip install -r requirements.txt`
3. Set environment variable `TELEGRAM_BOT_TOKEN` to the token from BotFather. Never commit the token.
4. `python bot.py`

## Render
Create a Background Worker from this repository.
Build command: `pip install -r requirements.txt`
Start command: `python bot.py`
Environment variable: `TELEGRAM_BOT_TOKEN` = your BotFather token.

Note: Render Background Workers are intended for continuously running processes, but availability/pricing depends on your Render plan. For initial free testing, run locally on your PC.

## Current scope
This first version scores posts you paste/forward to it. Automatic discovery from websites/social networks should be added source-by-source only where public access/API/terms permit it; it should not scrape private profiles or send unsolicited messages automatically.

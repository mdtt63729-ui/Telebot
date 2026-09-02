# Telegram Bot - Hosting Ready

## Required environment variables
- `BOT_TOKEN` = your Telegram bot token
- `PORT` = normally supplied automatically by the hosting platform

## Start command
```bash
python bot.py
```

Do not put the Telegram token directly in `bot.py` or commit it to GitHub.

The original archive contained a token in source code and a dependency mismatch
(`telebot` in the dependency file while the code imported `telegram`), plus the
dependency file was not actually named `requirements.txt`.

This safe version fixes the hosting/runtime structure but intentionally does
not implement personal-data lookup/leaking functionality.

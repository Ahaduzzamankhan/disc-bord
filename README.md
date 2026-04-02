# Discord Bot with Gemini AI

This is a Discord bot that provides suggestions for Discord server management, bot tips, game recommendations, and game strategies using Google Gemini AI.

## Setup

1. Install dependencies: `pip install -r requirements.txt`

2. Get your Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications).

3. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

4. Copy `.env.template` to `.env` and fill in your actual tokens.

5. Run the bot: `python main.py`

The bot will create a `.env` file with placeholders if it doesn't exist, but using the template is recommended.

## Hosting on Render.com

- Deploy as a Python app.
- Set environment variables in Render dashboard or keep in .env.
- The Flask server runs on port 8080 for keep-alive pings.

## Commands

The bot has over 50 commands, all starting with `!`.

### Discord Suggestions

- `!suggest_server_name`
- `!suggest_channel_names`
- `!suggest_role_names`
- `!suggest_emoji_ideas`
- `!suggest_bot_permissions`
- `!suggest_moderation_rules`
- `!suggest_welcome_message`
- `!suggest_goodbye_message`
- `!suggest_event_ideas`
- `!suggest_server_themes`

### Bot Tips

- `!suggest_bot_commands`
- `!suggest_bot_features`
- `!suggest_integration_ideas`
- `!suggest_custom_commands`
- `!suggest_bot_responses`
- `!suggest_error_handling`
- `!suggest_logging_ideas`
- `!suggest_backup_strategies`
- `!suggest_update_ideas`
- `!suggest_security_tips`

### Game Recommendations

- `!suggest_games_for_friends`
- `!suggest_single_player_games`
- `!suggest_multiplayer_games`
- `!suggest_indie_games`
- `!suggest_classic_games`
- `!suggest_new_releases`
- `!suggest_free_games`
- `!suggest_paid_games`
- `!suggest_mobile_games`
- `!suggest_pc_games`
- `!suggest_console_games`
- `!suggest_board_games`
- `!suggest_card_games`
- `!suggest_puzzle_games`
- `!suggest_action_games`

### Game Strategies

- `!strategy_for_chess`
- `!strategy_for_poker`
- `!strategy_for_dota`
- `!strategy_for_lol`
- `!strategy_for_csgo`
- `!strategy_for_overwatch`
- `!strategy_for_fortnite`
- `!strategy_for_apex`
- `!strategy_for_pubg`
- `!strategy_for_rocket_league`
- `!strategy_for_minecraft`
- `!strategy_for_terraria`
- `!strategy_for_stardew_valley`
- `!strategy_for_civilization`
- `!strategy_for_total_war`

### Other Suggestions

- `!suggest_music_playlists`
- `!suggest_movies`
- `!suggest_books`
- `!suggest_coding_projects`
- `!suggest_learning_resources`

# Membarr Project Context

## Project Overview
Membarr is a Python-based Discord bot designed to automate user management for **Plex** and **Jellyfin** media servers. It is a fork of Invitarr. The bot monitors Discord roles and automatically invites users to the respective media servers when they are assigned specific roles. It also supports manual invitation commands and database management.

## Architecture & Technology
*   **Language:** Python 3.9+
*   **Framework:** `discord.py` (v2.4.0) for Discord interactions.
*   **Media Server APIs:**
    *   `PlexAPI` for Plex integration.
    *   Direct HTTP requests for Jellyfin integration.
*   **Configuration:** Hybrid approach using Environment variables (`bot.env`) for the Discord token and an INI file (`app/config/config.ini`) for application settings.
*   **Database:** SQLite (implied) for storing user mappings between Discord IDs and media server accounts.
*   **Containerization:** Docker (`python:3.9.1-alpine`).

## Key Files & Directories
*   `run.py`: The entry point of the application. It initializes the `Bot` class, defines setup slash commands (`/plexsettings`, `/jellyfinsettings`), and loads the main extension.
*   `app/bot/cogs/app.py`: The main logic hub. It handles:
    *   `on_member_update`: Monitors role changes to trigger invites/removals.
    *   Slash commands for manual invites (`/plex invite`, `/jellyfin invite`) and database management.
*   `app/bot/helper/`: Contains helper modules:
    *   `confighelper.py`: Manages reading/writing `app/config/config.ini` and loading env vars.
    *   `db.py`: Database interaction layer.
    *   `plexhelper.py` & `jellyfinhelper.py`: API wrappers for the media servers.
*   `bot.env`: Stores the `discord_bot_token`.
*   `Dockerfile`: Defines the build image based on Alpine Linux.

## Setup & Development

### Prerequisites
*   Python 3.9+
*   Discord Bot Token (with Privileged Intents: Presence, Server Members, Message Content)

### Installation
1.  **Install Dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```
2.  **Environment Setup:**
    *   Create a `bot.env` file in the root directory.
    *   Add `discord_bot_token=YOUR_TOKEN`.
    *   Alternatively, set the `token` environment variable.

### Running the Bot
```bash
python3 run.py
```

### Docker Usage
```bash
# Build
docker build -t membarr .

# Run
docker run -d \
  --name membarr \
  -v $(pwd)/app/config:/app/app/config \
  -e token="YOUR_DISCORD_TOKEN" \
  membarr
```

## Configuration Guide
The bot uses a dynamic configuration system. Initial setup (like the Discord token) is done via environment variables. Runtime configuration (Plex/Jellyfin credentials, roles, libraries) is handled via Discord slash commands, which update `app/config/config.ini`.

**Important Slash Commands:**
*   `/plexsettings setup ...`: Configure Plex credentials.
*   `/jellyfinsettings setup ...`: Configure Jellyfin credentials.
*   `/plexsettings addrole @Role`: Link a Discord role to Plex auto-invites.
*   `/jellyfinsettings addrole @Role`: Link a Discord role to Jellyfin auto-invites.

## Contribution & Style
*   **Formatting:** Follows standard Python PEP 8 guidelines (mostly).
*   **Async/Await:** Extensive use of `asyncio` for non-blocking Discord and API operations.
*   **Error Handling:** Specific error handling for API timeouts and invalid user inputs is implemented in the cogs.

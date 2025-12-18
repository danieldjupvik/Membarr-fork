---
name: Plex Role Restriction
overview: ""
todos:
  - id: add-restrict-functions
    content: Add plex_restrict_user and plex_unrestrict_user functions to plexhelper.py
    status: completed
  - id: modify-role-removal
    content: Update role removal handler to restrict instead of remove user
    status: completed
    dependencies:
      - add-restrict-functions
  - id: modify-role-addition
    content: Update role addition handler to check DB and unrestrict returning users
    status: completed
    dependencies:
      - add-restrict-functions
---

# Plex Label Restriction Instead of User Removal

## Overview

Modify the Membarr bot to apply Plex label restrictions (`filterMovies` and `filterTelevision` set to `{"label": ["noAccess"]}`) when a user loses their Discord role, instead of removing them from Plex entirely. When the role is regained, remove the restrictions. Admin commands will continue to fully remove users.

## Current Behavior

In [`app/bot/cogs/app.py`](app/bot/cogs/app.py) (lines 283-300), when a Plex role is removed from a Discord user:

1. The bot calls `plexhelper.plexremove()` which removes the user from Plex friends
2. The email is cleared from the database
3. User receives "You have been removed from Plex" message

## New Behavior

**When role is removed:** Apply "noAccess" label restriction to both Movies and TV Shows libraries (user stays on Plex but can't see content).**When role is added:**

- If user already exists in DB (was previously restricted): Remove the label restrictions
- If user is new (no DB entry): Prompt for email and invite them (existing flow)

**Admin `/plex remove` command:** Still fully removes users from Plex (unchanged).**User leaves Discord server:** Still fully removes users from Plex (unchanged - `on_member_remove` handler).

## Implementation

### 1. Add restriction functions to plexhelper.py

Add two new functions to [`app/bot/helper/plexhelper.py`](app/bot/helper/plexhelper.py):

```python
def plex_restrict_user(plex, email):
    """Apply noAccess label restriction to Movies and TV Shows"""
    plex.myPlexAccount().updateFriend(
        user=email, 
        server=plex,
        filterMovies={"label": ["noAccess"]},
        filterTelevision={"label": ["noAccess"]}
    )

def plex_unrestrict_user(plex, email):
    """Remove label restrictions from user"""
    plex.myPlexAccount().updateFriend(
        user=email,
        server=plex,
        filterMovies={},
        filterTelevision={}
    )
```



### 2. Modify role removal handler in app.py

Change lines 283-300 to call `plex_restrict_user()` instead of `plexremove()`. Keep the email in the database (remove the `db.remove_email()` call). Update the user message.

### 3. Modify role addition handler in app.py

Change lines 270-281 to check if user already has an email in the database:

- If yes: Call `plex_unrestrict_user()` to restore access
- If no: Continue with current flow (prompt for email, invite to Plex)

## Flow Diagram

```mermaid
flowchart TD
    subgraph RoleRemoved [Role Removed from User]
        R1[Get email from DB] --> R2[Apply noAccess restriction]
        R2 --> R3[Keep email in DB]
        R3 --> R4[Notify user: Access restricted]
    end
    
    subgraph RoleAdded [Role Added to User]
        A1{Email in DB?}
        A1 -->|Yes| A2[Remove noAccess restriction]
        A2 --> A3[Notify user: Access restored]
        A1 -->|No| A4[Prompt for email]
        A4 --> A5[Invite to Plex]
        A5 --> A6[Save email to DB]
    end
    
    subgraph AdminRemove [Admin /plex remove]
        AD1[Remove user from Plex entirely]
        AD1 --> AD2[Unchanged behavior]








```
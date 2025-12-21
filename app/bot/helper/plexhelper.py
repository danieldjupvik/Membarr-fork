import asyncio
import re

import plexapi.exceptions
import requests
from plexapi.myplex import MyPlexAccount


def plexadd(plex, plexname, Plex_LIBS):
    try:
        if Plex_LIBS[0] == "all":
            Plex_LIBS = plex.library.sections()
        plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=Plex_LIBS, allowSync=False,
                                              allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                              filterTelevision=None, filterMusic=None)
        print(plexname +' has been added to plex')
        return True
    except Exception as e:
        print(e)
        return False


def plexremove(plex, plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname)
        print(plexname +' has been removed from plex')
        return True
    except Exception as e:
        print(e)
        return False
        '''

        plex python api has no tools to remove unaccepted invites... 

        print("Trying to remove invite...")
        removeinvite = plexremoveinvite(plex, plexname)
        if removeinvite:
            return True
        '''
        
'''
def plexremoveinvite(plex, plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname)
        print(plexname +' has been removed from plex')
        return True
    except Exception as e:
        print(e)
        return False        
'''

def _update_share_filters(account, user, filter_movies=None, filter_television=None):
    """Update sharing filters using the clients.plex.tv endpoint (same as Plex Web UI).
    
    Parameters:
        account: MyPlexAccount object
        user: MyPlexUser object
        filter_movies: Dict with filter criteria for movies (e.g., {"label": ["noAccess"]})
        filter_television: Dict with filter criteria for television (e.g., {"label": ["noAccess"]})
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = "https://clients.plex.tv/api/v2/sharing_settings"
    
    # Get current sharing settings from the user object
    def get_setting(attr, default):
        val = getattr(user, attr, None)
        return val if val is not None else default
    
    payload = {
        "settings": {
            "allowChannels": get_setting('allowChannels', False),
            "filterMovies": account._filterDictToStr(filter_movies or {}),
            "filterMusic": get_setting('filterMusic', "") or "",
            "filterPhotos": get_setting('filterPhotos', "") or "",
            "filterTelevision": account._filterDictToStr(filter_television or {}),
            "filterAll": get_setting('filterAll', "") or "",
            "allowSync": get_setting('allowSync', False),
            "allowCameraUpload": get_setting('allowCameraUpload', False),
            "allowSubtitleAdmin": get_setting('allowSubtitleAdmin', False),
            "allowTuners": get_setting('allowTuners', 0)
        },
        "invitedEmail": user.username
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        account.query(url, method=account._session.post, json=payload, headers=headers)
    except (plexapi.exceptions.PlexApiException, requests.exceptions.RequestException) as e:
        print(f"Failed to update share filters (API/Request error): {e}")
        return False
    except Exception as e:
        print(f"Failed to update share filters (unexpected error): {e}")
        return False
    else:
        return True


def _plex_restrict_user_sync(plex, email):
    try:
        account = plex.myPlexAccount()
        user = account.user(email)
        success = _update_share_filters(
            account, 
            user,
            filter_movies={"label": ["noAccess"]}, 
            filter_television={"label": ["noAccess"]}
        )
        if success:
            print(f"Restricted access for {email}")
            return True
        return False
    except plexapi.exceptions.NotFound as e:
        print(f"User not found when restricting {email}: {e}")
        return False
    except plexapi.exceptions.BadRequest as e:
        print(f"Bad request when restricting {email}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error restricting user {email}: {e}")
        return False

async def plex_restrict_user(plex, email):
    return await asyncio.to_thread(_plex_restrict_user_sync, plex, email)

def _plex_unrestrict_user_sync(plex, email):
    try:
        account = plex.myPlexAccount()
        user = account.user(email)
        success = _update_share_filters(
            account, 
            user,
            filter_movies={}, 
            filter_television={}
        )
        if success:
            print(f"Unrestricted access for {email}")
            return True
        return False
    except Exception as e:
        print(f"Error unrestricting user {email}: {e}")
        return False

async def plex_unrestrict_user(plex, email):
    return await asyncio.to_thread(_plex_unrestrict_user_sync, plex, email)

def verifyemail(addressToVerify):
    regex = "(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    match = re.match(regex, addressToVerify.lower())
    return match != None
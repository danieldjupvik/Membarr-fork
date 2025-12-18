import re

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

def plex_restrict_user(plex, email):
    """Apply noAccess label restriction to Movies and TV Shows"""
    try:
        plex.myPlexAccount().updateFriend(
            user=email,
            server=plex,
            filterMovies={"label": ["noAccess"]},
            filterTelevision={"label": ["noAccess"]}
        )
        print(email + ' has been restricted on plex')
        return True
    except Exception as e:
        print(e)
        return False

def plex_unrestrict_user(plex, email):
    """Remove label restrictions from user"""
    try:
        plex.myPlexAccount().updateFriend(
            user=email,
            server=plex,
            filterMovies={},
            filterTelevision={}
        )
        print(email + ' has been unrestricted on plex')
        return True
    except Exception as e:
        print(e)
        return False
        
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
def verifyemail(addressToVerify):
    regex = "(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    match = re.match(regex, addressToVerify.lower())
    return match != None
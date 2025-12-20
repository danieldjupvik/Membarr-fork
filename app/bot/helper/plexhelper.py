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

def plex_restrict_user(plex, email, plex_libs):
    try:
        sections = plex_libs
        if sections[0] == "all":
            sections = plex.library.sections()
        plex.myPlexAccount().updateFriend(
            user=email, 
            server=plex,
            sections=sections,
            filterMovies={"label": ["noAccess"]},
            filterTelevision={"label": ["noAccess"]}
        )
        print(f"Restricted access for {email}")
        return True
    except Exception as e:
        print(f"Error restricting user {email}: {e}")
        return False

def plex_unrestrict_user(plex, email, plex_libs):
    try:
        sections = plex_libs
        if sections[0] == "all":
            sections = plex.library.sections()
        plex.myPlexAccount().updateFriend(
            user=email,
            server=plex,
            sections=sections,
            filterMovies={},
            filterTelevision={}
        )
        print(f"Unrestricted access for {email}")
        return True
    except Exception as e:
        print(f"Error unrestricting user {email}: {e}")
        return False

def verifyemail(addressToVerify):
    regex = "(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    match = re.match(regex, addressToVerify.lower())
    return match != None
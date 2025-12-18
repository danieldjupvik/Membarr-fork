from plexapi.myplex import MyPlexAccount
import re

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

        return False

def plexapplyrestrictions(plex, plexname):
    try:
        account = plex.myPlexAccount()
        friend = None
        for user in account.users():
            if user.title == plexname or user.email == plexname:
                friend = user
                break

        if not friend:
            print(f"Plex user '{plexname}' not found among shared users.")
            return False
        else:
            # Apply restrictions: set movie and TV show filters to 'Empty' label
            friend.updateFriend(filterMovies={'label': ['Empty']}, filterTelevision={'label': ['Empty']})
            print(f"Successfully applied 'Empty' label restrictions for '{plexname}'.")
            return True
    except Exception as e:
        print(f"Error applying restrictions for '{plexname}': {e}")
        return False

def plexremoverestrictions(plex, plexname):
    try:
        account = plex.myPlexAccount()
        friend = None
        for user in account.users():
            if user.title == plexname or user.email == plexname:
                friend = user
                break

        if not friend:
            print(f"Plex user '{plexname}' not found among shared users.")
            return False
        else:
            # Remove restrictions: set movie and TV show filters to None
            friend.updateFriend(filterMovies=None, filterTelevision=None)
            print(f"Successfully removed restrictions for '{plexname}'.")
            return True
    except Exception as e:
        print(f"Error removing restrictions for '{plexname}': {e}")
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
def verifyemail(addressToVerify):
    regex = "(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    match = re.match(regex, addressToVerify.lower())
    return match != None
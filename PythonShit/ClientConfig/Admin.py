import logging
import win32.pywintypes
from getpass import getuser

import win32.win32net

import Ops


# Check if user is an Administrator group member
def IsAdmin(username):
    try:
        admins = win32net.NetLocalGroupGetMembers(None, 'Administrators', 1)[0]
        for a in admins:
            if a['name'] == username:
                return True
        # print(username + " is not an administrator or does not exist.")
    except pywintypes.error:
        pass
    return False


# Check if current user is part of local administrators and other logging stuff
def checkAdmin():
    if not IsAdmin(getuser()):
        logging.warning(f'{getuser()} is not yet part of the local Administrators group.')
        logging.info(f'Appends to list of errors...')
        Ops.operations.append("Admin: Not Local Admin")
    else:
        logging.info(f'{getuser()} is already part of Administrators group')
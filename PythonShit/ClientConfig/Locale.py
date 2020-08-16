import logging

import Ops


def GetFormat():
    from locale import getdefaultlocale, windows_locale
    HEBREW = 1037
    return True if getdefaultlocale()[0] in windows_locale[HEBREW] else False


def GetLocaleNonUnicode():
    from locale import getdefaultlocale
    return getdefaultlocale()


# GetLocation.exe is self made program using Microsoft Windows API,
# specifically the GetUserGeoID() function;
# Source code is provided.
def GetLocation():
    from subprocess import check_output, CalledProcessError
    try:
        check_output("GetLocation.exe")
        return False
    except CalledProcessError:
        return True


def LocaleSettings():
    if GetFormat():
        logging.info('Locale format is configured correctly!')
    else:
        logging.error(f'Current user is not configured to "Hebrew (Israel)" locale format.')
        logging.info(f'Appends to list of errors...')
        Ops.operations.append("Regional Settings: Format")

    if GetLocation():
        logging.info('Location is configured correctly!')
    else:
        logging.error(f'Current user is not configured to "Israel" home location.')
        logging.info(f'Appends to list of errors...')
        Ops.operations.append("Regional Settings: Location")


def Locale_config():
    import locale
    locale.setlocale()


if __name__ == '__main__':
    pass

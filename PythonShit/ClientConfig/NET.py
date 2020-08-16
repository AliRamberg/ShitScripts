from ctypes import windll

import pywintypes
import win32api
import win32con

versions4 = {'378389': '4.5', '378675': '4.5.1', '379893': '4.5.2',
             '393295': '4.6', '394254': '4.6.1', '394802': '4.6.2',
             '460798': '4.7', '461308': '4.7.1', '461808': '4.7.2',
             '528040': '4.8', '528049': '4.8'}
vers = [378389, 378675, 379893, 393295, 394254, 394802, 460798, 461308, 461808]


def GetCorrectVersion(number):
    low = 0
    high = len(vers) - 1
    while low <= high:
        mid = int((low + high) / 2)
        if number >= vers[high]:
            return high
        elif number <= vers[low]:
            return low
        elif number <= vers[mid]:
            high -= 1
        elif number >= vers[mid + 1]:
            low += 1
        elif vers[mid] <= number < vers[mid + 1]:
            return mid
        else:
            return -1


# return the current Dot Net version
def getDotNetVersion45():
    dot_net_key = r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full"
    try:
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, dot_net_key, 0, win32con.KEY_READ)
        current_version = win32api.RegQueryValueEx(key, 'Release')[0]
        version = versions4[str(vers[GetCorrectVersion(current_version)])]
        windll.user32.MessageBoxW(0, ".NET Framework Version: " + version, ".NET Version", 0)
        return version
    except pywintypes.error as e:
        print("Error " + str(e.winerror) + ": .NET framework v4.5+ is not installed.")
        return 1


def dotNetInstalled35():
    dot_net_key = r'SOFTWARE\Microsoft\NET Framework Setup\NDP\v3.5'
    try:
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, dot_net_key, 0, win32con.KEY_READ)
        win32api.RegQueryValueEx(key, 'Install')
        return True
    except pywintypes.error:
        return False


def net_check():
    import logging
    import Ops
    import regs
    import win32con
    import os
    if not dotNetInstalled35():
        logging.error('Dot Net Framework version 3.5 is not installed')
        logging.info(f"Appends to list of errors...")
        Ops.operations.append(".Net: Install")
    else:
        logging.info('Dot Net Framework version 3.5 is installed!')

    try:
        x64 = True if 'C:\\Program Files (x86)' in os.environ['PROGRAMFILES(X86)'] else False
    except KeyError:
        x64 = False

    # Check .net registry settings
    if x64:
        key = regs.ReadRegKey(win32con.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432NODE\MICROSOFT\.NETFRAMEWORK')
    else:
        key = regs.ReadRegKey(win32con.HKEY_LOCAL_MACHINE, r'SOFTWARE\MICROSOFT\.NETFRAMEWORK')

    try:
        ret = regs.ReadRegValue(key, 'EnableIEHosting')[0]
    except pywintypes.error:
        ret = 0

    if ret != 1:
        logging.warning('EnableIEHosting registry value is not configured or configured to the wrong value')
        Ops.operations.append(".NET: EnableIEHosting is not configured or configured")
        if x64:
            Ops.problems.append(
                Ops.RegistryProblem(win32con.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432NODE\MICROSOFT\.NETFRAMEWORK',
                                    'EnableIEHosting', 1, Ops.RegistryProblem.REG_DWORD))
        else:
            Ops.problems.append(
                Ops.RegistryProblem(win32con.HKEY_LOCAL_MACHINE, r'SOFTWARE\MICROSOFT\.NETFRAMEWORK',
                                    'EnableIEHosting', 1, Ops.RegistryProblem.REG_DWORD))
    else:
        logging.info('EnableIEHosting registry value is configured correctly!')


if __name__ == '__main__':
    pass
    # import Ops
    #
    # net_check()
    # for l in Ops.operations:
    #     l.fix()

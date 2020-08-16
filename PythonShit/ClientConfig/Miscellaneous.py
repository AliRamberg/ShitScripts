# Miscellaneous
import os

from pywintypes import error
from win32con import HKEY_CURRENT_USER as HKCU

import regs


# Adobe Reader. return True is protected mode is disabled at startup else False
def check_adobe():
    protected_key = r'Software\Adobe\Acrobat Reader\DC\Privileged'
    try:
        key = regs.ReadRegKey(HKCU, protected_key)
        ret = regs.ReadRegValue(key, 'bProtectedMode')
    except error:
        return False
    if ret[0] is 0:
        return False
    return True


def check_twaindsm():
    try:
        x64 = True if 'C:\\Program Files (x86)' in os.environ['PROGRAMFILES(X86)'] else False
    except KeyError:
        x64 = False

    if x64:
        pass


# MSCOMCTL ocx file. return True if exists else False
def check_mscomctl():
    try:
        x64 = True if 'C:\\Program Files (x86)' in os.environ['PROGRAMFILES(X86)'] else False
    except KeyError:
        x64 = False

    if x64:
        if os.path.exists(r'C:\Windows\SysWOW64\MSCOMCTL.OCX'):
            return "C:\\Windows\\SysWOW64"
        return None, "C:\\Windows\\SysWOW64"
    else:
        if os.path.exists(r'C:\Windows\System32\MSCOMCTL.OCX'):
            return "C:\\Windows\\System32"
        return None, "C:\\Windows\\System32"


# return the executable version using the win32api library.
def exe_vers(filename):
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except:
        return "Unknown version"


# Find the path location of the etafnit.exe file
def find_exe():
    from win32com.client import GetObject
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    for p in processes:
        if p.Properties_("Name").Value == 'eTafnit.exe':
            return p.Properties_[7].Value
    return 'eTafnit is not running'


# Convert dns to its IP address
def convert_dns(name):
    from socket import gethostbyname
    return gethostbyname(name)


# Convert ip address to its dns
def convert_ip(ip):
    from socket import gethostbyaddr
    return gethostbyaddr(ip)


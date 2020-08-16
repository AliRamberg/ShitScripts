import pywintypes
import win32api
import win32con
import winnt


class Registry:
    HKLM = win32con.HKEY_LOCAL_MACHINE
    HKCU = win32con.HKEY_CURRENT_USER
    ZONE_INTRANET = 1
    ZONE_TRUSTED = 2
    ZONE_INTERNET = 3
    ZONE_RESTRICTED = 4

    def __init__(self, hive, subkey):
        try:
            key = win32api.RegOpenKeyEx(hive, subkey, 0, win32con.KEY_READ | win32con.KEY_WRITE)
        except pywintypes.error:
            key = None
        self.iterator = 0
        self.hive = hive
        self.subkey = subkey
        self.key = key
        try:
            self.subs = win32api.RegEnumKeyEx(self.key)
        except pywintypes.error:
            self.subs = None

    def __str__(self):
        return f'{self.GetHKEY()}\\{self.subkey}'

    def __len__(self):
        pass

    def GetHKEY(self):
        HKEY = self.hive
        if HKEY is win32con.HKEY_CURRENT_USER:
            return f'HKEY_CURRENT_USER'
        if HKEY is win32con.HKEY_LOCAL_MACHINE:
            return f'HKEY_LOCAL_MACHINE'
        if HKEY is win32con.HKEY_USERS:
            return f'HKEY_USERS'
        if HKEY is win32con.HKEY_CLASSES_ROOT:
            return f'HKEY_CLASSES_ROOT'

    def RegClose(self):
        if self.key:
            win32api.RegCloseKey(self.key)
        else:
            return None


def RegCreateKey(hive, subkey):
    handle, flag = win32api.RegCreateKeyEx(hive, subkey, win32con.KEY_READ | win32con.KEY_WRITE, None,
                                           winnt.REG_OPTION_NON_VOLATILE, None, None)
    if flag:
        return handle, flag
    else:
        return None


def RegGetValue(handle, valueName):
    try:
        return win32api.RegQueryValueEx(handle, valueName)
    except pywintypes.error:
        return -1, None


def RegSetValue(handle, valueName, value, typeName):
    return win32api.RegSetValueEx(handle, valueName, 0, typeName, value)


def RegDeleteValue(handle, valueName):
    try:
        return win32api.RegDeleteValue(handle, valueName)
    except pywintypes.error as e:
        if e.winerror != 2:
            raise


def AddIntranetSite(ipaddr):
    hive = Registry.HKCU
    subkey = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
    try:
        handle, flag = RegCreateKey(hive, f'{subkey}\\{ipaddr}')
        RegSetValue(handle, ':Range', ipaddr, win32con.REG_SZ)
        RegSetValue(handle, '*', Registry.ZONE_INTRANET, win32con.REG_DWORD)
        RegDeleteValue(handle, 'http')
        RegDeleteValue(handle, 'https')
        return True
    except pywintypes.error as e:
        raise e


def SetZones(ipaddr):
    # Find all occurrences of 'ipaddr' and set them to the required 'zone'
    found = False
    subkey = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
    ranges = Registry(Registry.HKCU, subkey)
    for i, (name, _, _, _) in enumerate(ranges.subs):
        ip = Registry(Registry.HKCU, f'{subkey}\\{name}')
        value, _ = RegGetValue(ip.key, ':Range')
        zone1, _ = RegGetValue(ip.key, '*')
        zone2, _ = RegGetValue(ip.key, 'http')
        zone3, _ = RegGetValue(ip.key, 'https')
        if value == ipaddr and (zone1 > Registry.ZONE_INTRANET or int(zone2) > Registry.ZONE_INTRANET or int(
                zone3) > Registry.ZONE_INTRANET):
            found = True
            RegSetValue(ip.key, '*', Registry.ZONE_INTRANET, win32con.REG_DWORD)
            RegDeleteValue(ip.key, 'http')
            RegDeleteValue(ip.key, 'https')
        ip.RegClose()
    ranges.RegClose()
    if not found:
        AddIntranetSite(ipaddr)
    return True


def main():
    ip = '1.2.3.4'
    SetZones(ip)


if __name__ == "__main__":
    main()

import pywintypes
import win32api
import win32con
import Registry
import winnt

REG_DWORD = win32con.REG_DWORD
REG_SZ = win32con.REG_SZ


def ReadRegKey(hive, key):
    try:
        return win32api.RegOpenKeyEx(hive, key)
    except pywintypes.error:
        pass


def ReadRegValue(key, value):
    return win32api.RegQueryValueEx(key, value)


def CloseRegKey(key):
    return win32api.RegCloseKey(key)


def ReadRegValues(key):
    lst = []
    i = 0
    try:
        while win32api.RegEnumValue(key, i) is not None:
            lst += win32api.RegEnumValue(key, i)
            i += 1
    except pywintypes.error:
        pass
    return lst


def SetRegValue(hive, key, value_name, value, reg_type):
    """
    Ables to create a new or modify an already existing registry entry to the required value
    more details http://timgolden.me.uk/pywin32-docs/win32api__RegSetValueEx_meth.html
    and https://docs.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regsetvalueexa
    :param hive: any of the win32con constants; HKLM requires UAC elevated process
    :param key: subkey of the given hive
    :param value_name: the actual entry to set
    :param value: The value to set on the given entry
    :param reg_type: REG_SZ or REG_DWORD
    :return: True on success, False otherwise
    """
    reg = Registry.Registry(hive, key)
    try:
        Registry.RegSetValue(reg.key, value_name, value, reg_type)
    except pywintypes.error:
        pass
    reg.RegClose()
    return
    # try:
    #     PyHANDLE = win32api.RegOpenKeyEx(hive, key, 0, win32con.KEY_SET_VALUE | win32con.KEY_READ)
    # except pywintypes.error:
    #     key = win32api.RegCreateKeyEx(hive, key, win32con.KEY_WRITE | win32con.KEY_READ, None, 0, None, None)
    #     PyHANDLE = win32api.RegOpenKeyEx(hive, key, 0, win32con.KEY_WRITE | win32con.KEY_READ)
    # try:
    #     win32api.RegSetValueEx(PyHANDLE, value_name, 0, reg_type, value)
    # except:
    #     return False


def GetHiveName(hive):
    from win32con import HKEY_LOCAL_MACHINE as HKLM
    from win32con import HKEY_CURRENT_USER as HKCU
    if hive == HKLM:
        return 'HKLM'
    if hive == HKCU:
        return 'HKCU'
    else:
        return None


if __name__ == '__main__':
    pass

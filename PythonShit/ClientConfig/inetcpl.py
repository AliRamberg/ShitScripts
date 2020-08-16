import logging
import os

import pywintypes
from win32con import HKEY_CURRENT_USER as HKCU
from win32con import HKEY_LOCAL_MACHINE as HKLM
from win32con import REG_DWORD

import Miscellaneous
import Ops
import regs
from INET_CON import advanced_tab
from INET_CON import zones
from Logging import start_title


# based on the microsoft support article,
# https://support.microsoft.com/en-us/help/182569/internet-explorer-security-zones-registry-entries-for-advanced-users
def check_inet():
    r"""
    Internet Options settings are configured in four different keys in the Windows registry.
    The settings are set based on hierarchy thoroughly explained in this article:
    https://blogs.technet.microsoft.come/fdcc/2011/09/22/internet-explorers-explicit-security-zone-mappings/

    This function scans each value that can be set in the Custom Settings of the !Intranet! Zone in both
    the group policy locations, user's and computer's and also the local computer or user locations.

    Internet Options Zone Settings locations:
    The '1' marks the 'Intranet Zone'.
    User's Group Policy - HKCU\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1
    Computer's Group Policy - HKLM\Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1
    Current User Internet Options - HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1
    Computer's centralized Internet Options -  HKLM\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1


    :param hive: The registry hive to perform the checks. can be HKLM or HKCU.
    :return nothing. prints results to log file:
    """

    if only_HKLM():
        logging.info('\'Security_HKLM_only\' is set')
        key = r'Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings'
        hive = HKLM
        try:
            gpo_key = regs.ReadRegKey(HKLM, key)
        except pywintypes.error:
            gpo_key = None
        flag = False  # if errors were found
        for k, v in zones.items():
            try:
                gpo_ret = regs.ReadRegValue(gpo_key, str(k))[0]
            except pywintypes.error:
                gpo_ret = -1

            if gpo_ret != v[1]:
                flag = True
                logging.warning(f'{v[0]} is configured incorrectly!')
                logging.warning(f'\tIt\'s configured to {gpo_ret} should be {v[1]}')
                Ops.operations.append(f'Internet Options: {v[0]}')
                Ops.problems.append(Ops.RegistryProblem(hive=hive, key=key, value_name=k, value=v[1], reg_t=REG_DWORD))

        #  Advanced key
        advanced_key = regs.ReadRegKey(hive, r'Software\Microsoft\Internet Explorer\Main')
        for value, data in advanced_tab.items():
            try:
                local_ret = regs.ReadRegValue(advanced_key, value)[0]
                if str(local_ret) != data:
                    flag = True
                    logging.warning(f'{value} is configured incorrectly!')
                    logging.warning(f'\tIt\'s configured to {local_ret} should be {data}')
                    Ops.operations.append(f'Advanced Options: {value}')
                    # Ops.problems.append(
                    #     Ops.RegistryProblem(hive=hive, key=r'Software\Microsoft\Internet Explorer\Main', value=data,
                    #                         reg_t=REG_DWORD))
            except pywintypes.error:
                pass

    else:
        # Inetcpl options are applied from HKLM and HKCU together
        logging.info('Security_HKLM_only is not set')
        key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1'
        gpo_key = r'Software\Policies\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1'
        # Security Tab
        try:
            user_key = regs.ReadRegKey(HKCU, key)
        except pywintypes.error:
            user_key = None
        try:
            comp_key = regs.ReadRegKey(HKLM, key)
        except pywintypes.error:
            comp_key = None
        try:
            user_gpo = regs.ReadRegKey(HKCU, gpo_key)
        except pywintypes.error:
            user_gpo = None
        try:
            comp_gpo = regs.ReadRegKey(HKLM, gpo_key)
        except pywintypes.error:
            comp_gpo = None

        flag = False  # if errors were found
        for k, v in zones.items():
            try:
                comp_ret = regs.ReadRegValue(comp_key, str(k))[0]
            except pywintypes.error:
                comp_ret = -1
            try:
                user_ret = regs.ReadRegValue(user_key, str(k))[0]
            except pywintypes.error:
                user_ret = -1
            try:
                user_gpo_ret = regs.ReadRegValue(user_gpo, str(k))[0]
            except pywintypes.error:
                user_gpo_ret = -1
            try:
                comp_gpo_ret = regs.ReadRegValue(comp_gpo, str(k))[0]
            except pywintypes.error:
                comp_gpo_ret = -1

            if comp_gpo_ret != -1:
                ret = comp_gpo_ret
                hive = HKLM
                key = gpo_key
            elif user_gpo_ret != -1:
                ret = user_gpo_ret
                hive = HKCU
                key = gpo_key
            elif user_ret != -1:
                ret = user_ret
                hive = HKCU
            else:
                ret = comp_ret
                hive = HKLM

            if ret != v[1]:
                flag = True
                logging.warning(f'{v[0]} is configured incorrectly!')
                logging.warning(f'\tIt\'s configured to {ret} should be {v[1]}')

                #  No reason to add to Ops.problems because the gpo settings shall reapply
                if comp_gpo_ret != -1 or user_gpo_ret != -1:
                    logging.warning(f'{v[0]} is configured through a gpo rule')
                else:
                    # Ops.problems.append(
                    #     Ops.RegistryProblem(hive=HKCU, key=gpo_key, value_name=k, value=v[1], reg_t=REG_DWORD))
                    Ops.problems.append(
                        Ops.RegistryProblem(hive=HKCU, key=key, value_name=k, value=v[1], reg_t=REG_DWORD))
                Ops.operations.append(f'Internet Options: {v[0]}')

        # Advanced Tab
        advanced_key = regs.ReadRegKey(HKCU, r'Software\Microsoft\Internet Explorer\Main')
        for value, data in advanced_tab.items():
            try:
                local_ret = regs.ReadRegValue(advanced_key, value)[0]
                if str(local_ret) != data:
                    flag = True
                    logging.warning(f'{value} is configured incorrectly!')
                    logging.warning(f'\tIt\'s configured to {local_ret} should be {data}')
                    Ops.operations.append(f'Advanced Options: {value}')
                    # Ops.problems.append(
                    # Ops.RegistryProblem(hive=HKCU, key=r'Software\Microsoft\Internet Explorer\Main', value=data,
                    # reg_t=REG_DWORD))
            except pywintypes.error:
                pass

    if flag:
        logging.error('Internet options are not configured correctly!')
        logging.debug('')


# check if inet settings are computer centralized or per user
def only_HKLM():
    only_HKLM = 'Security_HKLM_only'
    if 'AMD64' in os.environ['PROCESSOR_ARCHITECTURE']:
        key = regs.ReadRegKey(HKLM,
                              r'SOFTWARE\WOW6432Node\Policies\Microsoft\Windows\CurrentVersion\Internet Settings')
        try:
            val = regs.ReadRegValue(key, only_HKLM)
        except pywintypes.error:
            val = None
        return val is not None and val[0] is 1
    else:
        key = regs.ReadRegKey(HKLM, r'SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\Internet Settings')
        try:
            val = regs.ReadRegValue(key, only_HKLM)
        except pywintypes.error:
            val = None
        return val is not None and val[0] is 1


# Zones Settings
def check_zones(name):
    if name is None or name == '':
        logging.info('No domain or IP address was checked')
        return
    if not name[0].isdigit():
        name = Miscellaneous.convert_dns(name)
    try:
        import win32api
        import win32timezone
        from win32con import HKEY_CURRENT_USER as HKCU
    except ModuleNotFoundError:
        return
    main_key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
    key = regs.ReadRegKey(HKCU, main_key)
    for address in range(len(win32api.RegEnumKeyEx(key))):
        subkey_name = win32api.RegEnumKey(key, address)
        subkey = regs.ReadRegKey(HKCU, f'{main_key}\\{subkey_name}')
        try:
            value = regs.ReadRegValue(subkey, ':Range')[0]
            if value == name:
                # if the required site is found
                #  searches for zone
                try:
                    http = regs.ReadRegValue(subkey, 'http')[0]
                except pywintypes.error:
                    http = 0  # Not found
                try:
                    https = regs.ReadRegValue(subkey, 'https')[0]
                except pywintypes.error:
                    https = 0  # Not found
                try:
                    either = regs.ReadRegValue(subkey, '*')[0]
                except pywintypes.error:
                    either = 0  # Not found

                if http is 1 or https is 1 or either is 1:
                    if http + https + either > 3:
                        logging.warning(f'{name} is set on both intranet and another zone')
                        Ops.operations.append(f'Internet Options: Add {name} to trusted sites')
                        return False
                    else:
                        logging.info(f'{name} is already in intranet zone')
                        return True
                else:
                    logging.warning(f'{name} is set in the wrong zone')
                    Ops.operations.append(f'Internet Options: Add {name} to trusted sites')
                    return False
        except pywintypes.error:
            value = None
    logging.debug('')
    logging.warning(f'{name} is not set in intranet zone or other zones')
    Ops.operations.append(f'Internet Options: Add {name} to trusted sites')
    return False


def check_ActiveX():
    """
    Checks each ActiveX that was made in Matrix resides in ActiveX directory.
    :return: current status and logs every files that failed to find
    """
    # return status
    status = False

    # Default ActiveX directory
    path = r'C:\Windows\Downloaded Program Files'

    # eTafnitTreeview
    if not os.path.exists(f'{path}\\eTafnitTreeview.inf'):
        logging.error('eTafnitTreeview.inf is missing, ActiveX might fail to load')
        status = True
    if not os.path.exists(f'{path}\\eTafnitTreeview.ocx'):
        logging.error('eTafnitTreeview.ocx is missing, ActiveX will fail to load')
        Ops.problems.append(Ops.OcxProblem("eTafnitTreeview.ocx"))
        status = True

    # httpImageList
    if not os.path.exists(f'{path}\\httpImageList.inf'):
        logging.error('httpImageList.inf is missing, ActiveX might fail to load')
        status = True
    if not os.path.exists(f'{path}\\httpImageList.ocx'):
        logging.error('httpImageList.ocx is missing, ActiveX will fail to load')
        Ops.problems.append(Ops.OcxProblem("httpImageList.ocx"))
        status = True

    # MatrixMapArea
    if not os.path.exists(f'{path}\\MatrixMapArea.inf'):
        logging.error('MatrixMapArea.inf is missing, ActiveX might fail to load')
        status = True
    if not os.path.exists(f'{path}\\MatrixMapArea.ocx'):
        logging.error('MatrixMapArea.ocx is missing, ActiveX will fail to load')
        Ops.problems.append(Ops.OcxProblem("MatrixMapArea.ocx"))
        status = True

    # WorkFlow
    if not os.path.exists(f'{path}\\WorkFlow.inf'):
        logging.error('WorkFlow.inf is missing, ActiveX might fail to load')
        status = True
    if not os.path.exists(f'{path}\\WorkFlow.ocx'):
        logging.error('WorkFlow.ocx is missing, ActiveX will fail to load')
        Ops.problems.append(Ops.OcxProblem("WorkFlow.ocx"))
        status = True

    # MatrixSignAndVerify - not mandatory

    # if not os.path.exists(f'{path}\\MatrixSignAndVerify.inf'):
    #     logging.error('MatrixSignAndVerify.inf is missing, ActiveX might fail to load')
    #     status = True
    # if not os.path.exists(f'{path}\\MatrixSignAndVerify.ocx'):
    #     logging.error('MatrixSignAndVerify.ocx is missing, ActiveX will fail to load')
    #     Ops.problems.append(Ops.OcxProblem("MatrixSignAndVerify.ocx"))
    #     status = True
    return status


def main():
    check_inet()

    name = input("Enter the Tafnit server address (optional): ")
    start_title('Zones')
    if not check_zones(name):
        main_key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
        zones = Ops.RegistryProblem(hive=HKCU, key=f'{main_key}\\{name}', value_name=name, value=1,
                                    reg_t=Ops.RegistryProblem.REG_SZ)
        zones.type = Ops.Problem.TYPE_ZONE
        Ops.problems.append(zones)

    start_title('ActiveX')
    if check_ActiveX():
        logging.error('Failed to locate all the required ActiveX files')
        Ops.operations.append('ActiveX Plug-In: Failed to load all plug-ins (check detailed log)')

    else:
        logging.info('All ActiveX plug-ins are installed correctly')
    return


def IntranetOnly(site):
    """
    checks if requested site is configured only on the intranet sites tab
    and is not configured on any other tab like trusted sites.
    :return: True if site is only on the intranet or it is not in the inet at all,
    False otherwise
    """
    pass


if __name__ == '__main__':
    name = '1.2.3.4'
    if not check_zones(name):
        main_key = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Ranges'
        Ops.problems.append(Ops.RegistryProblem(hive=HKCU, key=f'{main_key}\\{name}', value_name=name, value=1,
                                                reg_t=Ops.RegistryProblem.REG_SZ))
        for p, _ in Ops.problems:
            print(p)
    # IntranetOnly(site)

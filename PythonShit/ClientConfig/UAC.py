import logging

import win32con

import Ops
import regs


def uac_check():
    check = True
    sys_key = regs.ReadRegKey(win32con.HKEY_LOCAL_MACHINE,
                              r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System')
    EnableLUA = regs.ReadRegValue(sys_key, 'EnableLUA')[0]
    EnableInstallerDetection = regs.ReadRegValue(sys_key, "EnableInstallerDetection")[0]
    if EnableLUA is not 1:
        logging.warning(f'EnableLUA is enabled with value: {EnableLUA}')
        logging.info(f'Appends to list of errors...')
        Ops.operations.append("Registry: EnableLUA")
        Ops.problems.append(Ops.RegistryProblem(win32con.HKEY_LOCAL_MACHINE,
                                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',
                                                'EnableLUA', 1, Ops.RegistryProblem.REG_DWORD))
        check = False

    if EnableInstallerDetection is not 0:
        logging.warning(f"\'EnableInstallerDetectionis\' value is enabled with value: {EnableInstallerDetection}")
        Ops.problems.append(Ops.RegistryProblem(win32con.HKEY_LOCAL_MACHINE,
                                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',
                                                'EnableInstallerDetection', 0, Ops.RegistryProblem.REG_DWORD))
        check = False

    # returns the current status of UAC settings
    if check:
        logging.info('UAC is disabled!')
    return check


import ctypes
import logging
import subprocess as sb
from os import path

import Admin
import Locale
import Logging
import Miscellaneous
import NET
import Ops
import UAC
import inetcpl


def Checker():
    #####################################################################
    # Check UAC Status
    Logging.start_title("UAC Status")
    UAC.uac_check()

    #####################################################################
    # Check Language and regional Settings
    Logging.log_section("Language and Regional Settings")
    Locale.LocaleSettings()

    #####################################################################
    # Check version of .NET Framework 3.5
    Logging.log_section(".NET Framework Status and Installation")
    NET.net_check()

    #####################################################################
    # Check firewall state and settings
    Logging.start_title('Firewall Settings')
    ret = sb.check_output(['netsh', 'advfirewall', 'show', 'domainprofile', 'state'])
    if 'Ok.' in str(ret):
        logging.warning('Firewall state is up. May need to allow TCP 80')
    else:
        logging.info('Firewall state is down.')

    #####################################################################
    # Is user a local admin
    Logging.start_title('Check Lock Admin Privileges')
    Admin.checkAdmin()

    #####################################################################
    # Internet Options
    Logging.log_section('Internet Options')
    inetcpl.main()

    #####################################################################
    # Miscellaneous
    Logging.start_title('Miscellaneous')
    if Miscellaneous.check_adobe():
        from win32con import HKEY_CURRENT_USER as HKCU
        from win32con import REG_DWORD
        logging.warning('Adobe Reader protected mode is enabled.')
        Ops.operations.append('Miscellaneous: Adobe Reader protected mode')
        adobe = Ops.RegistryProblem(HKCU, r'Software\Adobe\Acrobat Reader\DC\Privileged', 'bProtectedMode', 0,
                                    REG_DWORD)
        Ops.problems.append(adobe)
    else:
        logging.info('Adobe Reader protected mode is disabled.')

    mscom = Miscellaneous.check_mscomctl()
    if not mscom[0]:
        logging.warning('Could not find the MSCOMCTL.OCX file on the system.')
        Ops.operations.append('Miscellaneous: MSCOMCTL.OCX file')
        comctl = Ops.FileProblem('MSCOMCTL.ocx')
        comctl.type = Ops.Problem.TYPE_MSCOMCTL
        comctl.dst = mscom[1]
        Ops.problems.append(comctl)
    else:
        logging.info('The MSCOMCTL.OCX file is found on the system.')

    # Final Results
    return Logging.end_log()


def Fixer():
    import subprocess as sp
    for p in Ops.problems:
        if p.type == Ops.Problem.TYPE_ZONE:
            p.zoneFix()
        else:
            p.fix()
    sp.run(["msiexec.exe", "/a", "TrustDotNetApplet.msi", "/quiet"], stdout=sp.DEVNULL, stderr=sp.STDOUT, shell=True)


# Checks if the script is running with administrative privileges.
# Returns True if is running as admin, False otherwise.
def is_running_as_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except ctypes.get_last_error():
        return False


def main():
    import win32con
    from webbrowser import open

    # Initialize Client Logging
    Logging.init()

    if Checker():
        Logging.error_file()

        # if path.exists(r'Logs\TafnitClientLog.log'):
        #     open(r'Logs\TafnitClientLog.log')
        if path.exists(r'Logs\TafnitErrors.log'):
            open(r'Logs\TafnitErrors.log')

        box = ctypes.windll.user32.MessageBoxW(0, "Configure the PC?", "Client Config",
                                               win32con.MB_YESNO)
        if box is win32con.IDNO:
            return
        elif box is win32con.IDYES and is_running_as_admin():
            Fixer()

        else:
            ctypes.windll.user32.MessageBoxW(0, "The fixer must be run as administrator. Existing", "Client Config", 0)
    return


if __name__ == '__main__':
    main()

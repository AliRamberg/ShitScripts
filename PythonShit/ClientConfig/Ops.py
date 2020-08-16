import os

import regs

operations = []
problems = []


class Problem:
    # TYPES
    TYPE_REG = 0
    TYPE_FILE = 1
    TYPE_INSTALL = 2
    TYPE_OCX = 3
    TYPE_ZONE = 4
    TYPE_MSCOMCTL = 5

    prob_num = 0  # number of problems found that are readily fixed

    def gettype(self):
        return self.type

    def __init__(self):
        self.prob_num += 1
        self.type = None

    def __str__(self):
        return f"There are currently {self.prob_num} fixes ready for your system"


class RegistryProblem(Problem):
    REG_DWORD = regs.REG_DWORD
    REG_SZ = regs.REG_SZ

    def __init__(self, hive, key, value_name, value, reg_t):
        Problem.__init__(self)
        self.type = self.TYPE_REG
        self.hive = hive
        self.key = key
        self.value_name = value_name
        self.value = value
        self.reg_t = reg_t

    def fix(self):
        regs.SetRegValue(self.hive, self.key, self.value_name, self.value, self.reg_t)

    def zoneFix(self):
        from Registry import SetZones
        SetZones(self.value_name)


class FileProblem(Problem):
    def __init__(self, file):
        Problem.__init__(self)
        self.type = self.TYPE_FILE
        self.file = file
        self.dst = None

    def __str__(self):
        return f'{self.file} was not found'

    def fix(self, dst=''):
        import subprocess as sp
        if self.type == Problem.TYPE_MSCOMCTL:
            dst = self.dst
        sp.run(['copy', f"{os.getcwd()}\\ocx\\{self.file}", f"{dst}\\{self.file}"], stdout=sp.DEVNULL, stderr=sp.STDOUT,
               shell=True)
        sp.run(["regsvr32", "/s", f"{dst}\\{self.file}"], shell=True)


class OcxProblem(FileProblem):
    def __init__(self, file):
        FileProblem.__init__(self, file)
        self.type = self.TYPE_OCX

    def fix(self, a=''):
        import subprocess as sp
        dst = r'C:\Windows\Downloaded Program Files'
        sp.run(['copy', f"{os.getcwd()}\\ocx\\{self.file}", f"{dst}"], stdout=sp.DEVNULL, stderr=sp.STDOUT, shell=True)
        sp.run(["regsvr32", "/s", f"{dst}\\{self.file}"], shell=True)


class InstallProblem(Problem):
    def __init__(self, value):
        Problem.__init__(self)
        self.type = self.TYPE_INSTALL
        self.value = value

    def fix(self):
        pass

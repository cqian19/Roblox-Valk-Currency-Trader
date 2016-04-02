#coding=utf-8

from cx_Freeze import setup, Executable
import requests
import os 
import sys

includes = ['atexit', 'lxml.etree','lxml._elementpath']
include_files = ['config.ini', (requests.certs.where(),'cacert.pem'), 'C:\Windows\System32\msvcp100.dll', 'valkTCBot/rbxAPI', 'valkTCBot/guifiles']
packages = ['easydict', 'cProfile', 'sys', 'inspect', 'os', 'requests', 'requests_futures', 'lxml', 'PySide.QtGui', 'PySide.QtCore']
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Valk TC Bot",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]ValkTCBot.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
]

msi_data = dict(
    Shortcut=shortcut_table,
)

bdist_msi_options = dict(
    add_to_path=True,
    initial_target_dir='C:\ValkTCBot',
    data=msi_data
)


buildOptions = dict(
    include_files=include_files,
    packages=packages,
    includes=includes,
    include_msvcr=True,
)


executables = [
    Executable(
        script='valktcbot/main.py',
        targetName='ValkTCBot.exe',
        copyDependentFiles=True,
        appendScriptToLibrary = True,
        appendScriptToExe = True,
        base='Win32GUI' if sys.platform=='win32' else None,
        icon='valktcbot/images/bot_desktop_icon.ico',
    )
]

setup(
    name="Valk TC Bot",
    version="2.5.0",
    description="Trade Currency Bot",
    options=dict(build_exe=buildOptions,bdist_msi=bdist_msi_options),
    executables=executables
)
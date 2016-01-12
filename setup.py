#coding=utf-8

from cx_Freeze import setup, Executable
import requests
import os 
import sys

includes = ['atexit', 'lxml.etree','lxml._elementpath']
include_files = ['images/', 'guifiles/', 'config.ini', (requests.certs.where(),'cacert.pem'), 'C:\Windows\System32\msvcp100.dll']
packages = ['sys', 'inspect', 'os', 'requests', 'PySide.QtGui', 'PySide.QtCore']

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
    append_script_to_exe=True,
    include_msvcr=True,
)


executables = [
    Executable(
        script='main.py',
        targetName='ValkTCBot.exe',
        base='Win32GUI', #if sys.platform=='win32' else None, # THIS ONE IS IMPORTANT FOR GUI APPLICATION
        icon='images/bot_desktop_icon.ico',
    )
]

setup(
    name="Valk TC Bot",
    version="2.0",
    description="Trade Currency Bot",
    options=dict(build_exe=buildOptions,bdist_msi=bdist_msi_options),
    executables=executables
)
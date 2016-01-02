#coding=utf-8

from cx_Freeze import setup, Executable
import requests
import os 

includes = ['lxml.etree','lxml._elementpath']
include_files = ['images/', 'guifiles/', 'config.ini', (requests.certs.where(),'cacert.pem')]
packages = ['inspect', 'os', 'requests', 'PySide.QtCore', 'PySide.QtGui', 'RbxAPI', ]


buildOptions = dict(
    include_files=include_files,
    packages=packages,
    includes=includes
)

executables = [
    Executable(
        script='main.py',
        targetName='ValkTCBot.exe',
        base="Win32GUI", # THIS ONE IS IMPORTANT FOR GUI APPLICATION
        icon='images/bot_icon.ico',
        shortcutName= "Valk TC Bot",
        shortcutDir="DesktopFolder",
    )
]

setup(
    name="Valk TC Bot",
    version="1.0",
    description="A trade currency bot for Roblox.",
    options=dict(build_exe=buildOptions),
    executables=executables
)
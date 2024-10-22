# -*- mode: python ; coding: utf-8 -*-

import os
import sys

sys.path.insert(0, 'src')

from VersionHelper import get_version, version_to_str

def make_version_info(major:int, minor:int, patch:int, rev:int):
	content = ''
	
	content += '# UTF-8\n'
	content += '#\n'
	content += 'VSVersionInfo(\n'
	content += '  ffi=FixedFileInfo(\n'
	content += f'    filevers=({major}, {minor}, {patch}, {rev}),\n'
	content += f'    prodvers=({major}, {minor}, {patch}, {rev}),\n'
	content += '    mask=0x3f,\n'
	content += '    flags=0x0,\n'
	content += '    OS=0x40004,\n'
	content += '    fileType=0x1,\n'
	content += '    subtype=0x0,\n'
	content += '    date=(0, 0)\n'
	content += '  ),\n'
	content += '  kids=[\n'
	content += '    StringFileInfo([\n'
	content += '      StringTable(\'040904B0\', [\n'
	content += '          StringStruct(\'CompanyName\', \'frechdev\'),\n'
	content += '          StringStruct(\'FileDescription\', \'Tool zur Erzeugung eines Bauplans.\'),\n'
	content += f'          StringStruct(\'FileVersion\', \'{version_to_str(major, minor, patch, rev)}\'),\n'
	content += '          StringStruct(\'InternalName\', \'CSV Floor Sketcher\'),\n'
	content += '          StringStruct(\'LegalCopyright\', \'Copyright 2024, Leo Kernstock\'),\n'
	content += '          StringStruct(\'OriginalFilename\', \'CSV Floor Sketcher.exe\'),\n'
	content += '          StringStruct(\'ProductName\', \'CSV Floor Sketcher\'),\n'
	content += f'          StringStruct(\'ProductVersion\', \'{version_to_str(major, minor, patch, rev)}\'),\n'
	content += '        ])\n'
	content += '    ]),\n'
	content += '    VarFileInfo([VarStruct(\'Translation\', [1033, 1200])])\n'
	content += '  ]\n'
	content += ')'
		
	with open('build\\version-info.txt', 'w') as f:
		f.write(content)

block_cipher = None

a = Analysis(
    ['src\\CSVFloorSketcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

maj, min, patch, rev = get_version()
make_version_info(maj, min, patch, rev)
version_str=version_to_str(maj, min, patch, rev)

exe = EXE(
    pyz,
    a.scripts,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name=f'CSVFloorSketcher_v{version_str}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    #icon='mein_icon.ico',
    version='build\\version-info.txt',  # Hier die Version-Datei angeben
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=f'CSVFloorSketcher_v{version_str}'
)
#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

block_cipher = None

import sys
sys.modules['FixTk'] = None

# Add packages from virtualenv
import distutils.sysconfig
venv_site_packages = distutils.sysconfig.get_python_lib()

# Datas from site-packages
def pkg_data(data):
    import os
    return os.path.join(venv_site_packages, os.path.normpath(data))

# All package modules
def get_all_modules(module_name):
    import pkgutil
    import importlib
    package = importlib.import_module(module_name)
    all = [module_name]
    for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,prefix=package.__name__+'.',onerror=lambda x: None):
        all.append(modname)
    return all

a = Analysis(
    ['ariva'],
    pathex=[
        venv_site_packages
    ],
    binaries=[],
    datas=[
        ( pkg_data('scrapy/VERSION'), '.' ),
        ( pkg_data('scrapy/mime.types'), '.' ),
    ],
    hiddenimports=[
        'six',
        'scrariva',
        'scrariva.items',
        'scrariva.middlewares',
        'scrariva.pipelines',
        'scrariva.settings',
        'scrariva.spiders',
        'scrariva.spiders.ariva',
    ] + get_all_modules('scrapy'),
    hookspath=[],
    runtime_hooks=[],
    excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    )
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='ariva',
    debug=False,
    strip=False,
    console=True,
    )
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    name='ariva',
    )



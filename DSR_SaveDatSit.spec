# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DSR_SaveDatSit.py'],
    pathex=[],
    binaries=[],
    datas=[('src/bg.png', 'src'), ('src/zkrvf.png', 'src'), ('src/icon.ico', 'src')],
    hiddenimports=['plyer.platforms.win.notification'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DSR_SaveDatSit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/icon.ico'],
)

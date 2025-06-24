# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['star_cvc.py'],
    pathex=[],
    binaries=[],
    datas=[('resources/icon/star.jpg', 'resources/icon'), ('resources/star/wrong_sound.mp3', 'resources/star'), ('resources/star/hooray_sound.mp3', 'resources/star'), ('resources/star/families', 'resources/star/families')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='StarCVC',
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
)

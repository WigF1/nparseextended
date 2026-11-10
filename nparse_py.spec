# -*- mode: python -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_all
# piper.train is the model-training code; it needs torch and is never used at runtime
p_datas, p_bins, p_hidden = collect_all(
    'piper', filter_submodules=lambda name: not name.startswith('piper.train'))

a = Analysis(
    ['nparseextended.py'],
    pathex=[],
    binaries=p_bins,
    datas=p_datas,
    hiddenimports=p_hidden,
    hookspath=[],
    hooksconfig={},
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

from glob import glob
a.datas += [(filename, filename, 'DATA') for filename in glob('data/fonts/*')]
a.datas += [('data/ui/_.css', 'data/ui/_.css', 'DATA')]
a.datas += [('data/ui/icon.png', 'data/ui/icon.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 388),
    text_size=13,
    text_color='#dae814',
    minify_script=True,
    always_on_top=False,
    max_img_size=(800, 400),
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    name='nparse-extended',
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
    icon='data/ui/icon.ico'
)

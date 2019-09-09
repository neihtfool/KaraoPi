# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/quangthien.nguyen/prjcts/KaraokePi/src/main/python/main.py'],
             pathex=['/Users/quangthien.nguyen/prjcts/KaraokePi/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Users/quangthien.nguyen/.local/share/virtualenvs/KaraokePi-LNiXYp-y/lib/python3.7/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/var/folders/39/y8ms98zn7b160f0186pc8k840000gp/T/tmppb6uyr8i/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='KaraoPi',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/quangthien.nguyen/prjcts/KaraokePi/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='KaraoPi')
app = BUNDLE(coll,
             name='KaraoPi.app',
             icon='/Users/quangthien.nguyen/prjcts/KaraokePi/target/Icon.icns',
             bundle_identifier=None)

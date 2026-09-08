from PyInstaller.utils.hooks import collect_data_files


datas = []

datas += collect_data_files("kivy")

datas += [
    ("app/ui/main.kv", "app/ui"),
    ("app/ui/theme.kv", "app/ui"),
]


a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "kivy",
        "kivy.core.window.window_sdl2",
        "kivy.core.text.text_sdl2",
        "kivy.core.image.img_sdl2",
        "kivy.core.audio.audio_sdl2",
        "app.services.drywall_service",
        "app.services.translation_service",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "kivy.tests",
    ],
    noarchive=False,
)


pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="drywall-calculator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

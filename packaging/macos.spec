# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller packaging/macos.spec  (rodar em macOS, Apple Silicon)
#
# onedir + BUNDLE gera um .app tradicional (nao onefile), pelos mesmos motivos
# de reducao de falso-positivo de antivirus descritos em windows.spec.
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "app" / "static"
ICON_PATH = ROOT / "packaging" / "icon.icns"

a = Analysis(
    [str(ROOT / "desktop_app.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(STATIC_DIR), "app/static"),
    ],
    hiddenimports=[
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ConversorDBC",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ConversorDBC",
)

app = BUNDLE(
    coll,
    name="ConversorDBC.app",
    icon=str(ICON_PATH) if ICON_PATH.exists() else None,
    bundle_identifier="br.com.elivansilva.conversordbc",
    info_plist={
        "CFBundleName": "Conversor DBC",
        "CFBundleDisplayName": "Conversor DBC (Datasus) para Excel",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
    },
)

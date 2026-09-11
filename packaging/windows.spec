# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller packaging/windows.spec  (rodar em Windows)
#
# Decisoes deliberadas para reduzir falso-positivo de antivirus:
# - onedir (nao onefile): onefile se autoextrai para uma pasta temp a cada
#   execucao, padrao classico de "dropper" que dispara heuristicas de AV.
# - upx=False: compressao UPX e outro gatilho heuristico comum.
# - console=False: nao abre janela de terminal (app grafico).
from pathlib import Path

ROOT = Path(SPECPATH).resolve().parent
STATIC_DIR = ROOT / "app" / "static"
ICON_PATH = ROOT / "packaging" / "icon.ico"
VERSION_FILE = ROOT / "packaging" / "version_info.txt"

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
    icon=str(ICON_PATH) if ICON_PATH.exists() else None,
    version=str(VERSION_FILE) if VERSION_FILE.exists() else None,
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

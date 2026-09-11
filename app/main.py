from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import io
import tempfile
from datetime import datetime

from .converter import convert_dbc_to_excel, ConversaoError


app = FastAPI(title="DBC to Excel Converter", version="1.0.0")


@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    filename = file.filename or "arquivo.dbc"
    if not filename.lower().endswith(".dbc"):
        raise HTTPException(status_code=400, detail="Anexe um arquivo com extensao .dbc")

    # Usa arquivo temporario para suportar uploads grandes
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dbc") as tmp_in:
            while True:
                chunk = await file.read(1024 * 1024)  # 1MB
                if not chunk:
                    break
                tmp_in.write(chunk)
            tmp_in_path = tmp_in.name

        # Gera Excel em memoria
        output_stream = io.BytesIO()
        convert_dbc_to_excel(tmp_in_path, output_stream)
        output_stream.seek(0)

        out_name = os.path.splitext(os.path.basename(filename))[0]
        out_name = f"{out_name}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.xlsx"

        headers = {"Content-Disposition": f"attachment; filename=\"{out_name}\""}

        return StreamingResponse(
            output_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )
    except ConversaoError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro inesperado ao converter o arquivo. Tente novamente.",
        )
    finally:
        try:
            if 'tmp_in_path' in locals() and os.path.exists(tmp_in_path):
                os.remove(tmp_in_path)
        except Exception:
            pass


@app.get("/health")
async def health():
    return {"status": "ok"}


def _static_dir() -> str:
    """Resolve o diretorio de estaticos tanto em dev quanto empacotado (PyInstaller).

    sys._MEIPASS aponta para o diretorio de dados bundled tanto em onefile
    (pasta temp extraida) quanto em onedir (pasta `_internal` ao lado do exe).
    """
    if getattr(sys, "frozen", False):
        return os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)), "app", "static")
    return os.path.join(os.path.dirname(__file__), "static")


# Mount static files AFTER API routes
static_dir = _static_dir()
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")



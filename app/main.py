from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import os
import io
import tempfile
from datetime import datetime

from .converter_clean import convert_dbc_to_excel


app = FastAPI(title="DBC to Excel Converter", version="1.0.0")


# Permite acesso do front-end (ajuste ALLOW_ORIGINS em producao se desejar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha na conversao: {exc}")
    finally:
        try:
            if 'tmp_in_path' in locals() and os.path.exists(tmp_in_path):
                os.remove(tmp_in_path)
        except Exception:
            pass


@app.get("/health")
async def health():
    return {"status": "ok"}


# Mount static files AFTER API routes
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")



import io
from typing import Union

import tempfile
import os
from openpyxl import Workbook


def convert_dbc_to_excel(dbc_path: str, output_stream: Union[io.BytesIO, io.BufferedWriter]) -> None:
    """Converte DBC (Datasus) em XLSX e grava no stream.

    Fluxo: DBC -> DBF (pyreaddbc) -> DataFrame (dbfread) -> XLSX
    """
    # Importes tardios para evitar erros de compatibilidade na inicialização
    from pyreaddbc.readdbc import dbc2dbf
    from dbfread import DBF

    with tempfile.TemporaryDirectory() as tmpdir:
        dbf_path = os.path.join(tmpdir, "saida.dbf")
        dbc2dbf(dbc_path, dbf_path)
        table = DBF(dbf_path, encoding="latin1", load=True)
        wb = Workbook()
        ws = wb.active
        ws.title = "dados"

        # Cabeçalhos
        headers = [field.name for field in table.fields]
        ws.append(headers)

        # Linhas
        for rec in table:
            row = [str(rec.get(h, "")) if rec.get(h) is not None else "" for h in headers]
            ws.append(row)

        wb.save(output_stream)



import tempfile
import logging
import uvicorn
from fastapi import FastAPI
import os
import shutil
from fastapi import UploadFile, File, HTTPException
from src.auditoria_brintell.main import executar_fluxo_auditoria

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Auditor-IA API")


@app.get("/")
def ler_raiz():
    return {"message": "Olá, Auditor-IA! O servidor está no ar."}


@app.post("/analisar-edital/")
async def analisar_edital(file: UploadFile = File(...)):
    temp_pdf_path = None
    try:  # tente
        temp_dir = "data/uploads"
        os.makedirs(temp_dir, exist_ok=True)  # criar o diretori uploads
        temp_pdf_path = os.path.join(  # type: ignore
            temp_dir, file.filename  # type: ignore
        )  # cria o caminho do arquivo
        with open(temp_pdf_path, "wb") as f:  # abra o arquivo
            shutil.copyfileobj(file.file, f)  # pegue o arquivo
        relatorio = executar_fluxo_auditoria(temp_pdf_path)  # execute o fluxo
        return {"relatorio_final": relatorio}  # retorne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_pdf_path is not None and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)


if __name__ == "__main__":
    print("Iniciando servidor FastAPI em http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

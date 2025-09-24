# Conversor DBC (Datasus) → Excel

🩺 **Ferramenta web para epidemiologistas e pesquisadores em saúde pública**

Interface moderna para converter arquivos `.dbc` do Datasus em `.xlsx` (Excel) com drag & drop, ideal para análise de grandes bases de dados do SUS.

## ✨ Características

- 🎯 **Interface intuitiva** com drag & drop
- 📊 **Conversão automática** DBC → Excel preservando estrutura
- 🚀 **Suporte a arquivos grandes** via streaming
- 🔒 **Privacidade total** - nenhum arquivo é armazenado
- 🐳 **Deploy simples** via Docker
- ⚡ **API REST** com FastAPI

## 🚀 Execução Rápida

### Docker (Recomendado)
```bash
docker build -t conversor-dbc .
docker run --rm -p 8000:8000 conversor-dbc
```

### Python Local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000

## 🏥 Casos de Uso

- **Epidemiologia**: Análise de dados do SINAN, SIM, SIH
- **Pesquisa em Saúde**: Bases do CNES, SIA, SIH
- **Gestão Hospitalar**: Dados administrativos do SUS
- **Academia**: Processamento de datasets para pesquisa

## 🛠️ Tecnologias

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Conversão**: pyreaddbc, dbfread, openpyxl
- **Deploy**: Docker, Uvicorn

## 📋 Requisitos

- Python 3.11+ ou Docker
- Navegador moderno
- Arquivos `.dbc` do Datasus

## 🔧 Desenvolvimento

```bash
git clone https://github.com/elivansouza/conversor-dbc-datasus.git
cd conversor-dbc-datasus
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📄 Licença

MIT License - Livre para uso acadêmico e profissional.

---

**Desenvolvido por**: [@elivansouza](https://github.com/elivansouza) - Epidemiologista e Cientista de Dados

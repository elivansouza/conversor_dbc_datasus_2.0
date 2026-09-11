# Conversor DBC (Datasus) → Excel

🩺 **Aplicativo desktop para epidemiologistas e pesquisadores em saúde pública**

Programa local (Windows e macOS) para converter arquivos `.dbc` do Datasus em `.xlsx` (Excel) com drag & drop, ideal para análise de bases de dados do SUS. Não requer instalação de Python, terminal ou servidor: baixe o programa e execute.

## ✨ Características

- 🖥️ **App desktop nativo** - janela própria, sem precisar abrir navegador
- 🎯 **Interface intuitiva** com drag & drop
- 📊 **Conversão automática** DBC → Excel preservando estrutura
- 🔒 **Privacidade total** - roda 100% local, nenhum arquivo sai da sua máquina
- 🚀 **Suporte a arquivos grandes** via streaming

## 🚀 Execução Rápida (usuário final)

Baixe o instalador mais recente na seção de builds do projeto:
- **Windows**: baixe e execute `ConversorDBC-Setup.exe` (instalador único, gerado com Inno Setup) e siga o assistente
- **macOS (Apple Silicon)**: extraia o `.app` e abra normalmente

> ⚠️ **Windows**: instale sempre pelo `ConversorDBC-Setup.exe`. O artefato `ConversorDBC-windows` (pasta com `ConversorDBC.exe` + `_internal/`) é para quem for testar localmente — se você copiar só o `.exe` sem a pasta `_internal` ao lado, o programa não abre (erro "Failed to load Python DLL").

Na primeira execução o sistema operacional pode exibir um aviso padrão de "aplicativo não reconhecido" (SmartScreen no Windows / Gatekeeper no macOS) por o programa ainda não ter assinatura de código paga — não é um bloqueio de antivírus, apenas clique em "Executar mesmo assim" / "Abrir mesmo assim".

## 🏥 Casos de Uso

- **Epidemiologia**: Análise de dados do SINAN, SIM, SIH
- **Pesquisa em Saúde**: Bases do CNES, SIA, SIH
- **Gestão Hospitalar**: Dados administrativos do SUS
- **Academia**: Processamento de datasets para pesquisa

## 🛠️ Tecnologias

- **App desktop**: pywebview (janela nativa) + FastAPI/Uvicorn rodando localmente (`127.0.0.1`)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Conversão**: pyreaddbc (DBC → DBF, extensão nativa), dbfread, openpyxl
- **Empacotamento**: PyInstaller (modo `onedir`, sem UPX) via GitHub Actions (Windows + macOS)

## 📋 Requisitos

- Windows 10/11 ou macOS com Apple Silicon (M1 ou superior)
- Arquivos `.dbc` do Datasus

## 🔧 Desenvolvimento

```bash
git clone https://github.com/elivansouza/conversor-dbc-datasus.git
cd conversor-dbc-datasus
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python desktop_app.py
```

Isso abre a janela do app apontando para um servidor local iniciado automaticamente. Não é necessário abrir navegador nem rodar `uvicorn` manualmente.

## 📦 Gerando o executável (build)

Builds nativos precisam rodar no respectivo sistema operacional (PyInstaller não faz cross-compile):

```bash
pip install pyinstaller pyinstaller-hooks-contrib

# Windows
pyinstaller packaging/windows.spec --noconfirm --clean

# macOS (Apple Silicon)
pyinstaller packaging/macos.spec --noconfirm --clean
```

No Windows, gere também o instalador único (requer [Inno Setup](https://jrsoftware.org/isinfo.php) instalado):

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" packaging\inno_setup.iss
```

O resultado fica em `dist\installer\ConversorDBC-Setup.exe` — é esse arquivo que deve ser distribuído (nunca o `ConversorDBC.exe` sozinho).

O workflow `.github/workflows/build-desktop.yml` automatiza os dois builds (Windows + macOS) via GitHub Actions, disparado manualmente ou ao criar uma tag `v*`.

## 🐳 Modo servidor (Docker, opcional)

O modo principal do projeto é o app desktop, mas o mesmo código de conversão também pode ser hospedado como serviço web para uso compartilhado em equipe:

```bash
docker build -t conversor-dbc .
docker run --rm -p 8000:8000 conversor-dbc
```

Acesse: http://localhost:8000

## 📄 Licença

MIT License - Livre para uso acadêmico e profissional.

---

**Desenvolvido por**: [@elivansouza](https://github.com/elivansouza) - Epidemiologista e Cientista de Dados

; Instalador Windows do Conversor DBC (Datasus) -> Excel
; Gera UM UNICO .exe de instalacao a partir da pasta onedir do PyInstaller
; (dist/ConversorDBC). Isso evita o erro "Failed to load Python DLL" que
; acontece quando alguem distribui o ConversorDBC.exe sozinho, sem a pasta
; _internal da qual ele depende (modo onedir e' proposital, para reduzir
; falso-positivo de antivirus - ver packaging/windows.spec).
;
; Build: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" packaging\inno_setup.iss
; Pre-requisito: rodar o PyInstaller antes (dist\ConversorDBC deve existir).

#define MyAppName "Conversor DBC (Datasus)"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Elivan Silva"
#define MyAppExeName "ConversorDBC.exe"

[Setup]
AppId={{B6C1F1B0-6E6B-4B0F-9C36-4B1B7B1E7A11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\ConversorDBC
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\dist\installer
OutputBaseFilename=ConversorDBC-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
Source: "..\dist\ConversorDBC\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName}"; Flags: nowait postinstall skipifsilent

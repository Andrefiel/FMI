
FMI Monitor - README

Este aplicativo é um monitor de arquivos em tempo real com geração de relatórios automáticos. Ele possui uma interface gráfica em PyQt5 e permite o monitoramento de uma pasta, captura de eventos de criação, exclusão e modificação de arquivos, geração de relatórios em PDF/HTML, e envio desses relatórios por e-mail. O sistema também inclui uma funcionalidade de agendamento para o envio de relatórios.
Estrutura do Projeto

fmi_app/
├── main.py
├── db.py
├── scheduler.py
├── file_monitor.py
├── reports/
│   ├── generate_report.py
│   ├── email_sender.py
├── templates/
│   └── report.html
├── assets/
│   └── icon.ico
├── database/
│   └── (vazio, será criado na execução)
├── gui/
│   ├── config_tab.py
│   ├── monitor_tab.py
│   ├── reports_tab.py
├── fmi_installer.nsi
├── requirements.txt
└── README.md

Pré-Requisitos

    Python (versão 3.6 ou superior)

    Bibliotecas Python especificadas no arquivo requirements.txt.

Instalação
1. Clonar o Repositório

Clone o repositório do projeto para sua máquina local:

git clone https://link-para-o-repositorio.git
cd fmi_app

2. Criar um Ambiente Virtual (Recomendado)

Crie e ative um ambiente virtual para o projeto:

    No Windows:

python -m venv venv
venv\Scripts\activate

No Linux/macOS:

    python3 -m venv venv
    source venv/bin/activate

3. Instalar as Dependências

Instale todas as dependências necessárias com o comando:

pip install -r requirements.txt

Isso irá instalar os pacotes listados no requirements.txt, que incluem:

    PyQt5: Para a interface gráfica do usuário.

    FPDF: Para a geração de relatórios em PDF.

    schedule: Para o agendamento de tarefas.

    watchdog: Para monitoramento eficiente de arquivos.

4. Rodando o Aplicativo

Agora que as dependências estão instaladas, você pode rodar o aplicativo com o seguinte comando:

python main.py

A aplicação abrirá a interface gráfica, onde você pode monitorar diretórios, gerar relatórios e configurar o envio de e-mails.
Configurações do Aplicativo

    Configurações de Monitoramento:

        Defina o diretório que você deseja monitorar.

        Inicie ou pare o monitoramento de alterações de arquivos.

        Visualize as alterações em tempo real (criação, modificação, exclusão).

    Relatórios:

        Visualize e baixe relatórios diários, semanais, mensais ou anuais.

        Agende o envio de relatórios em PDF ou HTML por e-mail.

    Configurações de Envio por E-mail:

        Defina as configurações de SMTP para o envio dos relatórios.

    Configurações de Logo:

        Carregue o logo da empresa para ser incluído no relatório gerado em PDF ou HTML.

Criando o Instalador

Se você deseja criar um instalador para o seu aplicativo, siga as instruções abaixo para Windows e Linux.
Criando o Instalador para Windows (NSIS)

O NSIS (Nullsoft Scriptable Install System) é uma ferramenta popular para criar instaladores para Windows.
1. Instalar o NSIS

Baixe e instale o NSIS a partir de https://nsis.sourceforge.io/Download.
2. Criar o Script do Instalador

Dentro do diretório fmi_app, você encontrará o arquivo fmi_installer.nsi. Este script configura o processo de instalação do aplicativo para o Windows.

Exemplo do script fmi_installer.nsi:

# Script para criar instalador do FMI Monitor

Outfile "FMI_Monitor_Installer.exe"
InstallDir $PROGRAMFILES\FMI_Monitor
RequestExecutionLevel admin

Section

    # Cria diretórios de instalação
    SetOutPath $INSTDIR

    # Inclui os arquivos do aplicativo
    File /r "fmi_app\*.*"

    # Cria o atalho no Menu Iniciar
    CreateShortCut $SMPROGRAMS\FMI_Monitor.lnk $INSTDIR\main.py

SectionEnd

Este script cria um instalador para o aplicativo, inclui todos os arquivos e cria um atalho no menu iniciar.
3. Compilar o Script NSIS

    Abra o NSIS.

    Vá até File > Open e selecione o arquivo fmi_installer.nsi.

    Clique em Compile para gerar o arquivo instalador FMI_Monitor_Installer.exe.

Agora, o instalador estará pronto para ser distribuído.
4. Executar o Instalador

Execute o instalador gerado (FMI_Monitor_Installer.exe) em um sistema Windows para instalar o aplicativo.
Criando o Instalador para Linux (usando PyInstaller)

Para criar um instalador para Linux, usamos o PyInstaller, uma ferramenta que empacota aplicativos Python em executáveis.
1. Instalar o PyInstaller

Instale o PyInstaller com o seguinte comando:

pip install pyinstaller

2. Criar o Executável

Execute o comando abaixo para gerar o executável do aplicativo:

pyinstaller --onefile --windowed main.py

Este comando criará um executável no diretório dist/.
3. Criar o Pacote de Instalação

Para criar um pacote .deb (para distribuições baseadas no Debian, como Ubuntu), você pode usar ferramentas como o fpm (Effing Package Management).

Instale o fpm:

gem install --user-install fpm

Depois, use o seguinte comando para criar um pacote .deb:

fpm -s dir -t deb -n fmi_monitor -v 1.0 --prefix /usr/local/bin dist/main

Este comando cria o pacote .deb que pode ser instalado com o dpkg:

sudo dpkg -i fmi_monitor-1.0.deb

Agora, você tem um instalador .deb pronto para ser instalado em sistemas Linux.
Conclusão

Com esses passos, você pode instalar e executar o FMI Monitor em Linux e Windows. Além disso, também mostramos como criar instaladores para ambos os sistemas operacionais.

Se tiver qualquer problema durante o processo de instalação ou execução, fique à vontade para perguntar!
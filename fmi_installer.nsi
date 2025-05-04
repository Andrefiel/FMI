# Nome do instalador
Outfile "FMI_Monitor_Installer.exe"
InstallDir "$PROGRAMFILES\FMI_Monitor"
RequestExecutionLevel user

Page directory
Page instfiles

Section "FMI Monitor"

    SetOutPath $INSTDIR
    File "dist\FMI_Monitor.exe"
    File /r "templates\*.*"
    File /r "assets\*.*"
    File /r "database\*.*"

    CreateShortCut "$DESKTOP\FMI_Monitor.lnk" "$INSTDIR\FMI_Monitor.exe"
    CreateShortCut "$SMPROGRAMS\FMI_Monitor\FMI_Monitor.lnk" "$INSTDIR\FMI_Monitor.exe"

    Exec "$INSTDIR\FMI_Monitor.exe"

SectionEnd

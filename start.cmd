@echo off
REM On récupère la valeur du registre dans str
for /f "delims=" %%a in ('reg query "HKLM\SOFTWARE\LibreOffice\UNO\InstallPath" /ve') do set str=%%a
REM On remplace la chaine REG_SZ par #
set str=%str:REG_SZ=#%
REM On split str au caractère #
for /f "tokens=1,2 delims=#" %%a in ("%str%") do set str=%%a&&set liboInstallPath=%%b
REM On enlève les espaces au début de la partie droite
for /f "tokens=* delims= " %%a in ("%liboInstallPath%") do set liboInstallPath=%%a
REM On nettoie l'environnement
set str=
%liboInstallPath%\python.exe runlibo.py %1%

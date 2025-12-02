@echo off
REM Windows Batch-Datei zum einfachen Entschlüsseln von wallet.dat
REM Verwendung: Kopiere diese Datei in den Ordner mit wallet.dat

echo ============================================================
echo     Bitcoin Wallet Decryption Tool
echo ============================================================
echo.

REM Prüfe ob wallet.dat existiert
if not exist wallet.dat (
    echo FEHLER: wallet.dat nicht gefunden!
    echo Bitte lege diese Datei in den gleichen Ordner wie wallet.dat
    echo.
    pause
    exit /b 1
)

echo Gefunden: wallet.dat
echo.
echo Waehle eine Option:
echo.
echo [1] Interaktiv - Passphrase eingeben (empfohlen)
echo [2] Nur Informationen anzeigen (OHNE Passphrase)
echo [3] GPU Cracking mit Hashcat (^>1 Million H/s!)
echo [4] Brute-Force Python (langsam, ~5 H/s)
echo [5] Hashcat manuell vorbereiten
echo [6] Beenden
echo.

set /p choice="Deine Wahl (1-6): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto info
if "%choice%"=="3" goto gpu_crack
if "%choice%"=="4" goto bruteforce
if "%choice%"=="5" goto hashcat_export
if "%choice%"=="6" goto end

echo Ungueltige Eingabe!
pause
exit /b 1

:interactive
echo.
echo ============================================================
echo Interaktiver Modus - Passphrase wird sicher abgefragt
echo ============================================================
echo.
py3 decrypt_wallet.py -w wallet.dat -i
goto end

:info
echo.
echo ============================================================
echo Zeige Wallet-Informationen (ohne Passphrase)
echo ============================================================
echo.
py3 pywallet.py -w wallet.dat
echo.
echo Moechtest du einen vollstaendigen Dump erstellen? (j/n)
set /p dump="Dump? "
if /i "%dump%"=="j" (
    echo Erstelle wallet_info.json...
    py3 pywallet.py -w wallet.dat -d > wallet_info.json
    echo.
    echo ✓ Gespeichert in: wallet_info.json
)
goto end

:gpu_crack
echo.
echo ============================================================
echo GPU CRACKING MIT HASHCAT (^>1 Million H/s!)
echo ============================================================
echo.
echo Dies ist die SCHNELLSTE Methode zum Testen vieler Passwoerter!
echo GPU Performance: GTX 1080 = 50k-200k H/s, RTX 4090 = 500k-2M+ H/s
echo.

if not exist passwords.txt (
    echo Erstelle Beispiel-Wortliste: passwords.txt
    echo password123 > passwords.txt
    echo Password123 >> passwords.txt
    echo bitcoin2010 >> passwords.txt
    echo Bitcoin2015 >> passwords.txt
    echo wallet >> passwords.txt
    echo Wallet2010 >> passwords.txt
    echo mybitcoin >> passwords.txt
    echo MyBitcoin >> passwords.txt
    echo SecretKey123 >> passwords.txt
    echo test123 >> passwords.txt
    echo.
    echo ✓ Beispiel-Wortliste erstellt (10 Eintraege)
    echo.
    echo WICHTIG: Fuer echtes Cracking brauchen Sie eine groessere Wortliste!
    echo.
    echo Empfohlene Wortlisten:
    echo   - RockYou (14 Millionen): https://github.com/brannondorsey/naive-hashcat/releases
    echo   - SecLists: https://github.com/danielmiessler/SecLists
    echo.
    set /p edit="Wortliste jetzt bearbeiten? (j/n): "
    if /i "%edit%"=="j" (
        notepad passwords.txt
    )
)

echo.
echo Starte GPU Cracking mit Hashcat...
echo.
echo Hinweis: Hashcat muss installiert sein!
echo   Download: https://hashcat.net/hashcat/
echo.

py3 decrypt_wallet.py -w wallet.dat -g passwords.txt -o decrypted_wallet.json

if exist hashcat_found.txt (
    echo.
    echo ============================================================
    echo ✓ ERFOLG! Passphrase wurde gefunden!
    echo ============================================================
    type hashcat_found.txt
    echo.
    echo Entschluesseltes Wallet wurde gespeichert.
)

goto end

:hashcat_export
echo.
echo ============================================================
echo Exportiere Hash fuer manuelles Hashcat Cracking
echo ============================================================
echo.
py3 decrypt_wallet.py -w wallet.dat -e
echo.
echo ✓ Hash wurde gespeichert
echo.
echo Verwende den Hash mit Hashcat:
echo   hashcat -m 11300 -a 0 wallet_hash.txt wordlist.txt
echo.
echo Oder mit Masken fuer Brute-Force:
echo   hashcat -m 11300 -a 3 wallet_hash.txt ?l?l?l?l?l?l
echo.
goto end

:bruteforce
echo.
echo ============================================================
echo Python Brute-Force (langsam, ~5 H/s)
echo ============================================================
echo.
echo ACHTUNG: Diese Methode ist SEHR LANGSAM (~5 Passwoerter/Sekunde)
echo.
echo Fuer schnelles Cracking verwende stattdessen:
echo   Option [3] GPU Cracking (^>1 Million H/s)
echo.
set /p continue="Trotzdem fortfahren? (j/n): "
if /i not "%continue%"=="j" goto end

echo.

if not exist passwords.txt (
    echo Erstelle Beispiel-Wortliste: passwords.txt
    echo password123 > passwords.txt
    echo Password123 >> passwords.txt
    echo bitcoin2010 >> passwords.txt
    echo wallet >> passwords.txt
    echo mybitcoin >> passwords.txt
    echo.
    echo ✓ Beispiel-Wortliste erstellt (5 Eintraege)
    echo   Bearbeite passwords.txt und fuege deine Passphrasen hinzu!
    echo.
    echo Wortliste jetzt bearbeiten? (j/n)
    set /p edit="Bearbeiten? "
    if /i "%edit%"=="j" (
        notepad passwords.txt
    )
)

echo.
echo Starte Python Brute-Force mit passwords.txt...
echo Performance: ~2-5 Passwoerter/Sekunde (LANGSAM!)
echo.
py3 decrypt_wallet.py -w wallet.dat -l passwords.txt -o decrypted_wallet.json
goto end

:end
echo.
echo ============================================================
pause

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
echo [3] Hashcat Export (fuer GPU Cracking)
echo [4] Brute-Force mit Wortliste
echo [5] Beenden
echo.

set /p choice="Deine Wahl (1-5): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto info
if "%choice%"=="3" goto hashcat
if "%choice%"=="4" goto bruteforce
if "%choice%"=="5" goto end

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

:hashcat
echo.
echo ============================================================
echo Exportiere Daten fuer Hashcat/John the Ripper
echo ============================================================
echo.
py3 decrypt_wallet.py -w wallet.dat -e > wallet_hash.txt
echo.
echo ✓ Hash gespeichert in: wallet_hash.txt
echo.
echo Kopiere die Hashcat-Zeile aus wallet_hash.txt und verwende:
echo   hashcat -m 11300 -a 0 hash.txt wordlist.txt
echo.
goto end

:bruteforce
echo.
echo ============================================================
echo Brute-Force mit Wortliste
echo ============================================================
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
echo Starte Brute-Force mit passwords.txt...
echo.
py3 decrypt_wallet.py -w wallet.dat -l passwords.txt -o decrypted_wallet.json
goto end

:end
echo.
echo ============================================================
pause

# 🚀 Quick Start für Windows

## ⚡ Schnellstart - 3 einfache Schritte

### Schritt 1: Dateien vorbereiten

```cmd
cd C:\Users\alina\Downloads\btc_test
```

Stelle sicher, dass folgende Dateien vorhanden sind:
- ✅ `wallet.dat` (deine Wallet)
- ✅ `pywallet.py`
- ✅ `decrypt_wallet.py` (NEU!)
- ✅ `extract_keys.py` (NEU!)
- ✅ `decrypt_windows.bat` (NEU! - Automatisches Menü)

### Schritt 2: Wähle deine Methode

---

## 🎯 Methode 1: Automatisches Menü (EINFACHSTE)

Doppelklick auf **`decrypt_windows.bat`** oder:

```cmd
decrypt_windows.bat
```

**Menü:**
```
============================================================
    Bitcoin Wallet Decryption Tool
============================================================

Gefunden: wallet.dat

Waehle eine Option:

[1] Interaktiv - Passphrase eingeben (empfohlen)
[2] Nur Informationen anzeigen (OHNE Passphrase)
[3] Hashcat Export (fuer GPU Cracking)
[4] Brute-Force mit Wortliste
[5] Beenden

Deine Wahl (1-5):
```

**Option wählen:**
- **[1]** → Du kennst die Passphrase → Sicher eingeben
- **[2]** → Nur Infos anzeigen (Salt, Iterations, Adressen)
- **[3]** → Für GPU-Cracking vorbereiten (Hashcat)
- **[4]** → Automatisch mehrere Passphrases testen

---

## 🔓 Methode 2: Interaktiv (EMPFOHLEN wenn Passphrase bekannt)

```cmd
py3 decrypt_wallet.py -w wallet.dat -i
```

**Was passiert:**
1. Fragt nach Passphrase (wird NICHT angezeigt - sicher!)
2. Testet Passphrase
3. Bei Erfolg: Fragt ob speichern
4. Zeigt erste 3 entschlüsselte Private Keys

**Beispiel-Ausgabe:**
```
Enter passphrase (input hidden): *********

✓ SUCCESS! Passphrase is correct!

Save decrypted wallet to file? (y/n): y
Output filename [decrypted_wallet.json]: meine_keys.json

✓ Decrypted wallet saved to: meine_keys.json

Total keys decrypted: 15
First 3 decrypted private keys (WIF format):
  1. 1A1zP1eP5Q...: 5Kb8kLf9zgWQ...
  2. 1BvBMSEYst...: 5HpHagT65TZz...
  3. 12cbQLTFMX...: 5J3mBbAH58Cp...
```

---

## 📊 Methode 3: Infos anzeigen (OHNE Passphrase)

```cmd
py3 pywallet.py -w wallet.dat
```

**Zeigt:**
- ✅ Salt (für Hashcat)
- ✅ Iterations/Rounds
- ✅ Verschlüsselter Master Key
- ✅ Alle Adressen
- ✅ Verschlüsselte Private Keys
- ✅ Public Keys

**Oder als JSON speichern:**
```cmd
py3 pywallet.py -w wallet.dat -d > wallet_encrypted.json
```

---

## 🔨 Methode 4: Brute-Force (Passphrase vergessen)

### A) Mit eigener Wortliste

**1. Erstelle `passwords.txt`:**
```
MeineWallet2015
Bitcoin2010
Geheim123
Family2015
SecretKey!
```

**2. Starte Brute-Force:**
```cmd
py3 decrypt_wallet.py -w wallet.dat -l passwords.txt -o gefunden.json
```

**Was passiert:**
```
Testing 5 passphrases...

[1/5] Tested 1 passphrases (2.5/sec, ETA: 2s)
[2/5] Tested 2 passphrases (2.8/sec, ETA: 1s)

======================================================================
✓ SUCCESS! PASSPHRASE FOUND!
======================================================================
Passphrase: MeineWallet2015
======================================================================

Decrypted wallet saved to: gefunden.json
```

### B) Mit großer Wortliste (RockYou)

**Download RockYou (14 Millionen Passphrases):**
https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

```cmd
py3 decrypt_wallet.py -w wallet.dat -l rockyou.txt -o gefunden.json
```

**Performance:**
- ~2-5 Passphrases/Sekunde
- 10.000 Passphrases = ~30-90 Minuten
- 1 Million Passphrases = ~2-6 Tage

---

## ⚡ Methode 5: GPU Cracking mit Hashcat (SCHNELLSTE)

### Schritt 1: Hash extrahieren
```cmd
py3 decrypt_wallet.py -w wallet.dat -e > hash.txt
```

**hash.txt enthält jetzt:**
```
[HASHCAT FORMAT]
$bitcoin$64$a1b2c3d4e5f67890...$fedcba9876543210...$65432$0$0

Usage:
  hashcat -m 11300 -a 0 hash.txt wordlist.txt
```

### Schritt 2: Hashcat installieren
Download: https://hashcat.net/hashcat/

### Schritt 3: Hash in Datei speichern
Kopiere die `$bitcoin$...` Zeile in neue Datei:
```cmd
echo $bitcoin$64$a1b2c3... > wallet_hash.txt
```

### Schritt 4: Hashcat starten
```cmd
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt
```

**Performance:**
- CPU: ~100-1.000 Hashes/Sekunde
- GTX 1080: ~50.000-200.000 Hashes/Sekunde
- RTX 4090: ~500.000+ Hashes/Sekunde

**GPU ist 100-1000x SCHNELLER als Python!**

---

## 🔑 Keys exportieren (nach erfolgreicher Entschlüsselung)

### Alle Formate auf einmal:
```cmd
py3 extract_keys.py -w wallet.dat -p "IhreGefundenePassphrase" -f all -o meine_keys
```

**Erstellt:**
- ✅ `meine_keys.json` - Volle JSON-Daten
- ✅ `meine_keys.csv` - Excel-Format
- ✅ `meine_keys.txt` - Textformat
- ✅ `meine_keys_electrum.txt` - Für Electrum Wallet
- ✅ `meine_keys_summary.txt` - Übersicht

### Nur Electrum-Import:
```cmd
py3 extract_keys.py -w wallet.dat -p "Passphrase" -f electrum -o electrum.txt
```

**Import in Electrum:**
1. Electrum öffnen
2. Wallet → Private Keys → Import
3. Inhalt von `electrum.txt` einfügen
4. ✓ Fertig!

---

## 📁 Dateien die du bekommst

Nach erfolgreicher Extraktion hast du:

```
C:\Users\alina\Downloads\btc_test\
├── wallet.dat (Original - NICHT löschen!)
├── decrypted_wallet.json (Entschlüsselte Wallet)
├── meine_keys.json (Alle Keys in JSON)
├── meine_keys.csv (Für Excel)
├── meine_keys.txt (Einfaches Text)
├── meine_keys_electrum.txt (Für Import)
└── meine_keys_summary.txt (Übersicht)
```

---

## 🔐 Sicherheit - WICHTIG!

### Nach der Extraktion:

```cmd
REM 1. Verschlüsseln mit 7-Zip
"C:\Program Files\7-Zip\7z.exe" a -p -mhe=on keys_backup.7z meine_keys*

REM Oder mit Windows eingebauten Tools
REM Rechtsklick auf Ordner → "Senden an" → "ZIP-komprimierter Ordner"
REM Dann ZIP mit Passwort schützen

REM 2. Original-Dateien löschen (NACH Backup!)
del meine_keys*.json
del meine_keys*.csv
del meine_keys*.txt

REM 3. Verschlüsseltes Archiv auf USB sichern
copy keys_backup.7z E:\backup\

REM 4. Computer neu starten (löscht RAM)
shutdown /r /t 0
```

### ⚠️ NIE:
- ❌ Unverschlüsselte Keys online speichern
- ❌ Per E-Mail versenden
- ❌ In Cloud hochladen (Dropbox, Google Drive, etc.)
- ❌ Screenshots machen und speichern

### ✅ IMMER:
- ✅ Mit 7-Zip/GPG verschlüsseln
- ✅ Auf USB-Stick offline sichern
- ✅ Original-Dateien sicher löschen
- ✅ Computer nach Extraktion neu starten

---

## ❓ Probleme?

### "py3 wird nicht erkannt"
```cmd
REM Verwende stattdessen:
python pywallet.py -w wallet.dat
REM oder
python3 pywallet.py -w wallet.dat
```

### "Syntax Error" oder "Module not found"
```cmd
REM Installiere Dependencies:
pip install bsddb3 ecdsa simplejson pycryptodome
```

### "No decrypted private keys found"
→ **Passphrase ist falsch!** Versuche:
1. Andere Schreibweise
2. Mit/ohne Leerzeichen
3. Groß-/Kleinschreibung
4. Brute-Force mit Wortliste

---

## 🎯 Welche Methode soll ich verwenden?

| Situation | Methode | Befehl |
|-----------|---------|--------|
| **Passphrase bekannt** | Interaktiv | `decrypt_windows.bat` → [1] |
| **Passphrase vergessen, paar Ideen** | Brute-Force | `decrypt_windows.bat` → [4] |
| **Passphrase völlig vergessen** | GPU Hashcat | `decrypt_windows.bat` → [3] |
| **Nur Infos sehen** | Anzeigen | `decrypt_windows.bat` → [2] |

---

## 💾 Komplettes Beispiel

```cmd
REM Schritt 1: In Wallet-Ordner wechseln
cd C:\Users\alina\Downloads\btc_test

REM Schritt 2: Menü starten
decrypt_windows.bat

REM Wähle [1] - Interaktiv
REM Gib Passphrase ein: **********

REM Schritt 3: Keys in allen Formaten exportieren
py3 extract_keys.py -w wallet.dat -p "MeinePassphrase" -f all -o backup

REM Schritt 4: Verschlüsseln
"C:\Program Files\7-Zip\7z.exe" a -p backup.7z backup*

REM Schritt 5: Originale löschen
del backup*.json
del backup*.csv
del backup*.txt

REM Schritt 6: Auf USB sichern
copy backup.7z E:\usb-stick\

REM Fertig! ✓
```

---

**Los geht's! Viel Erfolg! 🚀**

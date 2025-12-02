# ⚡ GPU Cracking - >1 Million Hashes/Sekunde

## 🚀 Schnellstart - Automatisch mit Hashcat

### Option 1: Windows Menü (EINFACHSTE)

```cmd
cd C:\Users\alina\Downloads\btc_test

REM Doppelklick auf:
decrypt_windows.bat

REM Wähle Option [3] - GPU Cracking
```

**Was passiert:**
1. Erstellt automatisch `wallet_hash.txt`
2. Startet Hashcat mit GPU
3. Testet >1 Million Passphrases/Sekunde
4. Bei Erfolg: Entschlüsselt automatisch die Wallet!

---

### Option 2: Kommandozeile

```cmd
py3 decrypt_wallet.py -w wallet.dat -g wordlist.txt -o decrypted.json
```

**Was passiert:**
1. Extrahiert Hash aus wallet.dat
2. Prüft ob Hashcat installiert ist
3. Startet GPU-Cracking automatisch
4. Speichert gefundene Passphrase
5. Entschlüsselt Wallet automatisch

---

## 📊 Performance-Vergleich

| Methode | Geschwindigkeit | Zeit für 1 Million |
|---------|----------------|---------------------|
| **Python Brute-Force** (`-l`) | ~5 H/s | **2-6 Tage** ❌ |
| **GPU GTX 1080** (`-g`) | ~50k-200k H/s | **5-20 Sekunden** ⚡ |
| **GPU RTX 3080** (`-g`) | ~300k-500k H/s | **2-3 Sekunden** ⚡⚡ |
| **GPU RTX 4090** (`-g`) | ~500k-2M+ H/s | **0.5-2 Sekunden** ⚡⚡⚡ |

**GPU ist 10.000-400.000x schneller!**

---

## 🛠️ Hashcat Installation

### Windows:

**1. Download Hashcat:**
https://hashcat.net/files/hashcat-6.2.6.7z

**2. Entpacken:**
```cmd
REM Entpacke nach C:\hashcat\
7z x hashcat-6.2.6.7z -oC:\hashcat\
```

**3. Zum PATH hinzufügen:**
```cmd
REM Einmalig ausführen:
setx PATH "%PATH%;C:\hashcat"

REM ODER in den Wallet-Ordner kopieren:
copy C:\hashcat\hashcat.exe C:\Users\alina\Downloads\btc_test\
```

**4. GPU-Treiber prüfen:**
- NVIDIA: https://www.nvidia.com/download/index.aspx
- AMD: https://www.amd.com/en/support

---

### Linux:

```bash
sudo apt update
sudo apt install hashcat

# GPU-Treiber
# NVIDIA:
sudo apt install nvidia-driver-535

# AMD:
sudo apt install mesa-opencl-icd
```

---

### macOS:

```bash
brew install hashcat

# Für M1/M2/M3 (Apple Silicon):
# Hashcat unterstützt Metal API
```

---

## 💾 Wordlist Download

### RockYou (14 Millionen Passphrases)

**Download:**
```cmd
REM Windows PowerShell:
Invoke-WebRequest -Uri "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt" -OutFile "rockyou.txt"

REM Oder manuell:
REM https://github.com/brannondorsey/naive-hashcat/releases
```

**Linux/macOS:**
```bash
wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
```

---

### Weitere Wordlists

| Name | Größe | Download |
|------|-------|----------|
| **RockYou** | 14M | https://github.com/brannondorsey/naive-hashcat/releases |
| **SecLists** | Viele | https://github.com/danielmiessler/SecLists |
| **CrackStation** | 1.5B | https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm |
| **Probable-Wordlists** | Verschiedene | https://github.com/berzerk0/Probable-Wordlists |

---

## 🎯 Komplettes Beispiel - GPU Cracking

### Schritt 1: Hashcat installieren

```cmd
REM Download & entpacken
REM https://hashcat.net/hashcat/

REM Ins Wallet-Verzeichnis kopieren
copy C:\hashcat\hashcat.exe C:\Users\alina\Downloads\btc_test\
```

### Schritt 2: Wordlist downloaden

```cmd
cd C:\Users\alina\Downloads\btc_test

REM RockYou herunterladen (14 Millionen)
REM https://github.com/brannondorsey/naive-hashcat/releases

REM ODER kleine Test-Liste erstellen:
echo password123 > test_passwords.txt
echo bitcoin2010 >> test_passwords.txt
echo MyWallet2015 >> test_passwords.txt
```

### Schritt 3: GPU Cracking starten

```cmd
REM Automatisch (empfohlen):
py3 decrypt_wallet.py -w wallet.dat -g rockyou.txt -o decrypted.json

REM ODER mit Batch-Menü:
decrypt_windows.bat
REM → [3] GPU Cracking wählen
```

**Ausgabe:**
```
======================================================================
GPU-ACCELERATED CRACKING WITH HASHCAT
======================================================================
Wallet: wallet.dat
Wordlist: rockyou.txt

Extracting hash from wallet...

[MASTER KEY INFORMATION]
Salt (hex): a1b2c3d4e5f67890
Iterations: 65432
Method: 0 (SHA512)
Encrypted Master Key (hex): fedcba...

✓ Hash saved to: wallet_hash.txt

GPU Performance estimate:
  GTX 1080:  ~50,000-200,000 H/s
  RTX 3080:  ~300,000-500,000 H/s
  RTX 4090:  ~500,000-2,000,000+ H/s

======================================================================
STARTING HASHCAT GPU CRACKING
======================================================================
This will use your GPU for maximum speed (>1 Million H/s)
Press Ctrl+C to stop

hashcat (v6.2.6) starting...

* Device #1: NVIDIA GeForce RTX 4090, 24576 MB
...

Status: Running
Speed: 1,523,456 H/s       <-- >1 Million H/s! ⚡
Progress: 5000000/14000000 (35.71%)
Time: 00:00:03
ETA: 00:00:06

...

$bitcoin$64$...:MyWallet2015

Session: Cracked
Status: Exhausted

======================================================================
✓ SUCCESS! PASSWORD FOUND!
======================================================================
Password: MyWallet2015
======================================================================

Decrypting wallet with found password...
✓ Decrypted wallet saved to: decrypted.json

Total keys decrypted: 15
```

### Schritt 4: Keys exportieren

```cmd
py3 extract_keys.py -w wallet.dat -p "MyWallet2015" -f all -o my_keys
```

---

## 🔧 Erweiterte Hashcat-Optionen

### Brute-Force mit Masken (kein Wordlist)

```cmd
REM Extrahiere Hash
py3 decrypt_wallet.py -w wallet.dat -e

REM Brute-Force: 6 Kleinbuchstaben
hashcat -m 11300 -a 3 wallet_hash.txt ?l?l?l?l?l?l

REM 8 Zeichen: Groß+Klein+Zahlen
hashcat -m 11300 -a 3 wallet_hash.txt ?1?1?1?1?1?1?1?1 -1 ?l?u?d

REM "Wallet" + 4 Ziffern
hashcat -m 11300 -a 3 wallet_hash.txt Wallet?d?d?d?d
```

**Masken-Syntax:**
- `?l` = Kleinbuchstaben (a-z)
- `?u` = Großbuchstaben (A-Z)
- `?d` = Ziffern (0-9)
- `?s` = Sonderzeichen (!@#$ etc.)
- `?a` = Alle (l+u+d+s)

---

### Kombinations-Attack

```cmd
REM Kombiniere 2 Wordlists
hashcat -m 11300 -a 1 wallet_hash.txt wordlist1.txt wordlist2.txt

REM Beispiel: names.txt + years.txt
REM → "Alice2015", "Bob2020", etc.
```

---

### Rules (Wort-Transformationen)

```cmd
REM Mit integrierten Rules
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt -r rules/best64.rule

REM Eigene Rules:
REM rules/custom.rule:
REM   c    (Capitalize: password → Password)
REM   u    (Uppercase: password → PASSWORD)
REM   $1   (Append 1: password → password1)
REM   ^!   (Prepend !: password → !password)

hashcat -m 11300 -a 0 wallet_hash.txt wordlist.txt -r rules/custom.rule
```

---

## 📈 Performance Optimierung

### GPU Auslastung maximieren

```cmd
REM Workload Tuning
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt -w 4

REM -w Werte:
REM   1 = Low     (Desktop nutzbar)
REM   2 = Default (guter Kompromiss)
REM   3 = High    (Desktop langsam)
REM   4 = Insane  (maximale Speed, Desktop eingefroren)
```

### Multi-GPU

```cmd
REM Nutze mehrere GPUs
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt -d 1,2,3

REM Liste GPUs auf:
hashcat -I
```

---

## 🔍 Status während Cracking

**Während Hashcat läuft:**
- Drücke `s` = Status anzeigen
- Drücke `p` = Pause
- Drücke `r` = Resume
- Drücke `q` = Quit (save progress)

**Session fortsetzen:**
```cmd
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt --session=mysession

REM Später fortsetzen:
hashcat --session=mysession --restore
```

---

## ❓ Troubleshooting

### "hashcat not found"
```cmd
REM Kopiere hashcat.exe in Wallet-Ordner:
copy C:\hashcat\hashcat.exe .

REM Oder voller Pfad:
C:\hashcat\hashcat.exe -m 11300 -a 0 wallet_hash.txt rockyou.txt
```

### "No devices found"
```cmd
REM GPU-Treiber aktualisieren:
REM NVIDIA: https://www.nvidia.com/download/index.aspx
REM AMD: https://www.amd.com/en/support

REM GPU prüfen:
hashcat -I
```

### "clBuildProgram(): CL_BUILD_PROGRAM_FAILURE"
```cmd
REM OpenCL-Treiber installieren:
REM NVIDIA: Im CUDA Toolkit enthalten
REM AMD: Im Adrenalin-Treiber enthalten
```

### Zu langsam trotz GPU?
```cmd
REM Workload erhöhen:
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt -w 4

REM Optimization disabled? Force enable:
hashcat -m 11300 -a 0 wallet_hash.txt rockyou.txt -O
```

---

## 🎯 Zusammenfassung - Was tun?

### Szenario: Passphrase völlig vergessen

**Schritt 1:** Hashcat installieren
```cmd
REM Download: https://hashcat.net/hashcat/
copy hashcat.exe C:\Users\alina\Downloads\btc_test\
```

**Schritt 2:** Große Wordlist herunterladen
```cmd
REM RockYou (14 Millionen):
REM https://github.com/brannondorsey/naive-hashcat/releases
```

**Schritt 3:** GPU Cracking starten
```cmd
cd C:\Users\alina\Downloads\btc_test

REM Automatisch:
py3 decrypt_wallet.py -w wallet.dat -g rockyou.txt -o found.json

REM ODER Batch-Menü:
decrypt_windows.bat
→ [3] GPU Cracking
```

**Schritt 4:** Warten (mit RTX 4090: ~10 Sekunden für 14 Millionen!)

**Schritt 5:** Bei Erfolg → Keys exportieren
```cmd
py3 extract_keys.py -w wallet.dat -p "gefundene_passphrase" -f all -o keys
```

---

## 🏆 Beste Strategie

**1. Zuerst: Eigene Passphrase-Ideen** (Option [1] oder [3] mit kleiner Liste)
- Alte Passwörter
- Wallet-Name + Jahr
- Variationen mit 123, !, etc.

**2. Dann: RockYou Wordlist** (Option [3] mit rockyou.txt)
- 14 Millionen häufigste Passwörter
- Mit GPU: ~10-60 Sekunden

**3. Falls nicht gefunden: Masken-Brute-Force**
- Wenn Sie Format kennen (z.B. "MyWallet" + 4 Ziffern)
- `hashcat -m 11300 -a 3 wallet_hash.txt MyWallet?d?d?d?d`

**4. Letzter Versuch: CrackStation (1.5 Milliarden)**
- Größte öffentliche Wordlist
- Mit RTX 4090: ~15-30 Minuten

---

**Mit >1 Million H/s sind Ihre Chancen VIEL höher! 🚀**

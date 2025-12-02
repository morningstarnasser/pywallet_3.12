# 🔓 Wallet Decryption Tools - Anleitung

Ich habe **2 spezialisierte Tools** erstellt, um verschlüsselte Private Keys zu extrahieren:

---

## 🛠️ Tool 1: `decrypt_wallet.py` - Passphrase Testing & Brute-Force

### Funktionen:
- ✅ **Interaktiver Modus** - Sichere Eingabe der Passphrase
- ✅ **Single Passphrase Test** - Teste eine einzelne Passphrase
- ✅ **Brute-Force / Dictionary Attack** - Teste tausende Passphrases automatisch
- ✅ **Hashcat/John Export** - Extrahiere Daten für externe Cracking-Tools

---

### 📋 Verwendung

#### **Modus 1: Interaktiv (empfohlen)**
```bash
python3 decrypt_wallet.py -w wallet.dat -i
```
- Fragt nach Passphrase (wird nicht angezeigt)
- Testet Passphrase
- Bei Erfolg: Speichert entschlüsselte Wallet

**Beispiel:**
```
INTERACTIVE WALLET DECRYPTION
======================================================================
Wallet: wallet.dat

Enter passphrase (input hidden): *********

Testing passphrase...

✓ SUCCESS! Passphrase is correct!

Save decrypted wallet to file? (y/n): y
Output filename [decrypted_wallet.json]: my_keys.json

✓ Decrypted wallet saved to: my_keys.json

Total keys decrypted: 15
First 3 decrypted private keys (WIF format):
  1. 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa: 5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF
  2. 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2: 5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf
  3. 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S: 5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn
```

---

#### **Modus 2: Single Passphrase Test**
```bash
python3 decrypt_wallet.py -w wallet.dat -p "MeinePassphrase123" -o decrypted.json
```

**Windows:**
```cmd
py3 decrypt_wallet.py -w wallet.dat -p "MeinePassphrase123" -o decrypted.json
```

---

#### **Modus 3: Brute-Force / Dictionary Attack**

Erstellen Sie eine Datei mit Passphrases (eine pro Zeile):

**passwords.txt:**
```
password123
MyWallet2015
SecretKey!
bitcoin2010
...
```

Dann starten Sie den Brute-Force:
```bash
python3 decrypt_wallet.py -w wallet.dat -l passwords.txt -o found_keys.json
```

**Ausgabe:**
```
PASSPHRASE BRUTE-FORCE / DICTIONARY ATTACK
======================================================================
Wallet: wallet.dat
Passphrase list: passwords.txt

Testing 10000 passphrases...

[10/10000] Tested 10 passphrases (2.5/sec, ETA: 3996s)
[20/10000] Tested 20 passphrases (2.8/sec, ETA: 3571s)
...

======================================================================
✓ SUCCESS! PASSPHRASE FOUND!
======================================================================
Passphrase: MyWallet2015
======================================================================

Decrypted wallet saved to: found_keys.json
```

**Performance:**
- ~2-5 Passphrases pro Sekunde (abhängig von Iterations)
- 10.000 Passphrases = ~30-90 Minuten
- 1 Million Passphrases = ~2-6 Tage

---

#### **Modus 4: Export für Hashcat/John the Ripper**

Für **schnelleres** Cracking (GPU-beschleunigt):

```bash
python3 decrypt_wallet.py -w wallet.dat -e
```

**Ausgabe:**
```
EXTRACTING ENCRYPTION INFO FOR PASSWORD CRACKING TOOLS
======================================================================
Wallet: wallet.dat

[MASTER KEY INFORMATION]
----------------------------------------------------------------------
Salt (hex): a1b2c3d4e5f67890
Iterations: 65432
Method: 0 (SHA512)
Encrypted Master Key (hex): fedcba9876543210...

[HASHCAT FORMAT]
----------------------------------------------------------------------
$bitcoin$64$fedcba9876543210...$a1b2c3d4e5f67890$65432$0$0

Usage:
  hashcat -m 11300 -a 0 hash.txt wordlist.txt
  (Mode 11300 = Bitcoin Core wallet)
```

Dann verwenden Sie **Hashcat** (100x schneller mit GPU):
```bash
# Hash in Datei speichern
echo '$bitcoin$64$...' > hash.txt

# Hashcat mit GPU
hashcat -m 11300 -a 0 hash.txt rockyou.txt

# Oder mit John the Ripper
john --format=bitcoin hash.txt --wordlist=rockyou.txt
```

---

## 🔑 Tool 2: `extract_keys.py` - Key Export in verschiedenen Formaten

Wenn Sie die **korrekte Passphrase** haben, extrahiert dieses Tool die Keys in verwendbaren Formaten.

### Funktionen:
- ✅ **JSON Export** - Vollständige Wallet-Daten
- ✅ **CSV Export** - Für Excel/Spreadsheets
- ✅ **TXT Export** - Einfache Textdatei
- ✅ **Electrum Format** - Direkt importierbar in Electrum Wallet
- ✅ **Summary Report** - Übersicht über alle Keys

---

### 📋 Verwendung

#### **Export als JSON (Standard)**
```bash
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -o keys.json
```

**Windows:**
```cmd
py3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -o keys.json
```

**Ausgabe: keys.json**
```json
{
  "keys": [
    {
      "addr": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "pubkey": "04678afdb0fe...",
      "sec": "5Kb8kLf9zgWQ...",
      "secret": "e9873d79c6d8...",
      "compressed": false
    }
  ]
}
```

---

#### **Export als CSV (Excel-kompatibel)**
```bash
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -f csv -o keys.csv
```

**Ausgabe: keys.csv**
```csv
Address,Private_Key_WIF,Private_Key_Hex,Public_Key,Compressed,Label
"1A1zP1eP...",5Kb8kLf9zgWQ...",e9873d79c6d8...","04678afdb0fe...",False,""
"1BvBMSEYs...",5HpHagT65TZz...",3aba4162c7be...","04c8a0e0f3e1...",False,"Savings"
```

**Öffnen mit Excel:**
1. Excel öffnen
2. Datei → Öffnen → `keys.csv`
3. Alle Keys sind in Spalten organisiert

---

#### **Export für Electrum Wallet**
```bash
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -f electrum -o electrum_import.txt
```

**Ausgabe: electrum_import.txt**
```
5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF
5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf
5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn
```

**Import in Electrum:**
1. Electrum öffnen
2. Wallet → Private Keys → Import
3. Inhalt von `electrum_import.txt` einfügen
4. ✓ Fertig - Keys sind importiert!

---

#### **Alle Formate auf einmal**
```bash
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -f all -o my_keys
```

**Erzeugt:**
- `my_keys.json` - JSON Format
- `my_keys.csv` - CSV/Excel Format
- `my_keys.txt` - Textformat (Address: WIF)
- `my_keys_electrum.txt` - Electrum-Import Format
- `my_keys_summary.txt` - Zusammenfassung

---

#### **Summary Report (Übersicht)**
```bash
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -f summary -o summary.txt
```

**Ausgabe: summary.txt**
```
WALLET EXTRACTION SUMMARY
======================================================================

[WALLET INFORMATION]
Version: 169900
Encrypted: Yes
Encryption iterations: 65432

[KEY STATISTICS]
Total keys: 15
Decrypted keys: 15
Compressed keys: 8
Uncompressed keys: 7

[ADDRESSES]
1. 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa - Private key: Yes
2. 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2 (Savings) - Private key: Yes
3. 12cbQLTFMXRnSzktFkuoG3eHoMeFtpTu3S - Private key: Yes
...
```

---

## 🎯 Vollständiger Workflow

### **Szenario 1: Sie kennen die Passphrase**

```bash
# Schritt 1: Interaktiv entschlüsseln
python3 decrypt_wallet.py -w wallet.dat -i

# Schritt 2: Keys in allen Formaten exportieren
python3 extract_keys.py -w wallet.dat -p "IhrePassphrase" -f all -o my_keys

# Fertig! Sie haben jetzt:
# - my_keys.json (volle Daten)
# - my_keys.csv (für Excel)
# - my_keys_electrum.txt (für Import)
# - my_keys_summary.txt (Übersicht)
```

---

### **Szenario 2: Passphrase vergessen - Dictionary Attack**

```bash
# Schritt 1: Erstellen Sie eine Passphrase-Liste
# Datei: possible_passwords.txt
cat > possible_passwords.txt << EOF
MyWallet2015
Bitcoin2010
SecretKey!
password123
Family2015
...
EOF

# Schritt 2: Brute-Force starten
python3 decrypt_wallet.py -w wallet.dat -l possible_passwords.txt -o found_keys.json

# Wenn gefunden: Exportieren
python3 extract_keys.py -w wallet.dat -p "gefundenes_passwort" -f all -o recovered_keys
```

---

### **Szenario 3: Passphrase völlig vergessen - Hashcat/John**

```bash
# Schritt 1: Extrahiere Hash für Hashcat
python3 decrypt_wallet.py -w wallet.dat -e > wallet_hash.txt

# Schritt 2: Hash formatieren (kopieren Sie die Hashcat-Zeile)
echo '$bitcoin$64$...' > hash.txt

# Schritt 3: Hashcat mit GPU (VIEL schneller!)
# Download: https://hashcat.net/hashcat/
# Wordlist: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

# GPU Brute-Force (Millionen Passphrases pro Sekunde!)
hashcat -m 11300 -a 0 hash.txt rockyou.txt

# Oder mit Masken (z.B. "Wallet" + 4 Ziffern)
hashcat -m 11300 -a 3 hash.txt 'Wallet?d?d?d?d'

# Wenn gefunden:
python3 extract_keys.py -w wallet.dat -p "gefundene_passphrase" -f all -o recovered
```

**Hashcat Performance:**
- CPU: ~100-1000 Hashes/sec
- GPU (GTX 1080): ~50.000-200.000 Hashes/sec
- GPU (RTX 4090): ~500.000+ Hashes/sec

Mit einer guten GPU können Sie **Millionen** von Passphrases in wenigen Stunden testen!

---

## 📚 Wordlists für Dictionary Attacks

**Beliebte Wordlists:**
- **RockYou** (14 Millionen): https://github.com/brannondorsey/naive-hashcat/releases
- **SecLists**: https://github.com/danielmiessler/SecLists
- **CrackStation**: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm

**Eigene Wordlist erstellen:**
```bash
# Kombiniere verschiedene Wörter
cat > custom.txt << EOF
# Wallet Namen
MyWallet
BitcoinWallet
Savings

# Jahre
2010
2015
2020

# Kombinationen (mit Tools wie crunch/hashcat)
EOF

# Crunch: Generiere alle Kombinationen
crunch 8 12 0123456789abcdefABCDEF -o generated.txt
```

---

## 🔐 Sicherheitshinweise

### ⚠️ WICHTIG:
1. **Niemals entschlüsselte Keys online speichern**
2. **Sofort nach Export offline gehen**
3. **Alle Exports mit GPG/7-Zip verschlüsseln**
4. **Original-Exports sicher löschen** (shred/srm)

### Sichere Verwendung:

```bash
# 1. Extrahieren
python3 extract_keys.py -w wallet.dat -p "..." -f all -o keys

# 2. Verschlüsseln
7z a -p -mhe=on keys.7z keys*
# oder
gpg -c keys.json

# 3. Original SICHER löschen
shred -vfz -n 10 keys*  # Linux
# oder
srm keys*  # macOS mit srm installiert

# 4. Verschlüsseltes Archiv auf USB sichern
mv keys.7z /media/usb-stick/

# 5. Computer neu starten (löscht RAM)
```

---

## ❓ Troubleshooting

### "No decrypted private keys found"
→ **Passphrase ist falsch** oder Wallet nicht verschlüsselt

### "Command timed out"
→ Wallet hat sehr viele Iterations (>100k), erhöhe Timeout im Code

### "Could not parse JSON output"
→ Überprüfe pywallet.py Installation
```bash
python3 pywallet.py -w wallet.dat -d
```

### Brute-Force zu langsam
→ Verwende **Hashcat mit GPU** statt Dictionary Attack (100-1000x schneller!)

---

## 🚀 Quick Start - Windows

```cmd
cd C:\Users\alina\Downloads\btc_test

REM Interaktiv (empfohlen)
py3 decrypt_wallet.py -w wallet.dat -i

REM Oder mit bekannter Passphrase
py3 decrypt_wallet.py -w wallet.dat -p "MeinPasswort" -o decrypted.json

REM Keys exportieren
py3 extract_keys.py -w wallet.dat -p "MeinPasswort" -f all -o my_keys

REM Für Hashcat vorbereiten
py3 decrypt_wallet.py -w wallet.dat -e > hash.txt
```

---

## 📊 Zusammenfassung

| Tool | Zweck | Wann verwenden |
|------|-------|----------------|
| `decrypt_wallet.py -i` | Interaktive Entschlüsselung | Passphrase bekannt |
| `decrypt_wallet.py -l` | Dictionary Attack | Passphrase vergessen, Liste vorhanden |
| `decrypt_wallet.py -e` | Hashcat/John Export | Passphrase vergessen, GPU verfügbar |
| `extract_keys.py -f all` | Alle Formate exportieren | Nach erfolgreicher Entschlüsselung |

---

**Viel Erfolg beim Extrahieren Ihrer Keys! 🔓**

# PyWallet Extraction Guide - Verschlüsselte Wallets

## 🔑 Was kann extrahiert werden?

### OHNE Passphrase (Verschlüsselte Wallet):
PyWallet kann folgende Informationen **ohne Passphrase** extrahieren:

✅ **Master Key Encryption Info:**
- Salt (für Key-Derivation)
- Iterations/Rounds (PBKDF2-Iterationen)
- Derivation Method
- Verschlüsselter Master Key (hex)

✅ **Public Keys & Adressen:**
- Alle Bitcoin-Adressen
- Public Keys (nicht verschlüsselt!)
- Komprimierungsstatus

✅ **Verschlüsselte Private Keys:**
- Verschlüsselte Private Keys (hex-encoded)
- Diese können SPÄTER mit der richtigen Passphrase entschlüsselt werden

✅ **Wallet Metadata:**
- Version
- Key Pool
- Transaktionen
- Labels/Namen

### MIT Passphrase:
✅ Alle oben genannten Daten PLUS:
- **Entschlüsselte Private Keys (WIF-Format)**
- Direkt verwendbare Private Keys für Import

---

## 📋 Nutzung - Schritt für Schritt

### 1. Basis-Extraktion (OHNE Passphrase)
Zeigt alle verfügbaren Informationen für verschlüsselte Wallet:

```bash
python3 pywallet.py -w wallet.dat
```

**Ausgabe:**
- Master Key Encryption Info (Salt, Iterations, verschlüsselter Master Key)
- Anzahl verschlüsselter Keys
- Sample von ersten 3 Keys (Address, Public Key, Encrypted Private Key)

### 2. Vollständiger JSON-Dump (OHNE Passphrase)
Extrahiert ALLE Daten als JSON (auch verschlüsselte Keys):

```bash
python3 pywallet.py -w wallet.dat -d > wallet_dump_encrypted.json
```

**Was ist im JSON:**
```json
{
  "keys": [
    {
      "addr": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "pubkey": "04...",
      "encrypted_privkey": "a1b2c3...",  // ← Verschlüsselt!
      "compressed": false
    }
  ],
  "mkey": {
    "salt": "1234567890abcdef",
    "nDerivationIterations": 65432,
    "encrypted_key": "fedcba..."  // ← Verschlüsselter Master Key
  }
}
```

### 3. Nur Adressen extrahieren
```bash
python3 pywallet.py -w wallet.dat -d --dumpformat=addr > addresses.txt
```

### 4. Mit Passphrase (Private Keys entschlüsseln)
```bash
python3 pywallet.py -w wallet.dat --passphrase "IhrePassphrase" -d > wallet_dump_decrypted.json
```

**Was ist jetzt NEU im JSON:**
```json
{
  "keys": [
    {
      "addr": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "pubkey": "04...",
      "secret": "...",          // ← NEU: Entschlüsselter Private Key (hex)
      "sec": "5Kb8kLf9...",     // ← NEU: Private Key im WIF-Format
      "compressed": false
    }
  ]
}
```

---

## 🛠️ Erweiterte Optionen

### Neuere Bitcoin Core Versionen
Falls Sie die Warnung "Version mismatch" sehen:

**Automatisch behoben:** Die neue Version unterstützt bereits Versionen bis 200000 (Bitcoin Core ~23+)

Falls immer noch Probleme:
```bash
python3 pywallet.py -w wallet.dat --dont_check_walletversion -d
```

### Alle Optionen anzeigen
```bash
python3 pywallet.py --help
```

---

## 💡 Anwendungsfälle

### Fall 1: Passphrase vergessen - Was kann ich tun?
**Sie können extrahieren:**
1. ✅ Salt und Iterations → für Passphrase-Recovery-Tools (hashcat, John the Ripper)
2. ✅ Verschlüsselte Private Keys → zur späteren Entschlüsselung
3. ✅ Adressen → um zu prüfen ob Guthaben vorhanden ist

**Workflow:**
```bash
# 1. Extrahieren Sie alle Daten
python3 pywallet.py -w wallet.dat -d > encrypted_backup.json

# 2. Prüfen Sie Adressen auf Guthaben
python3 pywallet.py -w wallet.dat -d --dumpformat=addr > addresses.txt
# Dann: Adressen auf blockchain.info/blockexplorer prüfen

# 3. Für Passphrase-Recovery: Salt + Iterations aus JSON extrahieren
# Nutzen Sie Tools wie hashcat mit dem Salt/Encrypted Master Key
```

### Fall 2: Backup-Zwecke
**Empfehlung:** Speichern Sie BEIDE Versionen:

```bash
# Verschlüsselte Version (sicher zu speichern)
python3 pywallet.py -w wallet.dat -d > backup_encrypted.json

# Entschlüsselte Version (NUR offline, verschlüsselt aufbewahren!)
python3 pywallet.py -w wallet.dat --passphrase "..." -d > backup_decrypted.json

# Komprimieren und verschlüsseln
tar -czf backup.tar.gz backup_*.json
gpg -c backup.tar.gz  # Mit neuem Passwort verschlüsseln
rm backup_*.json backup.tar.gz  # Originale löschen
```

### Fall 3: Migration zu anderer Software
**Private Keys im WIF-Format exportieren:**

```bash
# 1. JSON-Dump mit entschlüsselten Keys
python3 pywallet.py -w wallet.dat --passphrase "..." -d > wallet.json

# 2. Private Keys (sec/WIF) extrahieren aus JSON
# Jeder "sec"-Eintrag ist ein importierbarer Private Key

# 3. Import in andere Wallet (z.B. Electrum)
# → "Import Private Key" → WIF-String einfügen
```

---

## 🔐 Sicherheitshinweise

### ⚠️ WICHTIG - Private Keys
1. **Niemals unverschlüsselte Dumps online speichern**
2. **Sofort nach Export offline gehen**
3. **Dumps mit GPG/7-Zip verschlüsseln**
4. **Originaldateien sicher löschen** (mit shred/srm, nicht nur delete)

### ⚠️ Passphrase über Kommandozeile
```bash
# SCHLECHT (bleibt in Shell-History):
python3 pywallet.py -w wallet.dat --passphrase "meinPasswort123"

# BESSER (prompt):
# Aktuell nicht implementiert - verwenden Sie Vorsicht!

# WORKAROUND (aus Datei lesen - später implementiert):
# python3 pywallet.py -w wallet.dat --passphrase-file secret.txt
```

**Aktueller Workaround:**
```bash
# Löschen Sie die Shell-History nach Verwendung:
history -c  # (bash)
# oder
Clear-History  # (PowerShell)
```

---

## 📊 Was bedeuten die Felder?

### Master Key (mkey):
- **salt**: Zufälliger Wert für PBKDF2-Key-Derivation
- **nDerivationIterations**: Anzahl PBKDF2-Iterationen (meist 25000-100000)
- **nDerivationMethod**: Methode (0 = SHA512)
- **encrypted_key**: Der verschlüsselte Master Key (AES-256)

### Keys:
- **addr**: Bitcoin-Adresse (P2PKH/P2SH)
- **pubkey**: Public Key (hex) - NICHT verschlüsselt!
- **encrypted_privkey**: Verschlüsselter Private Key (hex)
- **secret**: Entschlüsselter Private Key (hex) - NUR mit Passphrase
- **sec**: Private Key im WIF-Format (importierbar) - NUR mit Passphrase
- **compressed**: True = komprimierter Key (33 bytes pubkey)

---

## ❓ Troubleshooting

### "The wallet is encrypted but no passphrase is used"
✅ **Das ist KEIN Fehler!** Das Tool zeigt trotzdem alle verfügbaren Informationen.

### "Version mismatch (must be <= 200000)"
✅ **Bereits behoben** in dieser Version. Falls weiterhin Probleme:
```bash
python3 pywallet.py -w wallet.dat --dont_check_walletversion -d
```

### Leere/Unvollständige Ausgabe
```bash
# Prüfen Sie die Wallet-Datei:
file wallet.dat
# Sollte "Berkeley DB" zeigen

# Prüfen Sie Berechtigungen:
ls -la wallet.dat
```

### "bsddb not found"
```bash
# macOS:
brew install berkeley-db@5
export BERKELEYDB_DIR=$(brew --prefix berkeley-db@5)
pip install bsddb3

# Linux:
sudo apt install libdb-dev libdb5.3-dev
pip install bsddb3
```

---

## 🎯 Zusammenfassung - Was tun?

### Szenario 1: Passphrase bekannt
```bash
python3 pywallet.py -w wallet.dat --passphrase "IhrPasswort" -d > full_dump.json
```
→ Erhalten Sie ALLE Daten inklusive entschlüsselter Private Keys

### Szenario 2: Passphrase vergessen
```bash
# Schritt 1: Alle verfügbaren Daten extrahieren
python3 pywallet.py -w wallet.dat -d > encrypted_dump.json

# Schritt 2: Master Key Info für Passphrase-Recovery
# Suchen Sie im JSON nach "salt", "nDerivationIterations", "encrypted_key"

# Schritt 3: Nutzen Sie Tools wie hashcat/John the Ripper
# mit den extrahierten Werten für Brute-Force/Dictionary-Attack
```

### Szenario 3: Nur Adressen prüfen
```bash
python3 pywallet.py -w wallet.dat -d --dumpformat=addr
```
→ Liste aller Adressen (auch ohne Passphrase!)

---

**Viel Erfolg beim Extrahieren! 🚀**

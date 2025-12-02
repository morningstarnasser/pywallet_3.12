#!/usr/bin/env python3
"""
extract_keys.py - Extrahiert Private Keys aus wallet.dat in verschiedenen Formaten

Dieses Tool extrahiert entschlüsselte Private Keys und exportiert sie in
verschiedenen verwendbaren Formaten.
"""

import sys
import os
import json
import argparse
import subprocess


def extract_keys_json(wallet_file, passphrase, output_format='all'):
    """Extrahiert Keys als JSON"""
    cmd = [
        'python3', 'pywallet.py',
        '-w', wallet_file,
        '--passphrase', passphrase,
        '-d'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"ERROR: pywallet.py exited with code {result.returncode}")
            print(result.stderr)
            return None

        data = json.loads(result.stdout)
        return data

    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON output: {e}")
        print("Output was:")
        print(result.stdout[:500])
        return None
    except subprocess.TimeoutExpired:
        print("ERROR: Command timed out after 30 seconds")
        return None
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return None


def export_to_csv(data, output_file):
    """Exportiert Keys als CSV"""
    print(f"\nExporting to CSV: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("Address,Private_Key_WIF,Private_Key_Hex,Public_Key,Compressed,Label\n")

        if 'keys' not in data:
            print("WARNING: No keys found in wallet data")
            return 0

        count = 0
        for key in data['keys']:
            addr = key.get('addr', '')
            wif = key.get('sec', '')
            hexkey = key.get('secret', '')
            pubkey = key.get('pubkey', '')
            compressed = key.get('compressed', False)
            label = key.get('label', '')

            # Only export if we have a private key
            if wif or hexkey:
                f.write(f'"{addr}","{wif}","{hexkey}","{pubkey}",{compressed},"{label}"\n')
                count += 1

        print(f"✓ Exported {count} keys to CSV")
        return count


def export_to_txt(data, output_file, format_type='wif'):
    """Exportiert Keys als einfache Textdatei"""
    print(f"\nExporting to TXT: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        if 'keys' not in data:
            print("WARNING: No keys found in wallet data")
            return 0

        count = 0
        for key in data['keys']:
            addr = key.get('addr', '')
            wif = key.get('sec', '')
            hexkey = key.get('secret', '')

            if format_type == 'wif' and wif:
                f.write(f"{addr}: {wif}\n")
                count += 1
            elif format_type == 'hex' and hexkey:
                f.write(f"{addr}: {hexkey}\n")
                count += 1
            elif format_type == 'both' and (wif or hexkey):
                f.write(f"{addr}\n")
                if wif:
                    f.write(f"  WIF: {wif}\n")
                if hexkey:
                    f.write(f"  HEX: {hexkey}\n")
                f.write("\n")
                count += 1

        print(f"✓ Exported {count} keys to TXT")
        return count


def export_to_electrum(data, output_file):
    """Exportiert Keys im Electrum-kompatiblen Format"""
    print(f"\nExporting to Electrum format: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        if 'keys' not in data:
            print("WARNING: No keys found in wallet data")
            return 0

        count = 0
        for key in data['keys']:
            wif = key.get('sec', '')

            # Electrum import format: one WIF per line
            if wif:
                f.write(f"{wif}\n")
                count += 1

        print(f"✓ Exported {count} keys in Electrum format")
        print("\nTo import into Electrum:")
        print(f"  1. Open Electrum wallet")
        print(f"  2. Go to: Wallet → Private Keys → Import")
        print(f"  3. Paste the contents of {output_file}")
        return count


def export_summary(data, output_file):
    """Erstellt eine Zusammenfassung"""
    print(f"\nCreating summary: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("WALLET EXTRACTION SUMMARY\n")
        f.write("="*70 + "\n\n")

        # Wallet info
        f.write("[WALLET INFORMATION]\n")
        f.write(f"Version: {data.get('version', 'N/A')}\n")
        f.write(f"Encrypted: {'Yes' if data.get('mkey', {}) else 'No'}\n")

        if 'mkey' in data and data['mkey']:
            mkey = data['mkey']
            f.write(f"Encryption iterations: {mkey.get('nDerivationIterations', 'N/A')}\n")

        f.write("\n")

        # Key statistics
        if 'keys' in data:
            total_keys = len(data['keys'])
            decrypted_keys = sum(1 for k in data['keys'] if 'sec' in k)
            compressed_keys = sum(1 for k in data['keys'] if k.get('compressed', False))

            f.write("[KEY STATISTICS]\n")
            f.write(f"Total keys: {total_keys}\n")
            f.write(f"Decrypted keys: {decrypted_keys}\n")
            f.write(f"Compressed keys: {compressed_keys}\n")
            f.write(f"Uncompressed keys: {total_keys - compressed_keys}\n")
            f.write("\n")

            # List all addresses
            f.write("[ADDRESSES]\n")
            for i, key in enumerate(data['keys'], 1):
                addr = key.get('addr', 'N/A')
                label = key.get('label', '')
                has_privkey = 'Yes' if 'sec' in key else 'No'

                f.write(f"{i}. {addr}")
                if label:
                    f.write(f" ({label})")
                f.write(f" - Private key: {has_privkey}\n")

        print("✓ Summary created")


def main():
    parser = argparse.ArgumentParser(
        description='Extract and export private keys from wallet.dat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all keys to JSON
  python3 extract_keys.py -w wallet.dat -p "password" -o keys.json

  # Extract to CSV
  python3 extract_keys.py -w wallet.dat -p "password" -f csv -o keys.csv

  # Extract to multiple formats
  python3 extract_keys.py -w wallet.dat -p "password" -f all -o keys

  # Create summary only
  python3 extract_keys.py -w wallet.dat -p "password" -f summary -o summary.txt
        """
    )

    parser.add_argument('-w', '--wallet', required=True,
                        help='Path to wallet.dat file')

    parser.add_argument('-p', '--passphrase', required=True,
                        help='Wallet passphrase')

    parser.add_argument('-f', '--format', default='json',
                        choices=['json', 'csv', 'txt', 'electrum', 'summary', 'all'],
                        help='Output format (default: json)')

    parser.add_argument('-o', '--output', required=True,
                        help='Output file (or base name for "all" format)')

    args = parser.parse_args()

    if not os.path.exists(args.wallet):
        print(f"ERROR: Wallet file not found: {args.wallet}")
        sys.exit(1)

    print("="*70)
    print("PRIVATE KEY EXTRACTION")
    print("="*70)
    print(f"Wallet: {args.wallet}")
    print(f"Format: {args.format}")
    print("\nExtracting keys with pywallet...")

    # Extract keys
    data = extract_keys_json(args.wallet, args.passphrase)

    if not data:
        print("\n✗ Failed to extract keys. Check passphrase and wallet file.")
        sys.exit(1)

    # Check if passphrase was correct
    if 'keys' in data and len(data['keys']) > 0:
        has_decrypted = any('sec' in k for k in data['keys'])
        if not has_decrypted:
            print("\n✗ WARNING: No decrypted private keys found.")
            print("   The passphrase may be incorrect, or the wallet is not encrypted.")
            sys.exit(1)

    print("✓ Keys extracted successfully")

    # Export in requested format(s)
    if args.format == 'json':
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✓ Saved to: {args.output}")

    elif args.format == 'csv':
        export_to_csv(data, args.output)

    elif args.format == 'txt':
        export_to_txt(data, args.output, format_type='both')

    elif args.format == 'electrum':
        export_to_electrum(data, args.output)

    elif args.format == 'summary':
        export_summary(data, args.output)

    elif args.format == 'all':
        base_name = args.output

        # JSON
        export_to_csv(data, f"{base_name}.csv")
        export_to_txt(data, f"{base_name}.txt", format_type='both')
        export_to_electrum(data, f"{base_name}_electrum.txt")
        export_summary(data, f"{base_name}_summary.txt")

        with open(f"{base_name}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n✓ All formats exported with base name: {base_name}")

    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()

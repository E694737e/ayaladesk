#!/usr/bin/env bash
# AyalaDesk branding on top of stock RustDesk. Run from the repo root, after the
# submodules are checked out and before building. Fails loudly if any target text
# is missing, so an upstream change can't silently ship an unbranded build.
set -euo pipefail
B=ayaladesk
HOST="91.99.1.3"
KEY="5WNbaKlprz+M15fKt521JVUVJc9uBJlXbtUOlsu+kSE="

sub() { # file, old (literal), new (literal)
  python3 - "$1" "$2" "$3" <<'PY'
import sys
f, old, new = sys.argv[1:]
s = open(f, encoding="utf-8").read()
if old not in s:
    sys.exit(f"BRANDING: '{old}' not found in {f}")
open(f, "w", encoding="utf-8", newline="").write(s.replace(old, new))
print(f"branded {f}")
PY
}

C=libs/hbb_common/src/config.rs
sub "$C" 'RwLock::new("RustDesk".to_owned())' 'RwLock::new("AyalaDesk".to_owned())'
sub "$C" 'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];' "pub const RENDEZVOUS_SERVERS: &[&str] = &[\"$HOST\"];"
sub "$C" 'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";' "pub const RS_PUB_KEY: &str = \"$KEY\";"

sub Cargo.toml 'ProductName = "RustDesk"' 'ProductName = "AyalaDesk"'
sub Cargo.toml 'FileDescription = "RustDesk Remote Desktop"' 'FileDescription = "AyalaDesk Remote Support"'
sub Cargo.toml 'LegalCopyright = "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved."' 'LegalCopyright = "AyalaDesk, based on RustDesk (AGPL-3.0)"'

R=flutter/windows/runner/Runner.rc
sub "$R" 'VALUE "CompanyName", "Purslane Tech Pte. Ltd." "\0"' 'VALUE "CompanyName", "Ayala" "\0"'
sub "$R" 'VALUE "FileDescription", "RustDesk Remote Desktop" "\0"' 'VALUE "FileDescription", "AyalaDesk Remote Support" "\0"'
sub "$R" 'VALUE "LegalCopyright", "Copyright © 2026 Purslane Tech Pte. Ltd. All rights reserved." "\0"' 'VALUE "LegalCopyright", "AyalaDesk, based on RustDesk (AGPL-3.0)" "\0"'
sub "$R" 'VALUE "ProductName", "RustDesk" "\0"' 'VALUE "ProductName", "AyalaDesk" "\0"'

# Icons and logos
cp $B/logo.ico res/icon.ico
cp $B/logo.ico res/tray-icon.ico
cp $B/logo.ico flutter/windows/runner/resources/app_icon.ico
cp $B/logo-256.png res/icon.png
cp $B/logo-32.png res/32x32.png
cp $B/logo-64.png res/64x64.png
cp $B/logo-128.png res/128x128.png
cp $B/logo-256.png res/128x128@2x.png
cp $B/logo.svg flutter/assets/icon.svg
cp $B/logo-256.png flutter/assets/icon.png
echo "AyalaDesk branding applied"

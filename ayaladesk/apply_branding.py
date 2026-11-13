"""AyalaDesk branding on top of stock RustDesk.

Run from the repo root after submodules are checked out, before building:
    python3 ayaladesk/apply_branding.py

Every edit is a whole-line regex replacement, so CRLF/LF checkouts and non-ASCII
text (the copyright sign) don't matter. If a target line is missing it fails with a
GitHub '::error::' annotation, so an upstream change can't silently ship unbranded.
"""
import re
import shutil
import sys
from pathlib import Path

HOST = "91.99.1.3"
KEY = "5WNbaKlprz+M15fKt521JVUVJc9uBJlXbtUOlsu+kSE="
NAME = "AyalaDesk"
DESC = "AyalaDesk Remote Support"
COPY = "AyalaDesk, based on RustDesk (AGPL-3.0)"
B = Path("ayaladesk")


def fail(msg):
    print(f"::error::BRANDING: {msg}")
    sys.exit(1)


def sub_line(path, pattern, replacement):
    """Replace every line matching `pattern` (regex on the line, without EOL)."""
    p = Path(path)
    data = p.read_bytes().decode("utf-8")
    lines = data.split("\n")
    rx = re.compile(pattern)
    hits = 0
    for i, ln in enumerate(lines):
        body, cr = (ln[:-1], "\r") if ln.endswith("\r") else (ln, "")
        if rx.search(body):
            indent = body[: len(body) - len(body.lstrip())]
            lines[i] = indent + replacement + cr
            hits += 1
    if not hits:
        fail(f"pattern {pattern!r} not found in {path}")
    p.write_bytes("\n".join(lines).encode("utf-8"))
    print(f"branded {path}: {pattern} ({hits})")



def main():
    C = "libs/hbb_common/src/config.rs"
    sub_line(C, r'pub static ref APP_NAME: RwLock<String> = RwLock::new\("RustDesk"',
             f'pub static ref APP_NAME: RwLock<String> = RwLock::new("{NAME}".to_owned());')
    sub_line(C, r'^pub const RENDEZVOUS_SERVERS: ',
             f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{HOST}"];')
    sub_line(C, r'^pub const RS_PUB_KEY: ',
             f'pub const RS_PUB_KEY: &str = "{KEY}";')

    sub_line("Cargo.toml", r'^ProductName = "RustDesk"', f'ProductName = "{NAME}"')
    sub_line("Cargo.toml", r'^FileDescription = "RustDesk', f'FileDescription = "{DESC}"')
    sub_line("Cargo.toml", r'^LegalCopyright = ', f'LegalCopyright = "{COPY}"')

    # The single-file wrapper (what the customer actually double-clicks)
    P = "libs/portable/Cargo.toml"
    sub_line(P, r'^ProductName = "RustDesk"', f'ProductName = "{NAME}"')
    sub_line(P, r'^FileDescription = "RustDesk', f'FileDescription = "{DESC}"')
    sub_line(P, r'^LegalCopyright = ', f'LegalCopyright = "{COPY}"')
    sub_line(P, r'^OriginalFilename = ', f'OriginalFilename = "{NAME}.exe"')

    R = "flutter/windows/runner/Runner.rc"
    sub_line(R, r'VALUE "CompanyName",', 'VALUE "CompanyName", "Ayala" "\\0"')
    sub_line(R, r'VALUE "FileDescription",', f'VALUE "FileDescription", "{DESC}" "\\0"')
    sub_line(R, r'VALUE "LegalCopyright",', f'VALUE "LegalCopyright", "{COPY}" "\\0"')
    sub_line(R, r'VALUE "ProductName",', f'VALUE "ProductName", "{NAME}" "\\0"')

    for src, dst in [
        ("logo.ico", "res/icon.ico"),
        ("logo.ico", "res/tray-icon.ico"),
        ("logo.ico", "flutter/windows/runner/resources/app_icon.ico"),
        ("logo-256.png", "res/icon.png"),
        ("logo-32.png", "res/32x32.png"),
        ("logo-64.png", "res/64x64.png"),
        ("logo-128.png", "res/128x128.png"),
        ("logo-256.png", "res/128x128@2x.png"),
        ("logo.svg", "flutter/assets/icon.svg"),
        ("logo-256.png", "flutter/assets/icon.png"),
    ]:
        if not Path(dst).parent.is_dir():
            fail(f"missing folder for {dst}")
        shutil.copyfile(B / src, dst)
        print(f"icon {dst}")

    print("AyalaDesk branding applied")


if __name__ == "__main__":
    import os, traceback
    print("cwd", os.getcwd(), "python", sys.version)
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        tb = traceback.format_exc().replace(chr(10), " | ")
        print(f"::error::BRANDING crashed: {tb}")
        sys.exit(1)

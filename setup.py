"""
Installation script for aerocement-calc package and CLI.

Run once to set up directories and symlink the CLI to /data/data/com.termux/files/home/bin/
"""

import sys
from pathlib import Path

HOME = Path("/data/data/com.termux/files/home")
AERO_PKG = HOME / "aerocement" / "aerocement_calc"
BIN_DIR = HOME / "bin"
REPO_DIR = Path(__file__).parent

print("AeroCement CPF Blender Setup")
print("=" * 50)

# Ensure bin directory exists
BIN_DIR.mkdir(parents=True, exist_ok=True)
print(f"✓ Bin directory: {BIN_DIR}")

# Ensure aerocement package directory exists
AERO_PKG.parent.mkdir(parents=True, exist_ok=True)
print(f"✓ Package directory: {AERO_PKG.parent}")

# Copy or symlink package files
for src_file in [REPO_DIR / "aerocement_calc" / "cpf_blender.py",
                  REPO_DIR / "aerocement_calc" / "__init__.py"]:
    if src_file.exists():
        dst_file = AERO_PKG / src_file.name
        dst_file.write_text(src_file.read_text())
        print(f"✓ Copied {src_file.name} to {dst_file}")

# Symlink or copy CLI
cli_src = REPO_DIR / "bin" / "cpf_blend.py"
cli_dst = BIN_DIR / "cpf_blend.py"
if cli_src.exists():
    cli_dst.write_text(cli_src.read_text())
    cli_dst.chmod(0o755)
    print(f"✓ CLI installed: {cli_dst}")

print("\n" + "=" * 50)
print("Setup complete. Usage:")
print(f"  python3 {cli_dst} card --v0 250 --jar 1500")
print(f"  python3 {cli_dst} take --v0 250 --vobs 960 --t 45 --batch GEL12-001")
print(f"  python3 {cli_dst} ledger")

#!/usr/bin/env python3
"""
CPF Blender CLI: card generation, take logging, and ledger management.

Usage:
  python3 /data/data/com.termux/files/home/bin/cpf_blend.py card --v0 250 --jar 1500
  python3 /data/data/com.termux/files/home/bin/cpf_blend.py take --v0 250 --vobs 960 --t 45 --batch GEL12-001
  python3 /data/data/com.termux/files/home/bin/cpf_blend.py ledger

Writes JSON lines to:
  /sdcard/openroot/ledger/cpf_blender.jsonl
  /sdcard/openroot/context_bridge/cpf_last.json
  /sdcard/openroot/agape_kb/cpf_jar_card.md
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

# PYTHONPATH insertion for aerocement package
HOME = Path("/data/data/com.termux/files/home")
sys.path.insert(0, str(HOME / "aerocement"))

from aerocement_calc.cpf_blender import (
    line_ml, v0_max_ml, calibration_card, take_record
)


LEDGER_PATH = Path("/sdcard/openroot/ledger/cpf_blender.jsonl")
BRIDGE_PATH = Path("/sdcard/openroot/context_bridge/cpf_last.json")
CARD_PATH = Path("/sdcard/openroot/agape_kb/cpf_jar_card.md")


def ensure_dirs():
    """Create output directories if missing."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    BRIDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CARD_PATH.parent.mkdir(parents=True, exist_ok=True)


def cmd_card(args):
    """Generate and display calibration card."""
    v0 = float(args.v0)
    jar = float(args.jar)
    
    card_text = calibration_card(v0, jar)
    print(card_text)
    
    # Also write to agape_kb
    ensure_dirs()
    md_content = f"""# CPF Blender Calibration Card

Generated: {datetime.now(timezone.utc).isoformat()}

## Settings
- V0 = {v0:.0f} ml
- Jar working volume = {jar:.0f} ml

## Lines (meniscus read at eye level, stop blending when foam hits line)

| Target | φ (void fraction) | V_line (ml) |
|--------|-------------------|------------|
| SC     | π/6 ≈ 0.5236      | {line_ml(v0, 'SC'):.1f} |
| RCP    | ≈ 0.64            | {line_ml(v0, 'RCP'):.1f} |
| CPF    | π/(3√2) ≈ 0.7405  | {line_ml(v0, 'CPF'):.1f} |
| OPEN   | 0.80              | {line_ml(v0, 'OPEN'):.1f} |

## Safety Limits
- V0_max for CPF target (10% headspace) = {v0_max_ml(jar, 'CPF'):.0f} ml

## Procedure
1. Charge blender with V0 ml of gel : cement (1:2 by volume)
2. Blend at full speed. Watch the foam surface rise toward your target line.
3. Stop power the instant meniscus kisses the line.
4. Wait 30 s. Read V_obs at eye level (meniscus center).
5. Photograph jar against this card.
6. Log the take: batch_id, path (GEL12|CS11|CS12), V_obs, blend time.

## Notes
- φ from this test = BULK VOID FRACTION only. Not proof of FCC, HCP, or Fuller VE.
- Smaller bubbles at same line = same φ, higher frequency, better Gibson-Ashby crush strength.
- 21-day wet cure remains mandatory for strength cubes.
- Fiber is last, low speed. Stator/blender shear is for bubbles, not filaments.
"""
    CARD_PATH.write_text(md_content)
    print(f"\n→ Card written to {CARD_PATH}")


def cmd_take(args):
    """Log a single blender take to ledger."""
    ensure_dirs()
    
    batch_id = args.batch
    path = args.path or "GEL12"
    V0_ml = float(args.v0)
    V_obs_ml = float(args.vobs)
    t_blend_s = float(args.t)
    target = args.target or "CPF"
    jar_working_ml = float(args.jar) if args.jar else 1500
    collapse_frac = float(args.collapse) if args.collapse else 0.0
    notes = args.notes or ""
    
    V_line_target = line_ml(V0_ml, target)
    
    record = take_record(
        batch_id=batch_id,
        path=path,
        V0_ml=V0_ml,
        V_obs_ml=V_obs_ml,
        V_line_target_ml=V_line_target,
        target=target,
        t_blend_s=t_blend_s,
        jar_working_ml=jar_working_ml,
        collapse_frac=collapse_frac,
        notes=notes
    )
    
    # Append to JSONL ledger
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")
    
    # Write bridge (last take)
    BRIDGE_PATH.write_text(json.dumps(record, indent=2))
    
    # Pretty print result
    print(f"\n✓ Take logged: {batch_id}")
    print(f"  path:      {record['path']}")
    print(f"  take:      {record['take']}")
    print(f"  φ_air:     {record['phi_air']:.4f}")
    print(f"  ρ*/ρs:     {record['rho_rel']:.4f}")
    print(f"  ρ_est:     {record['rho_est_kg_m3']:.0f} kg/m³")
    print(f"  blend_t:   {record['t_blend_s']:.1f} s")
    print(f"  η_proxy:   {record['eta_proxy']:.1f}")
    print(f"  synergy:   {record['synergy_mult']:.3f}")
    print(f"\n→ Ledger: {LEDGER_PATH}")
    print(f"→ Bridge: {BRIDGE_PATH}")
    
    # Try to call bridge hook if it exists
    bridge_hook = HOME / "bin" / "bridge.py"
    if bridge_hook.exists():
        import subprocess
        try:
            subprocess.run(
                ["python3", str(bridge_hook), "seed", f"--input={BRIDGE_PATH}"],
                check=False,
                timeout=10
            )
            print(f"→ Bridge hook executed")
        except Exception as e:
            print(f"⚠ Bridge hook failed (non-fatal): {e}")


def cmd_ledger(args):
    """Display ledger summary."""
    ensure_dirs()
    
    if not LEDGER_PATH.exists():
        print("Ledger is empty.")
        return
    
    records = []
    with open(LEDGER_PATH, "r") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    print(f"\nLedger: {len(records)} takes")
    print("-" * 100)
    print(f"{'batch_id':<15} {'path':<6} {'take':<10} {'V0':<6} {'V_obs':<6} {'φ':<7} {'ρ*/ρs':<7} {'η':<3}")
    print("-" * 100)
    
    for rec in records:
        print(f"{rec['batch_id']:<15} {rec['path']:<6} {rec['take']:<10} "
              f"{rec['V0_ml']:<6.0f} {rec['V_obs_ml']:<6.0f} "
              f"{rec['phi_air']:<7.4f} {rec['rho_rel']:<7.4f} {rec['eta_proxy']:<3.1f}")
    
    print("-" * 100)
    hit_count = sum(1 for r in records if r["take"] == "HIT")
    total_eta = sum(r["eta_proxy"] for r in records)
    avg_synergy = sum(r["synergy_mult"] for r in records) / len(records) if records else 0
    print(f"HITs: {hit_count}/{len(records)} | Σ(η): {total_eta:.1f} | ⟨synergy⟩: {avg_synergy:.3f}")


def main():
    parser = argparse.ArgumentParser(
        description="AeroCement CPF blender calibration CLI"
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Command")
    
    # card subcommand
    card_parser = subparsers.add_parser("card", help="Generate calibration card")
    card_parser.add_argument("--v0", required=True, help="Initial volume (ml)")
    card_parser.add_argument("--jar", required=True, help="Jar working volume (ml)")
    card_parser.set_defaults(func=cmd_card)
    
    # take subcommand
    take_parser = subparsers.add_parser("take", help="Log a blender take")
    take_parser.add_argument("--v0", required=True, help="Initial volume (ml)")
    take_parser.add_argument("--vobs", required=True, help="Observed volume (ml)")
    take_parser.add_argument("--t", required=True, help="Blend time (s)")
    take_parser.add_argument("--batch", required=True, help="Batch ID (e.g. GEL12-001)")
    take_parser.add_argument("--path", help="Path: GEL12|CS11|CS12 (default GEL12)")
    take_parser.add_argument("--target", help="Target: SC|RCP|CPF|OPEN (default CPF)")
    take_parser.add_argument("--jar", help="Jar working volume (ml, default 1500)")
    take_parser.add_argument("--collapse", help="Collapse fraction after 30s settle")
    take_parser.add_argument("--notes", help="Free-text notes")
    take_parser.set_defaults(func=cmd_take)
    
    # ledger subcommand
    ledger_parser = subparsers.add_parser("ledger", help="Display ledger summary")
    ledger_parser.set_defaults(func=cmd_ledger)
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return 1
    
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

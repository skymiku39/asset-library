"""Verify discovery ledger candidates for automated regression checks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from discovery_ledger import (  # noqa: E402
    LEDGER_PATH,
    load_ledger,
    save_ledger,
    verify_candidate,
    write_markdown,
)


def main() -> int:
    if not LEDGER_PATH.exists():
        print("FAIL: discovery_ledger.json missing; run discovery_ledger.py --bootstrap")
        return 2

    data = load_ledger()
    checked = 0
    failures: list[str] = []

    for cand in data.get("candidates", []):
        verdict = cand.get("verdict", "pending")
        if verdict not in {"ingested", "verified-downloadable", "pending", "rejected-broken"}:
            continue
        # Limit live network checks: prioritize ingested + pending + previously broken
        if verdict == "ingested" and checked >= 25:
            # Sample first 25 ingested for CI-friendly runtime; remaining stamped skipped.
            cand.setdefault(
                "verify",
                {
                    "skipped": True,
                    "reason": "ingested-sample-limit",
                    "last_verify_at": cand.get("verify", {}).get("last_verify_at"),
                },
            )
            continue
        payload = verify_candidate(cand)
        checked += 1
        if verdict in {"ingested", "verified-downloadable"}:
            if not payload.get("http_ok"):
                failures.append(f"{cand['id']}: http not ok ({payload.get('error')})")
            elif payload.get("downloadable") is False and verdict == "verified-downloadable":
                failures.append(f"{cand['id']}: expected downloadable")

    save_ledger(data)
    write_markdown(data)

    summary = {
        "candidates": len(data.get("candidates", [])),
        "checked": checked,
        "failures": len(failures),
    }
    print(json.dumps(summary, ensure_ascii=False))
    for f in failures[:20]:
        print("FAIL", f)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

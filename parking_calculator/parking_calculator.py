from __future__ import annotations

import math
import re
import sys
from datetime import datetime
from pathlib import Path

FREE_MINUTES = 30
ZONE1_MINUTES = 3 * 60
RATE_ZONE1_PER_HOUR = 300
RATE_ZONE2_PER_HOUR = 500
FLAT_24H_HUF = 10_000
MINUTES_PER_24H = 24 * 60

DEFAULT_INPUT = "input.txt"
DEFAULT_OUTPUT = "output.txt"


def _tiered_fee_for_segment(total_minutes: int) -> int:

    if total_minutes <= 0:
        return 0
    if total_minutes <= FREE_MINUTES:
        return 0

    billable = total_minutes - FREE_MINUTES
    zone1 = min(billable, ZONE1_MINUTES)
    zone2 = billable - zone1

    fee = math.ceil(zone1 / 60) * RATE_ZONE1_PER_HOUR
    if zone2 > 0:
        fee += math.ceil(zone2 / 60) * RATE_ZONE2_PER_HOUR
    return fee


def parking_fee_huf(entry: datetime, exit_time: datetime) -> tuple[int, float]:

    delta = exit_time - entry
    total_minutes = int(delta.total_seconds() // 60)
    if exit_time <= entry:
        raise ValueError("Exit time must be after entry time.")

    full_days = total_minutes // MINUTES_PER_24H
    remainder = total_minutes % MINUTES_PER_24H
    total_huf = full_days * FLAT_24H_HUF + _tiered_fee_for_segment(remainder)

    avg_per_min = total_huf / total_minutes if total_minutes > 0 else 0.0
    return total_huf, avg_per_min


def _parse_datetime(line: str) -> datetime:
    line = line.strip()
    if not line:
        raise ValueError("Empty datetime line.")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(line, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(line)
    except ValueError as exc:
        raise ValueError(f"Unrecognized datetime format: {line!r}") from exc


_ROW_RE = re.compile(
    r"^(\S+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*$"
)


def _is_header_or_separator(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.upper().startswith("RENDSZAM"):
        return True
    if len(s) >= 3 and set(s) == {"="}:
        return True
    return False


def _parse_data_line(line: str) -> tuple[str, datetime, datetime]:
    raw = line.rstrip("\n\r")
    m = _ROW_RE.match(raw.strip())
    if m:
        plate, erkezes, tavozas = m.groups()
        return plate.strip(), _parse_datetime(erkezes), _parse_datetime(tavozas)
    parts = [p for p in raw.split("\t") if p.strip()]
    if len(parts) >= 3:
        return (
            parts[0].strip(),
            _parse_datetime(parts[1]),
            _parse_datetime(parts[2]),
        )
    raise ValueError(f"Could not parse row (expected RENDSZAM, ERKEZES, TAVOZAS): {raw!r}")


def read_parking_sessions(path: Path) -> list[tuple[str, datetime, datetime]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[tuple[str, datetime, datetime]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _is_header_or_separator(line):
            continue
        try:
            rows.append(_parse_data_line(line))
        except ValueError as exc:
            raise ValueError(f"Line {lineno}: {exc}") from exc
    if not rows:
        raise ValueError("No data rows found (need RENDSZAM, ERKEZES, TAVOZAS per line).")
    return rows


def write_results(
    out_path: Path,
    sessions: list[tuple[str, datetime, datetime, int, float]],
) -> None:
    lines = [
        "RENDSZAM  Min    HUF",
        "--------  -----  -----",
    ]
    for plate, entry, exit_time, total_huf, _avg_per_min in sessions:
        delta = exit_time - entry
        total_minutes = int(delta.total_seconds() // 60)
        lines.append(f"{plate:<8}  {total_minutes:5d}    {total_huf}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    base = Path(__file__).resolve().parent
    in_file = base / DEFAULT_INPUT
    out_file = base / DEFAULT_OUTPUT

    if len(argv) >= 1:
        in_file = Path(argv[0])
    if len(argv) >= 2:
        out_file = Path(argv[1])

    try:
        sessions_raw = read_parking_sessions(in_file)
        sessions: list[tuple[str, datetime, datetime, int, float]] = []
        for plate, entry, exit_time in sessions_raw:
            total, avg = parking_fee_huf(entry, exit_time)
            sessions.append((plate, entry, exit_time, total, avg))
    except OSError as exc:
        sys.stderr.write(f"Input error: {exc}\n")
        return 1
    except ValueError as exc:
        sys.stderr.write(f"Invalid data: {exc}\n")
        return 1

    try:
        write_results(out_file, sessions)
    except OSError as exc:
        sys.stderr.write(f"Output error: {exc}\n")
        return 1

    grand = sum(s[3] for s in sessions)
    print(f"Wrote {out_file} — {len(sessions)} vehicle(s), total {grand} HUF")
    return 0


def _self_check() -> None:
    from datetime import timedelta

    base = datetime(2025, 1, 1, 8, 0, 0)
    cases = [
        (base, base + timedelta(minutes=20), 0),
        (base, base + timedelta(hours=2), 600),
        (base, base + timedelta(hours=4), 1400),
        (base, base + timedelta(hours=24), 10_000),
    ]
    for a, b, want in cases:
        got, _ = parking_fee_huf(a, b)
        assert got == want, (a, b, got, want)

    long_stay = base + timedelta(hours=30)
    fee30, _ = parking_fee_huf(base, long_stay)
    assert fee30 == 10_000 + _tiered_fee_for_segment(6 * 60)

    try:
        parking_fee_huf(base + timedelta(hours=1), base)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError when exit before entry")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        _self_check()
        print("self-check OK")
        raise SystemExit(0)
    raise SystemExit(main())


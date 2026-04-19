from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_INPUT = "input.txt"
DEFAULT_OUTPUT = "output.txt"


def min_num_of_drops(prototypes: int, height: int) -> int:

    if prototypes <= 0 or height <= 0:
        return 0
    
    if prototypes == 1:
        return height
    
    low, high = 0, height
    
    def max_testable_floors(eggs: int, drops: int) -> int:

        total = 0
        comb = 1
        
        for k in range(1, eggs + 1):
            if k > drops:
                break
            comb = comb * (drops - k + 1) // k
            total += comb
            
            if total >= height:
                return total
        
        return total
    
    while low < high:
        mid = (low + high) // 2
        
        if max_testable_floors(prototypes, mid) >= height:
            high = mid
        else:
            low = mid + 1
    
    return low


def read_test_cases(in_path: Path) -> list[tuple[int, int]]:

    text = in_path.read_text(encoding="utf-8", errors="replace").strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    test_cases = []
    
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        line = line.replace(',', ' ')
        parts = line.split()
        
        if len(parts) < 2:
            raise ValueError(f"Line {line_no}: Expected two integers (prototypes and height), got {line!r}")
        
        try:
            prototypes = int(parts[0])
            height = int(parts[1])
        except ValueError as exc:
            raise ValueError(f"Line {line_no}: Invalid integer format - {exc}") from exc
        
        if prototypes < 1:
            raise ValueError(f"Line {line_no}: Prototypes must be at least 1, got {prototypes}")
        
        if height < 1:
            raise ValueError(f"Line {line_no}: Height must be at least 1, got {height}")
        
        test_cases.append((prototypes, height))
    
    if not test_cases:
        raise ValueError("No valid test cases found in input file")
    
    return test_cases


def write_results(out_path: Path, results: list[tuple[int, int, int]]) -> None:

    lines = [
        "Prototypes  Height  Min drops",
        "----------  ------  ---------"
    ]
    
    for prototypes, height, drops in results:
        lines.append(f"{prototypes:10d}  {height:6d}  {drops:9d}")
    
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
        test_cases = read_test_cases(in_file)
        results = []
        
        for prototypes, height in test_cases:
            drops = min_num_of_drops(prototypes, height)
            results.append((prototypes, height, drops))
            
    except OSError as exc:
        sys.stderr.write(f"Input error: {exc}\n")
        return 1
    except ValueError as exc:
        sys.stderr.write(f"Invalid data: {exc}\n")
        return 1
    
    try:
        write_results(out_file, results)
    except OSError as exc:
        sys.stderr.write(f"Output error: {exc}\n")
        return 1
    
    print(f"Wrote {out_file} — {len(results)} test case(s) processed")
    return 0


def _self_check() -> None:

    assert min_num_of_drops(1, 100) == 100
    assert min_num_of_drops(2, 100) == 14
    assert min_num_of_drops(3, 100) == 9
    
    assert min_num_of_drops(1, 1) == 1
    assert min_num_of_drops(2, 456) == 30
    assert min_num_of_drops(3, 456) == 14
    assert min_num_of_drops(4, 456) == 11
    assert min_num_of_drops(2, 789) == 40
    assert min_num_of_drops(3, 789) == 17
    assert min_num_of_drops(4, 789) == 12
    
    assert min_num_of_drops(2, 100) <= min_num_of_drops(1, 100)
    assert min_num_of_drops(3, 100) <= min_num_of_drops(2, 100)
    assert min_num_of_drops(4, 456) <= min_num_of_drops(3, 456)
    
    assert min_num_of_drops(1, 1) == 1
    assert min_num_of_drops(2, 1) == 1
    assert min_num_of_drops(5, 1) == 1
    assert min_num_of_drops(2, 2) == 2
    
    print("All self-checks passed!")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        _self_check()
        raise SystemExit(0)
    raise SystemExit(main())
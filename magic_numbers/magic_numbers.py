from __future__ import annotations

import sys
from pathlib import Path

DEFAULT_INPUT = "input.txt"
DEFAULT_OUTPUT = "output.txt"


def is_magic_number(n: int) -> bool:
    s = str(n)
    return s == s[::-1]


def next_magic_num(n: int) -> int:

    if n < 0:
        raise ValueError("Input must be non-negative")
    
    if n < 9:
        return n + 1
    
    s = str(n)
    length = len(s)
    
    if all(ch == '9' for ch in s):
        return int('1' + '0' * (length - 1) + '1')
    
    half_len = (length + 1) // 2
    left_half = s[:half_len]
    
    if length % 2 == 0:
        candidate = left_half + left_half[::-1]
    else:
        candidate = left_half + left_half[-2::-1]
    
    candidate_num = int(candidate)
    
    if candidate_num > n:
        return candidate_num
    
    left_half_num = int(left_half) + 1
    new_left = str(left_half_num)
    
    if length % 2 == 0:
        result = new_left + new_left[::-1]
    else:
        result = new_left + new_left[-2::-1]
    
    return int(result)


def evaluate_expression(s: str) -> int:

    s = s.strip()
    
    if '^' in s:
        parts = s.split('^')
        if len(parts) == 2:
            base = int(parts[0].strip())
            exponent = int(parts[1].strip())
            return base ** exponent
    
    return int(s)


def read_inputs(in_path: Path) -> list[int]:

    text = in_path.read_text(encoding="utf-8", errors="replace").strip()
    
    if not text:
        raise ValueError("Input file is empty")
    
    inputs_list = []
    
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        try:
            value = evaluate_expression(line)
            inputs_list.append(value)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"Line {line_no}: Invalid number or expression {line!r} - {exc}") from exc
    
    if not inputs_list:
        raise ValueError("No valid inputs found in file")
    
    return inputs_list


def write_results(out_path: Path, results: list[tuple[int, int]]) -> None:

    lines = [
        "",
        "Input".ljust(35) + "Next magic number",
        "-----".ljust(35) + "-----------------",
        ""
    ]
    
    for original, next_magic in results:
        if original > 10**20:
            input_str = f"{original}"
        else:
            input_str = str(original)
        lines.append(f"{input_str:<35} {next_magic:>20}")
    
    lines.append("")
    
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
        inputs_list = read_inputs(in_file)
        results = []
        
        for val in inputs_list:
            next_magic = next_magic_num(val)
            results.append((val, next_magic))
            
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
    
    print(f"Wrote {out_file} — {len(results)} input(s) processed")
    return 0


def _self_check() -> None:

    assert next_magic_num(808) == 818
    assert next_magic_num(999) == 1001
    assert next_magic_num(2133) == 2222
    
    assert next_magic_num(0) == 1
    assert next_magic_num(1) == 2
    assert next_magic_num(8) == 9
    assert next_magic_num(9) == 11
    
    assert next_magic_num(10) == 11
    assert next_magic_num(11) == 22
    assert next_magic_num(99) == 101
    assert next_magic_num(100) == 101
    assert next_magic_num(101) == 111
    
    assert next_magic_num(12345) == 12421
    assert next_magic_num(123456) == 124421
    
    assert next_magic_num(9) == 11
    assert next_magic_num(99) == 101
    assert next_magic_num(999) == 1001
    assert next_magic_num(9999) == 10001
    
    assert evaluate_expression("3^39") == 3**39
    assert evaluate_expression("2^10") == 1024
    assert evaluate_expression("123") == 123
    
    huge_num = 3**39
    result = next_magic_num(huge_num)
    assert result > huge_num
    assert is_magic_number(result)
    
    assert next_magic_num(9) == 11
    assert next_magic_num(120) == 121
    
    print("All self-checks passed!")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        _self_check()
        raise SystemExit(0)
    raise SystemExit(main())
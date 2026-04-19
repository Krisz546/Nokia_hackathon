from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_FIELD_LINE = re.compile(
    r"^(\s*)(.+?)\s*(?:\.(?:\s*\.)*)\s*:\s*(.*)\s*$"
)

_FIELD_MAPPINGS: list[tuple[str, str]] = [
    ("connection-specific dns suffix", "connection_specific_dns_suffix"),
    ("temporary ipv6 address", "temporary_ipv6_address"),
    ("link-local ipv6 address", "link_local_ipv6_address"),
    ("ipv6 address", "ipv6_address"),
    ("autoconfiguration ipv4 address", "autoconfiguration_ipv4_address"),
    ("ipv4 address", "ipv4_address"),
    ("subnet mask", "subnet_mask"),
    ("default gateway", "default_gateway"),
    ("dns servers", "dns_servers"),
    ("description", "description"),
    ("physical address", "physical_address"),
    ("dhcp enabled", "dhcp_enabled"),
    ("media state", "media_state"),
]

_MULTI_VALUE_KEYS = frozenset({"dns_servers", "default_gateway"})


def _normalize_field_name(label: str) -> str | None:

    s = re.sub(r"\s+", " ", label.strip().lower())
    for value, key in _FIELD_MAPPINGS:
        if s == value or s.startswith(value + " "):
            return key
    return None


def _strip_ipv4_annotations(value: str) -> str:

    return re.sub(
        r"\s*\((?:Preferred|Deferred)\)\s*$",
        "",
        value,
        flags=re.IGNORECASE,
    ).strip()


def _is_adapter_header(line: str) -> bool:

    t = line.strip()
    if not t.endswith(":"):
        return False
    if t.lower().startswith("windows ip configuration"):
        return False
    return "adapter" in t.lower()


def _empty_adapter() -> dict[str, str | list[str]]:


    return {
        "adapter_name": "",
        "connection_specific_dns_suffix": "",
        "media_state": "",
        "description": "",
        "physical_address": "",
        "dhcp_enabled": "",
        "ipv6_address": "",
        "temporary_ipv6_address": "",
        "link_local_ipv6_address": "",
        "ipv4_address": "",
        "autoconfiguration_ipv4_address": "",
        "subnet_mask": "",
        "default_gateway": [],
        "dns_servers": [],
    }


def _parse_adapter_block(lines: list[str]) -> dict[str, str | list[str]]:


    out = _empty_adapter()
    if not lines:
        return out

    header = lines[0].strip()
    if header.endswith(":"):
        out["adapter_name"] = header[:-1].strip()

    pending: str | None = None
    i = 1
    while i < len(lines):
        raw = lines[i]
        m = _FIELD_LINE.match(raw)
        if m:
            _, label, value = m.groups()
            key = _normalize_field_name(label)
            value = value.strip()
            if key in _MULTI_VALUE_KEYS:
                pending = key
                if value:
                    out[key].append(value)
            elif key:
                pending = None
                if key == "ipv4_address":
                    value = _strip_ipv4_annotations(value)
                out[key] = value
            else:
                pending = None
            i += 1
            continue

        if pending and raw.strip():
            out[pending].append(raw.strip())
            i += 1
            continue

        pending = None
        i += 1

    return out


def parse_ipconfig_text(text: str) -> list[dict[str, str | list[str]]]:


    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    adapters: list[dict[str, str | list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        if not line[:1].isspace() and _is_adapter_header(line):
            block = [line]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    block.append(nxt)
                    i += 1
                    continue
                if not nxt[:1].isspace():
                    break
                block.append(nxt)
                i += 1
            adapters.append(_parse_adapter_block(block))
            continue
        i += 1

    return adapters


def _read_ipconfig_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig", errors="replace")
    return raw.decode("utf-8", errors="replace")


def _prune_empty_fields(
    record: dict[str, str | list[str]],
) -> dict[str, str | list[str]]:
    return {
        k: v
        for k, v in record.items()
        if v != "" and v != []
    }


def parse_files(paths: list[Path]) -> list[dict]:

    result = []
    for path in paths:
        text = _read_ipconfig_text(path)
        adapters = [_prune_empty_fields(a) for a in parse_ipconfig_text(text)]
        result.append({"file_name": path.name, "adapters": adapters})
    return result


_DEFAULT_OUTPUT = Path("parse_ipconfig.log")


def main() -> None:
    if len(sys.argv) < 2:
        paths = sorted(Path(".").glob("*.txt"))
        if not paths:
            print("Usage: parse_ipconfig.py <ipconfig_file> [...]", file=sys.stderr)
            sys.exit(2)
    else:
        paths = [Path(p) for p in sys.argv[1:]]

    out = parse_files(paths)
    payload = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    sys.stdout.write(payload)
    _DEFAULT_OUTPUT.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()

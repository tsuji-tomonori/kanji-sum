from __future__ import annotations

import csv
from csv import DictReader
from pathlib import Path

header = ("font","MJ文字図形名","対応するUCS","総画数(参考)","読み(参考)","バージョン")


def read_csv(file_name: Path) -> list[dict[str, str]]:
    with file_name.open("r", encoding="utf-8") as f:
        return list(DictReader(f))

def dict_to_list(item: dict[str, str]) -> list[str]:
    result = []
    for key in header:
        if key == "対応するUCS":
            result.append(f"U+{str(hex(ord(item["font"])))[2:]}".upper())
        else:
            result.append(item[key])
    return result

def write_csv(file_name: Path, items: list[list[str]]) -> None:
    with file_name.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(items)

input_path = Path.cwd() / "data" / "hiragana_katakana_database_before.csv"
output_path = Path.cwd() / "data" / "hiragana_katakana_database.csv"
items = [dict_to_list(item) for item in read_csv(input_path)]
write_csv(output_path, items)

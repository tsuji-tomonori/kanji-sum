from __future__ import annotations

import sys
import time
from csv import DictReader
from pathlib import Path
from typing import Any

import boto3
from tqdm import tqdm


def read_csv(file_name: Path) -> list[dict[str, str]]:
    with file_name.open("r", encoding="utf-8") as f:
        return list(DictReader(f))


def merge_duplicates(items: list[dict[str, str]]) -> dict[str, Any]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if result.get(item["対応するUCS"]) is None:
            result[item["対応するUCS"]] = item
        else:
            result[item["対応するUCS"]].get("重複したアイテム", []).append(list(item))
    return result


args = sys.argv[1:]
path = Path.cwd() / "data" / args[0]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("kanji-dynamodb-database")

with table.batch_writer() as batch:
    for item in tqdm(merge_duplicates(read_csv(path)).values()):
        batch.put_item(Item=item)
    time.sleep(0.1)

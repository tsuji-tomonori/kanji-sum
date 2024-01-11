from __future__ import annotations

import json
import os
import urllib.parse
from typing import TYPE_CHECKING, Any, NamedTuple, Self

import boto3
from aws_lambda_powertools.logging import Logger

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger()
dynamodb_client = boto3.client("dynamodb")
dynamodb_resource = boto3.resource("dynamodb")


class NoDataError(Exception):
    def __init__(self: Self, key: str, font: str) -> None:
        super().__init__(f"databaseにデータがありませんでした: key={key}, font={font}")


class EnvParam(NamedTuple):
    DATABASE_NAME: str
    DISTRIBUTION_DOMAIN_NAME: str

    @classmethod
    def from_env(cls: type[EnvParam]) -> EnvParam:
        return EnvParam(**{k: os.getenv(k) for k in EnvParam._fields})


def create_key(font: str) -> str:
    return f"U+{str(hex(ord(font)))[2:]}".upper()


class KanjiInfo(NamedTuple):
    font: str
    kakusu: int
    yomi: str

    @classmethod
    def from_db(cls: type[KanjiInfo], font: str, table_name: str) -> KanjiInfo:
        logger.info(font)
        table = dynamodb_resource.Table(table_name)
        key = create_key(font)
        logger.info(key)
        item = table.get_item(Key={"対応するUCS": key}).get("Item")
        if item is None:
            raise NoDataError(key, font)
        logger.info(json.dumps(item))
        return KanjiInfo(
            font=item.get("font", ""),
            kakusu=int(item.get("総画数(参考)", 0)),
            yomi=item.get("読み(参考)", ""),
        )

    def asdict(self: Self) -> dict[str, str | int]:
        return {
            "font": self.font,
            "総画数(参考)": self.kakusu,
            "読み(参考)": self.yomi,
        }


class Response(NamedTuple):
    status_code: int
    kanji_infos: list[KanjiInfo]
    DISTRIBUTION_DOMAIN_NAME: str

    def data(self: Self) -> dict[str, Any]:
        kanji_sum = sum(x.kakusu for x in self.kanji_infos)
        kanji_list = [x.asdict() for x in self.kanji_infos]
        return {
            "statusCode": self.status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": f"https://{self.DISTRIBUTION_DOMAIN_NAME}",
                "Access-Control-Allow-Methods": "GET, POST, DELETE",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "origin, x-requested-with, access-control-allow-origin",  # noqa: E501
            },
            "body": json.dumps(
                {
                    "kanji_sum": kanji_sum,
                    "kanji_list": kanji_list,
                },
            ),
            "isBase64Encoded": False,
        }


def service(event: dict[str, Any], env: EnvParam) -> Response:
    try:
        tokens = urllib.parse.unquote(event["queryStringParameters"]["tokens"])
        kanji_infos = [KanjiInfo.from_db(token, env.DATABASE_NAME) for token in tokens]
        return Response(200, kanji_infos, env.DISTRIBUTION_DOMAIN_NAME)
    except Exception:
        logger.exception("想定外エラーが発生しました")
        return Response(500, [], env.DISTRIBUTION_DOMAIN_NAME)


@logger.inject_lambda_context(
    correlation_id_path="requestContext.requestId",
)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    return service(
        event=event,
        env=EnvParam.from_env(),
    ).data()

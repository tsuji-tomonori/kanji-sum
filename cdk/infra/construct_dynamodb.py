from typing import Any, Self

import aws_cdk as cdk
from aws_cdk import aws_dynamodb as dynamdb
from constructs import Construct

from cdk.paramater import build_name


class DynamoDBConstruct(Construct):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB
        self.table_kanji = dynamdb.Table(
            scope=self,
            id="kanji",
            partition_key=dynamdb.Attribute(
                name="対応するUCS",
                type=dynamdb.AttributeType.STRING,
            ),
            billing_mode=dynamdb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            table_name=build_name("dynamodb", "database"),
        )

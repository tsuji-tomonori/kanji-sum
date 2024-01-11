from typing import Any, Self

from constructs import Construct

from cdk.infra.construct_apigw import ApigwConstruct
from cdk.infra.construct_dynamodb import DynamoDBConstruct


class InfraConstruct(Construct):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.dynamodb = DynamoDBConstruct(self, "dynamodb")
        self.api = ApigwConstruct(self, "apigw")

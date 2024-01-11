from typing import Any, Self

from aws_cdk import aws_apigateway as apigw
from aws_cdk.aws_apigateway import Resource
from constructs import Construct

from cdk.infra.construct_infra import InfraConstruct
from cdk.infra.construct_lambda import LambdaConstruct


class FunctionConstruct(Construct):
    def __init__(  # noqa: PLR0913
        self: Self,
        scope: Construct,
        construct_id: str,
        infra: InfraConstruct,
        kanji: Resource,
        distribution_domain_name: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lmd = LambdaConstruct(self, "function")

        # apigwとの紐づけ
        kanji.add_method(
            http_method="GET",
            integration=apigw.LambdaIntegration(
                handler=self.lmd.function,
            ),
        )

        # 権限の設定
        assert self.lmd.function.role is not None
        infra.dynamodb.table_kanji.grant_read_data(self.lmd.function.role)
        self.lmd.function.add_environment(
            key="DATABASE_NAME",
            value=infra.dynamodb.table_kanji.table_name,
        )

        # 環境変数
        self.lmd.function.add_environment(
            key="LOG_LEVEL",
            value="ERROR",
        )

        self.lmd.function.add_environment(
            key="DISTRIBUTION_DOMAIN_NAME",
            value=distribution_domain_name,
        )

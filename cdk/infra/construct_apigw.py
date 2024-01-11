from typing import Any, Self

import aws_cdk as cdk
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_logs as logs
from constructs import Construct

from cdk.paramater import build_name


class ApigwConstruct(Construct):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # APIGW
        self.api = apigw.RestApi(
            scope=self,
            id="api",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
            rest_api_name=build_name("apigw", "api"),
            description="kanji_sum",
            deploy_options=apigw.StageOptions(
                logging_level=apigw.MethodLoggingLevel.ERROR,
                stage_name="v1",
            ),
        )

        self.logs = logs.LogGroup(
            scope=self,
            id="logs",
            log_group_name=f"API-Gateway-Execution-Logs_{self.api.rest_api_id}/{self.api.deployment_stage.stage_name}",
            retention=logs.RetentionDays.THREE_MONTHS,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

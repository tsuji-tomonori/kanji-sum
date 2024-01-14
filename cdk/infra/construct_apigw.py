from typing import Any, Self

from aws_cdk import aws_apigateway as apigw
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

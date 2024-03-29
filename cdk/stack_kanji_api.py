from typing import Any, Self

from aws_cdk import Stack
from constructs import Construct

from cdk.app.construct_app import AppConstruct
from cdk.infra.construct_infra import InfraConstruct
from cdk.infra.construct_static import StaticConstruct


class KanjiApiStack(Stack):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.infra = InfraConstruct(self, "infra")
        self.static = StaticConstruct(self, "static")
        self.app = AppConstruct(self, "app", self.infra, self.static.distribution.attr_domain_name)  # noqa: E501

from typing import Any, Self

from aws_cdk import Stack
from constructs import Construct

from cdk.app.construct_app import AppConstruct
from cdk.infra.construct_infra import InfraConstruct


class KanjiApiStack(Stack):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        distribution_domain_name: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.infra = InfraConstruct(self, "infra")
        self.app = AppConstruct(self, "app", self.infra, distribution_domain_name)

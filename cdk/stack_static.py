from typing import Any, Self

from aws_cdk import Stack
from constructs import Construct

from cdk.infra.construct_static import StaticConstruct


class StaticStack(Stack):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.static = StaticConstruct(self, "static")

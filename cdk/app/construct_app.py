from typing import Any, Self

from constructs import Construct

from cdk.app.construct_function import FunctionConstruct
from cdk.infra.construct_infra import InfraConstruct


class AppConstruct(Construct):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        infra: InfraConstruct,
        distribution_domain_name: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kanji = infra.api.api.root.add_resource("kanji")
        self.function = FunctionConstruct(
            self,
            "function",
            infra,
            kanji,
            distribution_domain_name,
        )

from pathlib import Path

import aws_cdk as cdk
import tomllib
from aws_cdk import Tags

from cdk.stack_kanji_api import KanjiApiStack
from cdk.stack_static import StaticStack


def add_name_tag(scope):  # noqa: ANN001, ANN201
    for child in scope.node.children:
        if cdk.Resource.is_resource(child):
            Tags.of(child).add("Name", child.node.path.replace("/", "-"))
        add_name_tag(child)


with (Path.cwd() / "pyproject.toml").open("rb") as f:
    project = tomllib.load(f)["project"]["name"]

app = cdk.App()

stack = StaticStack(
    scope=app,
    construct_id=f"{project.replace('_', '-')}-static",
    env=cdk.Environment(
        region="us-east-1",
    ),
    cross_region_references=True,
)

KanjiApiStack(
    scope=app,
    construct_id=f"{project.replace('_', '-')}",
    env=cdk.Environment(
        region="ap-northeast-1",
    ),
    cross_region_references=True,
    distribution_domain_name=stack.static.distribution.attr_domain_name,
)

Tags.of(app).add("Project", project)
Tags.of(app).add("ManagedBy", "cdk")
add_name_tag(app)

app.synth()

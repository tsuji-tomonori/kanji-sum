from typing import Any, Self

import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as deployment
from constructs import Construct


class StaticConstruct(Construct):
    def __init__(
        self: Self,
        scope: Construct,
        construct_id: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self,
            "bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        self.distribution = cloudfront.Distribution(
            self,
            "cloudfront_distribution",
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket),
            ),
            comment="kanji-sum",
        )

        deployment.BucketDeployment(
            self,
            "deploy",
            sources=[deployment.Source.asset("./build")],
            destination_bucket=self.bucket,
            distribution=self.distribution,
            distribution_paths=["/*"],
        )

        # output
        cdk.CfnOutput(
            self,
            "static_web_url",
            value=f"https://{self.distribution.domain_name}",
        )

        cdk.Tags.of(self).add("Public", "True")

from typing import Any, Self

import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_iam as iam
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

        self.oac = cloudfront.CfnOriginAccessControl(
            self,
            "oac",
            origin_access_control_config=cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name="kanji-sum-s3",
                origin_access_control_origin_type="s3",
                description="kanji-sum-s3",
                signing_behavior="always",
                signing_protocol="sigv4",
            ),
        )

        self.distribution = cloudfront.CfnDistribution(
            self,
            "distribution",
            distribution_config=cloudfront.CfnDistribution.DistributionConfigProperty(
                origins=[
                    cloudfront.CfnDistribution.OriginProperty(
                        domain_name=self.bucket.bucket_regional_domain_name,
                        id=self.bucket.bucket_name,
                        origin_access_control_id=self.oac.attr_id,
                        s3_origin_config={},
                    ),
                ],
                default_cache_behavior=cloudfront.CfnDistribution.DefaultCacheBehaviorProperty(
                    cache_policy_id="658327ea-f89d-4fab-a63d-7e88639e58f6", # CachingOptimized  # noqa: E501
                    origin_request_policy_id="88a5eaf4-2fd4-4709-b370-b4c650ea3fcf", # CORS-S3Origin  # noqa: E501
                    target_origin_id=self.bucket.bucket_name,
                    viewer_protocol_policy="allow-all",
                ),
                enabled=True,
                default_root_object="index.html",
                comment="kanji-sum",
            ),
        )

        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{self.bucket.bucket_arn}/*"],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{cdk.Stack.of(self).account}:distribution/{self.distribution.attr_id}",  # noqa: E501
                    },
                },
            ),
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
            value=f"https://{self.distribution.attr_domain_name}",
        )

        cdk.Tags.of(self).add("Public", "True")

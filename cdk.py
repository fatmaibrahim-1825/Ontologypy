from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_logs as logs,
    aws_ec2 as ec2,
    aws_apigateway as apigw
)
import os

app = core.App()

environment = app.node.try_get_context('environment')
params = app.node.try_get_context('parameters')
tags = params["all"]["tags"]
vpc_tags = params["vpc"]["lookupTags"]
env_vars = params["lambda"]["environment_variables"]

fn_name = os.path.split(os.getcwd())[1]
if "name" in params["lambda"]:
    fn_name = params["lambda"]["name"]
memory_size = params["lambda"]["memory_size"]

env = {'env': environment}
print(f"Deploying to {environment}")


class LambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs):
        super(LambdaStack, self).__init__(
            scope=scope,
            id=f'SCube-{fn_name}-Lambda',
            **kwargs
        )

        vpc = ec2.Vpc.from_lookup(
            scope=self,
            id='VPC-Lookup',
            tags=vpc_tags,
        )

        role = iam.Role(
            scope=self,
            id="Role",
            assumed_by=iam.ServicePrincipal(f'lambda.{core.Aws.URL_SUFFIX}'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2FullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryReadOnly'),
            ]
        )

        # deploy course player
        fn = lambda_.DockerImageFunction(
            scope=self,
            id='Fn',
            code=lambda_.DockerImageCode.from_image_asset(
                directory='.',
                exclude=['cdk.out', '.env', 'cdk.json', 'cdk.py', 'Dockerfile', 'README.md', '.gitignore']
            ),
            role=role,
            timeout=core.Duration.minutes(2),
            memory_size=memory_size,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            log_retention=logs.RetentionDays.TWO_WEEKS,
            environment=env_vars,
            retry_attempts=2
        )

        api = apigw.RestApi.from_rest_api_attributes(
            scope=self,
            id="RestApi",
            rest_api_id="7qx5ef0hsb",
            root_resource_id='yyb1sm'# /api
        )

        res = api.root.add_resource('ontologypy')

        res.add_proxy(
            any_method=True,
            default_integration=apigw.LambdaIntegration(
                handler=fn
            )
        )

        for tag in tags:
            core.Tags.of(self).add(**tag)


LambdaStack(
    scope=app,
    **env
)

app.synth()

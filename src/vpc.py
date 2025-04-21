import hashlib
from typing import cast

from aws_cdk import CfnOutput
from aws_cdk.aws_ec2 import Vpc, SubnetConfiguration, SubnetType, SubnetSelection, IVpc, GatewayVpcEndpointAwsService, \
    GatewayVpcEndpointOptions
from constructs import Construct

from src.config import config


def setup_vpc(scope: Construct) -> IVpc:
    n_vpc_azs = config['n_vpc_azs']

    assert 1 <= n_vpc_azs <= 6, 'Number of VPC AZs must be between 1 and 6'

    vpc = Vpc(
        scope,
        f'Vpc{hashlib.md5(f"{n_vpc_azs}".encode()).hexdigest()[:8]}',
        max_azs=n_vpc_azs,
        nat_gateways=0,
        subnet_configuration=[
            SubnetConfiguration(name='Public', subnet_type=SubnetType.PUBLIC),
            SubnetConfiguration(name='Private', subnet_type=SubnetType.PRIVATE_WITH_EGRESS)
        ],
        gateway_endpoints={
            's3': GatewayVpcEndpointOptions(
                service=GatewayVpcEndpointAwsService.S3,
                subnets=[SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_EGRESS)]
            ),
            'dynamodb': GatewayVpcEndpointOptions(
                service=GatewayVpcEndpointAwsService.DYNAMODB,
                subnets=[SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_EGRESS)]
            )
        }
    )

    CfnOutput(
        scope,
        'VpcId',
        value=vpc.vpc_id
    )

    return cast(IVpc, vpc)

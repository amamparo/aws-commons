from typing import cast

from aws_cdk.aws_ec2 import Vpc, SubnetConfiguration, SubnetType, SubnetSelection, IVpc, GatewayVpcEndpointAwsService
from constructs import Construct


def setup_vpc(scope: Construct) -> IVpc:
    vpc = cast(IVpc, Vpc(
        scope,
        'Vpc',
        max_azs=1,
        nat_gateways=0,
        subnet_configuration=[
            SubnetConfiguration(
                name='Public',
                subnet_type=SubnetType.PUBLIC,
                cidr_mask=24
            ),
            SubnetConfiguration(
                name='Private',
                subnet_type=SubnetType.PRIVATE_WITH_EGRESS,
                cidr_mask=24
            )
        ]
    ))

    vpc.add_gateway_endpoint(
        'S3GatewayEndpoint',
        service=GatewayVpcEndpointAwsService.S3,
        subnets=[SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_EGRESS)]
    )

    vpc.add_gateway_endpoint(
        'DynamodbGatewayEndpoint',
        service=GatewayVpcEndpointAwsService.DYNAMODB,
        subnets=[SubnetSelection(subnet_type=SubnetType.PRIVATE_WITH_EGRESS)]
    )

    return vpc

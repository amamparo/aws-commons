from aws_cdk.aws_ec2 import SecurityGroup, Peer, Port, InstanceType, Instance, SubnetSelection, MachineImage, IVpc, \
    CfnRoute, AmazonLinuxCpuType
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from constructs import Construct


def setup_nat(scope: Construct, vpc: IVpc) -> None:
    nat_security_group = SecurityGroup(
        scope,
        'NatSecurityGroup',
        vpc=vpc,
        description='Security group for NAT',
        allow_all_outbound=True,
    )

    nat_security_group.add_ingress_rule(
        Peer.ipv4(vpc.private_subnets[0].ipv4_cidr_block),
        Port.all_traffic(),
        'Allow all traffic from private subnet'
    )

    nat_instance = Instance(
        scope,
        'NatInstance',
        instance_type=InstanceType('t4g.nano'),
        associate_public_ip_address=True,
        machine_image=MachineImage.latest_amazon_linux2023(cpu_type=AmazonLinuxCpuType.ARM_64),
        vpc=vpc,
        vpc_subnets=SubnetSelection(subnets=[vpc.public_subnets[0]]),
        security_group=nat_security_group,
        role=Role(
            scope,
            'NatInstanceRole',
            assumed_by=ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore')
            ],
        ),
    )

    nat_instance.node.default_child.source_dest_check = False  # type: ignore[union-attr]

    with open('nat_ec2_user_data.sh', 'r', encoding='utf-8') as user_data:
        nat_instance.user_data.add_commands(*user_data.read().splitlines())

    CfnRoute(
        scope,
        'PrivateSubnetToNatInstance',
        route_table_id=vpc.private_subnets[0].route_table.route_table_id,
        destination_cidr_block='0.0.0.0/0',
        instance_id=nat_instance.instance_id,
    )

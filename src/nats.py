from collections import defaultdict
from typing import Dict, Optional

from aws_cdk.aws_ec2 import InstanceType, Instance, SubnetSelection, MachineImage, IVpc, CfnRoute, AmazonLinuxCpuType, \
    Peer, Port, ISubnet
from aws_cdk.aws_iam import ManagedPolicy
from constructs import Construct


def setup_nats(scope: Construct, vpc: IVpc) -> None:
    az_subnets: Dict[str, Dict[str, Optional[ISubnet]]] = defaultdict(lambda: {'public': None, 'private': None})

    for subnet in vpc.public_subnets:
        az_subnets[subnet.availability_zone]['public'] = subnet

    for subnet in vpc.private_subnets:
        az_subnets[subnet.availability_zone]['private'] = subnet

    for az, subnets in az_subnets.items():
        __setup_nat(scope, az, subnets['public'], subnets['private'], vpc)


def __setup_nat(scope: Construct, az: str, public_subnet: ISubnet, private_subnet: ISubnet, vpc: IVpc) -> None:
    nat_instance = Instance(
        scope,
        f'NatInstance-{az}',
        instance_type=InstanceType('t4g.nano'),
        associate_public_ip_address=True,
        machine_image=MachineImage.latest_amazon_linux2023(cpu_type=AmazonLinuxCpuType.ARM_64),
        vpc=vpc,
        vpc_subnets=SubnetSelection(subnets=[public_subnet]),
        detailed_monitoring=True,
        allow_all_outbound=True,
    )

    nat_instance.role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))

    nat_instance.node.default_child.source_dest_check = False  # type: ignore[union-attr]

    nat_instance.user_data.add_commands(*'''
        #!/bin/bash -x
        yum update -y
        yum install -y iptables iproute
        echo "net.ipv4.ip_forward = 1" | tee -a /etc/sysctl.conf
        sysctl -p
        iptables -t nat -A POSTROUTING -o ens5 -s 0.0.0.0/0 -j MASQUERADE
    '''.strip().splitlines())

    nat_instance.connections.allow_from(
        Peer.ipv4(private_subnet.ipv4_cidr_block),
        Port.all_traffic()
    )

    CfnRoute(
        scope,
        f'NatRoute-{az}',
        route_table_id=private_subnet.route_table.route_table_id,
        destination_cidr_block='0.0.0.0/0',
        instance_id=nat_instance.instance_id,
    )

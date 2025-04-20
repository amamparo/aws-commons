from aws_cdk import Stack, App, CfnOutput
from constructs import Construct

from src.billing_alert import setup_billing_alert
from src.config import config
from src.dns import setup_dns
from src.nat import setup_nat
from src.vpc import setup_vpc


class Commons(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'Commons', env={
            'account': config['account_id'],
            'region': config['region']
        })
        hosted_zone = setup_dns(self)
        vpc = setup_vpc(self)
        setup_nat(self, vpc)
        setup_billing_alert(self)

        CfnOutput(
            self,
            'HostedZoneId',
            value=hosted_zone.hosted_zone_id,
        )

        CfnOutput(
            self,
            'VpcId',
            value=vpc.vpc_id
        )


if __name__ == '__main__':
    app = App()
    Commons(app)
    app.synth()

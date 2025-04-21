from aws_cdk import Stack, App
from constructs import Construct

from src.billing_alert import setup_billing_alert
from src.config import config
from src.dns import setup_dns
from src.nats import setup_nats
from src.vpc import setup_vpc


class Commons(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'Commons', env={
            'account': config['account_id'],
            'region': config['region']
        })
        setup_dns(self)
        setup_nats(self, setup_vpc(self))
        setup_billing_alert(self)


if __name__ == '__main__':
    app = App()
    Commons(app)
    app.synth()

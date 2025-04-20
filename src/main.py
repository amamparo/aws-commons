from aws_cdk import Stack, App
from constructs import Construct

from src.billing_alert import setup_billing_alert
from src.dns import setup_dns
from src.nat import setup_nat
from src.vpc import setup_vpc


class Commons(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'Commons')
        setup_dns(self)
        setup_nat(self, setup_vpc(self))
        setup_billing_alert(self)


if __name__ == '__main__':
    app = App()
    Commons(app)
    app.synth()

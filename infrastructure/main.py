from aws_cdk import Stack, App
from constructs import Construct

from infrastructure.dns import setup_dns
from infrastructure.nat import setup_nat
from infrastructure.vpc import setup_vpc


class Commons(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'Commons')
        setup_dns(self)
        setup_nat(self, setup_vpc(self))


if __name__ == '__main__':
    app = App()
    Commons(app)
    app.synth()

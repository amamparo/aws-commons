from aws_cdk import Stack, App
from constructs import Construct

from aws.dns import setup_dns
from aws.nat import setup_nat
from aws.vpc import setup_vpc


class Commons(Stack):
    def __init__(self, scope: Construct):
        super().__init__(scope, 'Commons')
        setup_dns(self)
        setup_nat(self, setup_vpc(self))


if __name__ == '__main__':
    app = App()
    Commons(app)
    app.synth()

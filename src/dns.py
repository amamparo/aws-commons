from aws_cdk import Duration, CfnOutput
from aws_cdk.aws_certificatemanager import Certificate, CertificateValidation
from aws_cdk.aws_route53 import HostedZone, TxtRecord
from constructs import Construct

from src.config import config


def setup_dns(scope: Construct) -> None:
    home_domain_name = config['dns']['home_domain_name']
    hosted_zone = HostedZone(scope, 'HostedZone', zone_name=home_domain_name)
    certificate = Certificate(scope, 'Certificate', domain_name=f'*.{home_domain_name}',
                              validation=CertificateValidation.from_dns(hosted_zone))

    TxtRecord(
        scope,
        'BlueskyTxtRecord',
        zone=hosted_zone,
        record_name='_atproto',
        values=['did=did:plc:3hw3tp545t752fk4unsct27a'],
        ttl=Duration.seconds(60)
    )

    TxtRecord(
        scope,
        'GithubTxtRecord',
        zone=hosted_zone,
        record_name='_github-pages-challenge-amamparo',
        values=['8e283acd637557961199ac3feb9e4a'],
        ttl=Duration.seconds(60)
    )

    CfnOutput(
        scope,
        'HostedZoneId',
        value=hosted_zone.hosted_zone_id,
    )

    CfnOutput(
        scope,
        'CertificateArn',
        value=certificate.certificate_arn,
    )

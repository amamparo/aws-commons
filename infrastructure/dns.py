from aws_cdk import CfnOutput, Duration
from aws_cdk.aws_route53 import HostedZone, TxtRecord
from constructs import Construct


def setup_dns(scope: Construct):
    hosted_zone = HostedZone(scope, 'HostedZone', zone_name='aaronmamparo.com')

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

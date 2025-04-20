from aws_cdk import Duration, aws_cloudwatch as cloudwatch
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_cloudwatch_actions import SnsAction
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from constructs import Construct


def setup_billing_alert(scope: Construct) -> None:
    billing_topic = Topic(
        scope,
        'BillingAlarmTopic',
        display_name='AWS Billing Alarm'
    )

    billing_topic.add_subscription(EmailSubscription('aaronmamparo@gmail.com'))

    billing_alarm = cloudwatch.Alarm(
        scope,
        'BillingAlarm',
        metric=cloudwatch.Metric(
            namespace='AWS/Billing',
            metric_name='EstimatedCharges',
            dimensions_map={
                'Currency': 'USD'
            },
            statistic='Maximum',
            period=Duration.hours(6)
        ),
        threshold=50,
        evaluation_periods=1,
        comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        alarm_description='Alarm when estimated charges exceed $50',
        treat_missing_data=cloudwatch.TreatMissingData.MISSING
    )

    billing_alarm.add_alarm_action(SnsAction(billing_topic))

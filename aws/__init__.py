from .client import AWSClientManager, BucketAlias, QueueAlias
from .polling import start_sqs_worker

aws_client = AWSClientManager()

__all__ = ["AWSClientManager", "aws_client", "BucketAlias", "QueueAlias", "start_sqs_worker"]

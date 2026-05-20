from .client import AWSClientManager, BucketAlias, QueueAlias

aws_client = AWSClientManager()

__all__ = ["AWSClientManager", "aws_client", "BucketAlias", "QueueAlias"]

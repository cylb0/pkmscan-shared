import logging
from .client import QueueAlias, AWSClientManager
from typing import Callable, List, Optional
import time

logger = logging.getLogger(__name__)

def start_sqs_worker(
    queue_alias: QueueAlias,
    message_handler: Callable[[List[dict]], None],
    max_messages: int = 5,
    wait_time_seconds: int = 20,
    max_empty_poll: Optional[int] = None,
    client: Optional[AWSClientManager] = None
):
    if client is None:
        from . import aws_client
        client = aws_client

    logger.info(f"Starting SQS worker for queue: {queue_alias.value}")
    empty_polls = 0

    while True:
        try:
            messages = client.receive_message(
                queue_alias=queue_alias,
                max_messages=max_messages,
                wait_time_seconds=wait_time_seconds
            )

            if not messages:
                empty_polls += 1
                logger.info(f"No messages on {queue_alias.value} (empty poll {empty_polls}/{max_empty_poll})")

                if max_empty_poll and empty_polls >= max_empty_poll:
                    logger.info(f"No messages for a while, stopping worker")
                    break
                continue
        
            empty_polls = 0
            logger.info(f"Received {len(messages)} from queue {queue_alias.value}")

            message_handler(messages)

        except Exception as err:
            logger.error(f"Error during SQS polling or handling on {queue_alias.value}: {err}")
            logger.info("Retrying in 5 seconds")
            time.sleep(5)
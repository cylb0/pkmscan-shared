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
    """Starts a generic SQS polling loop.

    Can run indefinitely (listener mode) or stop after consecutive empty polls (ephemeral mode).
    Handles network errors and retries automatically.

    Args:
        queue_alias: SQS target queue enum.
        message_handler: Callback function invoked with received raw SQS messages.
        max_messages: Max messages to fetch per call (AWS max is 10). Defaults to 5.
        wait_time_seconds: Long polling duration. Defaults to 20.
        max_empty_poll: Max empty requests before stopping. If None, runs forever.
        client: AWS client manager instance. Lazily imports global instance if None.
    """
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
                total_poll = max_empty_poll if max_empty_poll else "∞"
                logger.info(f"No messages on {queue_alias.value} (empty poll {empty_polls}/{total_poll})")

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
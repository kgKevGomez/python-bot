import logging
import os

import slack

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client = slack.WebClient(token=BOT_TOKEN)


def handler(data, context):
    if "challenge" in data:
        return data["challenge"]

    event = data.get("event")
    if event is None:
        return

    if "bot_id" in event:
        logging.warning("Ignore bot event")

    text = event.get("text", "")
    logger.info("message: " + text)

    # Get the ID of the channel where the message was posted.
    channel_id = event.get("channel")
    if channel_id is None:
        logger.warning("No channel ID was found")
        return

    logger.info("Posting to channel: " + channel_id)
    client.chat_postMessage(
        channel=channel_id,
        text="Hello world! ")

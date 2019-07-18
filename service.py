import logging
import os
import boto3
import slack
from base64 import b64decode

# Grab the Bot OAuth token from the environment.
BOT_TOKEN_ENCRYPTED = os.environ["BOT_TOKEN"]
# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
BOT_TOKEN = boto3.client('kms').decrypt(CiphertextBlob=b64decode(BOT_TOKEN_ENCRYPTED))["Plaintext"].decode()

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

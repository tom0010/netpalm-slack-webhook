import requests
import yaml
from netpalm.backend.core.confload.confload import config

"""
netpalm webhook for posting netpalm info directly to Slack
IMPORTANT NOTES:
    webook requires a payload as per below
    "webhook": {
        "name": "slack",
        "args": {
            "slack_response_url": "slack response url",
            "slack_text": "slack text",
            "slack_username": "slack username",
            "slack_command": "slack command"
        }
    }
"""


def run_webhook(payload=False):
    try:
        if payload:
            slack_response_url = payload["webhook_args"]["slack_response_url"]
            slack_text = payload["webhook_args"]["slack_text"]
            slack_username = payload["webhook_args"]["slack_username"]
            slack_command = payload["webhook_args"]["slack_command"]
            text = payload["data"]["task_result"][slack_text.split(" on ")[0]]
            length = len(text) * len(text[0])
            color = "#3AA3E3"

            # Slack doesn't like big payloads
            if length > 1500:
                output = yaml.safe_dump(text[0])
            else:
                output = yaml.safe_dump(text)
            slack_payload = {
                "response_type": "in_channel",
                "attachments": [
                    {
                        "color": color,
                        "blocks": [
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"@{slack_username} executed {slack_command} {slack_text}:\n```{output}```"
                                    },
                                "type": "section"
                                }
                            ]
                        }
                    ]
                }
            response = requests.post(slack_response_url, json=slack_payload)
            if response.status_code == 200:
                return True
        return "Slack error"
    except Exception as e:
        return f"Slack error: {e}"

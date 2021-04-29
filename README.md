# netpalm-slack-webhook
A simple Slack webhook example for ![netpalm](https://github.com/tbotnz/netpalm)

![netpalm](https://user-images.githubusercontent.com/41154665/116525235-38877f00-a8d0-11eb-8ea6-cc79da542cd3.gif)

Installing the webhook:
- Load slack.py to netpalm/backend/plugins/extensibles/custom_webhooks/

Example when using a slack slash command: 
`/myslackapp show version on <my_device_name>`

Create the end point for the Slack slash command:
```
@app.route("/slack/slash_command_netpalm", methods=["POST"])
def slack_netpalm():

    # verify the slack request
    # https://api.slack.com/authentication/verifying-requests-from-slack
    response = external.verify(request)

    if response[1] != 200:
        return response
    data = request.values

    if " on " in data["text"]:
        command = data["text"].split(" on ")[0]
        device = data["text"].split()[-1]

        payload = {
          "library": "netmiko",
          "connection_args": {
            "device_type": "cisco_ios",
            "host": device,
            "username": username,
            "password": password
          },
          "command": command,
          "webhook": {
            "name": "slack",
            "args": {
                "slack_response_url": data["response_url"],
                "slack_text": data["text"],
                "slack_username": data["user_name"],
                "slack_command": data["command"]
                }
            },
          "args": {
            "use_textfsm": True,
          },
          "queue_strategy": "pinned",
        }

        headers = {"x-api-key": "api_key_here"}
        response = requests.post("https://netpalm_url:9000/getconfig",
                                 json=payload, headers=headers)
        if response.status_code == 201:
            return "Working...", 200
    return "Invalid command", 400
```

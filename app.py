import os
from xml.etree.ElementInclude import include
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "action_id": "click_btn",
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.shortcut("take_note")
def open_modal(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        # A simple view payload for a modal
        view={
			"type": "modal",
			"callback_id": "submit_callback",
			"title": {
				"type": "plain_text",
				"text": "Smart Notes"
			},
			"submit": {
				"type": "plain_text",
				"text": "Submit"
			},
			"close": {
				"type": "plain_text",
				"text": "Close"
			},
			"blocks": [
				{
					"type": "section",
					"fields": [
						{
							"type": "plain_text",
							"text": "Welcome to Smart Notes!"
						}
					]
				},
				{
					"type": "divider"
				},
				{
					"type": "input",
					"block_id": "note-type",
					"element": {
						"type": "static_select",
						"placeholder": {
							"type": "plain_text",
							"text": "Select a note type"
						},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "Action Item"
							},
							"value": "action-item"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Decision"
							},
							"value": "Decision"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Dependency"
							},
							"value": "dependency"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Other"
							},
							"value": "other"
						}
					],
					"action_id": "note-type-action"
				},
				"label": {
					"type": "plain_text",
					"text": "Type"
				}
            },
            {
				"type": "input",
				"block_id": "note-text",
				"element": {
					"type": "plain_text_input",
					"action_id": "note-text-action"
				},
				"label": {
					"type": "plain_text",
					"text": "Note"
				}
            },
          ]
        }
	)

@app.view("submit_callback")
def handle_submission(body, ack, view, say):
	ack()
	note = view["state"]["values"]["note-text"]["note-text-action"]["value"]
	type = view["state"]["values"]["note-type"]["note-type-action"]["selected_option"]["text"]["text"]
	
	say(text=f"<@{body['user']['id']}> submitted {type}: {note}", channel="C03JT95529Z")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
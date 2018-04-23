import time
import json

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, TextMessage, TextSendMessage



""" Parameters """
CHANNEL_ACCESS_TOKEN = "bsNaIC3zHJ3p+1AuBxCkDLwwXmL+GSXej5qxLgHUbimFBjqrmGBvCzw39cNe6bxYf4VJNHcxkhmBsKef4H4/wNhzPhMlhiOj709zbur0WjKCjFJgf3MLjsy5bRDo8c4V8pAs28jHoLDDLjSIP5rzvQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ff12c0f4708b41a05074ab046a84cc87"



""" Declare """
app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



""" Functions """
def echo_console(console, content) :
    print ("\n======= {} =======\n{}".format(console, content))



""" APIs """
@app.route("/callback", methods=['POST'])
def callback():

    ### get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    ### get request body as text
    body = request.get_data(as_text=True)
    echo_console("RequestBody", body)

    app.logger.info("Request body: " + body)

    ### handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(FollowEvent)
def handle_join(event) :
    channel_handle_fp = "./data/channel_handle.json"
    num_user_join_text = 2
    user_id = event.source.sender_id

    with open(channel_handle_fp, "r") as f:
        data = json.load(f)

    ### Response
    for i in range(1, num_user_join_text + 1) :
        response = data["user_join_{}".format(i)]
        text_response = TextSendMessage(text=response)
        line_bot_api.push_message(user_id, text_response)
        time.sleep(5)



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.sender_id
    text = event.message.text
    echo_console("text", text)

    if text != None :
        text_handle(line_bot_api, user_id, event, text)



def text_handle(line_bot_api, user_id, event, text) :
    ### Import required package
    from richmenu_handle import delete_richmenu, create_facebook_richmenu
    from profile_handle import project_response, intro_response

    text = text.lower()


    ### Add rich menu and set it to the user
    if text == "menu" :
        # Create rich menu
        create_facebook_richmenu(line_bot_api, user_id)

        # Text response
        text_response = TextSendMessage(text="Now you can check your gift below ><")
        line_bot_api.push_message(user_id, text_response)
        time.sleep(6)
        text_response = TextSendMessage(text="Okay... It's my Facebook.\nI see your disappointment!\nDon't worry, if you want the gift to vanish into thin air, you can just type 'I dont't want menu' ")
        line_bot_api.push_message(user_id, text_response)

    ### Delete rich menu
    elif text == "i don't want menu" :
        delete_richmenu(line_bot_api, user_id)


    ### Projects display
    elif "project" in text :
        response = project_response(text)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

    ### Self-Introduction
    elif "intro" in text :
        responses, sleeps = intro_response(text)
        for i, response in enumerate(responses) :
            time.sleep(sleeps[i])
            line_bot_api.push_message(
                to=user_id,
                messages=response
            )



if __name__ == "__main__":
    app.run()
import json
from linebot.models import TextSendMessage, ImageSendMessage



""" Parameters """
project_response_fp = "./data//profile_handle.json"
num_project = 6
num_intro = 7



""" Functions """
def init_response_list(num_project) :
    responce_list = ["projects"]
    responce_list += ["project{}".format(i) for i in range(1, num_project + 1)]

    return responce_list



def project_response(user_words) :
    response_list = init_response_list(num_project)

    try :
        response_index = response_list.index(user_words)
    except :
        response_index = "none"

    with open(project_response_fp, "r" ) as f :
        response = json.load(f)["project_response_{}".format(response_index)]

    return response



def intro_response(user_words) :
    if user_words == "intro" :
        responses = []
        sleeps = []

        with open(project_response_fp, "r") as f :
            data = json.load(f)

        for i in range(1, num_intro + 1) :
            response = data["intro_response_{}".format(i)]

            if response["type"] == "img" :
                img_response = ImageSendMessage(
                    original_content_url=response["url"],
                    preview_image_url=response["url"]
                )
                responses.append(img_response)
                sleeps.append(response["sleep"])

            elif response["type"] == "text" :
                text_response = TextSendMessage(text=response["text"])
                responses.append(text_response)
                sleeps.append(response["sleep"])

        return responses, sleeps


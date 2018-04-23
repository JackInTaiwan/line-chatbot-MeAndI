from linebot.models import (
    URITemplateAction,
    RichMenu,
    RichMenuArea,
    RichMenuBound
)



def create_facebook_richmenu(line_bot_api, user_id) :
    facebook_uri = "https://www.facebook.com/profile.php?id=100002433519943"


    ### Create one rich menu
    rich_menu_to_create = RichMenu(
        size=RichMenuBound(
            width=2500,
            height=1686
        ),
        selected=False,
        name="Fabebook Page",
        chatBarText="Gift",
        areas=[
            RichMenuArea(
                RichMenuBound(x=0, y=0, width=2000, height=1300),
                URITemplateAction(uri=facebook_uri)
            )
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu_to_create)


    ### Set image to rich_menu
    with open("dog.jpg", "rb") as f:
        pic = f.read()
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", pic)


    ### Link rich_menu_id and user_id
    line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)


    ### Console
    print ("[Create] The facebook rich menu is created and linked to the user_id = {}".format(user_id))



def delete_richmenu(line_bot_api, user_id) :
    ### Link the rich menu to the user
    line_bot_api.unlink_rich_menu_from_user(user_id)


    ### Console
    print ("[Delete] The linked rich menu is deleted. User_id is {}".format(user_id))
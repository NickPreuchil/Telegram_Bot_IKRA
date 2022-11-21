
def get_hello_message() -> str:
    content = open('Content/HelloMessage.txt', 'r', encoding="utf-8")
    if(content):
        return content.read()
    else:
        return ''

def get_help_message() -> str:
    content = open('Content/HelpMessage.txt', 'r', encoding="utf-8")
    if(content):
        return content.read()
    else:
        return ''

def get_wheel_pic() -> any:
    photo = open('Content/wheel.png', 'rb')
    if(photo):
        return photo
    else:
        return None
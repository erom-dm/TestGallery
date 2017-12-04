import requests
from bs4 import BeautifulSoup
import re
import datetime as dt

def scrapper(post_url):
    """
    Gathers and parses relevant info from instagram's post HTML page
    Testing revealed that while instagram's HTML pages are generally uniform, exceptions from this rule still happen,
    resulting in failed post creation.
    Better yet much much more complex solutions should be possible and more reliable.
    :param post_url: any insta post link should do the trick
    :return: [title_item, comment_item, url_item, date_time_item]: a list of 4 'str' items holding everything needed 
    for our Post model: titleItem, commentItem, urlItem (containing url to the file that later will 
    be downloaded into our Post.FileField) and date_timeItem. 
    """
    if post_url.startswith("https://") is False:
        post_url = "https://" + post_url
    r = requests.get(post_url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    s_info = []
    c_info = ""

    # get strings for title, date and file url ("in range" implementation is simple, but probably not the best.)
    for i, link in enumerate(soup.find_all('meta'), 1):
        if i in range(9, 12):
            s_info.append(link.get('content'))
        elif i == 23 and link.get('content').endswith(".mp4"):
            s_info[1] = link.get('content')

    # get string containing full comment (emojis are cancer, btw)
    for tag in soup.find_all('script'):
        if (tag.find(string=re.compile("window._sharedData"))) is not None:
            c_info = tag.text

    # chop off unnecessary parts of scraped strings in order to get our sweet data
    c_info = c_info.split("{\"text\": ")
    try:
        comment_item = c_info[1].split("}")[0]
    except IndexError:
        print("<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>")
        print("Either URL does not lead to a valid instagram post, or its a slightly different HTML "
              "layout on instagram's end")
        pass

    # @instagram_user is sometimes wrapped in () inside HTML, and sometimes it is not. Here's the workaround:
    element = s_info[2]
    tag_index = element.index("@")
    element = element[tag_index:].split(" ")[0]
    if element.endswith(")"):
        element = element[0:len(element) - 1]
    s0split = s_info[0].split("• ")
    title_item = s0split[0] + element

    url_item = s_info[1]

    # Instagram date example: 'Dec 3, 2017 at 6:46pm UTC'
    # There's got to be a better way to do this
    date_time_item = s0split[1]
    month = date_time_item.split(" ")[0]
    cal = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
           "Nov": 11, "Dec": 12}
    month = int(cal[month])
    day = int(date_time_item.split(" ")[1].split(",")[0])
    year = int(date_time_item.split(", ")[1].split(" at")[0])
    hour = int(date_time_item.split("at ")[1].split(":")[0])
    minute = int(date_time_item.split(":")[1][0:2])
    date_time_item = dt.datetime(year, month, day, hour, minute, second=0, microsecond=0)
    print(date_time_item)

    model_stuff = [title_item, comment_item, url_item, date_time_item]

    return model_stuff


test = "https://www.instagram.com/p/BGFV0Jtg5hQ/?taken-by=python.programming"
aa = scrapper(test)
print(aa)

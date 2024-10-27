from collections import namedtuple
from datetime import datetime
import requests

POSTS = dict()

Post = namedtuple('Post', ['link', 'title', 'date'])

LAST_PAGE = 5

url = 'https://crosscountrymortgage.wd1.myworkdayjobs.com/wday/cxs/crosscountrymortgage/CCMCareers/jobs'

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US',
    'content-type': 'application/json',
    'cookie': 'wd-browser-id=04d11a03-233d-4be0-af44-e84380ad3545; CALYPSO_CSRF_TOKEN=a7ae1bf3-b24d-4f08-b82d-841aed1e1a91; PLAY_SESSION=43636b6932339b5094948f179b596cc16b38ebfe-crosscountrymortgage_pSessionId=u2seaa6gnohibkfnp9c78amerv&instance=vps-prod-m117ypap.prod-vps.pr502.cust.ash.wd; wday_vps_cookie=3245963274.53810.0000; __cflb=0H28vCu5mZQ5H5URQ4Xbzh7qZvE1AhPn1qZmKtwfrig; _cfuvid=.21mad8246Nqtloh0ujcUldlnSUGtiREdsvkLvTutWk-1730044055618-0.0.1.1-604800000; timezoneOffset=300; __cf_bm=uiS1uOozx6liPMCkMQYG9ds.3ppqbMa5qtc7Dl.CxL0-1730045786-1.0.1.1-CdQzt8GahobadlUONtCLY9qukGvApj3o9baIwDse3tX8QQDTem9Eb8lFFYC5oz5N1RiF3M.4u.RezvPTF9VQNQ',
    'origin': 'https://crosscountrymortgage.wd1.myworkdayjobs.com',
    'priority': 'u=1, i',
    'referer': 'https://crosscountrymortgage.wd1.myworkdayjobs.com/CCMCareers?locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-calypso-csrf-token': 'a7ae1bf3-b24d-4f08-b82d-841aed1e1a91',
}

json_data = {"appliedFacets":{"locationCountry":["bc33aa3152ec42d4995f4791a106ed09"]},"limit":20,"offset":0,"searchText":""}

for page in range(LAST_PAGE):
    json_data["offset"] = 20 * page

    response = requests.post(
        url=url,
        headers=headers,
        json=json_data
    )

    jobs = dict(response.json())['jobPostings']

    for job in jobs:
        title = job['title']
        link = "https://crosscountrymortgage.wd1.myworkdayjobs.com/en-US/CCMCareers"+job['externalPath']
        if not (link in POSTS.keys()):
            POSTS[link] = Post(link, title, -1 * len(POSTS))


STREAM = sorted([POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True)

if __name__ == "__main__":

    NOW = datetime.now()
    XML = "\n".join([ r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>Cross Country Mortgage Careers</title>""",
            r"""<description>Cross Country Mortgage Careers</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</pubDate>""",
            r"""<lastBuildDate>"""+NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")+r"""</lastBuildDate>""",
            "\n".join([r"""<item><title><![CDATA["""+x.title+r"""]]></title><link>"""+x.link+r"""</link></item>""" for x in STREAM]),
            r"""</channel>""",
            r"""</rss>""",
    ])

    print(XML)

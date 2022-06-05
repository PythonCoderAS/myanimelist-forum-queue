import re

from jikanpy import AioJikan
from aiohttp import ClientSession

from .models import Post
from myanimelist_forum_queue.secrets import csrf_token
from asyncio import sleep, Lock
from asgiref.sync import sync_to_async

lock = Lock()

valid_topic_id = re.compile(r'/forum/\?topicid=(\d+)')


async def post(item: Post):
    async with ClientSession() as session, AioJikan(session=session) as jikan, lock:
        params = {
            "action": "post",
        }
        data = {
            "msg_text": item.body,
            "action_type": "submit",
            "csrf_token": csrf_token,
        }
        if item.board_id:
            data["topic_title"] = item.title
            params["boardid"] = item.board_id
        elif item.club_id:
            data["topic_title"] = item.title
            params["club_id"] = item.club_id
        elif item.anime_id:
            params["anime_id"] = data["anime_id"] = item.anime_id
            if item.part_number:
                data["epcheck"] = 1
                data["epNum"] = item.part_number
                item.title = await jikan.anime(item.anime_id)["title"]
            else:
                data["topic_title"] = item.title
        elif item.manga_id:
            params["manga_id"] = data["manga_id"] = item.manga_id
            if item.part_number:
                data["epcheck"] = 1
                data["epNum"] = item.part_number
                item.title = await jikan.manga(item.manga_id)["title"]
            else:
                data["topic_title"] = item.title
        retry = False
        async with session.post("https://myanimelist.net/forum/", data=data, params=params) as response:
            if response.status == 200:
                text = await response.text()
                if match := valid_topic_id.search(text):
                    item.topic_id = match.group(1)
                    await sync_to_async(item.save, thread_sensitive=True)()
                else:
                    # Did not work, retry once
                    retry = True
        await sleep(300)
    if retry:
        return await post(item)

import asyncio
import aiohttp
from typing import Optional


class nhentaiException(Exception):
    pass


class nhentai():

    __slots__ = ('id', 'title', 'mediaId', 'tags', 'baseURL')
    def __init__(self, id: Optional[int] = None, mediaId: Optional[int] = None,
                 title: Optional[str] = None, tags: Optional[list] = None):

        """
        API Documentation:

        :param id[int]: The ID of the gallery.
        :param mediaId[int]: The ID of the media.
        :param title[str]: Search using doujin title.
        :param tags[list]: Search using tags.

        """
        
        self.tags    = '+'.join(tags) if tags else None
        self.id      = id
        self.title   = title
        self.mediaId = mediaId
        self.baseURL = 'https://nhentai.net/api/'

    async def getByID(self):
        return await self._request(url=self.baseURL+'gallery/'+str(self.id))

    def getCover(self):
        coverURL = "https://t.nhentai.net/galleries/" + str(self.mediaId) + "/cover.jpg"
        return coverURL

    async def getPageImage(self, page):
        coverURL = "https://i.nhentai.net/galleries/" + str(self.mediaId) + "/" + str(page) + ".jpg"
        return coverURL

    async def getByTitle(self, page = 1, sort='popular'):
        payload = {'query':'title:' + str(self.title),
                   'page': page,
                   'sort': sort}
        
        response = await self._request(url=self.baseURL+'galleries/search', params=payload)
        return response["result"]

    async def getByTag(self, page = 1, sort='popular'):
        payload = {'query':'tag:' + str(self.tags),
                   'page': page,
                   'sort': sort}

        response = await self._request(url=self.baseURL+'galleries/search', params=payload)
        return response["result"]

    async def _request(self, url, payload: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=payload) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    return response
                else:
                    raise nhentaiException(f"_request({resp.status}): Failed to get respone from server")

if __name__ == "__main__":
    pass
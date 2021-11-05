import aiohttp
from typing import Optional


class nhentaiException(Exception):
    pass


class nhentai():

    __slots__ = ('id', 'title', 'mediaId', 'tags', 'baseURL', 'response')
    def __init__(self, id: Optional[int] = None, mediaId: Optional[int] = None,
                 title: Optional[str] = None, tags: Optional[list] = None):

        """
        API Documentation:

        :param id[int]: The ID of the doujin.
        :param mediaId[int]: The ID of the media.
        :param title[str]: Search using doujin title.
        :param tags[list]: Search using tags.

        """
        
        self.tags    = '+'.join(tags) if tags else None
        self.id      = str(id)
        self.title   = str(title)
        self.mediaId = str(mediaId)
        self.baseURL = 'https://nhentai.net/api/'
        self.response = None

    async def getByID(self):
        self.response = await self._request(url=self.baseURL+'gallery/'+self.id)
        return self.response

    def getCover(self):
        coverURL = "https://t.nhentai.net/galleries/" + self.response['media_id'] + "/cover.jpg"
        return coverURL

    def getPageImage(self):
        """
        Get a list of image URLs for the doujin.
        """
        imageUrl = []
        for i in range(1, self.response['num_pages']+1):
            if self.response['images']['pages'][i-1]['t'] == 'p':
                type = 'png'
            else:
                type = 'jpg'
            imageUrl.append(f"https://i.nhentai.net/galleries/{self.response['media_id']}/{i}.{type}")
        
        return imageUrl

    async def getByTitle(self, page = 1, sort='popular'):
        """
        Arguments:
            page: Page number. (Default: 1)

            sort: popular, popular-year, popular-month, popular-week, popular-today, date (Default: popular)
        """
        payload = {'query':'title:' + self.title,
                   'page': page,
                   'sort': sort}
        
        response = await self._request(url=self.baseURL+'galleries/search', payload=payload)
        return response["result"]

    async def getByTag(self, page = 1, sort='popular'):
        """
        Arguments:
            page: Page number. (Default: 1)

            sort: popular, popular-year, popular-month, popular-week, popular-today, date (Default: popular)
        """
        payload = {'query':'tag:' + str(self.tags),
                   'page': page,
                   'sort': sort}

        response = await self._request(url=self.baseURL+'galleries/search', payload=payload)
        return response["result"]

    async def _request(self, url, payload: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=payload) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    return response
                else:
                    raise nhentaiException(f"_request({resp.status}): Failed to get respone from server\n{await resp.json()}")


if __name__ == "__main__":
    pass

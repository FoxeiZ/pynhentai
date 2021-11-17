import aiohttp
from typing import Optional
import reprlib


class nhentaiException(Exception):
    pass


class nhentaiContainer:

    __slots__ = ('id', 'tags', 'title', 'title_jpn', 'title_prt', 'media_id', 'images', 'pages', 'cover', 'scanlator', 'thumbnail')
    def __init__(self, payload: dict) -> None:
        self.id        = payload['id']
        self.tags      = payload['tags']
        self.title     = payload['title']['english']
        self.title_jpn = payload['title']['japanese'] # Sometime this is empty
        self.title_prt = payload['title']['pretty']   # Short title of the doujin
        self.media_id  = payload['media_id']
        self.pages     = payload['images']['pages']
        self.cover     = payload['images']['cover']
        self.thumbnail = payload['images']['thumbnail']
        self.scanlator = payload['scanlator']

        self.cover['url'] = "https://t.nhentai.net/galleries/" + self.media_id + "/cover.jpg"
        for i in range(0, payload['num_pages']):
            if self.pages[i]['t'] == 'p':
                type = 'png'
            else:
                type = 'jpg'
            self.pages[i]['url'] = f"https://i.nhentai.net/galleries/{self.media_id}/{i+1}.{type}"

    def __str__(self) -> str:
        return self.title

    def __int__(self) -> int:
        return self.id

    def __repr__(self):
        rep = reprlib.Repr()
        return f"<nhentaiContainer(id={self.id}, media_id={self.media_id}, title={rep.repr(self.title)})>"


class nhentai:

    __slots__ = ('baseURL', 'response')
    def __init__(self):

        self.baseURL  = 'https://nhentai.net/api/'
        self.response = None

    async def getByID(self, id: int = None):
        self.response = await self._request(url=self.baseURL + 'gallery/' + str(id))
        return nhentaiContainer(self.response)

    async def getCover(self, id: int):
        if self.response is None:
            resp = await self.getByID(id=id)
            return resp.cover['url']

        if "result" not in self.response and id == self.response['id']:
            return nhentaiContainer(self.response).cover['url']
        else:
            resp = await self.getByID(id=id)
            return resp.cover['url']

    async def getPageImage(self, id: int):
        """
        Get a list of image URLs for the doujin.
        """
        if self.response is None:
            resp = await self.getByID(id=id)
            return resp.pages

        if "result" not in self.response and id == self.response['id']:
            return nhentaiContainer(self.response).pages
        else:
            resp = await self.getByID(id=id)
            return resp.pages

    async def searchByTitle(self, title: str = None, page = 1, sort='popular'):
        """
        Arguments:
            title[str]: Search using doujin title.

            page[int]: Page number. (Default: 1)

            sort[str]: popular, popular-year, popular-month, popular-week, popular-today, date (Default: popular)
        """
        payload = {'query': 'title:' + title,
                   'page': page,
                   'sort': sort}

        response = await self._request(url=self.baseURL + 'galleries/search', payload=payload)

        if response['result'] == 0:
            raise nhentaiException(f"No results found for {title}")

        if isinstance(response['result'], list):
            result = [nhentaiContainer(_) for _ in response['result']]
        else:
            result = nhentaiContainer(response['result'])

        return result

    async def searchByTag(self, tags: list, page = 1, sort='popular'):
        """
        Arguments:
            tags[list]: List of tags.

            page[int]: Page number. (Default: 1)

            sort[str]: popular, popular-year, popular-month, popular-week, popular-today, date (Default: popular)
        """
        tags = '+'.join(tags) # Convert list to string
        payload = {'query': 'tag:' + str(tags),
                   'page': page,
                   'sort': sort}

        response = await self._request(url=self.baseURL + 'galleries/search', payload=payload)

        if response['result'] == 0:
            raise nhentaiException(f"No results found for {tags}")

        if isinstance(response['result'], list):
            result = [nhentaiContainer(_) for _ in response['result']]
        else:
            result = nhentaiContainer(response['result'])

        return result

    async def searchByPayload(self, payloadType, **payload):
        """
        Arguments:
            payloadType[str]: Type of payload. (ex: search)
            payload[dict]: Payload.

        """
        response = await self._request(url=self.baseURL + 'galleries/' + payloadType, payload=payload)
        return response

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

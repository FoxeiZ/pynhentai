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
        for i in range(1, payload['num_pages']+1):
            if self.pages[i-1]['t'] == 'p':
                type = 'png'
            else:
                type = 'jpg'
            self.pages[i-1]['url'] = f"https://i.nhentai.net/galleries/{self.media_id}/{i}.{type}"

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

        """
        API Documentation:

        :param id[int]: The ID of the doujin.
        :param mediaId[int]: The ID of the media.
        :param title[str]: Search using doujin title.
        :param tags[list]: Search using tags.

        """
        self.baseURL  = 'https://nhentai.net/api/'
        self.response = None

    async def getByID(self, id: int = None):
        self.response = await self._request(url=self.baseURL+'gallery/'+str(id))
        return nhentaiContainer(self.response)

    def getCover(self, id: int):
        if self.response is None:
            return self.getByID(id).cover['url']
        else:
            # TODO return a list of cover from nhentaiContainer
            pass 

    def getPageImage(self):
        """
        Get a list of image URLs for the doujin.
        """
        # TODO: Implement this
        pass

    async def searchByTitle(self, title: str = None, page = 1, sort='popular'):
        """
        Arguments:
            title[str]: Search using doujin title.

            page[int]: Page number. (Default: 1)

            sort[str]: popular, popular-year, popular-month, popular-week, popular-today, date (Default: popular)
        """
        payload = {'query':'title:' + title,
                   'page': page,
                   'sort': sort}
        
        response = await self._request(url=self.baseURL+'galleries/search', payload=payload)

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
        tags = '+'.join(tags) if tags else None
        payload = {'query':'tag:' + str(tags),
                   'page': page,
                   'sort': sort}

        response = await self._request(url=self.baseURL+'galleries/search', payload=payload)
        
        if response['result'] == 0:
            raise nhentaiException(f"No results found for {tags}")

        if isinstance(response['result'], list):
            result = [nhentaiContainer(_) for _ in response['result']]
        else:
            result = nhentaiContainer(response['result'])

        return result

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

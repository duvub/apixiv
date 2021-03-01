from ..base import PixivLogin


class New(PixivLogin):

    def __init__(self, cls, r18: str, limit: int, proxy=None):
        super().__init__(proxy=proxy)
        self.url = '/'.join([self._get_ajax_url, cls, 'new'])
        self.params = {
            'lastId': 0,
            'limit': limit,
            'r18': 'true' if r18 else 'false',
            'lang': self.lang
        }

    async def _nbody(self, cls):
        result = await self._async_GET_json(url=self.url, params=self.params, headers=self.headers)
        return result['body'][cls]

    @property
    async def result(self):
        """最新的条目"""
        return await self._body()

    @property
    async def ids(self) -> list:
        """最新的条目的ID"""
        result = await self.result
        return [work['id'] for work in result]


class NewIllust(New):
    """站内最新的插画"""
    def __init__(self, r18=False, limit=20, proxy=None):
        super().__init__(cls='illust', r18=r18, limit=limit, proxy=proxy)
        self.params['type'] = 'illust'

    async def _body(self) -> list:
        return await self._nbody(cls='illusts')


class NewManga(New):
    """站内最新的漫画"""
    def __init__(self, r18=False, limit=20, proxy=None):
        super().__init__(cls='illust', r18=r18, limit=limit, proxy=proxy)
        self.params['type'] = 'manga'

    async def _body(self) -> list:
        return await self._nbody(cls='illusts')


class NewNovel(New):
    """站内最新的小说"""
    def __init__(self, r18=False, limit=20, proxy=None):
        super().__init__(cls='novel', r18=r18, limit=limit, proxy=proxy)

    async def _body(self) -> list:
        return await self._nbody(cls='novels')

from ..base import PixivLogin


class Index(PixivLogin):

    def __init__(self, cls, proxy=None):
        super().__init__(proxy=proxy)
        self.mode = 'all'
        self.url = '/'.join([self._get_ajax_url, 'top', cls])
        self.params = {
            'mode': self.mode,
            'lang': self.lang
        }

    async def _body(self) -> dict:
        result = await self._async_GET_json(url=self.url, params=self.params, headers=self.headers)
        return result['body']

    async def recommend(self) -> list:
        """推荐插画列表"""
        result = await self._get_page(key='recommend')
        data = []
        for key, value in result['details'].items():
            data.append({'id': key, 'seedIllust': [si for si in value['seedIllustIds']]})
        return data

    async def recommend_tag(self) -> list:
        """推荐标签列表"""
        result = await self._get_page('recommendByTag')
        data = []
        for rec_tag in result:
            data.append({'tag': rec_tag['tag'], 'recommend': [iid for iid in rec_tag['ids']]})
        return data

    async def rank(self) -> list:
        """排行列表"""
        ranking = await self._get_page('ranking')
        return ranking['items']

    async def recommend_user(self) -> list:
        """推荐用户"""
        return await self._get_page('recommendUser')


class IndexIllust(Index):

    def __init__(self, proxy=None):
        super().__init__(cls='illust', proxy=proxy)


class IndexManga(Index):

    def __init__(self, proxy=None):
        super().__init__(cls='manga', proxy=proxy)


class IndexNovel(Index):

    def __init__(self, proxy=None):
        super().__init__(cls='novel', proxy=proxy)

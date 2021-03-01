from ..base import PixivLogin


class LUserInfoPage(PixivLogin):
    """用户信息页类"""
    def __init__(self, uid: str or int, **kwargs):
        super().__init__(**kwargs)
        self.uid = str(uid)
        self.params = {
            'full': 1,
            'lang': self.lang
        }
        self.url = '/'.join([self._get_ajax_url, 'user', self.uid])

    async def _body(self) -> dict:
        body = await self._async_GET_json(url=self.url, params=self.params, headers=self.headers)
        return body['body']

    @property
    async def name(self) -> str:
        """姓名"""
        return await self._get_body('name')

    @property
    async def follow(self) -> int:
        """关注量"""
        return await self._get_body('following')

    @property
    async def region(self) -> str:
        """所在地区"""
        region = await self._get_body('region')
        return region['name']

    @property
    async def comment(self) -> str:
        """简介"""
        return await self._get_body('comment')

    @property
    async def birthday(self) -> str:
        """生日"""
        birthday = await self._get_body('birthDay')
        return birthday['name']

    @property
    async def job(self) -> str:
        """工作"""
        job = await self._get_body('job')
        return job['name']

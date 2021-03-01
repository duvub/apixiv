from ..base import PixivLogin
import asyncio


class BookMark(PixivLogin):
    def __init__(self, cls, uid=None, page_number=0, limit=50, public=True, proxy=None):
        super().__init__(proxy=proxy)
        self.uid = uid if uid else self.userid
        self.url = '/'.join([self._get_ajax_url, 'user', self.uid, cls, 'bookmarks'])
        self.public = public
        self.page_number = page_number
        self.limit = limit
        self._page_numbers = None
        self.params = {
            'tag': '',
            'offset': page_number * limit,
            'limit': limit,
            'rest': 'show' if public else 'hide',
            'lang': self.lang
        }

    async def _body(self) -> dict:
        result = await self._async_GET_json(url=self.url, params=self.params, headers=self.headers)
        return result['body']

    @property
    async def total(self) -> int:
        """收藏量"""
        return await self._get_body('total')

    @property
    async def page_numbers(self) -> int:
        """收藏页数"""
        total = await self.total
        self._page_numbers = total // self.limit + 1 if total % self.limit else total // self.limit
        return self._page_numbers

    @property
    async def works(self) -> list:
        """当前页收藏条目"""
        return await self._get_body('works')

    def __aiter__(self):
        return self

    async def __anext__(self):
        ap = self._page_numbers if self._page_numbers else await self.page_numbers
        if self.page_number < ap:
            self.params['offset'] = self.page_number * self.limit
            self.page_number += 1
            return await self.works
        raise StopAsyncIteration


class IllustAndMangaBookMark(BookMark):

    def __init__(self, uid=None, page_number=0, public=True, proxy=None):
        super().__init__(cls='illusts', uid=uid, page_number=page_number, public=public, proxy=proxy)

    async def all(self):
        """
        查询所有页, 如果你有成百上千的页数时最好不要使用，除非你有能力控制你的同时并发数量。
        在这种情况下可以使用异步迭代器(async for)对该对象进行迭代，虽然速度会慢一些
        """
        pn = self._page_numbers if self._page_numbers else await self.page_numbers
        tasks = [asyncio.create_task(IllustAndMangaBookMark(uid=self.uid, page_number=p, public=self.public, proxy=self._proxy).works) for p in range(pn)]
        done, pending = await asyncio.wait(tasks)
        return [task.result() for task in done]


class NovelsBookMark(BookMark):

    def __init__(self, uid=None, page_number=0, public=True, proxy=None):
        super().__init__(cls='novels', uid=uid, page_number=page_number, public=public, proxy=proxy)

    async def all(self):
        """
        查询所有页, 如果你有成百上千的页数时最好不要使用，除非你有能力控制你的同时并发数量。
        在这种情况下可以使用异步迭代器(async for)对该对象进行迭代，虽然速度会慢一些
        """
        pn = self._page_numbers if self._page_numbers else await self.page_numbers
        tasks = [asyncio.create_task(NovelsBookMark(uid=self.uid, page_number=p, public=self.public, proxy=self._proxy).works) for p in range(pn)]
        done, pending = await asyncio.wait(tasks)
        return [task.result() for task in done]

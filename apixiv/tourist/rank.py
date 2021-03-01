from ..base import Pixiv
from datetime import datetime, timedelta
from pytz import timezone


class Rank(Pixiv):
    """
    时区查找: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    """
    UTC = 'Asia/Shanghai'

    def __init__(self, cls, page_number=0, day=None, proxy=None):
        super().__init__(proxy=proxy)
        self.url = '/'.join([self.BASEURL, 'ranking.php'])

        self.mode = cls
        self.date = (datetime.now(timezone(self.UTC)) + timedelta(days=-1)).strftime('%Y%m%d') if not day else day
        self._total = 0
        self._result = []
        self.page = 1 if not page_number else page_number
        self.params = {
            'mode': cls,
            'date': self.date,
            'format': 'json'
        }
        if page_number:
            self.params['p'] = page_number

    async def _body(self) -> dict:
        result = await self._async_GET_json(url=self.url, params=self.params)
        return result

    @property
    async def result(self) -> list:
        """条目"""
        self._result = await self._get_body('contents')
        return self._result

    @property
    async def ids(self) -> list:
        """排行榜所有的插画id"""
        result = self._result if self._result else await self.result
        return [il['illust_id'] for il in result]


class DayRank(Rank):
    """日榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='daily', proxy=proxy)


class WeekRank(Rank):
    """周榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='weekly', proxy=proxy)


class MonthRank(Rank):
    """月榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='monthly', proxy=proxy)


class BeginnerRank(Rank):
    """新人榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='rookie', proxy=proxy)


class OriginalRank(Rank):
    """原创榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='original', proxy=proxy)


class MaleRank(Rank):
    """男性喜欢榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='male', proxy=proxy)


class FemaleRank(Rank):
    """女性喜欢榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='female', proxy=proxy)


class IllustDayRank(DayRank):
    """插画日榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class IllustWeekRank(WeekRank):
    """插画周榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class IllustMonthRank(MonthRank):
    """插画月榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class IllustBeginnerRank(BeginnerRank):
    """插画新人榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class GifDayRank(DayRank):
    """动图日榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'ugoira'


class GifWeekRank(WeekRank):
    """动图周榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'ugoira'


class MangaDayRank(DayRank):
    """漫画日榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class MangaWeekRank(WeekRank):
    """漫画周榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class MangaMonthRank(MonthRank):
    """漫画月榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class MangaBeginnerRank(BeginnerRank):
    """漫画新人榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class NovelDayRank(DayRank):
    """插画日榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'

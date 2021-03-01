from .. import PixivLogin, Rank


class LRank(Rank, PixivLogin):

    async def _body(self) -> dict:
        result = await self._async_GET_json(url=self.url, params=self.params, headers=self.headers)
        return result


class LDayRank(LRank):
    """日榜"""
    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        if not r18:
            super().__init__(page_number=page_number, day=day, cls='daily', proxy=proxy)
        else:
            super().__init__(page_number=page_number, day=day, cls='daily_r18', proxy=proxy)


class LWeekRank(LRank):
    """周榜"""
    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        if not r18:
            super().__init__(page_number=page_number, day=day, cls='weekly', proxy=proxy)
        else:
            super().__init__(page_number=page_number, day=day, cls='weekly_r18', proxy=proxy)


class LMonthRank(LRank):
    """月榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='monthly', proxy=proxy)


class LBeginnerRank(LRank):
    """新人榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='rookie', proxy=proxy)


class LOriginalRank(LRank):
    """原创榜"""
    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, cls='original', proxy=proxy)


class LMaleRank(LRank):
    """男性喜欢榜"""
    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        if not r18:
            super().__init__(page_number=page_number, day=day, cls='male', proxy=proxy)
        else:
            super().__init__(page_number=page_number, day=day, cls='male_r18', proxy=proxy)


class LFemaleRank(LRank):
    """女性喜欢榜"""
    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        if not r18:
            super().__init__(page_number=page_number, day=day, cls='female', proxy=proxy)
        else:
            super().__init__(page_number=page_number, day=day, cls='female_r18', proxy=proxy)

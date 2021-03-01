from .complex import LDayRank, LWeekRank, LMonthRank, LBeginnerRank
from .illust import LIllustR18MaleRank, LIllustR18FemaleRank


class LMangaDayRank(LDayRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class LMangaWeekRank(LWeekRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class LMangaMonthRank(LMonthRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'manga'


class LMangaBeginnerRank(LBeginnerRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class LMangaR18MaleRank(LIllustR18MaleRank):
    pass


class LMangaR18FemaleRank(LIllustR18FemaleRank):
    pass

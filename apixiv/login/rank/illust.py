from .complex import LDayRank, LWeekRank, LMonthRank, LBeginnerRank, LMaleRank, LFemaleRank


class LIllustDayRank(LDayRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class LIllustWeekRank(LWeekRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class LIllustMonthRank(LMonthRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class LIllustBeginnerRank(LBeginnerRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'illust'


class LIllustR18MaleRank(LMaleRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(r18=True, page_number=page_number, day=day, proxy=proxy)


class LIllustR18FemaleRank(LFemaleRank):

    def __init__(self, page_number=0, day=None, proxy=None):
        super().__init__(r18=True, page_number=page_number, day=day, proxy=proxy)

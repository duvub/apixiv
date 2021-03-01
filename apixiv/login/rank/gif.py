from .complex import LDayRank, LWeekRank


class LGifDayRank(LDayRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'ugoira'


class LGifWeekRank(LWeekRank):

    def __init__(self, r18=False, page_number=0, day=None, proxy=None):
        super().__init__(r18=r18, page_number=page_number, day=day, proxy=proxy)
        self.params['content'] = 'ugoira'

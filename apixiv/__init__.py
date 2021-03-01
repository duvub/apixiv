
from .base import PixivError, Pixiv, PixivLogin
from .login import (LUserInfoPage,
                    IndexIllust, IndexManga, IndexNovel,
                    IllustAndMangaBookMark, NovelsBookMark,
                    NewIllust, NewManga, NewNovel,
                    LDayRank, LWeekRank, LMonthRank, LBeginnerRank, LOriginalRank, LMaleRank, LFemaleRank,
                    LIllustDayRank, LIllustWeekRank, LIllustMonthRank, LIllustBeginnerRank,
                    LIllustR18MaleRank, LIllustR18FemaleRank,
                    LGifDayRank, LGifWeekRank,
                    LMangaDayRank, LMangaWeekRank, LMangaMonthRank, LMangaBeginnerRank,
                    LMangaR18MaleRank, LMangaR18FemaleRank)
from .tourist import (IllustUrl, IllustInfo, UserInfoPage,
                      DayRank, WeekRank, MonthRank, BeginnerRank, OriginalRank, MaleRank, FemaleRank,
                      IllustDayRank, IllustWeekRank, IllustMonthRank, IllustBeginnerRank,
                      GifDayRank, GifWeekRank,
                      MangaDayRank, MangaWeekRank, MangaMonthRank, MangaBeginnerRank)


# language
LANG = 'zh'


# 配置文件保持路径
USER_CONFIG_PATH = '.userinfo.yml'

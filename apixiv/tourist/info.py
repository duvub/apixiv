from apixiv.base import PixivError, Pixiv
import asyncio
import os
import sys


class IllustUrl(Pixiv):
    def __init__(self, iid, proxy=None):
        super().__init__(proxy=proxy)
        self.iid = str(iid)
        self.url = '/'.join([self._get_ajax_url, 'illust', self.iid, 'pages'])
        self.params = {'lang': self.lang}

    async def _body(self) -> dict:
        """主体内容"""
        try:
            result = await self._async_GET_json(url=self.url, params=self.params)
            return result['body']
        except PixivError as error:
            print(f"{self.iid}:{error.message}")

    async def _get_url(self, key):
        body = await self._body()
        return [url['urls'].get(key) for url in body] if body else []

    @property
    async def thumb_minis(self) -> list:
        """迷你尺寸"""
        return await self._get_url('thumb_mini')

    @property
    async def smalls(self) -> list:
        """小尺寸"""
        return await self._get_url('small')

    @property
    async def regulars(self) -> list:
        """常规尺寸"""
        return await self._get_url('regular')

    @property
    async def originals(self) -> list:
        """原图尺寸"""
        return await self._get_url('original')


class IllustInfo(Pixiv):
    """多次调用可能导致IP被封"""
    def __init__(self, iid, proxy=None):
        super().__init__(proxy=proxy)
        self.iid = str(iid)
        self.url = '/'.join([self._get_ajax_url, 'illust', self.iid])
        self.params = {'lang': self.lang}

        self._page_count = 0
        self._title = ''

    def __repr__(self):
        return self.iid

    async def _body(self) -> dict:
        """主体内容"""
        result = await self._async_GET_json(url=self.url, params=self.params)
        return result['body']

    async def _get_body(self, key: str, another=None):
        body = await self._body()
        value = body.get(key)
        return value if value else another

    @property
    async def title(self):
        """标题"""
        self._title = await self._get_body('illustTitle')
        return self._title

    @property
    async def description(self):
        """描述"""
        return await self._get_body('description')

    @property
    async def create_date(self):
        """创建日期"""
        return await self._get_body('createDate')

    @property
    async def upload_date(self):
        """上传日期"""
        return await self._get_body('uploadDate')

    @property
    async def tags(self):
        """该插画所在的标签列表"""
        tags = await self._get_body('tags')
        return [tag['tag'] for tag in tags['tags']]

    @property
    async def page_count(self):
        """插画的数量"""
        self._page_count = await self._get_body('pageCount')
        return self._page_count

    @property
    async def width(self):
        """插画宽度"""
        return await self._get_body('width')

    @property
    async def height(self):
        """插画高度"""
        return await self._get_body('height')

    def illust_url(self) -> IllustUrl:
        return IllustUrl(iid=self.iid, proxy=self._proxy)

    async def down(self, load_path=os.getcwd(), down_type='original'):
        """
        :param load_path: 保存路径
        :param down_type: 下载类型
        :return:
        """
        title = self._title if self._title else await self.title

        async def fetch(number: int, url: str):
            nonlocal load_path
            nonlocal title
            content = await self._async_GET_content(url=url, headers={'referer': self.BASEURL+'/'})
            suffix = '.' + url.split('.')[-1]
            filename = f'[{str(number)}]' + self._windows_filename(title) + suffix
            filepath = os.path.join(load_path, filename)
            with open(filepath, 'wb') as f:
                f.write(content)
            sys.stdout.write(f"[finish] name:{title} number:{number} \n")

        url_obj = self.illust_url()
        if down_type == 'original':
            urls = await url_obj.originals
        elif down_type == 'thumb_mini':
            urls = await url_obj.thumb_minis
        elif down_type == 'small':
            urls = await url_obj.smalls
        elif down_type == 'regular':
            urls = await url_obj.regulars
        else:
            raise PixivError(f'not found {down_type}')
        if urls:
            if os.path.isdir(load_path):
                load_path = os.path.join(load_path, self.iid)
                os.mkdir(load_path)
            tasks = [asyncio.create_task(fetch(index, url)) for index, url in enumerate(urls)]
            await asyncio.wait(tasks)
            sys.stdout.flush()


class UserInfoPage(Pixiv):
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
        body = await self._async_GET_json(url=self.url, params=self.params)
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

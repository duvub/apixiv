import asyncio
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as Browser_options
import aiohttp
import yaml

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class PixivError(Exception):

    def __init__(self, message):
        self.message = message
        self.status_code = 2333

    def __str__(self):
        return self.message


class APixivRequest(object):
    """负责网络请求"""
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'

    def __init__(self, proxy=None):
        self._proxy = proxy

    def _headers(self, headers=None):
        if headers is None:
            headers = {}
        headers.update({"User-Agent": self.USER_AGENT})
        return headers

    @staticmethod
    async def _async_request(restype='json', **request_data):
        try:
            async with aiohttp.request(**request_data) as response:
                if restype == 'json':
                    resp = await response.json()
                elif restype == 'text':
                    resp = await response.text()
                elif restype == 'bytes':
                    resp = await response.read()
                elif restype == 'headers':
                    resp = response.headers
        except aiohttp.ClientConnectorError as error:
            await asyncio.sleep(3)
            async with aiohttp.request(**request_data) as response:
                if restype == 'json':
                    resp = await response.json()
                elif restype == 'text':
                    resp = await response.text()
                elif restype == 'bytes':
                    resp = await response.read()
                elif restype == 'headers':
                    resp = response.headers

        return resp

    async def _async_GET(self, url: str, method='GET', **request_data):

        request_data['url'] = url
        request_data['method'] = method
        request_data['headers'] = self._headers(request_data.get('headers'))        # 当请求不携带headers的时候自动添加
        request_data['proxy'] = self._proxy

        return await self._async_request(**request_data)

    async def _async_GET_text(self, **request_data) -> str:
        return await self._async_GET(restype='text', **request_data)

    async def _async_GET_json(self, **request_data) -> dict:
        response = await self._async_GET(restype='json', **request_data)
        if response.get('error'):
            message = response.get('message')
            if message:
                raise PixivError(message)
            else:
                print(response, request_data)
                raise PixivError(response.get('error'))
        return response

    async def _async_GET_content(self, **request_data) -> bytes:
        return await self._async_GET(restype='bytes', **request_data)

    async def _async_GET_headers(self, **kwargs) -> dict:
        return await self._async_GET(restype='headers', **kwargs)


class Pixiv(APixivRequest):
    BASEURL = 'https://www.pixiv.net'

    def __init__(self, proxy=None):
        super().__init__(proxy)
        from . import LANG
        self.lang = LANG

    @property
    def _get_ajax_url(self):
        return '/'.join([self.BASEURL, 'ajax'])

    @staticmethod
    def _linux_filename(old_filename: str):
        """适用于Linux的文件名"""
        return old_filename.replace('/', '、')

    def _windows_filename(self, old_filename: str):
        """适用于Windows平台的文件名"""
        nf = self._linux_filename(old_filename)
        nf = nf.replace('?', '？')
        nf = nf.replace('\\', '、')
        nf = nf.replace('*', '⭐')
        nf = nf.replace('<', '《')
        nf = nf.replace('>', '》')
        nf = nf.replace('|', '丨')
        nf = nf.replace('"', '“')
        nf = nf.replace(':', '：')
        return nf

    async def _body(self) -> dict:
        """用于子类中被调取"""

    async def _get_body(self, key, another=None):
        body = await self._body()
        value = body.get(key)
        return value if value else another

    async def _page(self) -> dict:
        body = await self._body()
        return body['page']

    async def _get_page(self, key, another=None):
        page = await self._page()
        value = page.get(key)
        return value if value else another


class PixivLogin(Pixiv):

    def __init__(self, proxy=None):
        super().__init__(proxy=proxy)
        from . import USER_CONFIG_PATH
        self.user_config_path = USER_CONFIG_PATH
        self.login_url = 'https://accounts.pixiv.net/login'

    async def _chrome_browser_login(self, username: str, password: str, driver_path: str, stopping=3) -> str:

        """
        :param username: 登录账号
        :param password: 登录密码
        :param driver_path: Chrome驱动路径
        :param stopping: 登录后等待获取cookie值时间 根据网络环境调整 建议不低于2s
        :return: cookie
        """

        settings = Browser_options()
        settings.add_argument('--headless')
        settings.add_argument('--disable-gpu')
        settings.add_experimental_option('excludeSwitches', ['enable-automation'])

        chrome_browser = Chrome(executable_path=driver_path, options=settings)

        chrome_browser.get(self.login_url)

        username_input = chrome_browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
        password_input = chrome_browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
        login_button = chrome_browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')

        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button.click()
        await asyncio.sleep(stopping)
        cookies = chrome_browser.get_cookies()

        chrome_browser.quit()

        cookie = ';'.join(['='.join((ck['name'], ck['value'])) for ck in cookies])

        yaml.dump({'cookie': cookie}, open(self.user_config_path, 'w', encoding='utf8'))

        return cookie

    async def _get_userid(self, cookie: str):
        response_headers = await self._async_GET_headers(url=self.BASEURL+'/', headers={'cookie': cookie})
        yaml.dump({'userid': response_headers['X-UserId']}, open(self.user_config_path, 'a', encoding='utf8'))

    async def login(self, username: str, password: str, driver_path: str):
        cookie = await self._chrome_browser_login(username, password, driver_path)
        await self._get_userid(cookie)

    @property
    def userid(self):
        conf = yaml.safe_load(open(self.user_config_path, 'r'))
        return conf['userid']

    @property
    def cookie(self):
        conf = yaml.safe_load(open(self.user_config_path, 'r'))
        return conf['cookie']

    @property
    def headers(self):
        data = {
            'x-user-id': self.userid,
            'cookie': self.cookie,
        }
        return self._headers(data)

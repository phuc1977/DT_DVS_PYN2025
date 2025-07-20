import asyncio
import aiohttp

class RestAPI:
    def __init__(self, base_url, **kwargs):
        self._base_url = base_url
        self._token_header = 'token'
        self._token_return = 'access_token'
        self._token = ''

    async def post(self, api, payload=None, **kwargs):
        async with aiohttp.ClientSession(headers={self._token_header: self._token}) as session:
            resp = await session.post(f"{self._base_url}/{api}", json=payload, **kwargs)
            reply = await resp.json()
            if resp.status != 200: reply['error'] = True
            return reply

    async def get(self, api, params=None, **kwargs):
        async with aiohttp.ClientSession(headers={self._token_header: self._token}) as session:
            resp = await session.get(f"{self._base_url}/{api}", params=params, **kwargs)
            reply = await resp.json()
            if resp.status != 200: reply['error'] = True
            return reply
                
    async def login(self, username, password, **kwargs):
        login_api = kwargs.get('login_api', 'login')
        user_key = kwargs.get('username', 'username')
        pass_key = kwargs.get('password', 'password')
        payload = {user_key: username, pass_key: password}
        reply = await self.post(login_api, payload)
        if 'error' not in reply: self._token = reply[self._token_return]
        return reply 
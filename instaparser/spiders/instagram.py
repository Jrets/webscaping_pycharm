import json
import os
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from dotenv import load_dotenv
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from instaparser.items import InstaparserItem

users_name = list(
    map(
        str,
        input("Введите имена пользователей через запятую, без пробелов : ").split(","),
    )
)


class InstagramSpider(scrapy.Spider):
    # атрибуты класса
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com/"]
    # параметры логина
    load_dotenv("D:\Learning\Project\.env")
    insta_login = os.getenv("insta_login", None)
    insta_pwd = os.getenv("insta_pwd", None)
    insta_queryParams = "{}"
    insta_optIntoOneTap = "false"
    insta_stopDeletionNonce = ""
    insta_trustedDeviceRecords = "{}"

    insta_login_link = "https://www.instagram.com/accounts/login/ajax/"
    parse_user = users_name  # Пользователи, у которых собираем подписчиков/подписки
    insta_graphql_url = "https://www.instagram.com/graphql/query/?"
    posts_hash = "02e14f6a7812a876f7d133c9555b1151"  # hash для получения данных о подписчиков/подписки

    def parse(self, response: HtmlResponse):  # Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)  # csrf token из html
        yield scrapy.FormRequest(  # заполнение формы для авторизации
            self.insta_login_link,
            method="POST",
            callback=self.user_parse,
            formdata={
                "username": self.insta_login,
                "enc_password": self.insta_pwd,
                "queryParams": self.insta_queryParams,
                "optIntoOneTap": self.insta_optIntoOneTap,
                "stopDeletionNonce": self.insta_stopDeletionNonce,
                "trustedDeviceRecords": self.insta_trustedDeviceRecords,
            },
            headers={"X-CSRFToken": csrf_token},
        )

    def user_parse(self, response: HtmlResponse):
        print()
        j_body = json.loads(response.text)
        if j_body["authenticated"]:  # Проверка ответа после авторизации
            for user in self.parse_user:
                yield response.follow(  # Переход на страницу пользователя
                    f"/{user}",
                    callback=self.followers_parse,
                    cb_kwargs={"username": user},
                )

    def followers_parse(self, response, username):
        user_id = self.fetch_user_id(
            response.text, username
        )  # Получение id пользователя
        variables = {
            "count": 12,  # Формирование словаря для передачи даных в запрос
            "search_surface": "follow_list_page",
        }

        url_followers = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}"
        yield response.follow(
            url_followers,
            headers={"User-Agent": "Instagram 64.0.0.14.96"},
            callback=self.body_parse,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                "type": "followers",
                "variables": deepcopy(variables),
            },
        )

        url_following = f"https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}"
        yield response.follow(
            url_following,
            headers={"User-Agent": "Instagram 64.0.0.14.96"},
            callback=self.body_parse,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                "type": "following",
                "variables": deepcopy(variables),
            },
        )
        print()

    def body_parse(self, response, username, user_id, type, variables):
        j_data = json.loads(response.text)
        users = j_data.get("users")
        for user in users:
            loader = ItemLoader(item=InstaparserItem(), response=response)
            loader.add_value("parent_name", username)
            loader.add_value("parent_id", user_id)
            loader.add_value("user_id", user.get("pk"))
            loader.add_value("name", user.get("full_name"))
            loader.add_value("photo", user.get("profile_pic_url"))
            loader.add_value("type", type)
            yield loader.load_item()

        next_page = j_data.get("next_max_id")
        if next_page:
            variables["max_id"] = next_page
            url = f"https://i.instagram.com/api/v1/friendships/{user_id}/{type}/?{urlencode(variables)}"

            yield response.follow(
                url,
                headers={"User-Agent": "Instagram 64.0.0.14.96"},
                callback=self.body_parse,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    "type": type,
                    "variables": deepcopy(variables),
                },
            )

    # Получение токена для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('"csrf_token":"\\w+"', text).group()
        return matched.split(":").pop().replace(r'"', "")

    # Получение id указанного пользователя
    def fetch_user_id(self, text, username):
        matched = re.search('{"id":"\\d+","username":"%s"}' % username, text).group()
        return json.loads(matched).get("id")

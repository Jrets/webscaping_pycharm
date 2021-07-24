import os
from dotenv import load_dotenv
#относительный путь для примера, использовать глобальный
#load_dotenv("./.env")
load_dotenv("D:/Learning/Project/webscaping_pycharm/.env")

key = 'key'
key = os.getenv(key, None)
print(key)
#
# load_dotenv("D:/Learning/Project/web_scaping/.env")
#         key = "key_openweathermap"
#         API_key = os.getenv(key, None)
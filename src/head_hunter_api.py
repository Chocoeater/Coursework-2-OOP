from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError, RequestException


class BaseHeadHunterAPI(ABC):
    @abstractmethod
    def _connect_to_api(self, keyword: str) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    def __init__(self):
        self.api_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def _connect_to_api(self, keyword, pages: int = 1):
        self.__params["text"] = keyword
        self.__params["page"] = 0
        self.__vacancies = []
        try:
            while self.__params["page"] < pages:
                response = requests.get(self.api_url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                vacancies = response.json().get("items", [])
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
        except HTTPError as e:
            print(f"Ошибка API: {e}")
        except RequestException as e:
            print(f"Сетевая ошибка: {e}")

    def get_vacancies(self, keyword, pages: int = 1) -> list:
        self._connect_to_api(keyword, pages)
        return self.__vacancies

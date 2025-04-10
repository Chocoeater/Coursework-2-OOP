from abc import ABC, abstractmethod


class BaseVacancy(ABC):
    __slots__ = ("name", "area", "url", "salary", "description", "requirements")


    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        """
        Обрабатывает JSON-строку и возвращает список объектов-вакансий
        :param vacancies: Список JSON-строк для формирования объектов
        :return: Список объектов
        """

    def __eq__(self, other) -> bool:
        """
        Равенство
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __ne__(self, other) -> bool:
        """
        Неравенство
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __lt__(self, other) -> bool:
        """
        Меньше
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __le__(self, other) -> bool:
        """
        Меньше или равно
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __gt__(self, other) -> bool:
        """
        Больше
        :param other: Объект BaseVacancy
        :return: True/False
        """

    def __ge__(self, other) -> bool:
        """
        Больше или равно
        :param other: Объект BaseVacancy
        :return: True/False
        """


class Vacancy(BaseVacancy):
    def __init__(self, name: str, area: str, url: str, salary: dict, description: str, requirements: str):
        self.name = self.__validate_name(name)
        self.area = self.__validate_area(area)
        self.url = self.__validate_url(url)
        self.salary = self.__validation_salary(salary)
        self.description = self.__validate_description(description)
        self.requirements = self.__validate_requirements(requirements)

    @staticmethod
    def __validate_description(description: str) -> str:
        if not description or not isinstance(description, str):
            return "Не указано"
        return description.strip()

    @staticmethod
    def __validate_requirements(requirements: str) -> str:
        if not requirements or not isinstance(requirements, str):
            return "Не указано"
        return requirements.strip()

    @staticmethod
    def __validate_name(name: str) -> str:
        if not name or not isinstance(name, str):
            raise ValueError("Название вакансии должно быть непустой строкой.")
        return name.strip()

    @staticmethod
    def __validate_area(area: str) -> str:
        if not area or not isinstance(area, str):
            raise ValueError("Название региона должно быть непустой строкой.")
        return area.strip()

    @staticmethod
    def __validate_url(url: str) -> str:
        if not url or not isinstance(url, str):
            return "Не указано"
        return url.strip()

    @staticmethod
    def __validation_salary(salary: dict | None) -> dict:
        if not salary:
            return {"from": 0, "to": 0, "currency": "RUR", "gross": False}
        else:
            return salary

    @classmethod
    def get_vacancy(cls, json_str: dict):
        return cls(name=json_str["name"], area=json_str["area"]["name"], url=json_str["alternate_url"],
            salary=json_str["salary"], description=json_str["snippet"]["responsibility"],
            requirements=json_str["snippet"]["requirement"], )

    @classmethod
    def cast_to_object_list(cls, vacancies: list) -> list:
        return [cls.get_vacancy(vacancy_dict) for vacancy_dict in vacancies]

    @staticmethod
    def _get_left_right(left: int | dict, right: int | dict) -> tuple:
        if left:
            left = left["from"]
        if right:
            right = right["from"]
        return left, right

    def __eq__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left == right

    def __ne__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left != right

    def __lt__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left < right

    def __le__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left <= right

    def __gt__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left > right

    def __ge__(self, other):
        left, right = self._get_left_right(self.salary, other.salary)
        return left >= right

    def to_dict(self) -> dict:
        """
        Возвращает словарь с атрибутами объекта
        :return: Словарь с атрибутами
        """
        data = {"name": self.name, "url": self.url, "salary": self.salary, "description": self.description,
            "requirements": self.requirements, }
        return data

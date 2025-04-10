import json
from abc import ABC, abstractmethod
from src.vacancies import Vacancy
from pathlib import Path
from typing import List, Dict


class BaseJSONSaver(ABC):
    """
    Базовый абстрактный класс для задания интерфейса сохранения в файл вакансий
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл
        :param vacancy: Объект-вакансия
        :return: None
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> bool:
        """
        Удаляет вакансию из файла
        :param vacancy: Объект-вакансия
        :return: True, если удаление прошло успешно, False, если удаления не было
        """
        pass


class JSONSaver(BaseJSONSaver):
    def __init__(self, file_name="vacancies.json"):
        self.__file_name = file_name
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        self.__path_to_file = Path(data_dir, self.__file_name)
        if not self.__path_to_file.exists():
            self.__path_to_file.write_text("[]", encoding="utf-8")

    def _load_vacancies(self) -> List[Dict]:
        """Загружает список вакансий из файла"""
        with open(self.__path_to_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_vacancies(self, vacancies: List[Dict]) -> None:
        """Сохраняет список вакансий в файл"""
        with open(self.__path_to_file, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, indent=4, ensure_ascii=False)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл, если ее еще нет"""
        vacancies = self._load_vacancies()
        vacancy_data = vacancy.to_dict()
        if not any(vac.get("url") == vacancy.url for vac in vacancies):
            vacancies.append(vacancy_data)
            self._save_vacancies(vacancies)

    def delete_vacancy(self, url: str) -> bool:
        vacancies = self._load_vacancies()
        old_len_of_vacancies = len(vacancies)
        update_vacancies = [vac for vac in vacancies if vac.get("url") != url]
        if len(update_vacancies) == old_len_of_vacancies:
            return False
        self._save_vacancies(update_vacancies)
        return True

    def search_vacancies(self, keyword: str = None, salary: int = None) -> List[Dict]:
        """Поиск по вакансиям"""
        vacancies = self._load_vacancies()
        result = vacancies

        if keyword:
            low = keyword.lower()
            result = [
                vac
                for vac in result
                if (
                    low in vac.get("description", "").lower()
                    or low in vac.get("requirements", "").lower()
                    or low in vac.get("name", "").lower()
                )
            ]

        if salary:
            result = [vac for vac in result if vac.get("salary", {}).get("from", 0) >= salary]

        return result

    def get_all_vacancies(self) -> List[Dict]:
        """Публичный метод для получения всех вакансий в файле"""
        return self._load_vacancies()

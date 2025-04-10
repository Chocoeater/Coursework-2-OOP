import json
from src.vacancies import Vacancy


def test_add_vacancy_success(json_saver, vacancy_data):
    # Тест успешного добавления вакансии
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)

    with open(json_saver._JSONSaver__path_to_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["url"] == vacancy.url


def test_add_vacancy_duplicate(json_saver, vacancy_data):
    # Тест добавления дубликата вакансии
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)  # Пытаемся добавить второй раз

    with open(json_saver._JSONSaver__path_to_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1  # Дубликат не добавился


def test_delete_vacancy_success(json_saver, vacancy_data):
    # Тест успешного удаления вакансии
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)
    result = json_saver.delete_vacancy(vacancy.url)

    assert result is True
    with open(json_saver._JSONSaver__path_to_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 0


def test_delete_vacancy_not_found(json_saver):
    # Тест попытки удаления несуществующей вакансии
    result = json_saver.delete_vacancy("non_existent_url")
    assert result is False


def test_search_vacancies_by_keyword(json_saver, vacancy_data):
    # Тест поиска по ключевому слову
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)

    # Поиск по слову, которое есть в описании
    result = json_saver.search_vacancies(keyword="Тестовый")
    assert len(result) == 1

    # Поиск по слову, которого нет
    result = json_saver.search_vacancies(keyword="Java")
    assert len(result) == 0


def test_search_vacancies_by_salary(json_saver, vacancy_data):
    # Тест поиска по зарплате
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)

    # Зарплата ниже указанной
    result = json_saver.search_vacancies(salary=50000)
    assert len(result) == 1

    # Зарплата выше указанной
    result = json_saver.search_vacancies(salary=120000)
    assert len(result) == 0


def test_get_all_vacancies(json_saver, vacancy_data):
    # Тест получения всех вакансий
    vacancy = Vacancy.get_vacancy(vacancy_data)
    json_saver.add_vacancy(vacancy)
    result = json_saver.get_all_vacancies()
    assert len(result) == 1
    assert result[0]["url"] == vacancy.url

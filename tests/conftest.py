import pytest
from src.head_hunter_api import HeadHunterAPI
from unittest.mock import patch, MagicMock
from src.vacancies import Vacancy
from src.json_saver import JSONSaver


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {"items": [{"id": 1, "name": "Python Developer"}]}
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@pytest.fixture
def vacancy_data():
    vacancy_data = {
        "name": "Тестовый",
        "area": {"name": "Тестовый"},
        "alternate_url": "http://example.com/vacancy/1",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR", "gross": False},
        "snippet": {"responsibility": "Описание", "requirement": "Требование"},
    }
    return vacancy_data


@pytest.fixture
def json_saver(tmp_path):
    # Используем временную директорию pytest для изоляции тестов
    file_path = tmp_path / "vacancies.json"
    saver = JSONSaver(file_name=str(file_path))
    # Переопределяем путь к файлу для тестов
    saver._JSONSaver__path_to_file = file_path
    return saver


@pytest.fixture
def vacancy_without_salary():
    return Vacancy(
        name="Python Developer",
        area="Moscow",
        url="http://example.com/vacancy/2",
        salary=None,
        description="Описание",
        requirements="Требование",
    )


@pytest.fixture
def vacancy_normal():
    return Vacancy(
        name="Python Developer",
        area="Moscow",
        url="http://example.com/vacancy/2",
        salary={"from": 100000, "to": 150000, "currency": "RUR", "gross": False},
        description="Описание",
        requirements="Требование",
    )


# Мок для сейвера
@pytest.fixture
def mock_saver():
    saver = MagicMock()
    saver.get_all_vacancies.return_value = [
        {
            "name": "Python Developer",
            "url": "http://example.com/1",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python job",
            "requirements": "Python experience",
        }
    ]
    saver.search_vacancies.return_value = [
        {
            "name": "Found Python Job",
            "url": "http://example.com/2",
            "salary": {"from": 120000, "to": 180000},
            "description": "Python description",
            "requirements": "Python requirements",
        }
    ]
    saver.add_vacancy.return_value = True
    saver.delete_vacancy.return_value = True
    return saver

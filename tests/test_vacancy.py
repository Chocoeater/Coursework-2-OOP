from src.vacancies import Vacancy


def test_vacancy_creation(vacancy_data):
    vac = Vacancy.get_vacancy(vacancy_data)

    assert vac.name == "Тестовый"
    assert vac.area == "Тестовый"
    assert vac.url == "http://example.com/vacancy/1"
    assert vac.salary == {"from": 100000, "to": 150000, "currency": "RUR", "gross": False}
    assert vac.description == "Описание"
    assert vac.requirements == "Требование"


def test_vacancy_without_salary(vacancy_without_salary):
    assert vacancy_without_salary.salary == {"from": 0, "to": 0, "currency": "RUR", "gross": False}


def test_cast_to_object_list(vacancy_data):
    vacancies = Vacancy.cast_to_object_list([vacancy_data])
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Тестовый"


def test_to_dict(vacancy_normal):
    result = vacancy_normal.to_dict()

    assert isinstance(result, dict)
    assert result["name"] == "Python Developer"
    assert result["url"] == "http://example.com/vacancy/2"
    assert result["salary"]["from"] == 100000


def test_comparison_operators():
    v1 = Vacancy(
        name="Developer 1",
        area="Moscow",
        url="http://example.com/vacancy/1",
        salary={"from": 100000, "to": 150000},
        description="Описание",
        requirements="Требование",
    )

    v2 = Vacancy(
        name="Developer 2",
        area="Moscow",
        url="http://example.com/vacancy/2",
        salary={"from": 120000, "to": 180000},
        description="Описание",
        requirements="Требование",
    )

    v3 = Vacancy(
        name="Developer 3",
        area="Moscow",
        url="http://example.com/vacancy/3",
        salary={"from": 100000, "to": 150000},
        description="Описание",
        requirements="Требование",
    )

    # Тестирование операторов сравнения
    assert v1 < v2
    assert v2 > v1
    assert v1 <= v3
    assert v3 >= v1
    assert v1 == v3
    assert v1 != v2


def test_missing_fields_in_json(vacancy_data):
    # Удаляем некоторые поля для теста
    vacancy_data["snippet"]["requirement"] = None
    vacancy_data["salary"] = None

    vacancy = Vacancy.get_vacancy(vacancy_data)

    assert vacancy.requirements == "Не указано"
    assert vacancy.salary == {"from": 0, "to": 0, "currency": "RUR", "gross": False}

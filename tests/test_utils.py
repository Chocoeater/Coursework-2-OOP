import pytest
from unittest.mock import patch, MagicMock
from src.utils import (
    user_interaction,
    show_saved_vacancies,
    search_in_saved_vacancies,
    add_vacancy_manually,
    delete_vacancy_interactive,
    search_vacancies_in_hh,
    salary_print,
)


def test_salary_print():
    # Тестирование зарплаты
    assert salary_print({"from": 100000, "to": 150000}) == "от 100000 до 150000"
    assert salary_print({"from": 0, "to": 0}) == "Не указана"
    assert salary_print({"from": 100000, "to": 0}) == "от 100000 до 0"


@patch("builtins.print")
def test_show_saved_vacancies(mock_print, mock_saver):
    show_saved_vacancies(mock_saver)

    # Проверяем что функция выводит ожидаемые данные
    output = "\n".join([call[0][0] for call in mock_print.call_args_list])
    assert "Python Developer" in output
    assert "от 100000 до 150000" in output
    assert "http://example.com/1" in output


@patch("builtins.input")
@patch("builtins.print")
def test_add_vacancy_manually(mock_print, mock_input, mock_saver):
    mock_input.side_effect = ["Test Job", "http://test.com", "100000", "Test desc", "Test reqs"]
    with patch("src.vacancies.Vacancy.get_vacancy") as mock_get_vacancy:
        mock_vacancy = MagicMock()
        mock_get_vacancy.return_value = mock_vacancy

        add_vacancy_manually(mock_saver)

        # Проверяем что вакансия была добавлена
        mock_saver.add_vacancy.assert_called_once_with(mock_vacancy)
        mock_print.assert_called_with("✅ Вакансия добавлена!")


# Чуть не умер, пока пытался разобраться, как это написать хд
@patch("builtins.input")
@patch("builtins.print")
def test_search_in_saved_vacancies(mock_print, mock_input):
    mock_input.return_value = "Python"

    mock_saver = MagicMock()
    mock_saver.search_vacancies.return_value = [
        {
            "name": "Python Developer",
            "url": "http://example.com/1",
            "salary": {"from": 100000, "to": 150000},
            "description": "Python",
            "requirements": "Python",
        }
    ]

    search_in_saved_vacancies(mock_saver)

    mock_saver.search_vacancies.assert_called_once_with("Python")

    # Особенно здесь, двойной цикл: сначала вызываем список с аргументами
    # затем берем элемент списка и идем по аргументам и все склеиваем
    output = "\n".join(" ".join(str(arg) for arg in call.args) for call in mock_print.call_args_list)

    assert "Python Developer" in output
    assert "от 100000 до 150000" in output
    assert "http://example.com/1" in output
    assert "Python" in output
    assert "Python" in output


@patch("builtins.input")
@patch("builtins.print")
@patch("src.utils.show_saved_vacancies")  # иначе в тесте начнёт печатать
def test_delete_vacancy_interactive(mock_show, mock_print, mock_input):
    mock_input.return_value = "http://example.com/1"

    mock_saver = MagicMock()
    mock_saver.delete_vacancy.return_value = True

    delete_vacancy_interactive(mock_saver)

    mock_saver.delete_vacancy.assert_called_once_with("http://example.com/1")
    output = "\n".join(" ".join(str(arg) for arg in call.args) for call in mock_print.call_args_list)
    assert "✅ Вакансия удалена!" in output


@patch("builtins.input")
@patch("builtins.print")
@patch("src.utils.show_saved_vacancies")
def test_delete_vacancy_interactive_not_found(mock_show, mock_print, mock_input):
    mock_input.return_value = "http://example.com/not-found"

    mock_saver = MagicMock()
    mock_saver.delete_vacancy.return_value = False

    delete_vacancy_interactive(mock_saver)

    mock_saver.delete_vacancy.assert_called_once_with("http://example.com/not-found")
    output = "\n".join(" ".join(str(arg) for arg in call.args) for call in mock_print.call_args_list)
    assert "❌ Вакансия не найдена." in output

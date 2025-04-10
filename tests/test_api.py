from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError, RequestException


def test_connect_to_api_success(hh_api, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        vac = hh_api.get_vacancies("Python")

        mock_get.assert_called_once_with(
            hh_api.api_url,
            headers={"User-Agent": "HH-User-Agent"},
            params={"text": "Python", "page": 1, "per_page": 100},
        )
        assert len(vac) == 1
        assert vac[0]["id"] == 1


def test_connect_to_api_pages(hh_api, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        vac = hh_api.get_vacancies("Python", pages=3)

        assert mock_get.call_count == 3
        assert len(vac) == 3
        assert hh_api._HeadHunterAPI__params["page"] == 3


def test_connect_to_api_http_error(hh_api):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("API Error")

    with patch("requests.get", return_value=mock_response), patch("builtins.print") as mock_print:
        vac = hh_api.get_vacancies("Python")

        mock_print.assert_called_once_with("Ошибка API: API Error")
        assert len(vac) == 0


def test_connect_to_api_request_exception(hh_api):
    with patch("requests.get", side_effect=RequestException("Network Error")), patch("builtins.print") as mock_print:
        vac = hh_api.get_vacancies("Python")

        mock_print.assert_called_once_with("Сетевая ошибка: Network Error")
        assert len(vac) == 0

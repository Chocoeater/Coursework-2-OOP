from src.head_hunter_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancies import Vacancy


def salary_print(salary: dict) -> str:
    """Приводит зарплату к читаемому виду"""
    if salary["from"] == 0 and salary["to"] == 0:
        return "Не указана"
    return f'от {salary["from"]} до {salary["to"]}'


def user_interaction() -> None:
    """Основная функция для взаимодействия с пользователем"""
    saver = JSONSaver()

    print("Добро пожаловать в Vacancy Manager — консольное приложение для поиска, сохранения и управления вакансиями!")
    while True:
        print("\n=== Управление вакансиями ===")
        print("1. Поиск вакансий в API (HeadHunter)")
        print("2. Показать сохранённые вакансии")
        print("3. Добавить вакансию вручную")
        print("4. Удалить вакансию")
        print("5. Поиск по ключевому слову в сохранённых")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ").strip()

        if choice == "1":
            search_vacancies_in_hh(saver)
        elif choice == "2":
            show_saved_vacancies(saver)
        elif choice == "3":
            add_vacancy_manually(saver)
        elif choice == "4":
            delete_vacancy_interactive(saver)
        elif choice == "5":
            search_in_saved_vacancies(saver)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def show_saved_vacancies(saver: JSONSaver) -> None:
    """Выводит вакансии из файла"""
    vacancies = saver.get_all_vacancies()

    if not vacancies:
        print("Список вакансий пуст.\n")
        return

    print("\n=== Все вакансии ===")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy.get('name', 'Без названия')}")
        print(f"Зарплата: {salary_print(vacancy.get('salary'))}")
        print(f"URL: {vacancy.get('url', 'Нет ссылки')}")
        print(f"Описание: {vacancy.get('description', 'Нет описания')}")
        print(f"Требования: {vacancy.get('requirements', 'Требования не указаны')}")
        print("-" * 40)


def search_in_saved_vacancies(saver: JSONSaver) -> None:
    """Поиск вакансий через метод класса."""
    keyword = input("Введите ключевое слово для поиска: ").strip()
    results = saver.search_vacancies(keyword)

    if not results:
        print("Вакансии не найдены.")
        return

    print("\n=== Результаты поиска ===")
    for i, vacancy in enumerate(results, 1):
        print(f"{i}. {vacancy.get('name', 'Без названия')}")
        print(f"Зарплата: {salary_print(vacancy.get('salary'))}")
        print(f"URL: {vacancy.get('url', 'Нет ссылки')}")
        print(f"Описание: {vacancy.get('description', 'Нет описания')}")
        print(f"Требования: {vacancy.get('requirements', 'Требования не указаны')}")
        print("-" * 40)


def add_vacancy_manually(saver: JSONSaver) -> None:
    """Добавляет вакансию через метод класса."""
    print("\nВведите данные вакансии:")
    vacancy_data = {
        "name": input("Название: "),
        "url": input("URL: "),
        "salary": input("Зарплата: "),
        "description": input("Описание: "),
        "requirements": input("Требования: "),
    }
    vacancy = Vacancy.get_vacancy(vacancy_data)
    if saver.add_vacancy(vacancy):  # Используем метод класса
        print("✅ Вакансия добавлена!")
    else:
        print("❌ Вакансия уже существует или ошибка данных.")


def delete_vacancy_interactive(saver: JSONSaver) -> None:
    """Удаляет вакансию через метод класса."""
    show_saved_vacancies(saver)
    url = input("\nВведите URL вакансии для удаления: ").strip()

    if saver.delete_vacancy(url):  # Используем метод класса
        print("✅ Вакансия удалена!")
    else:
        print("❌ Вакансия не найдена.")


def search_vacancies_in_hh(saver: JSONSaver) -> None:
    """Поиск вакансий с постраничным выводом"""
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")
    pages = input("Сколько страниц загрузить? [1]: ") or "1"

    try:
        pages = int(pages)
        vacancies_list = hh_api.get_vacancies(search_query, pages)
        if vacancies_list:
            all_vacancies = Vacancy.cast_to_object_list(vacancies_list)
        else:
            all_vacancies = None

        if not all_vacancies:
            print("❌ Вакансии не найдены.")
            return

        start_idx = 0
        while True:
            # Выводим текущую страницу (10 вакансий)
            print("\n=== Найденные вакансии ===")
            for i, vacancy in enumerate(all_vacancies[start_idx : start_idx + 10], start_idx + 1):
                print(vacancy.to_dict())
                print(
                    f"""
                    {i}
                    {vacancy.name}
                    Ссылка на вакансию: {vacancy.url}
                    Заработная плата: {salary_print(vacancy.salary)}
                    Описание: {vacancy.description}
                    Требования: {vacancy.requirements}
                    """
                )
                print("-" * 40)

            # Проверяем, есть ли еще вакансии
            if start_idx + 10 >= len(all_vacancies):
                print("\nЭто все найденные вакансии.")
                break

            # Предлагаем продолжить просмотр
            action = input("\n1 - Следующие 10\n2 - Сохранить все\n3 - Выйти в меню\nВыберите: ").strip()

            if action == "1":
                start_idx += 10
            elif action == "2":
                saved_count = 0
                for vacancy in all_vacancies:
                    saver.add_vacancy(vacancy)
                    saved_count += 1
                print(f"✅ Сохранено {saved_count} вакансий.")
                break
            elif action == "3":
                break
            else:
                print("❌ Некорректный ввод")
    except ValueError:
        print("❌ Ошибка: количество страниц должно быть числом")
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")

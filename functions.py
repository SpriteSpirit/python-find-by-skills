import os
import json


def load_students() -> list[dict]:
    """Загружает список студентов из файла"""
    file_path = os.path.join('data', 'students.json')

    with open(file_path) as file:
        data = json.load(file)

    return data


def load_professions() -> list[dict]:
    """Загружает список профессий из файла"""
    file_path = os.path.join('data', 'professions.json')

    with open(file_path) as file:
        data = json.load(file)

    return data


def get_student_by_pk(pk: int) -> dict:
    """Получает словарь с данными студента по его pk"""

    students = load_students()

    for student in students:
        if pk == student['pk']:
            return student


def get_profession_by_title(title: str) -> dict:
    """Получает словарь с инфо о профессии по названию"""

    professions = load_professions()

    for profession in professions:
        if title.lower() == profession['title'].lower():
            return profession


def get_student_name(pk: int) -> str:
    """Получает имя студента по его pk"""

    students = load_students()

    for student in students:
        if pk == student['pk']:
            return student['full_name']


def check_fitness(student: dict, profession: dict) -> dict:
    """Получает студента и профессию и возвращает словарь скиллов и % пригодности"""

    student_skills = set(student['skills'])
    profession_skills = set(profession['skills'])

    lacks = list(profession_skills - student_skills) if (profession_skills - student_skills) else []
    has = list(student_skills & profession_skills) if (student_skills & profession_skills) else []
    ratio = (len(has) * 100) // len(profession_skills)

    criteria = ["has", "lacks", "fit_percent"]
    values = [has, lacks, ratio]

    fit = dict(zip(criteria, values))

    return fit


def get_text_info(text: str = "", members: int = 2) -> None or str:
    """Выводит указанный текст в соответствии с ролями"""

    progr = "Программа:"
    user = "Пользователь:"

    if members == 1:
        print(f"{progr} {text} ")
    elif members == 2:
        print(f"{progr} {text} ")
        user = input(f"{user} ")

        return user


def get_all_students(students: list) -> list:
    """Обрабатывает словарь студентов и отбирает только ключи порядковых номеров(pk)"""

    all_pk = []

    for student in students:
        all_pk.append(student['pk'])

    return all_pk


def get_all_prof(professions: list) -> list:
    """Обрабатывает словарь профессий и отбирает только ключи названий(title)"""

    all_prof = []

    for profession in professions:
        all_prof.append(profession['title'].lower())

    return all_prof


def run_app():
    """Запускает программу цикла и выполняет проверку и вывод информации по студенту/профессии."""

    while True:
        student = get_text_info("Введите номер студента")
        all_students = get_all_students(load_students())

        if student.isdigit() and int(student) in all_students:
            student = int(student)
            get_text_info(f"Студент {get_student_name(student)}", 1)
            get_text_info(f"Знает {', '.join(get_student_by_pk(student)['skills'])}", 1)

            profession = get_text_info(f"Выберите специальность для оценки студента {get_student_name(student)}").lower()
            all_professions = get_all_prof(load_professions())

            if profession in all_professions:
                student_info = get_student_by_pk(student)
                prof_info = get_profession_by_title(profession)

                fit = check_fitness(student_info, prof_info)
                has = ', '.join(check_fitness(student_info, prof_info)['has']) if not fit['has'] == [] else "-"
                lacks = ', '.join(check_fitness(student_info, prof_info)['lacks']) if not fit['lacks'] == [] else "-"

                get_text_info(f"Пригодность {fit['fit_percent']}%\n"
                              f"{get_student_name(student)} знает {has}\n"
                              f"{get_student_name(student)} не знает {lacks}", 1)
            else:
                print("У нас нет такой специальности")
        else:
            print("У нас нет такого студента")

        do_you_want_continue = input("Желаете посмотреть еще информацию? Да/Нет ")

        if do_you_want_continue.lower() == "нет" or do_you_want_continue.lower() == "ytn":
            break

    print("Благодарим за использование программы!")
    quit()

"""
Реализовать телефонный справочник со следующими возможностями:
1. Вывод постранично записей из справочника на экран
2. Добавление новой записи в справочник
3. Возможность редактирования записей в справочнике
4. Поиск записей по одной или нескольким характеристикам
Требования к программе:
1. Реализация интерфейса через консоль (без веб- или графического интерфейса)
2. Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист
3. В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон
личный (сотовый)
Плюсом будет:
1. аннотирование функций и переменных
2. документирование функций
3. подробно описанный функционал программы
4. размещение готовой программы и примера файла с данными на github.

"""
import msvcrt
import os
import json
import uuid


def compare(a: int, b: int) -> int:
    return min(a, b)


def data_read_from_json(file_name=None) -> dict:
    """
    Функция чтения из файла
    :param file_name:
    :return:
    """
    with open(file_name, encoding="utf8") as f:
        d = f.read()
        data_json = json.loads(d)
    return data_json


def search_data_in_nested_dict_by_value(this_data, param=None, sort_mode=None) -> dict:
    """
    Функция формирования new_dict с указанным ключом
    :param this_data:
    :param param:
    :param sort_mode:
    :return:
    """
    result = {}
    index = find_by_key(dict(this_data), param, sort_mode=sort_mode)
    for i in index:
        tmp = this_data.get(i)
        result.update({i: tmp})
    return result


def data_write_to_json(file_name=None, new_dict=None) -> None:
    """
    Функция записи в файл
    :param file_name:
    :param new_dict:
    :return:
    """
    with open(file_name, 'w', encoding="UTF-8") as fp:
        json.dump(new_dict, fp, ensure_ascii=False, indent=4)


def find_by_key(this_data: dict, target, sort_mode=None, parent=None):
    """
    Псевдо-рекурсивная функция на генераторах для поиска значений в nested dict
    возвращает объект генератора содержащий parent-key of nested dict
    :param this_data:
    :param target:
    :param sort_mode:
    :param parent:
    :return:
    """
    for key, value in this_data.items():
        if isinstance(value, dict):
            parent = key
            yield from find_by_key(value, target, sort_mode, parent)
        elif key == sort_mode and value == target:
            yield parent


class DataAdd:
    """
    Класс добавления записи
    """

    def __init__(self, data_class, data_edit_class):
        self.d = None
        self.data = None
        self.data_class = data_class
        self.data_edit_class = data_edit_class
        self.init_data()
        self.id_get_from_user = None
        self.new_personal_phone = None
        self.new_work_phone = None
        self.new_name_of_organization = None
        self.new_otchestvo = None
        self.new_name = None
        self.new_surname = None

    def init_data(self):
        self.d = None
        self.data = None
        self.data = data_read_from_json("final_results.json")
        self.d = [i for i in self.data.values()]

    def create_data(self):
        os.system("cls")
        try:
            print(f"Создание записи:\n"
                  f"Выход Ctrl + C\n")

            self.new_surname = str(input("Введите новую фамилию: "))
            self.new_name = str(input("Введите новое имя: "))
            self.new_otchestvo = str(input("Введите новое отчество: "))
            self.new_name_of_organization = str(input("Введите новую организацию: "))
            self.new_work_phone = str(input("Введите новый рабочий телефон:"))
            self.new_personal_phone = str(input("Введите новый личный телефон: "))
            print("Сохранить запись y/n?")
            while True:
                key = msvcrt.getch()
                if ord(key) == 27:  # ESC
                    break

                if ord(key) == 121:
                    self.save_to_json()
                    break

                if ord(key) == 110:
                    break

            return 0
        except KeyboardInterrupt:
            return 0

    def save_to_json(self):
        result = {
            str(len(self.data) + 1):
                {
                    "uuid": str(uuid.uuid4()),
                    'surname': self.new_surname,
                    'name': self.new_name,
                    'otchestvo': self.new_otchestvo,
                    'name_of_organization': self.new_name_of_organization,
                    'work_phone': self.new_work_phone,
                    'personal_phone': self.new_personal_phone
                }
        }
        self.data.update(result)
        data_write_to_json("final_results.json", self.data)
        self.init_data()
        self.data_class.init_data()
        self.data_edit_class.init_data()


class DataEdit:
    """
    Класс редактирование записи
    """

    def __init__(self, data_class):
        self.d = None
        self.data = None
        self.data_class = data_class
        self.init_data()
        self.id_get_from_user = None
        self.new_personal_phone = None
        self.new_work_phone = None
        self.new_name_of_organization = None
        self.new_otchestvo = None
        self.new_name = None
        self.new_surname = None

    def init_data(self):
        self.d = None
        self.data = None
        self.data = data_read_from_json("final_results.json")
        self.d = [i for i in self.data.values()]

    def before_edit(self):
        os.system("cls")
        try:
            print(f"Выход Ctrl + C\n")
            self.id_get_from_user = int(input("Введите N-записи: "))
        except KeyboardInterrupt:
            return 0

        if self.id_get_from_user > 0 and self.id_get_from_user - 1 <= len(self.d):
            self.edit_data()
        else:
            print("N-записи невалидный :(")

    def edit_data(self):
        os.system("cls")
        try:
            print(f"Редактирование записи: {self.id_get_from_user}\n"
                  f"Фамилия: {self.data[str(self.id_get_from_user)]['surname']}\n"
                  f"Имя: {self.data[str(self.id_get_from_user)]['name']}\n"
                  f"Отчество: {self.data[str(self.id_get_from_user)]['otchestvo']}\n"
                  f"Организация: {self.data[str(self.id_get_from_user)]['name_of_organization']}\n"
                  f"Рабочий телефон: {self.data[str(self.id_get_from_user)]['work_phone']}\n"
                  f"Личный телефон: {self.data[str(self.id_get_from_user)]['personal_phone']}\n"
                  f"Выход Ctrl + C\n")

            self.new_surname = str(input("Введите новую фамилию: "))
            self.new_name = str(input("Введите новое имя: "))
            self.new_otchestvo = str(input("Введите новое отчество: "))
            self.new_name_of_organization = str(input("Введите новую организацию: "))
            self.new_work_phone = str(input("Введите новый рабочий телефон:"))
            self.new_personal_phone = str(input("Введите новый личный телефон: "))
            print("Сохранить изменения y/n?")
            while True:
                key = msvcrt.getch()
                if ord(key) == 27:  # ESC
                    break

                if ord(key) == 121:
                    self.save_edited_json()
                    break

                if ord(key) == 110:
                    break

            return 0
        except KeyboardInterrupt:
            return 0

    def save_edited_json(self):
        self.data[str(self.id_get_from_user)]['surname'] = self.new_surname
        self.data[str(self.id_get_from_user)]['name'] = self.new_name
        self.data[str(self.id_get_from_user)]['otchestvo'] = self.new_otchestvo
        self.data[str(self.id_get_from_user)]['name_of_organization'] = self.new_name_of_organization
        self.data[str(self.id_get_from_user)]['work_phone'] = self.new_work_phone
        self.data[str(self.id_get_from_user)]['personal_phone'] = self.new_personal_phone
        data_write_to_json("final_results.json", self.data)
        self.init_data()
        self.data_class.init_data()


class Data:
    """
    Класс отображения записей
    """
    def __init__(self):
        self.data_tmp = None
        self.new_data = None
        self.iter = 0
        self.data = None
        self.init_data()
        self.d = None
        self.search_mode = None

    def init_data(self):
        self.data = data_read_from_json("final_results.json")
        self.data_tmp = data_read_from_json("final_results.json")
        self.data = [i for i in self.data.values()]
        self.d = None
        self.new_data = None

    def print_to_console(self):
        if self.data:
            os.system('cls')
            if not self.search_mode:
                self.init_data()
                print(f"№\t{'Фамилия'.ljust(15)}\t{'Имя'.ljust(15)}\t{'Отчество'.ljust(20)}"
                      f"\t{'Организация'.ljust(30)}\t{'Рабочий номер'.ljust(30)}\t{'Личный номер'.ljust(30)}")
                for i in range(self.iter, compare(self.iter + 40, len(self.data))):
                    if i < len(self.data):
                        msg = f"{str(i + 1) + '.'.ljust(1)}" \
                              f"\t{self.data[i]['surname'].ljust(15)}" \
                              f"\t{self.data[i]['name'].ljust(15)}" \
                              f"\t{self.data[i]['otchestvo'].ljust(20)}" \
                              f"\t{self.data[i]['name_of_organization'].ljust(30)}" \
                              f"\t{self.data[i]['work_phone'].ljust(30)}" \
                              f"\t{self.data[i]['personal_phone'].ljust(30)}"
                        print(msg)
                print("←,↑ - (Шаг -10)\t→,↓(Шаг +10)\tCtrl+F - Поиск по..")
            else:
                if self.new_data:
                    print(f"№\t{'Фамилия'.ljust(15)}\t{'Имя'.ljust(15)}\t{'Отчество'.ljust(20)}"
                          f"\t{'Организация'.ljust(30)}\t{'Рабочий номер'.ljust(30)}\t{'Личный номер'.ljust(30)}")
                    for i in range(self.iter, compare(self.iter + 40, len(self.new_data))):
                        if i < len(self.data):
                            msg = f"{str(i + 1) + '.'.ljust(1)}" \
                                  f"\t{self.new_data[i]['surname'].ljust(15)}" \
                                  f"\t{self.new_data[i]['name'].ljust(15)}" \
                                  f"\t{self.new_data[i]['otchestvo'].ljust(20)}" \
                                  f"\t{self.new_data[i]['name_of_organization'].ljust(30)}" \
                                  f"\t{self.new_data[i]['work_phone'].ljust(30)}" \
                                  f"\t{self.new_data[i]['personal_phone'].ljust(30)}"
                            print(msg)
                else:
                    print("Совпадений не найдено!\n"
                          "ESC - назад\n"
                          "Ctrl-F - поиск")
                    return 0

    def prepare_data(self):
        os.system('cls')
        print(f"№\t{'Фамилия'.ljust(15)}\t{'Имя'.ljust(15)}\t{'Отчество'.ljust(20)}"
              f"\t{'Организация'.ljust(30)}\t{'Рабочий номер'.ljust(30)}\t{'Личный номер'.ljust(30)}")
        for i in range(min(40, len(self.data))):
            msg = f"{str(i + 1) + '.'.ljust(1)}" \
                  f"\t{self.data[i]['surname'].ljust(15)}" \
                  f"\t{self.data[i]['name'].ljust(15)}" \
                  f"\t{self.data[i]['otchestvo'].ljust(20)}" \
                  f"\t{self.data[i]['name_of_organization'].ljust(30)}" \
                  f"\t{self.data[i]['work_phone'].ljust(30)}" \
                  f"\t{self.data[i]['personal_phone'].ljust(30)}"
            print(msg)
        print("←,↑ - (Шаг -10)\t→,↓(Шаг +10)\tCtrl+F - Поиск по..")

        while True:
            """
            Цикл обработки нажатий
            """
            key = msvcrt.getch()
            if ord(key) == 27:  # ESC
                self.iter = 0
                self.search_mode = None
                break

            if ord(key) in [75, 72]:  # Arrow Up 72   left 75
                if self.iter > 0:
                    self.iter -= 10
                    self.print_to_console()

            if ord(key) == 6:
                self.search_mode = None
                self.search_by_value()

            elif ord(key) in [77, 80]:  # Arrow Down 80  right 77
                if self.iter < len(self.data) - 1:
                    self.iter += 10
                    self.print_to_console()

    def search_by_value(self):
        try:
            self.search_mode = int(input("Поиск по:\n"
                                         "[1]Фамилии "
                                         "[2]Имени "
                                         "[3]Отчеству "
                                         "[4]Организации "
                                         "[5]Рабочему телефону "
                                         "[6]Личному телефону\n"
                                         "Введите N>"))

            self.new_data = None
            match self.search_mode:
                case 1:
                    surname = str(input("Введите фамилию: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, surname, "surname")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()
                case 2:
                    name = str(input("Введите имя: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, name, "name")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()
                case 3:
                    otchestvo = str(input("Введите отчество: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, otchestvo, "otchestvo")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()
                case 4:
                    name_of_organization = str(input("Введите организацию: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, name_of_organization,
                                                                        "name_of_organization")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()
                case 5:
                    work_phone = str(input("Введите рабочий телефон: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, work_phone, "work_phone")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()
                case 6:
                    personal_phone = str(input("Введите личный телефон: "))
                    self.new_data = search_data_in_nested_dict_by_value(self.data_tmp, personal_phone, "personal_phone")
                    self.new_data = [i for i in self.new_data.values()]
                    self.print_to_console()

        except KeyboardInterrupt:
            self.print_to_console()
        except ValueError:
            self.search_by_value()


class Menu:
    """
    Класс отображения меню
    """
    def __init__(self, items):
        self.items = items
        self.position = 0

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        while True:
            os.system('cls')
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = True
                else:
                    mode = False

                msg = "%d. %s" % (index + 1, item[0])
                if mode:
                    msg += " #"
                print(msg)
            key = msvcrt.getch()
            if ord(key) == 27:  # ESC
                break
            if ord(key) == 13:  # Enter
                if self.position == len(self.items) - 1:
                    break
                else:
                    self.items[self.position][1]()
                    os.system('cls')
            if ord(key) == 72:  # Arrow Up
                self.navigate(-1)
            elif ord(key) == 80:  # Arrow Down
                self.navigate(1)


if __name__ == "__main__":
    data = Data()
    data_edit = DataEdit(data)
    data_add = DataAdd(data, data_edit)
    menu = Menu([("Справочник", data.prepare_data),
                 ("Добавить запись", data_add.create_data),
                 ("Редактировать запись {укз. N-записи}", data_edit.before_edit),
                 ("Выход", "exit")])
    menu.display()

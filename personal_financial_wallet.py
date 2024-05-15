import os
from typing import List, Dict, Callable


class FinancialWallet:
    DATA_FILE: str = 'finance_data.txt'

    def __init__(self) -> None:
        self.entries: List[Dict[str, str]] = self.load_entries()

    @staticmethod
    def load_entries() -> List[Dict[str, str]]:
        """ Загрузка записей из файла. """
        if not os.path.exists(FinancialWallet.DATA_FILE):
            return []
        with open(FinancialWallet.DATA_FILE, 'r', encoding='utf-8') as file:
            data = file.read().split('\n\n')
            return [dict((kv.split(':') for kv in entry.split('\n'))) for entry in data if entry.strip()]

    def save_entries(self) -> None:
        """ Сохранение записей в файл. """
        with open(FinancialWallet.DATA_FILE, 'w', encoding='utf-8') as file:
            for entry in self.entries:
                for key, value in entry.items():
                    file.write(f"{key}:{value}\n")
                file.write("\n")

    def display_entries(self) -> None:
        """ Отображение всех записей и расчет баланса. """
        total_income: int = 0
        total_expense: int = 0
        for entry in self.entries:
            print(f"Дата: {entry['Дата']}, Категория: {entry['Категория']}, Сумма: {entry['Сумма']}, Описание: {entry.get('Описание', '')}")
            if entry['Категория'] == 'Доход':
                total_income += int(entry['Сумма'])
            else:
                total_expense += int(entry['Сумма'])
        print(f"\nОбщий баланс: {total_income - total_expense}")
        print(f"Всего доходов: {total_income}, Всего расходов: {total_expense}")

    def add_entry(self) -> None:
        """ Добавление новой записи. """
        entry: Dict[str, str] = {
            'Дата': input("Введите дату (YYYY-MM-DD): "),
            'Категория': input("Введите категорию (Доход/Расход): "),
            'Сумма': input("Введите сумму: "),
            'Описание': input("Введите описание: ")
        }
        self.entries.append(entry)
        self.save_entries()
        print("Запись добавлена успешно.")

    def edit_entry(self) -> None:
        """ Редактирование существующей записи. """
        date: str = input("Введите дату записи для редактирования (YYYY-MM-DD): ")
        for entry in self.entries:
            if entry['Дата'] == date:
                print(f"Редактирование записи: {entry}")
                entry['Категория'] = input(f"Введите новую категорию (Доход/Расход) [{entry['Категория']}]: ") or entry['Категория']
                entry['Сумма'] = input(f"Введите новую сумму [{entry['Сумма']}]: ") or entry['Сумма']
                entry['Описание'] = input(f"Введите новое описание [{entry['Описание']}]: ") or entry['Описание']
                self.save_entries()
                print("Запись обновлена успешно.")
                return
        print("Запись не найдена.")

    def search_entries(self) -> None:
        """ Поиск записей по критериям. """
        print("Выберите критерий поиска:")
        print("1 - По категории")
        print("2 - По дате")
        print("3 - По сумме")
        criteria: str = input("Введите номер критерия поиска: ")

        if criteria == '1':
            category: str = input("Введите категорию (Доход/Расход): ")
            self.search_by_category(category)
        elif criteria == '2':
            date: str = input("Введите дату (YYYY-MM-DD): ")
            self.search_by_date(date)
        elif criteria == '3':
            sum_value: str = input("Введите сумму: ")
            self.search_by_amount(sum_value)
        else:
            print("Неверный ввод критерия.")

    def search_by_category(self, category: str) -> None:
        """ Поиск записей по категории. """
        found_entries = [entry for entry in self.entries if entry['Категория'] == category]
        if not found_entries:
            print("Записи не найдены.")
        else:
            for entry in found_entries:
                print(entry)

    def search_by_date(self, date: str) -> None:
        """ Поиск записей по дате. """
        found_entries = [entry for entry in self.entries if entry['Дата'] == date]
        if not found_entries:
            print("Записи не найдены.")
        else:
            for entry in found_entries:
                print(entry)

    def search_by_amount(self, amount: str) -> None:
        """ Поиск записей по сумме. """
        found_entries = [entry for entry in self.entries if entry['Сумма'] == amount]
        if not found_entries:
            print("Записи не найдены.")
        else:
            for entry in found_entries:
                print(entry)


def main():
    """ Главный цикл программы. """
    wallet = FinancialWallet()
    actions: Dict[str, Callable[[], None]] = {
        '1': wallet.display_entries,
        '2': wallet.add_entry,
        '3': wallet.edit_entry,
        '4': wallet.search_entries
    }

    while True:
        print("\n1 - Показать все записи")
        print("2 - Добавить запись")
        print("3 - Редактировать запись")
        print("4 - Поиск по записям")
        print("q - Выход")

        choice: str = input("Выберите действие: ").strip()
        if choice == 'q':
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()

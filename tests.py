import unittest
from personal_financial_wallet import FinancialWallet
from unittest.mock import patch, mock_open
import io


class TestFinancialWallet(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом."""
        self.wallet = FinancialWallet()
        self.wallet.entries = [
            {'Дата': '2024-01-01', 'Категория': 'Доход', 'Сумма': '1000', 'Описание': 'Зарплата'},
            {'Дата': '2024-01-02', 'Категория': 'Расход', 'Сумма': '500', 'Описание': 'Продукты'}
        ]

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='Дата:2024-05-15\nКатегория:Доход\nСумма:1000\n\n')
    def test_load_entries(self, mock_file, mock_exists):
        """Тестирование загрузки записей из файла."""
        mock_exists.return_value = True
        wallet = FinancialWallet()
        self.assertEqual(len(wallet.entries), 1)
        self.assertEqual(wallet.entries[0]['Категория'], 'Доход')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_entries(self, mock_stdout):
        """Тестирование отображения баланса"""
        self.wallet.display_entries()
        self.assertIn('Общий баланс: 500', mock_stdout.getvalue())
        self.assertIn('Всего доходов: 1000', mock_stdout.getvalue())
        self.assertIn('Всего расходов: 500', mock_stdout.getvalue())
        self.assertEqual(len(self.wallet.entries), 2)

    @patch('builtins.input', side_effect=['2024-02-01', 'Доход', '1500', 'Бонус'])
    @patch('builtins.open', new_callable=mock_open)
    def test_add_entry(self, mock_input, mock_file):
        """Тестирование добавления новой записи"""
        self.wallet.add_entry()
        expected_entry = {'Дата': '2024-02-01', 'Категория': 'Доход', 'Сумма': '1500', 'Описание': 'Бонус'}
        self.assertIn(expected_entry, self.wallet.entries)

    @patch('builtins.input', side_effect=['2024-01-01', 'Расход', '900', 'Кофе'])
    def test_edit_entry(self, mock_input):
        """Тестирование редактирования записи"""
        self.wallet.edit_entry()
        self.assertEqual(self.wallet.entries[0]['Категория'], 'Расход')

    @patch('builtins.input', side_effect=['3', '1000'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_entries(self, mock_stdout, mock_input):
        """Тестирование поиска"""
        self.wallet.search_entries()
        self.assertIn('Зарплата', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_by_category(self, mock_stdout):
        """Тестирование поиска по категории"""
        self.wallet.search_by_category('Доход')
        self.assertIn('Доход', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_by_date(self, mock_stdout):
        """Тестирование поиска по дате"""
        self.wallet.search_by_date('2024-01-01')
        self.assertIn('2024-01-01', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_search_by_amount(self, mock_stdout):
        """Тестирование поиска по дате"""
        self.wallet.search_by_amount('1000')
        self.assertIn('1000', mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()

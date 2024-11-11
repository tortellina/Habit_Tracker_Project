from unittest.mock import  patch
from models import Habit, Datamanager
import time

current_date = time.strftime('%Y-%m-%d')

def test_add_habit_can_add_habit_to_db_but_not_duplicates():
     with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        mock_habit = ('esercizio',2)
        Habit.add_habit(mock_habit)

        mock_cur.execute.side_effect = Exception('Duplicate entry')
        Habit.add_habit(mock_habit)
        mock_connection.commit.assert_not_called()

def test_delete_an_habit():
    mock_habit = Habit('esercizio' , 2)
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
         mock_cur.fetchall.return_value = [('esercizio', 2)]
         mock_habit.delete_habit()

         mock_cur.execute.assert_any_call('''INSERT INTO history_habits (habit, starting_date, periodicity, streak ) SELECT habit, starting_date, periodicity, streak FROM active_habits WHERE habit = ?''', ('esercizio',))
         mock_cur.execute.assert_any_call('''DELETE FROM active_habits WHERE habit = ? ''', ('esercizio',))
         mock_connection.commit.assert_called()

def test_modify_habit():
    mock_habit = Habit('esercizio' , 4)
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
         mock_cur.fetchall.return_value = [('esercizio', 1)]
         mock_habit.modify_habit()
         mock_cur.execute.assert_any_call('''UPDATE active_habits SET periodicity = ? WHERE habit = ?''' , (4, 'esercizio'))
         mock_connection.commit.assert_called()

def test_check_complete(monkeypatch):
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        mock_cur.fetchall.side_effect = [[('esercizio', 1 , 12)], [(12,)]]
        
        monkeypatch.setattr('builtins.input', lambda _: 'YES')
        Datamanager.check_complete()
        
        mock_cur.execute.assert_any_call('''UPDATE active_habits SET streak = ? WHERE habit = ? ''', (13, 'esercizio'))
        mock_connection.commit.assert_called()

def test_delete_all_active():
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        Datamanager.delete_all_active()
        mock_cur.execute.assert_any_call('''INSERT INTO history_habits (habit, starting_date, periodicity, streak ) SELECT habit, starting_date, periodicity, streak FROM active_habits''')
        mock_cur.execute.assert_any_call('''DELETE FROM active_habits ''')
        mock_connection.commit.assert_called()

def test_delete_all_history():
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        Datamanager.delete_all_history()
        mock_cur.execute.assert_any_call('''DELETE FROM history_habits ''')
        mock_connection.commit.assert_called()

def test_all_active():
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        Datamanager.all_active()
        mock_cur.execute.assert_any_call('''SELECT * FROM active_habits''')
        mock_connection.commit.assert_called()

def test_show_history():
    with patch('models.cur') as mock_cur, patch('models.connection') as mock_connection:
        Datamanager.show_history()
        mock_cur.execute.assert_any_call('''SELECT * FROM history_habits''')
        mock_connection.commit.assert_called()

def test_longest_active():
    with patch('models.cur') as mock_cur , patch('builtins.print') as mock_print:
        mock_cur.fetchall.return_value = [('esercizio', 1), ('giocare', 3), ('pranzare', 8)]
        Datamanager.longest_active()
        mock_print.assert_called_once_with("the longest active habit is ['pranzare'] with streak of 8 days!")

def test_compare_history():
    with patch('models.cur') as mock_cur , patch('builtins.print') as mock_print:
        mock_cur.fetchall.return_value = [('esercizio', 1), ('giocare', 3), ('pranzare', 8)]
        Datamanager.compare_history()
        mock_print.assert_called_once_with("the longest habit stored in history is ['pranzare'] with streak of 8 days!")

def test_check_date():
    with patch('models.cur') as mock_cur ,patch('models.connection') as mock_connection, patch('builtins.print') as mock_print:
        mock_cur.fetchall.return_value = [('2024-10-22', )]
        Datamanager.last_check_date()
        mock_cur.execute.assert_any_call('''UPDATE check_in_date SET date = ? WHERE date = ?''', (current_date, '2024-10-22'))
        mock_connection.commit.assert_called()

def test_check_date_first_use_of_app():
    with patch('models.cur') as mock_cur ,patch('models.connection') as mock_connection, patch('builtins.print') as mock_print:
        mock_cur.fetchall.return_value = []
        Datamanager.last_check_date()
        mock_cur.execute.assert_any_call(''' INSERT INTO check_in_date VALUES (?)''', (current_date,))
        mock_connection.commit.assert_called()

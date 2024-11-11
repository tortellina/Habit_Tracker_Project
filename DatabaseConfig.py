import sqlite3

def get_connection():
    connection = sqlite3.connect('habit_tracker.db')
    cursor = connection.cursor()

    active_table = ''' CREATE TABLE IF NOT EXISTS active_habits(habit TEXT PRIMARY KEY, starting_date TEXT, periodicity INTEGER, streak INTEGER)'''  
    history_table = ''' CREATE TABLE IF NOT EXISTS history_habits(habit TEXT, starting_date TEXT, periodicity INTEGER, streak INTEGER)'''   

    check_in_date = ''' CREATE TABLE IF NOT EXISTS check_in_date(date TEXT PRIMARY KEY)'''

    cursor.execute(active_table)
    cursor.execute(history_table)
    cursor.execute(check_in_date)
    
    connection.commit()

    return connection





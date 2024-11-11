from DatabaseConfig import get_connection
import time

current_date = time.strftime('%Y-%m-%d')

#open connection with db
connection = get_connection()
cur = connection.cursor()



#all self related def
class Habit:
    def __init__(self, habit, periodicity):
        try:
            self.habit = habit.lower()
            self.periodicity = periodicity
        except:
            print('insert accepted values')

    def add_habit(self):    #add a new active habit to db active_habits
        streak = 0
        try:
            cur.execute('''INSERT INTO active_habits (habit, starting_date, periodicity, streak ) VALUES (?,?,?,?)''', (self.habit, current_date, self.periodicity, streak))
            connection.commit()
            print(f'Habit {self.habit} inserted')

        except:
            print('habit already present in the database')

    def delete_habit(self): #delete an active habit and save it in history_habits
        try:
            cur.execute('''SELECT * FROM active_habits''')
            result= cur.fetchall()
            result = [row[0] for row in result]
            if self.habit in result:
                cur.execute('''INSERT INTO history_habits (habit, starting_date, periodicity, streak ) SELECT habit, starting_date, periodicity, streak FROM active_habits WHERE habit = ?''', (self.habit,))
                cur.execute('''DELETE FROM active_habits WHERE habit = ? ''', (self.habit,))
                
                connection.commit()
                print(f'Habit {self.habit} deleted')

            else:
                print('habit not found, verify all active habits with mod 4')

        except:
            print('habit not found, verify all active habits with mod 4')

    def modify_habit(self): #modify the periodicity of an active habit
        try:
            cur.execute('''SELECT * FROM active_habits''')
            result= cur.fetchall()
            result = result[0][0]
            if self.habit in result:
                cur.execute('''UPDATE active_habits SET periodicity = ? WHERE habit = ?''' , (self.periodicity, self.habit))
                connection.commit()
                print(f'habit {self.habit} periodicity updated to: {self.periodicity}')
            else:
                print('habit not found, check active habits with mod 4')
        except:
            print('habit not found, verify all active habits with mod 4')
    



#notify user if a 7, 21 or 31 days streak has been made
class Notifications:
    
    def streaks_notif():   # notify 7, 21, 30 days streaks
        cur.execute('''SELECT * FROM active_habits''')
        result= cur.fetchall()
        connection.commit()
        for x in result:
            if x[3] == 7:
                habit = x[0]
                print(f'you have made a 7 days streak in the habit {habit}')
            elif x[3] == 21:
                habit = x[0]
                print(f'you have made a 21 days streak in the habit {habit}') 
            
            elif x[3] == 31:
                habit = x[0]
                print(f'you have made a 31 days streak in the habit {habit}')
            
            else:
                pass



#manages data withouth self
class Datamanager:

    def delete_all_active(): #delete all data store in db active_habits and save them in db history_habits
        cur.execute('''INSERT INTO history_habits (habit, starting_date, periodicity, streak ) SELECT habit, starting_date, periodicity, streak FROM active_habits''')
        cur.execute('''DELETE FROM active_habits ''')  
        connection.commit()
        print('the active habits database has been reset, data saved on history')
    
    def delete_all_history():   #delete all data stored in history_habits
        cur.execute('''DELETE FROM history_habits ''')
        connection.commit()
        print('the history of habits database has been reset')
    
    def all_active():  #return all habits in active_habits
        cur.execute('''SELECT * FROM active_habits''')
        result= cur.fetchall()
        connection.commit()
        print('ACTIVE HABITS: ' , result)
      
    def show_history():      #return all habits in history_habits
        cur.execute('''SELECT * FROM history_habits''')
        result= cur.fetchall()
        connection.commit()
        print('HABITS SAVED IN HISTORY: ' , result)
   
    def check_complete():     #ask the user if habit has been completed for the day, update streaks in active_habits or save the broken habit in history_habits.
        cur.execute('''SELECT habit, periodicity, streak FROM active_habits ''')
        result = cur.fetchall()
        connection.commit()
    
        today_active_habits = {row[0]: [row[1] , row[2]] for row in result}  #traform tuple in iterable
        
        for name in today_active_habits:
            
            period = int(today_active_habits[name][0])
            current_streak = int(today_active_habits[name][1])
           
            if current_streak % period == 0: #consent to ask the question periodically, the streak is increased until a multiple is reached and then the question is asked

                while True:
                    
                    check = input(f'did you complete {name}? YES/NO:   ')

                    if check.upper() == 'YES':   #update streak
                        cur.execute('''SELECT streak FROM active_habits WHERE habit = ? ''' , (name,))
                        streak = cur.fetchall()
                        streak = streak[0][0]   #trasform touple
                        
                        streak += 1
                        cur.execute('''UPDATE active_habits SET streak = ? WHERE habit = ? ''', (streak, name))
                        connection.commit()

                        print(' \n great! \n ')
                        break
                    
                    elif check.upper() == 'NO':  #habit broken, delete active habit and insert it in history_habit 
                        print(f'habit {name} interrupted therefore deleted. saved in history')
                        cur.execute('''INSERT INTO history_habits (habit, starting_date, periodicity, streak ) SELECT habit, starting_date, periodicity, streak FROM active_habits WHERE habit = ?''', (name,))
                        cur.execute('''DELETE FROM active_habits WHERE habit = ? ''' , (name,))
                        connection.commit()
                        break
                    
                    else:
                        print('incorrect spelling, try again')
                        pass

            elif current_streak % period != 0: 
                cur.execute('''SELECT streak FROM active_habits WHERE habit = ? ''' , (name,))
                streak = cur.fetchall()
                streak = streak[0][0]   #trasform touple
                
                streak += 1
                cur.execute('''UPDATE active_habits SET streak = ? WHERE habit = ? ''', (streak, name))
                connection.commit()
                   
    def longest_active(): #return habits with the longest streak in active_habits
        cur.execute('''SELECT habit, streak FROM active_habits''')
        result = cur.fetchall()

        try:
            max_streak = max(x[1] for x in result)
            longest_habits = [x[0] for x in result if x[1] == max_streak]

            if len(longest_habits) == 1:
                print(f'the longest active habit is {longest_habits} with streak of {max_streak} days!' )
            elif len(longest_habits) > 1:
                print(f'the longest active habits are {longest_habits} with streak of {max_streak} days!')
            
            else:
                print('An error has occured')
        
        except:
            print('no habits found')
    
    def compare_history():  #return  habits with longest streak in history_habits
        cur.execute('''SELECT habit, streak, starting_date FROM history_habits''')
        result = cur.fetchall()
        
        try:
            max_streak = max(x[1] for x in result)
            longest_habits = [x[0] for x in result if x[1] == max_streak]

            if len(longest_habits) == 1:
                print(f'the longest habit stored in history is {longest_habits} with streak of {max_streak} days!' )
            elif len(longest_habits) > 1:
                print(f'the longest habits in history are {longest_habits} with streak of {max_streak} days!')
            
            else:
                print('An error has occured')
        
        except:
            print('no habits found')

    def close_db_connections(): #close connection with db
        cur.close()
        connection.close()

    def last_check_date():   #check if the application was already open today
        cur.execute('''SELECT date FROM check_in_date''')
        last_check = cur.fetchall()
        connection.commit()
        
        try:
            last_check = last_check[0][0]
            
            if last_check == current_date:
                return True
            elif last_check != current_date:
                cur.execute('''UPDATE check_in_date SET date = ? WHERE date = ?''', (current_date, last_check))
                connection.commit()
                return False
        except: 
            cur.execute(''' INSERT INTO check_in_date VALUES (?)''', (current_date,))
            connection.commit()
            return False



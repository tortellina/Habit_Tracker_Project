from models import Notifications , Datamanager , Habit

if __name__ == '__main__':

    print('-'*8, 'HABIT TRACKING APPLICATION', '-'*8)
    
    check_date_bool = Datamanager.last_check_date()
   
   #activate notifications and datamanager for checking if the habits have been completed only once a day
    if check_date_bool == False:
        Notifications.streaks_notif()
        Datamanager.check_complete()
    elif check_date_bool == True:
        pass
    else:
        print('an error has occured')


    print('''CHOSE A MODALITY:
            1 - ADD NEW HABIT
            2 - DELETE HABIT
            3 - UPDATE HABIT PERIODICITY
            4 - SHOW ALL ACTIVE HABITS
            5 - SHOW THE HISTORY OF HABITS
            6 - DELETE ALL ACTIVE HABITS
            7 - DELETE ALL HISTORY OF HABITS
            8 - RETURN ACTIVE HABIT WITH THE LONGEST STREAK
            9 - RETURN LONGEST STREAK EVER MADE IN HISTORY
            10 - CLOSE APPLICATION
            ''')
    

    while True:
    
        choice = input(' \n INSERT MODALITY NUMBER HERE: ')
        
        if choice == '1':
            try:
                habit_name = input('NAME OF NEW HABIT: ')
                period = int(input('HABIT PERIODICITY: '))
                new_habit = Habit(habit_name, period)
                Habit.add_habit(new_habit)
            except:
                print('insert accepted values')

        elif choice == '2':
            try:
                habit_name = input('NAME OF THE HABIT YOU WANT TO DELETE: ')
                period = int(input('PERIODICITY OF THE HABIT YOU WANT TO DELETE: '))
                old_habit = Habit(habit_name, period)
                Habit.delete_habit(old_habit)
            except:
                print('habit not found, verify all active habits with mod 4')
        
        elif choice == '3':
            try:
                habit_name = input('NAME OF THE HABIT YOU WANT TO MODIFY: ')
                period = int(input('UPDATED PERIODICITY: '))
                updated_habit = Habit(habit_name, period)
                Habit.modify_habit(updated_habit)
            except:
               print('habit not found, verify active habits with mod 4')

        elif choice == '4':
            Datamanager.all_active()
        
        elif choice == '5':
            Datamanager.show_history()
        
        elif choice == '6':
            while True:
                
                check = input('Are you sure of deleting all currently tracked habits? YES/NO ').lower()

                if check == 'yes':
                    Datamanager.delete_all_active()
                    break
                elif check == 'no':
                    print('exit modality')
                    break
                else:
                    print('invalid value inserted, try again')

        elif choice == '7':
            while True:
                
                check = input('Are you sure of deleting all the history of habits? YES/NO ').lower()

                if check == 'yes':
                    Datamanager.delete_all_history()
                    break
                elif check == 'no':
                    print('exit modality')
                    break
                else:
                    print('invalid value inserted, try again')

        elif choice == '8':
            Datamanager.longest_active()
        
        elif choice == '9':
            Datamanager.compare_history()
        
        elif choice == '10':
            Datamanager.close_db_connections()
            print('-'*8 , 'APPLICATION CLOSED, GOODBYE!', '-'*8)
            break

        else:
            print('number inserted not valid')
            pass
    
        
    
        

    
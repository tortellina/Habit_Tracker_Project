# HABIT TRACKER APPLICATION

This is a habit tracker application used to track habits and perform comparisons between the data gathered.

## FUNCTIONALITY

The application is based on the use of OOP and FB programming supported by an SQLITE3 database. In the Databaseconfig file there are three tables: 'active_habits' used to store and manage the activly tracked habits, 'history_habits' used to store past habits (broken or deleted habits saved in memory), and 'check_in_date' used to  track when the application was last opended.

The functionalities of the application are found in the models file, divided in three classes: Habit, Datamanager and Notifications.
Habit class store the def functions related to self, which include adding, deleting, modifying a habit.
Datamanger perform static methods, withouth the need to use self, which compare data inside the databases as comparing the streaks, checking if the habits were completed for the day, retrive informations from the db and resetting the db.
Notifications notify the user if a 7, 21 or 31 days streak was made at the opening of the application.

The testing is done in the tests file, made by the use of the library unittest.mock in particular the functionality patch used to mock the db, cursor and connection. It can be run in the terminal by running 'pytest tests.py'

Everything is then linked togheter in the main.py file: the shell of the application is an CLI interface based on inputs that consent the user to interract with the specified functions contained in the printed list.

## INSTALLATION

The application has been enclosed in a executable file using Pyinstaller. A copy of the python intepreter and all the dependecies required have been included. 

The file is a standalone executable, with no need of extra installations from the user that can be run by click on the icon.

## USAGE EXAMPLE

Everytime that you open the app during the day for the first time you are asked if you have completed for the day the activly tracked habits you have previously inserted. If the periodicity you have inserted is not 1 (daily) you are going to be reminded automatically periodically. At the same time you will be notified if any of the tracked habits reached a streak goal (7, 21, 31 days).

The funcionalities can be accessed anytime of the day by inserting only the corresponding number, one at the time, when asked by the application:

'''CHOSE A MODALITY:
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
            '''

1 - you will be asked to insert the name of the habit you want to track and then the periodicity which have to be expressed in number format. 
    examples: 
        daily = 1
        weekly = 7
        every two days = 2
        every eleven days = 11

2 - you will be asked to insert the name of the habit you want to delete and then the corresponding periodicity. The habit will be deleted and saved in the history database.

3 - if needed you can modify the periodicity of the habit withouth losing the steak. You will be asked to insert the habit name and then the new desired periodicity.

4 - displays all the habits that are currently tracked with the relative informations: habit name , starting date, periodicity, streak.

5 -  display all the habits that are stored in memory and NOT currently tracked with the relative informations: habit name , starting date, periodicity, streak. They are deleted or broken streak habits.

6 - reset the active_habits table. All the activly tracked habits are going to be deleted and stored in the history_habits table.

7 - reset the history_habits table. The content is permanently lost.

8 - compare the activly tracked habits and return the habit/habits with the longest streak.

9 - compare the streaks of the habits saved in history and return the habit/habits with the longest streak.

10 - exit the application


## HELP

contact me for help :)
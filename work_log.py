import datetime
from collections import OrderedDict
import os

from peewee import *


# create the database
db = SqliteDatabase('log.db')

# table for Entries (Entry)
class Entry(Model):
    employee = CharField(max_length = 20)
    task = CharField(max_length = 255, unique = True)
    time = IntegerField(default = 0)
    note = TextField()
    timestamp = DateTimeField(default = datetime.date.today)

    # reference the db
    class Meta():
        database = db

def check_emp_task(data):
    """Throws an error if there is no employee or task name"""
    if data == '' or None:
        raise ValueError('Must give input')
    else:
        return data

def check_data(data, date, num):
    """Checks either a date, duration, employee or task name"""
    if num:
        try:
            data = int(data)
            return data
        except ValueError as err:
            print(err)
    elif date:
        try:
            datetime.datetime.strptime(data, '%Y-%m-%d')
            return data
        except ValueError as err:
            print(err)
        except TypeError as err:
            print(err)
    else:
        try:
            check_emp_task(data)
            return data
        except ValueError as err:
            print(err)

def loop_data(data, str, date, num):
    """Recurses until a valid input is received"""
    data = check_data(data, date, num)
    while not data:
        data = loop_data(input(str), str, date, num)
    return data

def get_data():
    """get data for an entry"""
    data = []
    name = loop_data(input('Employee: '), 'Employee: ', False, False)
    data.append(name)
    task = loop_data(input('Task Name: '), 'Task Name: ', False, False)
    data.append(task)
    dur = loop_data(input('Duration (in min): '), 'Duration (in min): ', False, False)
    data.append(dur)
    data.append(
        input('Input notes here (optional). Press enter to continue. \n>>> '))

    if input("Use a date besides today's? [N][y]: ").lower() == 'y':
        date = loop_data(input('Input date in format YYYY-MM-DD: '), 'Input date in format YYYY-MM-DD: ', True, False)
        data.append(date)
    else:
        data.append(datetime.date.today())
    
    return data
    
def add_entry(*args):
    """create an entry"""
    Entry.create(employee=args[0], task=args[1], 
                time=args[2], note=args[3], timestamp = args[4])

def display_entries(entries):
    """Shows the contents of the query results"""
    entries = entries.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('DATE: {}\n'.format(entry.timestamp))
        print('EMPLOYEE: {}\n'.format(entry.employee))
        print('TASK: {}\n'.format(entry.task))
        print('DURATION: {} min\n'.format(entry.time))
        print('NOTES: {}\n'.format(entry.note))
        input('ANY KEY TO CONTINUE > ')
    if entries:
        return True
    return False

# search functions available
def search_employee(name):
    """Employee name search"""
    entries = Entry.select().where(Entry.employee == name)
    return entries

def search_date(date):
    """Timestamp search"""
    entries = Entry.select().where(Entry.timestamp == date)
    return entries

def search_time(time):
    """Duration search"""
    entries = Entry.select().where(Entry.time == time)
    return entries

def search_term(term):
    """Keyword search"""
    entries = Entry.select().where(
        Entry.task.contains(term) | Entry.note.contains(term))
    return entries

def range_search(date1, date2):
    """Date range search"""
    entries = Entry.select().where(Entry.timestamp.between(date1, date2))
    return entries

def menu_loop():
    """Loop through menu until quit"""
    choice = None

    while choice != 'q':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('enter q) to quit')
        for key, value in menu.items():
            print('{}): {}'.format(key, value.__doc__))
        choice = input('\nAction:  ').lower().strip()
        print('\n')

        if choice == 'a':
            add_entry(*get_data())
        elif choice =='e':
            display_entries(search_employee(input('Employee: ')))
        elif choice == 't' or choice == 'r':
            date1 = loop_data(input('Date (YYYY-MM-DD): '), 'Date (YYYY-MM-DD): ', True, False)
            if choice == 't':
                display_entries(search_date(date1))
            elif choice == 'r':
                date2 = loop_data(input('End Date (YYYY-MM-DD): '), 'End Date (YYYY-MM-DD): ', True, False)
                display_entries(range_search(date1, date2))
        elif choice == 'd':
            dur = loop_data(input('Duration (in min): '), 'Duration (in min): ', False, True)
            display_entries(search_time(dur))
        elif choice == 'k':
            display_entries(search_term(input('Keyword: ')))
        elif choice == 'q':
            return True

# the menu
menu = OrderedDict([
        ('a', add_entry),
        ('e', search_employee), 
        ('t', search_date),
        ('r', range_search), 
        ('d', search_time), 
        ('k', search_term)
])

# run if in main
if __name__ == "__main__":
    db.connect()
    db.create_tables([Entry], safe = True)
    menu_loop()
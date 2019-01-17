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

def check_date(date):
    # try date, and if valid add to entry data
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError as err:
        print(err)
    except TypeError as err:
        print(err)

def check_emp_task(data):
    if data == '' or None:
        raise ValueError('Must give an employee or task')
    else:
        return data

def check_data(data):
    # try data, and if valid add to entry data
    try:
        check_emp_task(data)
        return data
    except ValueError as err:
        print(err)

def get_data():
    """get data for an entry"""
    data = []
    name = check_data(input('Employee: '))
    while not name:
        name = check_data(input('Employee: '))
    data.append(name)
    task = check_data(input('Task Name: '))
    while not task:
        task = check_data(input('Task Name: '))
    data.append(task)
    while True:
        try:
            time = int(input('Time Spent (in min): '))
            break
        except ValueError as err:
            print(err)
    data.append(time)
    data.append(
        input('Input notes here (optional). Press enter to continue. \n>>> '))

    if input("Use a date besides today's? [N][y]: ").lower() == 'y':
        date = check_date(input('Input date in format YYYY-MM-DD: '))
        while not date:
            date = check_date(input('Input date in format YYYY-MM-DD: '))
        data.append(date)
    else:
        data.append(datetime.date.today())
    
    return data
    
def add_entry(*args):
    """create an entry"""
    Entry.create(employee=args[0], task=args[1], 
                time=args[2], note=args[3], timestamp = args[4])
    return True

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

# search functions available
def search_employee(name):
    """Employee name search"""
    entries = Entry.select().where(Entry.employee == name)
    display_entries(entries)
    if entries:
        return len(entries)
    return False

def search_date(date):
    """Timestamp search"""
    entries = Entry.select().where(Entry.timestamp == date)
    display_entries(entries)
    if entries:
        return len(entries)
    return False

def search_time(time):
    """Duration search"""
    entries = Entry.select().where(Entry.time == time)
    display_entries(entries)
    if entries:
        return len(entries)
    return False

def search_term(term):
    """Keyword search"""
    entries = Entry.select().where(Entry.task.contains(term) 
                                or Entry.note.contains(term))
    display_entries(entries)
    if entries:
        return len(entries)
    return False

def range_search(date1, date2):
    """Date range search"""
    entries = Entry.select().order_by(Entry.timestamp.asc())
    entries = entries.select().where(Entry.timestamp.between(date1, date2))
    display_entries(entries)
    if entries:
        return len(entries)
    return False

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
            search_employee(input('Employee: '))
        elif choice == 't' or choice == 'r':
            date1 = check_date(input('Date (YYYY-MM-DD): '))
            while not date1:
                date1 = check_date(input('Date (YYYY-MM-DD): '))
            if choice == 't':
                search_date(date1)
            elif choice == 'r':
                date2 = check_date(input('End Date (YYYY-MM-DD): '))
                while not date2:
                    date2 = check_date(input('2nd Date (YYYY-MM-DD): '))
                range_search(date1, date2)
        elif choice == 'd':
            search_time(input('Duration: '))
        elif choice == 'k':
            search_term(input('Keyword: '))
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
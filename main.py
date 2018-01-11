import csv
import datetime
import os
import re


def clear():
    """Clear console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu():
    """Displays available functionality in menu."""
    welcome_menu = ('Welcome!\n'
                    'What would you like to do?\n'
                    '(a) Add entry\n'
                    '(b) Search existing entries\n'
                    )
    print(welcome_menu)

    while True:
        choice = input('> ').lower()
        if choice == 'a':
            clear()
            Entry().new_entry()
            break
        elif choice == 'b':
            # checks if work_log.csv exists
            if not os.path.exists('work_log.csv'):
                clear()
                input('Woops! Looks like there is no file to search.\n'
                      'Press enter to return to main menu.\n'
                      )
                clear()
                print(welcome_menu)
                continue
            else:
                clear()
                Entry().search_entries()
                break
        else:
            clear()
            print(welcome_menu +
                  '** Please enter either \'a\' or \'b\' **\n')
            continue


class Entry:
    """Class describing work log entries."""
    def __init__(self):
        """Sets out variables of an Entry instance."""
        self.date = None
        self.name = None
        self.time_spent = None
        self.notes = None

    def new_entry(self):
        """Gets new entry information and prints to csv file"""
        date_prompt = 'Date of task (DD/MM/YYYY):'
        print(date_prompt)
        self.date = input('> ')

        while True:
            try:
                # ensure user input is valid datetime format
                self.date = datetime.datetime.strptime(self.date,
                                                       '%d/%m/%Y').date()
            except ValueError:
                clear()
                print(date_prompt + '\n** Incorrect format **')
                self.date = input('> ')
                continue
            else:
                clear()
                break
        name_prompt = 'Task name:'
        print(name_prompt)
        self.name = input('> ')
        clear()
        time_spent_prompt = 'Time spent (in minutes):'
        print(time_spent_prompt)
        self.time_spent = input('> ')

        while True:
            # ensures user input is integer
            try:
                self.time_spent = int(self.time_spent)
            except ValueError:
                clear()
                print(time_spent_prompt +
                      '\n** Please round time to the nearest minute **')
                self.time_spent = input('> ')
                continue
            else:
                clear()
                break
        notes_prompt = 'Notes (optional):'
        print(notes_prompt)
        self.notes = input('> ')
        # pass 'None' into notes if no user input
        if len(self.notes) == 0:
            self.notes = 'None'
        headers = ['Date', 'Task Name', 'Time Spent (minutes)', 'Notes']
        # if work_log.csv does not exist, create file with appropriate headers
        if not os.path.exists('work_log.csv'):
            with open('work_log.csv', 'w') as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
                csv_writer.writeheader()
        with open('work_log.csv', 'a') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
            csv_writer.writerow({'Date': str(self.date.strftime('%d/%m/%Y')),
                                 'Task Name': self.name,
                                 'Time Spent (minutes)': str(self.time_spent),
                                 'Notes': self.notes
                                 })
        # successful entry message
        clear()
        input('Entry added! Press enter to return to main menu.')
        clear()
        main_menu()

    def search_entries(self):
        """Search work_log.csv for entries."""

        search_menu = ('Search existing entries using:\n'
                       '(a) Date\n'
                       '(b) Time spent\n'
                       '(c) Exact search\n'
                       '(d) Regex pattern\n'
                       '(e) Return to main menu\n'
                       )
        # allows range of user inputs to select menu item
        date = ('a',
                '(a)',
                'a)',
                'date',
                )
        time = ('b',
                '(b)',
                'b)',
                'time',
                'time spent'
                )
        exact = ('c',
                 '(c)',
                 'c)',
                 'exact',
                 'exact search'
                 )
        regex = ('d',
                 '(d)',
                 'd)',
                 'regex',
                 'regex pattern'
                 )
        back = ('e',
                '(e)',
                'e)',
                'return',
                'return to main menu',
                'menu',
                'main menu',
                'return to menu'
                )
        print(search_menu)
        choice = input('> ').lower()
        while True:
            if choice in date:
                clear()
                date_prompt = 'Date of task (DD/MM/YYYY):'
                print(date_prompt)
                # display dates of entries in work_log.csv
                entry_dates = []
                with open('work_log.csv', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    rows = list(csv_reader)[1:]
                    for row in rows:
                        if row[0] not in entry_dates:
                            entry_dates.append(row[0])
                print('The existing dates are ' + ', '.join(entry_dates) + '.')
                self.search_date = input('> ')

                # ensure user input is valid datetime format
                while True:
                    try:
                        self.search_date = (datetime.datetime.
                                            strptime(self.search_date,
                                                     '%d/%m/%Y').date())
                        clear()
                        break
                    except ValueError:
                        clear()
                        print(date_prompt + '\n** Invalid date **')
                        self.search_date = input('> ')
                        continue
                # find entries with matching date
                with open('work_log.csv', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    rows = list(csv_reader)[1:]
                    for row in rows:
                        if row[0] == self.search_date.strftime('%d/%m/%Y'):
                            print('\nDate: ' + row[0] +
                                  '\nTask Name: ' + row[1] +
                                  '\nTime Spent (min): ' + row[2] +
                                  '\nNotes: ' + row[3]
                                  )
                break
            elif choice in time:
                clear()
                time_prompt = 'Time spent (in minutes):'
                print(time_prompt)
                self.search_time = input('> ')
                # ensures user input is integer

                while True:
                    try:
                        self.search_time = int(self.search_time)
                    except ValueError:
                        clear()
                        print(time_prompt +
                              '\n** Please round time to the nearest '
                              'minute **')
                        self.search_time = input('> ')
                        continue
                    else:
                        clear()
                        break
                # find entries with matching time
                with open('work_log.csv', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    rows = list(csv_reader)[1:]
                    for row in rows:
                        if row[2] == str(self.search_time):
                            print('\nDate: ' + row[0] +
                                  '\nTask Name: ' + row[1] +
                                  '\nTime Spent (min): ' + row[2] +
                                  '\nNotes: ' + row[3]
                                  )
                break
            elif choice in exact:
                clear()
                name_prompt = 'Task name/notes:'
                print(name_prompt)
                self.search_name = input('> ')
                clear()
                # find entries with same string as Name or Notes
                with open('work_log.csv', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    rows = list(csv_reader)[1:]
                    for row in rows:
                        if (row[1] == str(self.search_name) or
                                row[3] == str(self.search_name)):
                            print('\nDate: ' + row[0] +
                                  '\nTask Name: ' + row[1] +
                                  '\nTime Spent (min): ' + row[2] +
                                  '\nNotes: ' + row[3]
                                  )
                break
            elif choice in regex:
                clear()
                regex_prompt = 'Regular expression:'
                print(regex_prompt)
                self.search_regex = str(input('> '))
                clear()
                # find entries with string or regex pattern in name or notes
                with open('work_log.csv', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    rows = list(csv_reader)[1:]
                    for row in rows:
                        if (re.search(self.search_regex, row[1]) or
                                re.search(self.search_regex, row[3])):
                            print('\nDate: ' + row[0] +
                                  '\nTask Name: ' + row[1] +
                                  '\nTime Spent (min): ' + row[2] +
                                  '\nNotes: ' + row[3]
                                  )
                break
            # return to main menu
            elif choice in back:
                clear()
                main_menu()
                break
            else:
                clear()
                print(search_menu +
                      '\n** Please enter either \'a\', \'b\', \'c\', '
                      '\'d\', \'e\' **'
                      )
                continue


if __name__ == '__main__':
    clear()
    main_menu()

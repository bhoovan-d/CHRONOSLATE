
# CHRONOSLATE

It is an automatic time table generator for group 1 and group 2 students. It can generate countless timetable combinations pertaining to the student's needs.
Made as a plugin for ChronoFactorem developed by CRUx-BPHC



## USAGE

This Python program serves as a timetable generator that retrieves scheduling data from a MySQL database and JSON file to create conflict-free course schedules for students. The program allows users to input a group number, which corresponds to predefined sets of courses, and generates a detailed timetable by randomly selecting sections (lectures, tutorials, and practicals) for each subject while ensuring there are no time conflicts.
Users can also use two other features:



-  Specify the number of teachers that are unavailable or that you dont want in your schedule
-  specify the number of teachers that must remain in your schedule.
you can put 0 in the entries input if you dont want any such constraints.


## INSTALLATION

To use the program , ensure python 3 and MYSQL are installed and up and running.
Now do the following:
- Create a .sql file using the syntaxes given in "sqlformat.sql"

- Download the "timetable.json" file. It contains the data for the whole schedule.
- Create a ".env" file as shown and replace with your actual MYSQL credentials.
- Install the required dependencies listed in "requirements.txt" file.

You are now ready to run the program!

### Notes

There are some extra bits of code in the program that may seem unnecessary but they are supposed to be used for future updates.


## Feedback

If you have any feedback or queries, please reach out to me at bhoovand123@gmail.com




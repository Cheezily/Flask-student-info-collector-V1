# Flask Student Info Collector V1

## Flask/MySQL

Small Flask app to collect student contact info for extra credit. Used from redirect after a separate survey was completed.  Keeping survey responses and respondent info separate is a requirement for IRB approval to run academic studies.

This app contains a page for students to enter their contact info into a SQL database as well as a page where a password can be entered to retrieve the contact info in .csv format.  When the information in the database is requested, it is exported to a .csv file and then emailed as an attachment to an address specified in the __init__.py file.

# Personal Expense Tracker

A command-line Python application to track personal expenses,
connected to an Oracle Database.

## Features
- Add expenses with category, description, and amount
- View all expenses in a clean table
- View total spending summary by category
- Data stored permanently in Oracle DB

## Tech Stack
- Python 3
- Oracle Database (XE)
- oracledb library

## Project Structure
```
expense_tracker/
├── db_connect.py        # Database connection logic
├── expense_tracker.py   # Main application
├── config.py            # DB credentials (not uploaded to GitHub)
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone this repository
2. Install the required library:
```
   pip install oracledb
```
3. Create a `config.py` file with your Oracle credentials:
```python
   DB_USER     = "your_username"
   DB_PASSWORD = "your_password"
   DB_DSN      = "localhost/XE"
```
4. Run the Oracle setup SQL to create the table:
```sql
   CREATE TABLE expenses (
       id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       category    VARCHAR2(50),
       description VARCHAR2(200),
       amount      NUMBER(10, 2),
       expense_date DATE DEFAULT SYSDATE
   );
```
5. Run the app:
```
   python expense_tracker.py
```

## Author
Karthik V — [GitHub Profile](https://github.com/karthik7mca)
```


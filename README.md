# Personal Expense Tracker

A command-line Python application to track personal expenses, connected to an Oracle Database.

---

## Features

- Add expenses with category, description, and amount
- View all expenses in a clean formatted table
- View total spending summary by category
- Filter expenses by any month and year with a running total
- Delete any expense by ID (with confirmation prompt)
- Data stored permanently in Oracle DB

---

## Tech Stack

- Python 3
- Oracle Database (XE)
- oracledb library

---

## Project Structure
```
expense_tracker/
├── db_connect.py        # Database connection logic
├── expense_tracker.py   # Main application
├── README.md            # Project documentation
└── .gitignore           # Files excluded from GitHub
```

---

## Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/karthik7mca/expense_tracker.git
cd expense_tracker
```

### 2. Install the required library
```bash
pip install oracledb
```

### 3. Update your DB credentials in `db_connect.py`

Open `db_connect.py` and update these values with your Oracle credentials:
```python
connection = oracledb.connect(
    user="system",
    password="your_password",   # change this
    dsn="localhost/XE"
)
```

### 4. Create the table in Oracle SQL Developer

Run this SQL once to create the expenses table:
```sql
CREATE TABLE expenses (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category    VARCHAR2(50),
    description VARCHAR2(200),
    amount      NUMBER(10, 2),
    expense_date DATE DEFAULT SYSDATE
);
```

### 5. Run the app
```bash
python expense_tracker.py
```

---

## How to Use

| Option | What it does |
|--------|-------------|
| 1. Add expense | Enter category, description, and amount |
| 2. View all expenses | See every expense in a formatted table |
| 3. View summary | See total spent per category |
| 4. Filter by month | View all expenses for a specific month and year |
| 5. Delete expense | Delete any entry by ID, with a confirmation step |
| 6. Exit | Close the application |

---

## Sample Output
```
========================================
   Personal Expense Tracker
   Connected to Oracle DB
========================================

What would you like to do?
  1. Add expense
  2. View all expenses
  3. View summary by category
  4. Delete an expense
  5. Exit
```

---

## Author

Karthik V — [GitHub Profile](https://github.com/karthik7mca)
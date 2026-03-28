# Personal Expense Tracker

A full-featured expense tracking application built with Python and Oracle Database.
Available in two modes — a command-line interface and a browser-based web interface.

---

## Features

- Add expenses with category, description, and amount
- View all expenses in a clean formatted table
- View total spending summary by category
- Visualize spending with bar chart and pie chart
- Filter expenses by any month and year
- Delete any expense by ID with a confirmation step
- Data stored permanently in Oracle Database (XE)

---

## Two Ways to Run

### Option 1 — Command Line Interface
Run the app directly in your terminal. Navigate menus by typing a number.

### Option 2 — Web Interface (Flask)
Run the app in your browser at `http://localhost:5000`.
Includes a live dashboard, charts, forms, and full navigation.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3 |
| Database | Oracle Database XE |
| DB Driver | oracledb |
| Charts | matplotlib |
| Web Framework | Flask |
| Templating | Jinja2 |

---

## Project Structure
```
expense_tracker/
├── app.py                   # Flask web application
├── expense_tracker.py       # Command-line application
├── db_connect.py            # Shared database connection logic
├── templates/               # HTML pages for the web interface
│   ├── base.html            # Shared layout and navigation
│   ├── index.html           # Dashboard with charts and summary
│   ├── add.html             # Add expense form
│   ├── expenses.html        # View all expenses table
│   ├── filter.html          # Filter expenses by month
│   └── delete.html          # Delete expense by ID
├── .gitignore               # Files excluded from GitHub
└── README.md                # Project documentation
```

---

## Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/karthik7mca/expense_tracker.git
cd expense_tracker
```

### 2. Install required libraries
```bash
pip install oracledb flask matplotlib
```

### 3. Update your DB credentials in `db_connect.py`

Open `db_connect.py` and update with your Oracle credentials:
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

---

## Running the App

### Command-line version
```bash
python expense_tracker.py
```

### Web version
```bash
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

---

## CLI Menu
```
========================================
   Personal Expense Tracker
   Connected to Oracle DB
========================================

What would you like to do?
  1. Add expense
  2. View all expenses
  3. View summary by category
  4. Visualize spending (charts)
  5. Filter expenses by month
  6. Delete an expense
  7. Exit
```

| Option | What it does |
|--------|-------------|
| 1 | Enter category, description, and amount |
| 2 | See every expense in a formatted table |
| 3 | See total spent grouped by category |
| 4 | Open bar chart and pie chart in a window |
| 5 | View expenses filtered by month and year |
| 6 | Delete any entry by ID with confirmation |
| 7 | Exit the application |

---

## Web Interface Pages

| Page | URL | What it does |
|------|-----|-------------|
| Dashboard | `/` | Summary stats and spending charts |
| Add Expense | `/add` | Form to add a new expense |
| All Expenses | `/expenses` | Full table of every expense |
| Filter by Month | `/filter` | View expenses for a specific month |
| Delete Expense | `/delete` | Find and delete an expense by ID |

---

## Author

Karthik V — [GitHub Profile](https://github.com/karthik7mca)
# expense_tracker.py
# Main program — Personal Expense Tracker
# Connects to Oracle DB and lets you manage your expenses

from db_connect import get_connection  # import our connection function

# ── FUNCTION 1: Add a new expense ──────────────────────────────────────────
def add_expense():
    print("\n--- Add New Expense ---")
    category    = input("Category (e.g. Food, Travel, Bills): ").strip()
    description = input("Description (e.g. Lunch at cafe): ").strip()
    
    # Keep asking until user gives a valid number
    while True:
        try:
            amount = float(input("Amount (e.g. 250.50): ").strip())
            break
        except ValueError:
            print("  Please enter a valid number.")

    # Connect to DB, insert the row, save (commit), close
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (category, description, amount) VALUES (:1, :2, :3)",
        (category, description, amount)
    )

    conn.commit()   # saves the data permanently
    cursor.close()
    conn.close()

    print(f"  Saved! ₹{amount:.2f} added under '{category}'.")


# ── FUNCTION 2: View all expenses ──────────────────────────────────────────
def view_expenses():
    print("\n--- All Expenses ---")

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, category, description, amount, expense_date FROM expenses ORDER BY expense_date DESC"
    )
    rows = cursor.fetchall()   # get every row as a list

    cursor.close()
    conn.close()

    if not rows:
        print("  No expenses found yet.")
        return

    # Print a neat table header
    print(f"\n{'ID':<5} {'Category':<15} {'Description':<25} {'Amount':>10} {'Date':<12}")
    print("-" * 70)

    for row in rows:
        exp_id, category, description, amount, date = row
        print(f"{exp_id:<5} {category:<15} {description:<25} {amount:>10.2f} {str(date)[:10]:<12}")


# ── FUNCTION 3: View summary by category ───────────────────────────────────
def view_summary():
    print("\n--- Expense Summary by Category ---")

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        print("  No expenses to summarize.")
        return

    print(f"\n{'Category':<20} {'Total Spent':>12} {'No. of Entries':>15}")
    print("-" * 50)

    total_all = 0
    for category, total, count in rows:
        print(f"{category:<20} {total:>12.2f} {count:>15}")
        total_all += total

    print("-" * 50)
    print(f"{'TOTAL':<20} {total_all:>12.2f}")


# ── MAIN MENU ───────────────────────────────────────────────────────────────
def main():
    print("=" * 40)
    print("   Personal Expense Tracker")
    print("   Connected to Oracle DB")
    print("=" * 40)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Add expense")
        print("  2. View all expenses")
        print("  3. View summary by category")
        print("  4. Exit")

        choice = input("\nEnter choice (1/2/3/4): ").strip()

        if   choice == "1": add_expense()
        elif choice == "2": view_expenses()
        elif choice == "3": view_summary()
        elif choice == "4":
            print("\nGoodbye! Your expenses are saved safely in Oracle DB.")
            break
        else:
            print("  Invalid choice. Please enter 1, 2, 3, or 4.")

# This line means: only run main() if we run THIS file directly
if __name__ == "__main__":
    main()
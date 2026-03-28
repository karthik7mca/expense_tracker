# expense_tracker.py
# Main program — Personal Expense Tracker
# Connects to Oracle DB and lets you manage your expenses

from db_connect import get_connection  # import our connection function
import matplotlib.pyplot as plt

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

    # ── FUNCTION 6: Visualize spending with charts ─────────────────────────────
def show_charts():
    print("\n--- Generating Spending Charts ---")

    # Fetch category totals from DB (same query as summary)
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # If no data yet, nothing to chart
    if not rows:
        print("  No expenses found. Add some expenses first.")
        return

    # Split the rows into two separate lists — one for labels, one for values
    categories = [row[0] for row in rows]   # e.g. ["Food", "Travel", "Bills"]
    amounts    = [row[1] for row in rows]   # e.g. [1200.0, 800.0, 500.0]

    total = sum(amounts)
    print(f"  Found {len(categories)} categories. Total spent: ₹{total:.2f}")
    print("  Opening chart window...")

    # ── Chart colours (one per category, cycles if more than 8) ──
    colors = [
        "#4C9BE8", "#E87B4C", "#4CE8A0",
        "#E84C6B", "#A04CE8", "#E8D44C",
        "#4CE8D4", "#E84CA0"
    ]

    # ── Create a figure with two side-by-side charts ──────────────
    # figsize controls the window size in inches
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Personal Expense Tracker — Spending Overview",
                 fontsize=14, fontweight="bold", y=1.01)

    # ── LEFT CHART: Horizontal bar chart ──────────────────────────
    bar_colors = colors[:len(categories)]

    bars = ax1.barh(categories, amounts, color=bar_colors, height=0.5)

    ax1.set_title("Spending by Category", fontsize=12, pad=12)
    ax1.set_xlabel("Amount (₹)", fontsize=10)
    ax1.invert_yaxis()   # highest bar at top

    # Add amount labels at the end of each bar
    for bar, amount in zip(bars, amounts):
        ax1.text(
            bar.get_width() + (total * 0.01),   # small gap after bar
            bar.get_y() + bar.get_height() / 2,
            f"₹{amount:,.0f}",
            va="center", fontsize=9
        )

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_xlim(0, max(amounts) * 1.25)   # extra space for labels

    # ── RIGHT CHART: Pie chart ─────────────────────────────────────
    wedges, texts, autotexts = ax2.pie(
        amounts,
        labels=categories,
        colors=bar_colors,
        autopct="%1.1f%%",       # show percentage on each slice
        startangle=140,          # rotate so biggest slice starts at top
        pctdistance=0.75,        # percentage label sits inside the slice
        wedgeprops={"linewidth": 0.8, "edgecolor": "white"}
    )

    # Make percentage text bold and readable
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    ax2.set_title("Spending Breakdown (%)", fontsize=12, pad=12)

    # Add a total label below the pie
    ax2.text(
        0, -1.3,
        f"Total: ₹{total:,.2f}",
        ha="center", fontsize=10, fontweight="bold"
    )

    plt.tight_layout()
    plt.show()   # opens the chart window — program waits here until you close it
    print("  Chart window closed.")


# ── FUNCTION 5: Filter expenses by month and year ──────────────────────────
def filter_by_month():
    print("\n--- Filter Expenses by Month ---")

    # Ask for month (1-12) with validation
    while True:
        try:
            month = int(input("  Enter month (1-12): ").strip())
            if 1 <= month <= 12:
                break
            else:
                print("  Please enter a number between 1 and 12.")
        except ValueError:
            print("  Please enter a valid number.")

    # Ask for year with validation
    while True:
        try:
            year = int(input("  Enter year (e.g. 2026): ").strip())
            if 2000 <= year <= 2100:
                break
            else:
                print("  Please enter a valid year.")
        except ValueError:
            print("  Please enter a valid number.")

    # Connect and query only expenses matching that month and year
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, category, description, amount, expense_date
        FROM   expenses
        WHERE  EXTRACT(MONTH FROM expense_date) = :1
        AND    EXTRACT(YEAR  FROM expense_date) = :2
        ORDER  BY expense_date ASC
        """,
        (month, year)
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Convert month number to a readable name (e.g. 3 → March)
    import calendar
    month_name = calendar.month_name[month]   # built-in Python, no install needed

    print(f"\n  Expenses for {month_name} {year}")
    print(f"  {'ID':<5} {'Category':<15} {'Description':<25} {'Amount':>10} {'Date':<12}")
    print("  " + "-" * 70)

    if not rows:
        print(f"  No expenses found for {month_name} {year}.")
        return

    total = 0
    for row in rows:
        exp_id, category, description, amount, date = row
        print(f"  {exp_id:<5} {category:<15} {description:<25} {amount:>10.2f} {str(date)[:10]:<12}")
        total += amount

    # Show total at the bottom
    print("  " + "-" * 70)
    print(f"  {'Total':<45} {total:>10.2f}")
    print(f"\n  {len(rows)} expense(s) found for {month_name} {year}.")


# ── FUNCTION 4: Delete an expense by ID ────────────────────────────────────
def delete_expense():
    print("\n--- Delete an Expense ---")

    # First, show all expenses so the user knows which ID to pick
    view_expenses()

    # Ask for the ID to delete
    while True:
        try:
            exp_id = int(input("\nEnter the ID you want to delete (0 to cancel): ").strip())
            break
        except ValueError:
            print("  Please enter a valid number.")

    # User changed their mind
    if exp_id == 0:
        print("  Cancelled. Nothing was deleted.")
        return

    # Fetch that specific row to show the user what they are about to delete
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, category, description, amount FROM expenses WHERE id = :1",
        (exp_id,)
    )
    row = cursor.fetchone()   # fetchone() gets just one row (or None if not found)

    # If no row found with that ID
    if row is None:
        print(f"  No expense found with ID {exp_id}. Nothing deleted.")
        cursor.close()
        conn.close()
        return

    # Show the expense they are about to delete
    exp_id_found, category, description, amount = row
    print(f"\n  You are about to delete:")
    print(f"  ID: {exp_id_found} | {category} | {description} | ₹{amount:.2f}")

    # Ask for confirmation before permanently deleting
    confirm = input("\n  Are you sure? Type YES to confirm: ").strip().upper()

    if confirm == "YES":
        cursor.execute("DELETE FROM expenses WHERE id = :1", (exp_id,))
        conn.commit()   # permanently saves the deletion
        print(f"  Deleted successfully. Expense ID {exp_id} is removed.")
    else:
        print("  Cancelled. Nothing was deleted.")

    cursor.close()
    conn.close()
    
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
        print("  4. Visualize spending (charts)")
        print("  5. Filter expenses by month")
        print("  6. Delete an expense")
        print("  7. Exit")
        
        choice = input("\nEnter choice (1/2/3/4/51): ").strip()
        if   choice == "1": add_expense()
        elif choice == "2": view_expenses()
        elif choice == "3": view_summary()
        elif choice == "4": show_charts()
        elif choice == "5": filter_by_month()
        elif choice == "6": delete_expense()
        elif choice == "7":
            print("\nGoodbye! Your expenses are saved safely in Oracle DB.")
            break
        else:
            print("  Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")

# This line means: only run main() if we run THIS file directly
if __name__ == "__main__":
    main()
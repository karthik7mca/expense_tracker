# app.py
# Flask web application for Personal Expense Tracker
# Runs on http://localhost:5000

from flask import Flask, render_template, request, redirect, url_for, flash
from db_connect import get_connection
import matplotlib
matplotlib.use("Agg")          # use non-interactive backend (no popup window)
import matplotlib.pyplot as plt
import calendar
import io
import base64

app = Flask(__name__)
app.secret_key = "expense_tracker_secret"   # needed for flash messages


# ── HELPER: generate chart image and return as base64 string ───────────────
# Instead of showing a popup window, we convert the chart to an image
# that gets embedded directly into the HTML page
def generate_chart():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return None

    categories = [row[0] for row in rows]
    amounts    = [float(row[1]) for row in rows]
    total      = sum(amounts)

    colors = ["#4C9BE8","#E87B4C","#4CE8A0","#E84C6B",
              "#A04CE8","#E8D44C","#4CE8D4","#E84CA0"]
    bar_colors = colors[:len(categories)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Spending Overview", fontsize=13, fontweight="bold")

    # Bar chart
    bars = ax1.barh(categories, amounts, color=bar_colors, height=0.5)
    ax1.set_title("Spending by Category", fontsize=11)
    ax1.set_xlabel("Amount (₹)")
    ax1.invert_yaxis()
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_xlim(0, max(amounts) * 1.3)
    for bar, amount in zip(bars, amounts):
        ax1.text(bar.get_width() + (total * 0.01),
                 bar.get_y() + bar.get_height() / 2,
                 f"₹{amount:,.0f}", va="center", fontsize=9)

    # Pie chart
    wedges, texts, autotexts = ax2.pie(
        amounts, labels=categories, colors=bar_colors,
        autopct="%1.1f%%", startangle=140, pctdistance=0.75,
        wedgeprops={"linewidth": 0.8, "edgecolor": "white"}
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")
    ax2.set_title("Spending Breakdown (%)", fontsize=11)
    ax2.text(0, -1.3, f"Total: ₹{total:,.2f}",
             ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()

    # Convert chart to base64 image string (so HTML can embed it directly)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    chart_data = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return chart_data


# ── ROUTE 1: Dashboard ──────────────────────────────────────────────────────
@app.route("/")
def index():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), NVL(SUM(amount), 0) FROM expenses")
    count, total = cursor.fetchone()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    )
    summary = cursor.fetchall()
    cursor.close()
    conn.close()

    chart_data = generate_chart()
    return render_template("index.html",
                           count=count, total=total,
                           summary=summary, chart_data=chart_data)


# ── ROUTE 2: Add expense ────────────────────────────────────────────────────
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        category    = request.form["category"].strip()
        description = request.form["description"].strip()
        amount      = request.form["amount"].strip()

        # Simple validation
        if not category or not description or not amount:
            flash("All fields are required.", "error")
            return redirect(url_for("add"))
        try:
            amount = float(amount)
        except ValueError:
            flash("Amount must be a valid number.", "error")
            return redirect(url_for("add"))

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (category, description, amount) VALUES (:1, :2, :3)",
            (category, description, amount)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f"Expense of ₹{amount:.2f} added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


# ── ROUTE 3: View all expenses ──────────────────────────────────────────────
@app.route("/expenses")
def expenses():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, category, description, amount, expense_date FROM expenses ORDER BY expense_date DESC"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("expenses.html", expenses=rows)


# ── ROUTE 4: Filter by month ────────────────────────────────────────────────
@app.route("/filter", methods=["GET", "POST"])
def filter_expenses():
    results = []
    month_name = ""
    total = 0

    if request.method == "POST":
        month = int(request.form["month"])
        year  = int(request.form["year"])

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, category, description, amount, expense_date
               FROM expenses
               WHERE EXTRACT(MONTH FROM expense_date) = :1
               AND   EXTRACT(YEAR  FROM expense_date) = :2
               ORDER BY expense_date ASC""",
            (month, year)
        )
        results    = cursor.fetchall()
        cursor.close()
        conn.close()

        month_name = f"{calendar.month_name[month]} {year}"
        total      = sum(float(row[3]) for row in results)

    return render_template("filter.html",
                           results=results, month_name=month_name, total=total)


# ── ROUTE 5: Delete expense ─────────────────────────────────────────────────
@app.route("/delete", methods=["GET", "POST"])
def delete():
    expense = None

    if request.method == "POST":
        action = request.form.get("action")
        exp_id = request.form.get("exp_id")

        if action == "find":
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, category, description, amount FROM expenses WHERE id = :1",
                (exp_id,)
            )
            expense = cursor.fetchone()
            cursor.close()
            conn.close()
            if not expense:
                flash(f"No expense found with ID {exp_id}.", "error")

        elif action == "confirm":
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = :1", (exp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            flash(f"Expense ID {exp_id} deleted successfully.", "success")
            return redirect(url_for("expenses"))

    return render_template("delete.html", expense=expense)


# ── START THE APP ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
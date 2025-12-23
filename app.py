from flask import Flask, render_template, request, redirect, send_file
import csv
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "expenses.csv"
MONTHLY_BUDGET = 3000  # You can change this amount

@app.route("/")
def index():
    expenses = []
    total = 0
    category_summary = {}
    monthly_summary = {}
    budget_alert = False

    with open(FILE_NAME, mode="r") as file:
        reader = list(csv.reader(file))
        header = reader[0]
        rows = reader[1:]

        for index, row in enumerate(rows):
            amount = float(row[0])
            category = row[1]
            date = row[2]

            expenses.append([index, amount, category, date])
            total += amount

            # Category-wise summary
            category_summary[category] = category_summary.get(category, 0) + amount

            # Monthly summary
            month = date[:7]  # YYYY-MM
            monthly_summary[month] = monthly_summary.get(month, 0) + amount

    # Budget alert
    if total > MONTHLY_BUDGET:
        budget_alert = True

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        category_summary=category_summary,
        monthly_summary=monthly_summary,
        budget_alert=budget_alert,
        budget=MONTHLY_BUDGET
    )

@app.route("/add", methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"]
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, date])

    return redirect("/")

@app.route("/delete/<int:index>")
def delete_expense(index):
    with open(FILE_NAME, mode="r") as file:
        rows = list(csv.reader(file))

    header = rows[0]
    data = rows[1:]

    if 0 <= index < len(data):
        data.pop(index)

    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    return redirect("/")

@app.route("/export")
def export_csv():
    return send_file(FILE_NAME, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

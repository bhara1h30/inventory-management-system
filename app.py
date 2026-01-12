from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "shura_secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory_system"
)

cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s,%s,%s)",
                       (name, quantity, price))
        db.commit()

        return redirect(url_for("view_products"))

    return render_template("add_product.html")

@app.route("/products")
def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("view_products.html", products=products)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cursor.execute("UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s",
                       (name, quantity, price, id))
        db.commit()
        return redirect(url_for("view_products"))

    cursor.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cursor.fetchone()
    return render_template("edit_product.html", product=product)

@app.route("/delete/<int:id>")
def delete_product(id):
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for("view_products"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

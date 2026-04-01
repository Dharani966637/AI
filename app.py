from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# DB CONNECTION
import random
import os
from urllib.parse import urlparse
 
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:fEQwqttKIzMTwWHjOYdohZGsuiFnCsKK@switchback.proxy.rlwy.net:22867/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:fEQwqttKIzMTwWHjOYdohZGsuiFnCsKK@switchback.proxy.rlwy.net:22867/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
 
cursor = db.cursor()
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():

    # ADD / UPDATE
    if request.method == 'POST':

        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']

        if 'add' in request.form:
            try:
                cursor.execute(
                    "INSERT INTO customer VALUES (%s,%s,%s,%s)",
                    (name, mobile, amount, location)
                )
                db.commit()
                flash("✅ Customer Added Successfully")
            except:
                flash("❌ Mobile already exists!")

        elif 'update' in request.form:
            cursor.execute(
                "UPDATE customer SET name=%s, amount=%s, location=%s WHERE mobile=%s",
                (name, amount, location, mobile)
            )
            db.commit()
            flash("✏️ Updated Successfully")

        return redirect('/')

    # DELETE
    delete_id = request.args.get('delete')
    if delete_id:
        cursor.execute("DELETE FROM customer WHERE mobile=%s", (delete_id,))
        db.commit()
        flash("🗑️ Deleted Successfully")
        return redirect('/')

    # EDIT
    edit_id = request.args.get('edit')
    edit_data = None
    if edit_id:
        cursor.execute("SELECT * FROM customer WHERE mobile=%s", (edit_id,))
        edit_data = cursor.fetchone()

    # READ
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()

    return render_template('index.html', customers=data, edit_data=edit_data)

if __name__ == '__main__':
    app.run(debug=True)
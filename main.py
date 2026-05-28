from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# ======================================================
# LOAD ENV VARIABLES
# ======================================================

load_dotenv()

# ======================================================
# FASTAPI OBJECT
# ======================================================

app = FastAPI()

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ======================================================
# MYSQL CONNECTION
# ======================================================

conn = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_name"),
    port=int(os.getenv("db_port"))
)

cursor = conn.cursor(dictionary=True)

# ======================================================
# CREATE TABLE
# ======================================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS expense_tracker(

    id INT AUTO_INCREMENT PRIMARY KEY,

    expense_title VARCHAR(200),

    expense_amount FLOAT,

    expense_category VARCHAR(100),

    payment_type VARCHAR(100),

    expense_created_date DATE,

    expense_description TEXT

)

""")

conn.commit()

# ======================================================
# HOME API
# ======================================================

@app.get("/")
def home():

    return {
        "message": "Expense Tracker API Running"
    }

# ======================================================
# ADD EXPENSE
# ======================================================

@app.post("/add_expense")
def add_expense(payload: dict):

    try:

        query = """

        INSERT INTO expense_tracker(

            expense_title,
            expense_amount,
            expense_category,
            payment_type,
            expense_created_date,
            expense_description

        )

        VALUES(%s,%s,%s,%s,%s,%s)

        """

        values = (

            payload["expense_title"],
            payload["expense_amount"],
            payload["expense_category"],
            payload["payment_type"],
            payload["expense_created_date"],
            payload["expense_description"]

        )

        cursor.execute(query, values)

        conn.commit()

        return {
            "message": "Expense Added Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# ======================================================
# GET ALL EXPENSES
# ======================================================

@app.get("/get_expenses")
def get_expenses():

    try:

        query = """

        SELECT *
        FROM expense_tracker

        """

        cursor.execute(query)

        data = cursor.fetchall()

        return {
            "expenses": data
        }

    except Exception as e:

        return {
            "error": str(e)
        }
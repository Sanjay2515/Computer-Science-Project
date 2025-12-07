import mysql.connector

# --------------------------------------------
# CONNECT TO MYSQL (edit user/password if needed)
# --------------------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""  # <-- Put your MySQL password if required
)

cursor = db.cursor()

# --------------------------------------------
# CREATE DATABASE
# --------------------------------------------
cursor.execute("DROP DATABASE IF EXISTS pharmacy")
cursor.execute("CREATE DATABASE pharmacy")
cursor.execute("USE pharmacy")

# --------------------------------------------
# CREATE TABLES EXACTLY AS PROVIDED
# --------------------------------------------

# admins
cursor.execute("""
CREATE TABLE admins (
    U_ID   INT         NOT NULL PRIMARY KEY,
    U_NAME VARCHAR(20) NULL,
    U_PASS VARCHAR(20) NULL
)
""")

# labs
cursor.execute("""
CREATE TABLE labs (
    L_ID         INT          NOT NULL PRIMARY KEY,
    TEST_NAME    VARCHAR(50)  NULL,
    DATE         DATE         NULL,
    Manager_Name VARCHAR(20)  NULL
)
""")

# medicine
cursor.execute("""
CREATE TABLE medicine (
    M_ID       INT         NOT NULL PRIMARY KEY,
    M_NAME     VARCHAR(20) NULL,
    M_TYPE     VARCHAR(20) NULL,
    M_MFN      VARCHAR(20) NULL,
    M_PRICE    INT         NULL,
    M_QUANTITY INT         NULL
)
""")

# orders
cursor.execute("""
CREATE TABLE orders (
    O_ID     INT          NULL,
    O_STRING VARCHAR(100) NULL,
    O_COST   INT          NULL
)
""")

# patients
cursor.execute("""
CREATE TABLE patients (
    P_ID      INT          NOT NULL PRIMARY KEY,
    P_NAME    VARCHAR(20)  NOT NULL,
    P_AGE     INT          NULL,
    P_PICTURE VARCHAR(500) NULL,
    P_GENDER  VARCHAR(20)  NULL,
    L_ID      INT          NULL,
    O_ID      INT          NULL,
    FOREIGN KEY (L_ID) REFERENCES labs(L_ID)
)
""")

# --------------------------------------------
# INSERT 1 DUMMY ROW PER TABLE
# --------------------------------------------

cursor.execute("""
INSERT INTO admins (U_ID, U_NAME, U_PASS)
VALUES (1, 'admin', 'admin123')
""")

cursor.execute("""
INSERT INTO labs (L_ID, TEST_NAME, DATE, Manager_Name)
VALUES (1, 'Blood Test', '2025-01-01', 'Dr.Smith')
""")

cursor.execute("""
INSERT INTO medicine (M_ID, M_NAME, M_TYPE, M_MFN, M_PRICE, M_QUANTITY)
VALUES (1, 'Paracetamol', 'Tablet', 'ABC Pharma', 50, 100)
""")

cursor.execute("""
INSERT INTO orders (O_ID, O_STRING, O_COST)
VALUES (1, '1x Paracetamol', 50)
""")

cursor.execute("""
INSERT INTO patients (P_ID, P_NAME, P_AGE, P_PICTURE, P_GENDER, L_ID, O_ID)
VALUES (1, 'John Doe', 30, 'none', 'Male', 1, 1)
""")

# --------------------------------------------
# SAVE & CLOSE
# --------------------------------------------
db.commit()
cursor.close()
db.close()

print("Database 'pharmacy' created successfully with all tables and dummy records!")

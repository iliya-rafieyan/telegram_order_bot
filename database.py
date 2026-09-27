import sqlite3


DATABASE_NAME = "orders.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            phone TEXT NOT NULL,

            item_type TEXT NOT NULL,

            item_name TEXT NOT NULL,

            quantity INTEGER NOT NULL,

            price INTEGER NOT NULL,

            total_price INTEGER NOT NULL,

            payment_method TEXT NOT NULL,

            receipt_file_id TEXT,

            status TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


def create_order(
    user_id,
    name,
    phone,
    item_type,
    item_name,
    quantity,
    price,
    total_price,
    payment_method,
    receipt_file_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO orders (
            user_id,
            name,
            phone,
            item_type,
            item_name,
            quantity,
            price,
            total_price,
            payment_method,
            receipt_file_id,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        name,
        phone,
        item_type,
        item_name,
        quantity,
        price,
        total_price,
        payment_method,
        receipt_file_id,
        "pending"
    ))

    order_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return order_id


def update_order_status(order_id, status):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE orders

        SET status = ?

        WHERE id = ?
    """, (
        status,
        order_id
    ))

    connection.commit()

    connection.close()


def get_order(order_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *

        FROM orders

        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    return order


def get_pending_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE status = 'pending'
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    connection.close()

    return orders


def get_approved_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE status = 'approved'
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    connection.close()

    return orders


def get_rejected_orders():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE status = 'rejected'
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    connection.close()

    return orders


def get_order_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) AS approved,
            SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) AS rejected
        FROM orders
    """)

    result = cursor.fetchone()

    connection.close()

    return result
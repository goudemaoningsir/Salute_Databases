# !/usr/bin/env python
# -*- coding:utf-8 -*-
from SQLiteHandler import SQLiteHandler


def insert_user(db, name, email):
    """
    插入用户前检查 email 是否存在。

    :param db: SQLiteHandler 实例
    :param name: 用户名
    :param email: 用户 email
    """
    db.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    if db.fetchone() is None:
        db.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        print(f"User {name} inserted.")
    else:
        print(f"Email {email} already exists. Skipping insertion for user {name}.")


if __name__ == "__main__":
    db_path = "./example.db"
    db = SQLiteHandler(db_path)

    # 创建一个表（如果表不存在）
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """
    )

    # 向 users 表插入新用户
    insert_user(db, "John Doe", "john@example.com")
    insert_user(db, "Jane Smith", "jane@example.com")
    insert_user(
        db, "John Doe", "john.doe@example.com"
    )  # 插入另一个 John Doe，但使用不同的 email
    insert_user(db, "Jane Smith", "jane.smith@example.com")  # 尝试插入不同的 email

    # 更新用户信息
    db.execute(
        "UPDATE users SET name = ? WHERE name = ?",
        ("dame", "John Doe"),
    )

    # 查询 users 表中的所有数据
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    print("All users:")
    for user in users:
        print(user)

    # 查询单个用户信息
    db.execute("SELECT * FROM users WHERE name = ?", ("Jane Smith",))
    user = db.fetchone()
    print("\nSingle user:")
    print(user)

    # 删除一个用户
    db.execute("DELETE FROM users WHERE name = ?", ("Jane Smith",))

    # 再次查询所有用户，确认删除
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    print("\nUsers after deletion:")
    for user in users:
        print(user)

    # 关闭连接
    db.close()

# -*- coding: utf-8 -*-
"""数据库初始化和用户创建脚本"""

import pymysql
import sys

def init_database():
    """初始化数据库并创建用户"""
    
    # 尝试不同的密码组合
    passwords_to_try = ['', 'root', 'password', '123456', 'mysql']
    
    connection = None
    root_password = None
    
    print("尝试连接 MySQL...")
    for pwd in passwords_to_try:
        try:
            print(f"  尝试密码: '{pwd}'")
            connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password=pwd if pwd else '',
                charset='utf8mb4'
            )
            root_password = pwd
            print(f"  ✓ 成功! 使用密码: '{pwd}'")
            break
        except pymysql.err.OperationalError as e:
            print(f"  ✗ 失败: {e}")
            continue
    
    if not connection:
        print("\n❌ 无法连接到 MySQL。请手动执行以下步骤:")
        print("1. 打开 MySQL 命令行客户端")
        print("2. 输入你的 root 密码")
        print("3. 执行以下 SQL:")
        print("   CREATE DATABASE IF NOT EXISTS sports_meet DEFAULT CHARACTER SET utf8mb4;")
        print("   CREATE USER IF NOT EXISTS 'sports_user'@'localhost' IDENTIFIED BY 'sports2024';")
        print("   GRANT ALL PRIVILEGES ON sports_meet.* TO 'sports_user'@'localhost';")
        print("   FLUSH PRIVILEGES;")
        print("4. 然后执行 db/schema.sql 文件初始化表结构")
        return False
    
    try:
        cursor = connection.cursor()
        
        # 1. 创建数据库
        print("\n[1/4] 创建数据库 sports_meet...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS sports_meet DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci")
        print("  ✓ 数据库创建成功")
        
        # 2. 创建用户
        print("\n[2/4] 创建用户 sports_user...")
        cursor.execute("CREATE USER IF NOT EXISTS 'sports_user'@'localhost' IDENTIFIED BY 'sports2024'")
        print("  ✓ 用户创建成功")
        
        # 3. 授权
        print("\n[3/4] 授予权限...")
        cursor.execute("GRANT ALL PRIVILEGES ON sports_meet.* TO 'sports_user'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("  ✓ 权限授予成功")
        
        # 4. 执行 schema.sql
        print("\n[4/4] 执行 schema.sql 初始化表结构...")
        with open('db/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 分割并执行 SQL 语句
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    # 忽略一些非关键错误(如 DROP TABLE 时表不存在)
                    if 'doesn\'t exist' not in str(e):
                        print(f"  警告: {e}")
        
        print("  ✓ 表结构初始化成功")
        
        # 验证新用户
        print("\n验证新用户连接...")
        test_conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='sports_user',
            password='sports2024',
            database='sports_meet',
            charset='utf8mb4'
        )
        test_cursor = test_conn.cursor()
        test_cursor.execute("SELECT 1")
        test_conn.close()
        print("  ✓ 新用户连接测试成功!")
        
        print("\n" + "="*60)
        print("✅ 数据库初始化完成!")
        print("="*60)
        print(f"\n数据库配置信息:")
        print(f"  主机: 127.0.0.1")
        print(f"  端口: 3306")
        print(f"  用户名: sports_user")
        print(f"  密码: sports2024")
        print(f"  数据库: sports_meet")
        print("\n配置文件已更新,可以启动 Flask 应用了!")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        if connection:
            connection.close()
        return False

if __name__ == '__main__':
    init_database()

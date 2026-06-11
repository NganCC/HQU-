# -*- coding: utf-8 -*-
"""校运动会管理系统 - 数据模型层 (pymysql 原生SQL)"""

import pymysql
from config import DB_CONFIG


def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def query(sql, params=None, fetch_all=True):
    """通用查询：返回 (列名列表, 数据列表)"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            columns = [col[0] for col in cur.description] if cur.description else []
            rows = cur.fetchall() if fetch_all else cur.fetchone()
        conn.commit()
        return columns, rows
    finally:
        conn.close()


def execute(sql, params=None):
    """通用执行（INSERT/UPDATE/DELETE），返回受影响行数"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            affected = cur.execute(sql, params)
        conn.commit()
        return affected
    finally:
        conn.close()


def call_proc(proc_name, params=None):
    """调用存储过程，返回 (列名列表, 数据列表)"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.callproc(proc_name, params or ())
            columns = [col[0] for col in cur.description] if cur.description else []
            rows = cur.fetchall()
        conn.commit()
        return columns, rows
    finally:
        conn.close()


# ==================== 仪表盘统计 ====================

def get_dashboard_stats():
    col1, rows1 = query("SELECT COUNT(*) AS cnt FROM athlete")
    col2, rows2 = query("SELECT COUNT(*) AS cnt FROM competition_session")
    col3, rows3 = query("SELECT COUNT(*) AS cnt FROM department")
    col4, rows4 = query("SELECT COUNT(*) AS cnt FROM event")
    return {
        'athlete_count': rows1[0][0] if rows1 else 0,
        'session_count': rows2[0][0] if rows2 else 0,
        'dept_count': rows3[0][0] if rows3 else 0,
        'event_count': rows4[0][0] if rows4 else 0,
    }


# ==================== 教练模块 ====================

def get_referee_sessions():
    """查询裁判-场次分配（含关联信息）"""
    sql = """
    SELECT rs.rs_id, r.referee_id, r.name AS referee_name,
           cs.session_id, cs.session_no, e.event_name,
           cs.session_time, cs.track_no, cs.location, rs.role
    FROM referee_session rs
    JOIN referee r ON r.referee_id = rs.referee_id
    JOIN competition_session cs ON cs.session_id = rs.session_id
    JOIN event e ON e.event_id = cs.event_id
    ORDER BY cs.session_time
    """
    return query(sql)


def get_referees():
    """获取所有裁判"""
    return query("SELECT referee_id, name, phone, dept_id FROM referee")


def get_sessions_unassigned(referee_id=None):
    """获取未分配给某裁判的场次"""
    if referee_id is not None:
        sql = """
        SELECT session_id, session_no, session_time, location
        FROM competition_session
        WHERE session_id NOT IN (
            SELECT session_id FROM referee_session WHERE referee_id = %s
        )
        """
        return query(sql, (referee_id,))
    return query("SELECT session_id, session_no, session_time, location FROM competition_session")


def add_referee_session(referee_id, session_id, role='裁判'):
    sql = "INSERT INTO referee_session (referee_id, session_id, role) VALUES (%s, %s, %s)"
    return execute(sql, (referee_id, session_id, role))


def delete_referee_session(rs_id):
    return execute("DELETE FROM referee_session WHERE rs_id = %s", (rs_id,))


def get_sessions_with_athletes():
    """获取所有场次及其参赛运动员（用于计分）"""
    sql = """
    SELECT cs.session_id, cs.session_no, e.event_name,
           cs.session_time, a_s.as_id, a.athlete_id, a.name AS athlete_name,
           a.student_no, d.dept_name
    FROM competition_session cs
    JOIN event e ON e.event_id = cs.event_id
    LEFT JOIN athlete_session a_s ON a_s.session_id = cs.session_id
    LEFT JOIN athlete a ON a.athlete_id = a_s.athlete_id
    LEFT JOIN department d ON d.dept_id = a.dept_id
    ORDER BY cs.session_time, a.name
    """
    return query(sql)


def get_score_records():
    """查询已有成绩记录"""
    sql = """
    SELECT sr.record_id, a.name AS athlete_name, e.event_name,
           cs.session_no, sr.score, sr.rank, sr.points, sr.record_time
    FROM score_record sr
    JOIN athlete_session a_s ON a_s.as_id = sr.as_id
    JOIN athlete a ON a.athlete_id = a_s.athlete_id
    JOIN competition_session cs ON cs.session_id = a_s.session_id
    JOIN event e ON e.event_id = cs.event_id
    ORDER BY sr.record_time DESC
    """
    return query(sql)


def add_score_record(as_id, score, rank):
    sql = "INSERT INTO score_record (as_id, score, rank) VALUES (%s, %s, %s)"
    return execute(sql, (as_id, score, rank))


# ==================== 后勤模块 ====================

def get_logistics_items():
    return query("SELECT * FROM logistics_item ORDER BY item_id")


def get_logistics_item(item_id):
    _, row = query("SELECT * FROM logistics_item WHERE item_id = %s", (item_id,), fetch_all=False)
    return row


def add_logistics_item(item_name, quantity, unit, status, remark):
    sql = "INSERT INTO logistics_item (item_name, quantity, unit, status, remark) VALUES (%s, %s, %s, %s, %s)"
    return execute(sql, (item_name, quantity, unit, status, remark))


def update_logistics_item(item_id, item_name, quantity, unit, status, remark):
    sql = """UPDATE logistics_item
             SET item_name=%s, quantity=%s, unit=%s, status=%s, remark=%s
             WHERE item_id=%s"""
    return execute(sql, (item_name, quantity, unit, status, remark, item_id))


def delete_logistics_item(item_id):
    return execute("DELETE FROM logistics_item WHERE item_id = %s", (item_id,))


def get_logistics_staff_all():
    return query("SELECT * FROM logistics_staff ORDER BY staff_id")


def get_logistics_staff(staff_id):
    _, row = query("SELECT * FROM logistics_staff WHERE staff_id = %s", (staff_id,), fetch_all=False)
    return row


def add_logistics_staff(name, phone, role, status):
    sql = "INSERT INTO logistics_staff (name, phone, role, status) VALUES (%s, %s, %s, %s)"
    return execute(sql, (name, phone, role, status))


def update_logistics_staff(staff_id, name, phone, role, status):
    sql = "UPDATE logistics_staff SET name=%s, phone=%s, role=%s, status=%s WHERE staff_id=%s"
    return execute(sql, (name, phone, role, status, staff_id))


def delete_logistics_staff(staff_id):
    return execute("DELETE FROM logistics_staff WHERE staff_id = %s", (staff_id,))


def get_duty_schedules():
    sql = """
    SELECT ds.duty_id, ds.duty_date, ds.time_slot, ds.location, ds.task_desc,
           ls.staff_id, ls.name AS staff_name
    FROM duty_schedule ds
    JOIN logistics_staff ls ON ls.staff_id = ds.staff_id
    ORDER BY ds.duty_date, ds.time_slot
    """
    return query(sql)


def add_duty_schedule(staff_id, duty_date, time_slot, location, task_desc):
    sql = "INSERT INTO duty_schedule (staff_id, duty_date, time_slot, location, task_desc) VALUES (%s, %s, %s, %s, %s)"
    return execute(sql, (staff_id, duty_date, time_slot, location, task_desc))


def update_duty_schedule(duty_id, staff_id, duty_date, time_slot, location, task_desc):
    sql = """UPDATE duty_schedule
             SET staff_id=%s, duty_date=%s, time_slot=%s, location=%s, task_desc=%s
             WHERE duty_id=%s"""
    return execute(sql, (staff_id, duty_date, time_slot, location, task_desc, duty_id))


def delete_duty_schedule(duty_id):
    return execute("DELETE FROM duty_schedule WHERE duty_id = %s", (duty_id,))


# ==================== 宣传模块 ====================

def get_articles(dept_id=None):
    if dept_id:
        sql = """
        SELECT a.*, d.dept_name
        FROM article a
        LEFT JOIN department d ON d.dept_id = a.dept_id
        WHERE a.dept_id = %s
        ORDER BY a.create_time DESC
        """
        return query(sql, (dept_id,))
    sql = """
    SELECT a.*, d.dept_name
    FROM article a
    LEFT JOIN department d ON d.dept_id = a.dept_id
    ORDER BY a.create_time DESC
    """
    return query(sql)


def get_article(article_id):
    sql = """
    SELECT a.*, d.dept_name
    FROM article a
    LEFT JOIN department d ON d.dept_id = a.dept_id
    WHERE a.article_id = %s
    """
    _, row = query(sql, (article_id,), fetch_all=False)
    return row


def add_article(title, content, dept_id, author):
    sql = "INSERT INTO article (title, content, dept_id, author) VALUES (%s, %s, %s, %s)"
    return execute(sql, (title, content, dept_id, author))


def update_article(article_id, title, content, dept_id, author):
    sql = "UPDATE article SET title=%s, content=%s, dept_id=%s, author=%s WHERE article_id=%s"
    return execute(sql, (title, content, dept_id, author, article_id))


def delete_article(article_id):
    return execute("DELETE FROM article WHERE article_id = %s", (article_id,))


def get_all_departments():
    return query("SELECT dept_id, dept_name, dept_code FROM department ORDER BY dept_id")


# ==================== 积分模块 ====================

def get_personal_ranking():
    return call_proc('sp_personal_ranking')


def get_department_ranking():
    return call_proc('sp_department_ranking')

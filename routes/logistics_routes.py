# -*- coding: utf-8 -*-
"""后勤管理模块路由 (学生B负责)"""

from flask import Blueprint, render_template, request, redirect, url_for
import models

logistics_bp = Blueprint('logistics', __name__)


# ==================== 物品管理 ====================

@logistics_bp.route('/items')
def items():
    cols, rows = models.get_logistics_items()
    return render_template('logistics/items.html', columns=cols, rows=rows)


@logistics_bp.route('/item_add', methods=['POST'])
def item_add():
    models.add_logistics_item(
        request.form.get('item_name', ''),
        request.form.get('quantity', 0, type=int),
        request.form.get('unit', '个'),
        request.form.get('status', '正常'),
        request.form.get('remark', '')
    )
    return redirect(url_for('logistics.items'))


@logistics_bp.route('/item_edit', methods=['POST'])
def item_edit():
    models.update_logistics_item(
        request.form.get('item_id', type=int),
        request.form.get('item_name', ''),
        request.form.get('quantity', 0, type=int),
        request.form.get('unit', '个'),
        request.form.get('status', '正常'),
        request.form.get('remark', '')
    )
    return redirect(url_for('logistics.items'))


@logistics_bp.route('/item_delete/<int:item_id>')
def item_delete(item_id):
    models.delete_logistics_item(item_id)
    return redirect(url_for('logistics.items'))


# ==================== 人员管理 ====================

@logistics_bp.route('/staff')
def staff():
    cols, rows = models.get_logistics_staff_all()
    return render_template('logistics/staff.html', columns=cols, rows=rows)


@logistics_bp.route('/staff_add', methods=['POST'])
def staff_add():
    models.add_logistics_staff(
        request.form.get('name', ''),
        request.form.get('phone', ''),
        request.form.get('role', ''),
        request.form.get('status', '在岗')
    )
    return redirect(url_for('logistics.staff'))


@logistics_bp.route('/staff_edit', methods=['POST'])
def staff_edit():
    models.update_logistics_staff(
        request.form.get('staff_id', type=int),
        request.form.get('name', ''),
        request.form.get('phone', ''),
        request.form.get('role', ''),
        request.form.get('status', '在岗')
    )
    return redirect(url_for('logistics.staff'))


@logistics_bp.route('/staff_delete/<int:staff_id>')
def staff_delete(staff_id):
    models.delete_logistics_staff(staff_id)
    return redirect(url_for('logistics.staff'))


# ==================== 值班管理 ====================

@logistics_bp.route('/schedule')
def schedule():
    cols, rows = models.get_duty_schedules()
    staff_cols, staff_rows = models.get_logistics_staff_all()
    return render_template('logistics/schedule.html',
                           columns=cols, rows=rows,
                           staff_columns=staff_cols, staff_rows=staff_rows)


@logistics_bp.route('/schedule_add', methods=['POST'])
def schedule_add():
    models.add_duty_schedule(
        request.form.get('staff_id', type=int),
        request.form.get('duty_date', ''),
        request.form.get('time_slot', '上午'),
        request.form.get('location', ''),
        request.form.get('task_desc', '')
    )
    return redirect(url_for('logistics.schedule'))


@logistics_bp.route('/schedule_edit', methods=['POST'])
def schedule_edit():
    models.update_duty_schedule(
        request.form.get('duty_id', type=int),
        request.form.get('staff_id', type=int),
        request.form.get('duty_date', ''),
        request.form.get('time_slot', '上午'),
        request.form.get('location', ''),
        request.form.get('task_desc', '')
    )
    return redirect(url_for('logistics.schedule'))


@logistics_bp.route('/schedule_delete/<int:duty_id>')
def schedule_delete(duty_id):
    models.delete_duty_schedule(duty_id)
    return redirect(url_for('logistics.schedule'))

# -*- coding: utf-8 -*-
"""运动员管理路由 (学生A负责)"""

from flask import Blueprint, render_template

athlete_bp = Blueprint('athlete', __name__)


@athlete_bp.route('/')
@athlete_bp.route('/list')
def list_view():
    """运动员列表页 - 由学生A实现"""
    return render_template('athlete/list.html')

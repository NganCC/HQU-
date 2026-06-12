# -*- coding: utf-8 -*-
"""比赛管理路由 (学生A负责)"""

from flask import Blueprint, render_template

competition_bp = Blueprint('competition', __name__)


@competition_bp.route('/')
@competition_bp.route('/list')
def list_view():
    """比赛场次列表 - 由学生A实现"""
    return render_template('competition/list.html')

# -*- coding: utf-8 -*-
"""积分排行路由"""

from flask import Blueprint, render_template
import models

score_bp = Blueprint('score', __name__)


@score_bp.route('/personal')
def personal():
    """个人积分排行 TOP 20"""
    cols, rows = models.get_personal_ranking()
    return render_template('score/personal.html', columns=cols, rows=rows)


@score_bp.route('/department')
def department():
    """院系积分排行"""
    cols, rows = models.get_department_ranking()
    return render_template('score/department.html', columns=cols, rows=rows)

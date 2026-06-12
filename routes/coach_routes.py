# -*- coding: utf-8 -*-
"""教练管理模块路由 (学生B负责)"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
import models

coach_bp = Blueprint('coach', __name__)


@coach_bp.route('/list')
def list_view():
    """裁判场次分配列表"""
    cols, rows = models.get_referee_sessions()
    r_cols, referees = models.get_referees()
    s_cols, sessions = models.get_sessions_unassigned()
    return render_template('coach/list.html',
                           columns=cols, rows=rows,
                           referees=referees, sessions=sessions,
                           r_columns=r_cols, s_columns=s_cols)


@coach_bp.route('/add', methods=['POST'])
def add():
    """添加裁判场次分配"""
    referee_id = request.form.get('referee_id', type=int)
    session_id = request.form.get('session_id', type=int)
    role = request.form.get('role', '裁判')
    if referee_id and session_id:
        try:
            models.add_referee_session(referee_id, session_id, role)
        except Exception:
            pass  # 唯一键冲突静默处理
    return redirect(url_for('coach.list_view'))


@coach_bp.route('/delete/<int:rs_id>')
def delete(rs_id):
    """删除裁判场次分配"""
    models.delete_referee_session(rs_id)
    return redirect(url_for('coach.list_view'))


@coach_bp.route('/scoring')
def scoring():
    """计分确认页面"""
    cols, rows = models.get_sessions_with_athletes()
    score_cols, score_rows = models.get_score_records()
    return render_template('coach/scoring.html',
                           columns=cols, rows=rows,
                           score_columns=score_cols, score_rows=score_rows)


@coach_bp.route('/score_add', methods=['POST'])
def score_add():
    """录入成绩"""
    as_id = request.form.get('as_id', type=int)
    score = request.form.get('score', type=float)
    rank = request.form.get('rank', type=int)
    if as_id and score is not None and rank:
        models.add_score_record(as_id, score, rank)
    return redirect(url_for('coach.scoring'))

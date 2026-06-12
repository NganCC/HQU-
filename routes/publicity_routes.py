# -*- coding: utf-8 -*-
"""宣传管理模块路由 (学生B负责)"""

from flask import Blueprint, render_template, request, redirect, url_for
import models

publicity_bp = Blueprint('publicity', __name__)


@publicity_bp.route('/list')
def list_view():
    """文章报道列表，支持按院系筛选"""
    dept_id = request.args.get('dept_id', type=int)
    cols, rows = models.get_articles(dept_id)
    dept_cols, departments = models.get_all_departments()
    return render_template('publicity/list.html',
                           columns=cols, rows=rows,
                           departments=departments,
                           current_dept=dept_id)


@publicity_bp.route('/edit')
@publicity_bp.route('/edit/<int:article_id>')
def edit(article_id=None):
    """文章编辑/发布页面"""
    article = None
    if article_id:
        article = models.get_article(article_id)
    dept_cols, departments = models.get_all_departments()
    return render_template('publicity/edit.html',
                           article=article,
                           departments=departments)


@publicity_bp.route('/save', methods=['POST'])
def save():
    """新增或更新文章"""
    article_id = request.form.get('article_id', type=int)
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    dept_id = request.form.get('dept_id', type=int)
    author = request.form.get('author', '管理员')

    if article_id:
        models.update_article(article_id, title, content, dept_id, author)
    else:
        models.add_article(title, content, dept_id, author)
    return redirect(url_for('publicity.list_view'))


@publicity_bp.route('/delete/<int:article_id>')
def delete(article_id):
    """删除文章"""
    models.delete_article(article_id)
    return redirect(url_for('publicity.list_view'))

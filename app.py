# -*- coding: utf-8 -*-
"""校运动会管理系统 - Flask 主应用入口"""

from flask import Flask, render_template
import models

app = Flask(__name__)
app.secret_key = 'sports_meet_2024_secret_key'

# 注册蓝图
from routes.athlete_routes import athlete_bp
from routes.competition_routes import competition_bp
from routes.coach_routes import coach_bp
from routes.logistics_routes import logistics_bp
from routes.publicity_routes import publicity_bp
from routes.score_routes import score_bp

app.register_blueprint(athlete_bp, url_prefix='/athlete')
app.register_blueprint(competition_bp, url_prefix='/competition')
app.register_blueprint(coach_bp, url_prefix='/coach')
app.register_blueprint(logistics_bp, url_prefix='/logistics')
app.register_blueprint(publicity_bp, url_prefix='/publicity')
app.register_blueprint(score_bp, url_prefix='/score')


@app.route('/')
def index():
    """首页仪表盘"""
    # 临时跳过数据库查询，使用默认值
    stats = {
        'athlete_count': 0,
        'session_count': 0,
        'dept_count': 0,
        'event_count': 0,
    }
    return render_template('index.html', stats=stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

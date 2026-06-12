-- ============================================================
-- 校运动会管理系统 - 数据库建表脚本 (MySQL 8.0, 符合3NF)
-- ============================================================

CREATE DATABASE IF NOT EXISTS sports_meet
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE sports_meet;

-- ----------------------------
-- 1. 院系表
-- ----------------------------
DROP TABLE IF EXISTS department_score;
DROP TABLE IF EXISTS score_record;
DROP TABLE IF EXISTS referee_session;
DROP TABLE IF EXISTS athlete_session;
DROP TABLE IF EXISTS competition_session;
DROP TABLE IF EXISTS referee;
DROP TABLE IF EXISTS athlete;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS class_info;
DROP TABLE IF EXISTS duty_schedule;
DROP TABLE IF EXISTS logistics_staff;
DROP TABLE IF EXISTS logistics_item;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS department;

CREATE TABLE department (
    dept_id   INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL UNIQUE,
    dept_code VARCHAR(10) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ----------------------------
-- 2. 班级表
-- ----------------------------
CREATE TABLE class_info (
    class_id   INT AUTO_INCREMENT PRIMARY KEY,
    dept_id    INT          NOT NULL,
    class_name VARCHAR(50)  NOT NULL,
    grade      VARCHAR(10)  NOT NULL COMMENT '年级，如 2024',
    FOREIGN KEY (dept_id) REFERENCES department(dept_id),
    UNIQUE KEY uk_dept_class (dept_id, class_name, grade)
) ENGINE=InnoDB;

-- ----------------------------
-- 3. 运动员表
-- ----------------------------
CREATE TABLE athlete (
    athlete_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_no   VARCHAR(20)  NOT NULL UNIQUE,
    name         VARCHAR(30)  NOT NULL,
    gender       ENUM('男','女') NOT NULL,
    dept_id      INT          NOT NULL,
    class_id     INT          NOT NULL,
    grade        VARCHAR(10)  NOT NULL COMMENT '年级',
    athlete_group VARCHAR(10) NOT NULL COMMENT '分组: 甲组/乙组',
    phone        VARCHAR(20),
    FOREIGN KEY (dept_id)  REFERENCES department(dept_id),
    FOREIGN KEY (class_id) REFERENCES class_info(class_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 4. 比赛项目表
-- ----------------------------
CREATE TABLE event (
    event_id   INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(50)  NOT NULL,
    event_type ENUM('田赛','径赛') NOT NULL,
    gender_req ENUM('男','女','不限') NOT NULL DEFAULT '不限',
    group_req  VARCHAR(10)  NOT NULL DEFAULT '甲组' COMMENT '组别要求',
    unit       VARCHAR(10)  NOT NULL DEFAULT '秒' COMMENT '成绩单位'
) ENGINE=InnoDB;

-- ----------------------------
-- 5. 比赛场次表
-- ----------------------------
CREATE TABLE competition_session (
    session_id    INT AUTO_INCREMENT PRIMARY KEY,
    event_id      INT          NOT NULL,
    session_no    VARCHAR(10)  NOT NULL COMMENT '场次编号，如 S01',
    session_time  DATETIME     NOT NULL,
    track_no      VARCHAR(10)  COMMENT '赛道编号',
    location      VARCHAR(100) COMMENT '比赛地点',
    status        ENUM('未开始','进行中','已结束') NOT NULL DEFAULT '未开始',
    FOREIGN KEY (event_id) REFERENCES event(event_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 6. 运动员参赛分配表（多对多）
-- ----------------------------
CREATE TABLE athlete_session (
    as_id      INT AUTO_INCREMENT PRIMARY KEY,
    athlete_id INT NOT NULL,
    session_id INT NOT NULL,
    bib_no     VARCHAR(10) COMMENT '号码布',
    FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id),
    FOREIGN KEY (session_id) REFERENCES competition_session(session_id),
    UNIQUE KEY uk_athlete_session (athlete_id, session_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 7. 裁判表
-- ----------------------------
CREATE TABLE referee (
    referee_id   INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(30) NOT NULL,
    phone        VARCHAR(20),
    dept_id      INT,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 8. 裁判场次分配表
-- ----------------------------
CREATE TABLE referee_session (
    rs_id      INT AUTO_INCREMENT PRIMARY KEY,
    referee_id INT NOT NULL,
    session_id INT NOT NULL,
    role       VARCHAR(30) DEFAULT '裁判' COMMENT '角色: 主裁判/裁判/计时员',
    FOREIGN KEY (referee_id) REFERENCES referee(referee_id),
    FOREIGN KEY (session_id) REFERENCES competition_session(session_id),
    UNIQUE KEY uk_referee_session (referee_id, session_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 9. 成绩记录表
-- ----------------------------
CREATE TABLE score_record (
    record_id  INT AUTO_INCREMENT PRIMARY KEY,
    as_id      INT           NOT NULL COMMENT '运动员场次分配ID',
    score      DECIMAL(10,2) NOT NULL COMMENT '成绩值 (时间/距离)',
    rank       INT           COMMENT '名次',
    points     INT           COMMENT '积分',
    record_time DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (as_id) REFERENCES athlete_session(as_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 10. 院系积分汇总表
-- ----------------------------
CREATE TABLE department_score (
    ds_id    INT AUTO_INCREMENT PRIMARY KEY,
    dept_id  INT NOT NULL UNIQUE,
    gold     INT DEFAULT 0,
    silver   INT DEFAULT 0,
    bronze   INT DEFAULT 0,
    total_points INT DEFAULT 0,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 11. 后勤物品表
-- ----------------------------
CREATE TABLE logistics_item (
    item_id    INT AUTO_INCREMENT PRIMARY KEY,
    item_name  VARCHAR(100) NOT NULL,
    quantity   INT          NOT NULL DEFAULT 0,
    unit       VARCHAR(20)  DEFAULT '个',
    status     VARCHAR(20)  DEFAULT '正常' COMMENT '状态: 正常/不足/损坏',
    remark     VARCHAR(200)
) ENGINE=InnoDB;

-- ----------------------------
-- 12. 后勤人员表
-- ----------------------------
CREATE TABLE logistics_staff (
    staff_id   INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(30) NOT NULL,
    phone      VARCHAR(20),
    role       VARCHAR(50) COMMENT '职责',
    status     VARCHAR(20) DEFAULT '在岗'
) ENGINE=InnoDB;

-- ----------------------------
-- 13. 值班安排表
-- ----------------------------
CREATE TABLE duty_schedule (
    duty_id    INT AUTO_INCREMENT PRIMARY KEY,
    staff_id   INT  NOT NULL,
    duty_date  DATE NOT NULL,
    time_slot  VARCHAR(30) NOT NULL COMMENT '时段: 上午/下午/全天',
    location   VARCHAR(100),
    task_desc  VARCHAR(200),
    FOREIGN KEY (staff_id) REFERENCES logistics_staff(staff_id)
) ENGINE=InnoDB;

-- ----------------------------
-- 14. 文章报道表
-- ----------------------------
CREATE TABLE article (
    article_id INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    content    TEXT         NOT NULL,
    dept_id    INT          COMMENT '作者院系',
    author     VARCHAR(30)  DEFAULT '管理员',
    create_time DATETIME    DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (dept_id) REFERENCES department(dept_id)
) ENGINE=InnoDB;

-- ============================================================
-- 触发器
-- ============================================================

DELIMITER //

-- 插入成绩后自动更新积分和院系汇总
CREATE TRIGGER trg_after_score_insert
AFTER INSERT ON score_record
FOR EACH ROW
BEGIN
    DECLARE v_dept_id INT;
    DECLARE v_points  INT;

    -- 获取运动员所属院系
    SELECT a.dept_id INTO v_dept_id
    FROM athlete_session a_s
    JOIN athlete a ON a.athlete_id = a_s.athlete_id
    WHERE a_s.as_id = NEW.as_id;

    -- 根据名次计算积分 (第1名9分, 第2名7分, 第3名6分, 以此类推)
    SET v_points = CASE NEW.rank
        WHEN 1 THEN 9
        WHEN 2 THEN 7
        WHEN 3 THEN 6
        WHEN 4 THEN 5
        WHEN 5 THEN 4
        WHEN 6 THEN 3
        WHEN 7 THEN 2
        WHEN 8 THEN 1
        ELSE 0
    END;

    -- 更新 score_record 中的 points
    UPDATE score_record SET points = v_points WHERE record_id = NEW.record_id;

    -- 更新院系积分汇总
    INSERT INTO department_score (dept_id, gold, silver, bronze, total_points)
    VALUES (v_dept_id,
            IF(NEW.rank = 1, 1, 0),
            IF(NEW.rank = 2, 1, 0),
            IF(NEW.rank = 3, 1, 0),
            v_points)
    ON DUPLICATE KEY UPDATE
        gold        = gold        + IF(NEW.rank = 1, 1, 0),
        silver      = silver      + IF(NEW.rank = 2, 1, 0),
        bronze      = bronze      + IF(NEW.rank = 3, 1, 0),
        total_points = total_points + v_points;
END //

-- ============================================================
-- 存储过程
-- ============================================================

-- 个人积分排行 TOP 20
CREATE PROCEDURE sp_personal_ranking()
BEGIN
    SELECT
        a.athlete_id,
        a.name       AS athlete_name,
        a.student_no,
        d.dept_name,
        IFNULL(SUM(sr.points), 0) AS total_points,
        COUNT(sr.record_id)        AS event_count
    FROM athlete a
    JOIN department d ON d.dept_id = a.dept_id
    LEFT JOIN athlete_session a_s ON a_s.athlete_id = a.athlete_id
    LEFT JOIN score_record sr     ON sr.as_id = a_s.as_id
    GROUP BY a.athlete_id, a.name, a.student_no, d.dept_name
    ORDER BY total_points DESC
    LIMIT 20;
END //

-- 院系积分排行
CREATE PROCEDURE sp_department_ranking()
BEGIN
    SELECT
        d.dept_id,
        d.dept_name,
        IFNULL(ds.gold, 0)         AS gold,
        IFNULL(ds.silver, 0)       AS silver,
        IFNULL(ds.bronze, 0)       AS bronze,
        IFNULL(ds.total_points, 0) AS total_points
    FROM department d
    LEFT JOIN department_score ds ON ds.dept_id = d.dept_id
    ORDER BY total_points DESC, gold DESC, silver DESC;
END //

DELIMITER ;

-- ============================================================
-- 示例数据
-- ============================================================

INSERT INTO department (dept_name, dept_code) VALUES
('计算机科学与技术学院', 'CS'),
('电子信息工程学院',   'EE'),
('数学与统计学院',     'MATH'),
('物理学院',           'PHY'),
('经济管理学院',       'EM');

INSERT INTO class_info (dept_id, class_name, grade) VALUES
(1, '计科2401', '2024'),
(1, '计科2402', '2024'),
(1, '软工2401', '2024'),
(2, '电信2401', '2024'),
(2, '通信2401', '2024'),
(3, '应数2401', '2024'),
(4, '物理2401', '2024'),
(5, '工商2401', '2024');

INSERT INTO athlete (student_no, name, gender, dept_id, class_id, grade, athlete_group, phone) VALUES
('2024001', '张伟',   '男', 1, 1, '2024', '甲组', '13800001001'),
('2024002', '李娜',   '女', 1, 2, '2024', '甲组', '13800001002'),
('2024003', '王强',   '男', 2, 4, '2024', '甲组', '13800001003'),
('2024004', '赵敏',   '女', 2, 5, '2024', '甲组', '13800001004'),
('2024005', '刘洋',   '男', 3, 6, '2024', '甲组', '13800001005'),
('2024006', '陈静',   '女', 3, 6, '2024', '甲组', '13800001006'),
('2024007', '周杰',   '男', 4, 7, '2024', '甲组', '13800001007'),
('2024008', '吴芳',   '女', 5, 8, '2024', '甲组', '13800001008');

INSERT INTO event (event_name, event_type, gender_req, group_req, unit) VALUES
('男子100米',     '径赛', '男',   '甲组', '秒'),
('女子100米',     '径赛', '女',   '甲组', '秒'),
('男子跳远',       '田赛', '男',   '甲组', '米'),
('女子跳远',       '田赛', '女',   '甲组', '米'),
('男子4x100米接力','径赛', '男',   '甲组', '秒'),
('女子4x100米接力','径赛', '女',   '甲组', '秒'),
('男子铅球',       '田赛', '男',   '甲组', '米'),
('女子铅球',       '田赛', '女',   '甲组', '米');

INSERT INTO competition_session (event_id, session_no, session_time, track_no, location, status) VALUES
(1, 'S01', '2026-06-07 09:00:00', '1号跑道', '田径场', '未开始'),
(1, 'S02', '2026-06-07 09:15:00', '2号跑道', '田径场', '未开始'),
(2, 'S03', '2026-06-07 09:30:00', '1号跑道', '田径场', '未开始'),
(3, 'S04', '2026-06-07 10:00:00', '沙坑A',   '跳远区', '未开始'),
(4, 'S05', '2026-06-07 10:30:00', '沙坑B',   '跳远区', '未开始');

INSERT INTO athlete_session (athlete_id, session_id, bib_no) VALUES
(1, 1, '101'),
(3, 1, '102'),
(5, 2, '201'),
(7, 2, '202'),
(2, 3, '301'),
(4, 3, '302'),
(1, 4, '103'),
(5, 5, '203');

INSERT INTO referee (name, phone, dept_id) VALUES
('黄老师', '13900002001', 1),
('林老师', '13900002002', 1),
('郑老师', '13900002003', 2),
('何老师', '13900002004', 3);

INSERT INTO referee_session (referee_id, session_id, role) VALUES
(1, 1, '主裁判'),
(2, 1, '计时员'),
(1, 2, '主裁判'),
(3, 2, '计时员'),
(4, 3, '主裁判'),
(3, 4, '主裁判'),
(4, 5, '主裁判');

INSERT INTO logistics_item (item_name, quantity, unit, status) VALUES
('号码布',   200, '个', '正常'),
('发令枪',     3, '把', '正常'),
('秒表',      10, '块', '正常'),
('铅球(5kg)',  5, '个', '正常'),
('跳远测量尺', 3, '把', '正常'),
('饮用水',    20, '箱', '正常'),
('急救箱',     5, '个', '正常');

INSERT INTO logistics_staff (name, phone, role) VALUES
('孙师傅', '13700003001', '场地布置'),
('钱阿姨', '13700003002', '物资发放'),
('周同学', '13700003003', '引导员'),
('吴同学', '13700003004', '引导员');

INSERT INTO duty_schedule (staff_id, duty_date, time_slot, location) VALUES
(1, '2026-06-07', '上午', '田径场'),
(1, '2026-06-07', '下午', '田径场'),
(2, '2026-06-07', '上午', '物资站'),
(3, '2026-06-07', '全天', '入口处'),
(4, '2026-06-07', '全天', '颁奖台');

INSERT INTO article (title, content, dept_id, author) VALUES
('校运动会盛大开幕', '6月7日上午，校运动会在田径场隆重开幕。全校师生齐聚一堂，共同见证这一盛事。', 1, '张伟'),
('运动员风采展示',   '本次运动会涌现出众多优秀运动员，他们在赛场上奋勇拼搏，展现了当代大学生的精神风貌。', 2, '李娜'),
('后勤保障有力推进', '为确保运动会顺利进行，后勤团队已提前完成各项准备工作。', 1, '管理员');

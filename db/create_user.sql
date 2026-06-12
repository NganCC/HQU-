-- 创建数据库用户并授权
CREATE USER IF NOT EXISTS 'sports_user'@'localhost' IDENTIFIED BY 'sports2024';
GRANT ALL PRIVILEGES ON sports_meet.* TO 'sports_user'@'localhost';
FLUSH PRIVILEGES;

-- 显示用户信息
SELECT user, host FROM mysql.user WHERE user = 'sports_user';

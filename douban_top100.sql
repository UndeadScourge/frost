SHOW DATABASES;
USE douban_top100;
SHOW TABLES;
DESCRIBE movies;
-- 查看前10条数据
SELECT * FROM movies LIMIT 10;

-- 按排名查看
SELECT movie_rank, title, rating, release_year 
FROM movies 
ORDER BY movie_rank 
LIMIT 10;

-- 查看统计信息
SELECT COUNT(*) as 总数量 FROM movies;
SELECT AVG(rating) as 平均评分 FROM movies;
SELECT MIN(release_year) as 最早年份, MAX(release_year) as 最晚年份 FROM movies;
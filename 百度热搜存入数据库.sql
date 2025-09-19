-- 查看表结构
USE hotsearch_db;
DESCRIBE baidu_hot;

-- 查看数据
SELECT * FROM baidu_hot;

-- 按排名排序查看
SELECT hot_rank, title, hot_index, crawl_time 
FROM baidu_hot 
ORDER BY hot_rank ASC;
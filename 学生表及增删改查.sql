-- 1. 创建数据库（如果不存在的话）
CREATE DATABASE IF NOT EXISTS school_db;
USE school_db;

-- 2. 删除已存在的表（避免冲突）
DROP TABLE IF EXISTS students;

-- 3. 创建学生表（三个字段：学号、姓名、身高）
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    height DECIMAL(5,2)
);

-- 4. 查看表结构（验证创建是否成功）
DESCRIBE students;

-- 5. 插入示例数据
INSERT INTO students (student_id, name, height) VALUES 
('2023001', '宋江', 176.2),
('2023002', '卢俊义', 162.8),
('2023003', '吴用', 181.5),
('2023004', '公孙胜', 169.3),
('2023005', '关胜', 174.9);

-- 6. 查询数据（验证插入是否成功）
SELECT * FROM students;

-- ==================== 查询操作（READ） ====================

-- 1. 查询所有学生
SELECT '=== 所有学生数据 ===' as '';
SELECT * FROM students;

-- 2. 查询特定字段
SELECT '=== 学号、姓名、身高 ===' as '';
SELECT student_id, name, height FROM students;

-- 3. 条件查询：身高大于175的学生
SELECT '=== 身高大于175cm的学生 ===' as '';
SELECT * FROM students WHERE height > 175;

-- 4. 条件查询：姓宋的学生
SELECT '=== 姓宋的学生 ===' as '';
SELECT * FROM students WHERE name LIKE '宋%';

-- 5. 条件查询：名字包含"胜"的学生
SELECT '=== 名字包含"胜"的学生 ===' as '';
SELECT * FROM students WHERE name LIKE '%胜%';

-- 6. 排序查询：按身高降序
SELECT '=== 按身高降序排列 ===' as '';
SELECT * FROM students ORDER BY height DESC;

-- 7. 排序查询：按名字拼音顺序
SELECT '=== 按名字拼音顺序排列 ===' as '';
SELECT * FROM students ORDER BY name ASC;

-- 8. 统计查询
SELECT '=== 统计信息 ===' as '';
SELECT 
    COUNT(*) as 总人数,
    AVG(height) as 平均身高,
    MAX(height) as 最高身高,
    MIN(height) as 最矮身高
FROM students;

-- ==================== 插入操作（CREATE） ====================

-- 9. 插入新学生
SELECT '=== 插入新学生前 ===' as '';
SELECT * FROM students;

INSERT INTO students (student_id, name, height) VALUES 
('2023006', '林冲', 178.6),
('2023007', '秦明', 165.2);

SELECT '=== 插入新学生后 ===' as '';
SELECT * FROM students;

-- ==================== 更新操作（UPDATE） ====================

-- 10. 更新数据：修改宋江的身高
SELECT '=== 更新宋江的身高前 ===' as '';
SELECT * FROM students WHERE student_id = '2023001';

UPDATE students SET height = 179.0 WHERE student_id = '2023001';

SELECT '=== 更新宋江的身高后 ===' as '';
SELECT * FROM students WHERE student_id = '2023001';

-- 11. 批量更新：使用安全的方式
SELECT '=== 批量更新前 ===' as '';
SELECT * FROM students;

-- 临时禁用安全模式进行批量更新
SET SQL_SAFE_UPDATES = 0;
UPDATE students SET height = height + 2 WHERE name LIKE '%小%';
SET SQL_SAFE_UPDATES = 1;

SELECT '=== 批量更新后 ===' as '';
SELECT * FROM students;

-- 12. 更新名字：公孙胜改为樊瑞
UPDATE students SET name = '樊瑞' WHERE student_id = '2023004';

SELECT '=== 公孙胜改名为樊瑞后 ===' as '';
SELECT * FROM students WHERE student_id = '2023004';

-- ==================== 删除操作（DELETE） ====================

-- 13. 删除数据前的确认
SELECT '=== 要删除的学生 ===' as '';
SELECT * FROM students WHERE student_id = '2023005';

-- 14. 删除数据
DELETE FROM students WHERE student_id = '2023005';

-- 15. 验证删除结果
SELECT '=== 删除后的所有数据 ===' as '';
SELECT * FROM students;

-- 16. 删除身高低于165cm的学生
SELECT '=== 删除身高低于165cm的学生前 ===' as '';
SELECT * FROM students WHERE height < 165;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM students WHERE height < 165;
SET SQL_SAFE_UPDATES = 1;

SELECT '=== 删除身高低于165cm的学生后 ===' as '';
SELECT * FROM students;

-- ==================== 高级查询操作 ====================

-- 17. 分页查询（每页3条记录）
SELECT '=== 分页查询（每页3条）===' as '';
SELECT '第1页:' as '';
SELECT * FROM students ORDER BY id LIMIT 0, 3;

SELECT '第2页:' as '';
SELECT * FROM students ORDER BY id LIMIT 3, 3;

-- 18. 分组统计：按身高范围
SELECT '=== 按身高范围分组统计 ===' as '';
SELECT 
    CASE 
        WHEN height < 170 THEN '170cm以下'
        WHEN height BETWEEN 170 AND 180 THEN '170-180cm'
        ELSE '180cm以上'
    END as 身高范围,
    COUNT(*) as 人数,
    AVG(height) as 平均身高
FROM students
GROUP BY 
    CASE 
        WHEN height < 170 THEN '170cm以下'
        WHEN height BETWEEN 170 AND 180 THEN '170-180cm'
        ELSE '180cm以上'
    END
ORDER BY 平均身高 DESC;

-- 19. 复杂查询：找出最高的学生
SELECT '=== 最高的学生 ===' as '';
SELECT * FROM students 
WHERE height = (SELECT MAX(height) FROM students);

-- 20. 复杂查询：找出身高高于平均身高的学生
SELECT '=== 身高高于平均身高的学生 ===' as '';
SELECT * FROM students 
WHERE height > (SELECT AVG(height) FROM students)
ORDER BY height DESC;

-- 21. 最终数据状态
SELECT '=== 最终所有学生数据 ===' as '';
SELECT * FROM students;

-- 22. 表信息总结
SELECT '=== 表信息总结 ===' as '';
SELECT 
    COUNT(*) as 当前记录数,
    AVG(height) as 最终平均身高,
    MAX(height) as 最终最高身高,
    MIN(height) as 最终最矮身高
FROM students;
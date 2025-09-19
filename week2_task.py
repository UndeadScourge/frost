import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import ssl

# 跳过SSL验证
ssl._create_default_https_context = ssl._create_unverified_context

def get_baidu_hot():
    """获取百度热搜"""
    print("开始爬取百度热搜...")
    
    try:
        # 发送请求
        req = urllib.request.Request(
            "https://top.baidu.com/board?tab=realtime",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # 解析HTML
        soup = BeautifulSoup(html, 'html.parser')
        hot_items = soup.select('.category-wrap_iQLoo')[:10]
        
        hot_list = []
        for i, item in enumerate(hot_items, 1):
            title_elem = item.select_one('.c-single-text-ellipsis')
            hot_elem = item.select_one('.hot-index_1Bl1a')
            
            if title_elem and hot_elem:
                title = title_elem.get_text(strip=True)
                hot_index = hot_elem.get_text(strip=True).replace(',', '')
                hot_list.append((i, title, hot_index))
                print(f"{i}. {title} - {hot_index}")
        
        return hot_list
        
    except Exception as e:
        print(f"爬取出错: {e}")
        return []

def save_to_mysql(hot_list, password):
    """保存到MySQL"""
    if not hot_list:
        return
    
    try:
        # 先连接MySQL服务器（不指定数据库）
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )
        
        cursor = conn.cursor()
        
        # 创建数据库（如果不存在）
        cursor.execute("CREATE DATABASE IF NOT EXISTS hotsearch_db")
        cursor.execute("USE hotsearch_db")
        
        # 创建表（如果不存在）- 修复语法错误
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS baidu_hot (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hot_rank INT,
                title VARCHAR(255),
                hot_index VARCHAR(50),
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 插入数据
        for rank, title, hot_index in hot_list:
            cursor.execute(
                "INSERT INTO baidu_hot (hot_rank, title, hot_index) VALUES (%s, %s, %s)",
                (rank, title, hot_index)
            )
        
        conn.commit()
        print(f"\n成功保存 {len(hot_list)} 条数据到数据库")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"数据库错误: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("百度热搜爬虫")
    print("=" * 50)
    
    # 设置你的MySQL密码
    mysql_password = "tmnwsdlc"
    
    # 爬取数据
    hot_data = get_baidu_hot()
    
    if hot_data:
        # 保存到数据库
        save_to_mysql(hot_data, mysql_password)
    else:
        print("没有获取到数据")
    
    print("程序执行完毕！")
    input("按回车退出...")

if __name__ == "__main__":
    main()

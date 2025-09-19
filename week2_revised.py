import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import ssl
from typing import List, Tuple, Optional

class BaiduHotSearch:
    """百度热搜爬虫类"""
    
    def __init__(self):
        self.url = "https://top.baidu.com/board?tab=realtime"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        # 跳过SSL验证
        ssl._create_default_https_context = ssl._create_unverified_context
    
    def get_hot_list(self) -> List[Tuple[int, str, str]]:
        """获取百度热搜Top10"""
        print("开始爬取百度热搜...")
        
        try:
            # 发送请求
            req = urllib.request.Request(self.url, headers=self.headers)
            
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

class MySQLDatabase:
    """MySQL数据库操作类"""
    
    def __init__(self, host: str = 'localhost', user: str = 'root', 
                 password: str = 'tmnwsdlc', database: str = 'hotsearch_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """连接到MySQL服务器"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            return True
        except Exception as e:
            print(f"数据库连接错误: {e}")
            return False
    
    def create_database_and_table(self) -> bool:
        """创建数据库和表"""
        try:
            cursor = self.connection.cursor()
            # 创建数据库（如果不存在）
            cursor.execute("CREATE DATABASE IF NOT EXISTS hotsearch_db")
            cursor.execute("USE hotsearch_db")
            # 创建表（如果不存在）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS baidu_hot (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hot_rank INT,
                    title VARCHAR(255),
                    hot_index VARCHAR(50),
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.close()
            return True
        except Exception as e:
            print(f"创建数据库表错误: {e}")
            return False
    
    def save_hot_data(self, hot_list: List[Tuple[int, str, str]]) -> bool:
        """保存热搜数据到数据库"""
        if not hot_list:
            return False
        
        try:
            cursor = self.connection.cursor()
            # 插入数据
            for rank, title, hot_index in hot_list:
                cursor.execute(
                    "INSERT INTO baidu_hot (hot_rank, title, hot_index) VALUES (%s, %s, %s)",
                    (rank, title, hot_index)
                )
            
            self.connection.commit()
            print(f"\n成功保存 {len(hot_list)} 条数据到数据库")
            cursor.close()
            return True
            
        except Exception as e:
            print(f"数据保存错误: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()

class HotSearchApp:
    """热搜应用主类"""
    
    def __init__(self):
        self.spider = BaiduHotSearch()
        self.db = MySQLDatabase()
    
    def run(self):
        """运行应用程序"""
        self._print_header()
        
        # 爬取数据
        hot_data = self.spider.get_hot_list()
        
        if not hot_data:
            print("没有获取到数据")
            return
        
        # 连接数据库
        if not self.db.connect():
            return
        
        # 创建数据库和表
        if not self.db.create_database_and_table():
            self.db.close()
            return
        
        # 保存数据
        if self.db.save_hot_data(hot_data):
            print("数据保存成功！")
        else:
            print("数据保存失败")
        
        # 关闭连接
        self.db.close()
        print("程序执行完毕！")
    
    def _print_header(self):
        """打印程序标题"""
        print("=" * 50)
        print("百度热搜爬虫 - 面向对象版本")
        print("=" * 50)

def main():
    """程序入口函数"""
    app = HotSearchApp()
    app.run()
    input("按回车退出...")

if __name__ == "__main__":
    main()

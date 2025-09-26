# -*- coding: utf-8 -*-
"""
第三周任务：豆瓣电影Top100爬虫 + 数据库设计
"""

import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import re
import time
import ssl

# 跳过SSL验证
ssl._create_default_https_context = ssl._create_unverified_context

class DoubanMovieSpider:
    """豆瓣电影爬虫类"""
    
    def __init__(self):
        self.base_url = "https://movie.douban.com/top250"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    
    def get_html(self, url):
        """获取网页内容"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(req, timeout=10)
            return response.read().decode('utf-8')
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def crawl_top100(self):
        """爬取Top100电影"""
        print("开始爬取豆瓣电影Top100...")
        all_movies = []
        
        # 爬取4页，每页25部电影
        for page in range(4):
            start = page * 25
            url = f"{self.base_url}?start={start}"
            print(f"爬取第{page + 1}页...")
            
            html = self.get_html(url)
            if html:
                movies = self.parse_page(html)
                all_movies.extend(movies)
                print(f"本页获取 {len(movies)} 部电影")
            
            time.sleep(1)
        
        return all_movies[:100]
    
    def parse_page(self, html):
        """解析单页电影数据"""
        soup = BeautifulSoup(html, 'html.parser')
        movie_items = soup.select('.item')
        movies = []
        
        for item in movie_items:
            movie_data = self.parse_movie_item(item)
            if movie_data:
                movies.append(movie_data)
        
        return movies
    
    def parse_movie_item(self, item):
        """解析单个电影信息"""
        try:
            # 排名
            rank_elem = item.select_one('em')
            rank = int(rank_elem.get_text()) if rank_elem else 0
            
            # 标题
            title_elem = item.select_one('.title')
            title = title_elem.get_text(strip=True) if title_elem else "未知"
            
            # 评分
            rating_elem = item.select_one('.rating_num')
            rating = float(rating_elem.get_text()) if rating_elem else 0.0
            
            # 评价人数
            rating_count_elem = item.select_one('.star span:last-child')
            rating_count_text = rating_count_elem.get_text() if rating_count_elem else ""
            rating_count = self.extract_number(rating_count_text)
            
            # 其他信息
            info_elem = item.select_one('.bd p')
            info_text = info_elem.get_text() if info_elem else ""
            director, actors, year, country, movie_type = self.parse_movie_info(info_text)
            
            # 经典台词
            quote_elem = item.select_one('.quote')
            quote = quote_elem.get_text(strip=True) if quote_elem else ""
            
            # 链接
            link_elem = item.select_one('a')
            link = link_elem['href'] if link_elem else ""
            
            return {
                'rank': rank,
                'title': title,
                'rating': rating,
                'rating_count': rating_count,
                'director': director,
                'actors': actors,
                'year': year,
                'country': country,
                'movie_type': movie_type,
                'quote': quote,
                'link': link
            }
            
        except Exception as e:
            print(f"解析电影信息出错: {e}")
            return None
    
    def parse_movie_info(self, info_text):
        """解析电影详细信息"""
        director, actors, year, country, movie_type = "", "", 0, "", ""
        
        try:
            # 提取导演
            director_match = re.search(r'导演:\s*(.*?)\s*主演:', info_text)
            if director_match:
                director = director_match.group(1).strip()
            
            # 提取主演
            actors_match = re.search(r'主演:\s*(.*?)\s*\d', info_text)
            if actors_match:
                actors = actors_match.group(1).strip()
            
            # 提取年份等信息
            lines = info_text.split('\n')
            if len(lines) > 1:
                detail_line = lines[1].strip()
                parts = detail_line.split('/')
                if parts:
                    # 提取年份
                    year_match = re.search(r'(\d{4})', detail_line)
                    if year_match:
                        year = int(year_match.group(1))
                    
                    # 国家和类型
                    if len(parts) > 1:
                        country = parts[1].strip()
                    if len(parts) > 2:
                        movie_type = '/'.join(parts[2:]).strip()
                        
        except Exception as e:
            print(f"解析详情出错: {e}")
        
        return director, actors, year, country, movie_type
    
    def extract_number(self, text):
        """从文本提取数字"""
        numbers = re.findall(r'\d+', text.replace(',', ''))
        return int(numbers[0]) if numbers else 0

class MovieDatabase:
    """电影数据库类"""
    
    def __init__(self, password="tmnwsdlc"):
        self.host = "localhost"
        self.user = "root"
        self.password = password
        self.database = "douban_top100"
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            print("数据库连接成功")
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False
    
    def create_database(self):
        """创建数据库和表"""
        try:
            cursor = self.connection.cursor()
            
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # 创建电影表 - 使用movie_rank代替rank关键字
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_rank INT NOT NULL,
                title VARCHAR(200) NOT NULL,
                rating DECIMAL(3,1) NOT NULL,
                rating_count INT,
                release_year INT,
                country VARCHAR(100),
                movie_type VARCHAR(100),
                director VARCHAR(100),
                actors TEXT,
                quote TEXT,
                link VARCHAR(500),
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_sql)
            cursor.close()
            print("数据表创建成功")
            return True
            
        except Exception as e:
            print(f"创建数据库失败: {e}")
            return False
    
    def save_movies(self, movies):
        """保存电影数据"""
        if not movies:
            return False
        
        try:
            cursor = self.connection.cursor()
            
            # 清空旧数据
            cursor.execute("DELETE FROM movies")
            
            # 插入新数据 - 使用movie_rank字段
            insert_sql = """
            INSERT INTO movies (movie_rank, title, rating, rating_count, director, 
                              actors, release_year, country, movie_type, quote, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            count = 0
            for movie in movies:
                cursor.execute(insert_sql, (
                    movie['rank'], movie['title'], movie['rating'],
                    movie['rating_count'], movie['director'], movie['actors'],
                    movie['year'], movie['country'], movie['movie_type'],
                    movie['quote'], movie['link']
                ))
                count += 1
            
            self.connection.commit()
            cursor.close()
            print(f"成功保存 {count} 部电影数据")
            return True
            
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

class DoubanMovieApp:
    """豆瓣电影应用主类"""
    
    def __init__(self):
        self.spider = DoubanMovieSpider()
        self.db = MovieDatabase()
    
    def run(self):
        """运行应用程序"""
        print("=" * 60)
        print("第三周任务：豆瓣电影Top100爬虫")
        print("=" * 60)
        
        # 爬取数据
        print("1. 开始爬取电影数据...")
        movies = self.spider.crawl_top100()
        
        if not movies:
            print("爬取数据失败")
            return
        
        print(f"成功爬取 {len(movies)} 部电影")
        
        # 显示前5部电影信息
        print("\n前5部电影信息:")
        for movie in movies[:5]:
            print(f"  {movie['rank']:2d}. {movie['title']} - 评分: {movie['rating']}")
        
        # 保存到数据库
        print("\n2. 保存数据到数据库...")
        if not self.db.connect():
            return
        
        if not self.db.create_database():
            self.db.close()
            return
        
        if self.db.save_movies(movies):
            self.show_statistics(movies)
            print("\n第三周任务完成！")
        else:
            print("数据保存失败")
        
        self.db.close()
    
    def show_statistics(self, movies):
        """显示数据统计"""
        print("\n数据统计信息:")
        print(f"总电影数: {len(movies)}部")
        
        # 评分统计
        ratings = [m['rating'] for m in movies]
        print(f"平均评分: {sum(ratings)/len(ratings):.2f}")
        print(f"最高评分: {max(ratings)}")
        print(f"最低评分: {min(ratings)}")
        
        # 年份分布
        years = [m['year'] for m in movies if m['year'] > 0]
        if years:
            print(f"年份范围: {min(years)}年 - {max(years)}年")
        
        # 类型统计
        types = {}
        for movie in movies:
            if movie['movie_type']:
                if '/' in movie['movie_type']:
                    for t in movie['movie_type'].split('/'):
                        t = t.strip()
                        types[t] = types.get(t, 0) + 1
                else:
                    types[movie['movie_type']] = types.get(movie['movie_type'], 0) + 1
        
        if types:
            top_types = sorted(types.items(), key=lambda x: x[1], reverse=True)[:3]
            print("主要类型:", ", ".join([f"{t}({c}部)" for t, c in top_types]))

def main():
    """程序入口"""
    app = DoubanMovieApp()
    app.run()
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()

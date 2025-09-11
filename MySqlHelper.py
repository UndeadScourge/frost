import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Any, Optional, Dict, Union

class MySqlHelper:
    """
    MySQL数据库操作辅助类
    封装常用的数据库操作，简化MySQL交互
    """
    
    def __init__(self, host: str = 'localhost', 
                 database: str = None,
                 user: str = 'root', 
                 password: str = None,
                 port: int = 3306,
                 autocommit: bool = True):
        """
        初始化数据库连接参数
        
        Args:
            host: 数据库主机地址
            database: 数据库名称
            user: 用户名
            password: 密码
            port: 端口号
            autocommit: 是否自动提交事务
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.autocommit = autocommit
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        连接到MySQL数据库
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                autocommit=self.autocommit
            )
            
            if self.connection.is_connected():
                print(f"成功连接到MySQL数据库: {self.database}")
                self.cursor = self.connection.cursor(dictionary=True)  # 返回字典格式的结果
                return True
                
        except Error as e:
            print(f"数据库连接错误: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("MySQL连接已关闭")
    
    def execute_query(self, query: str, params: Tuple = None) -> Optional[int]:
        """
        执行SQL查询（INSERT, UPDATE, DELETE）
        
        Args:
            query: SQL语句
            params: 参数元组
            
        Returns:
            int: 受影响的行数，失败返回None
        """
        try:
            self.cursor.execute(query, params or ())
            if not self.autocommit:
                self.connection.commit()
            return self.cursor.rowcount
            
        except Error as e:
            print(f"执行查询错误: {e}")
            if not self.autocommit:
                self.connection.rollback()
            return None
    
    def fetch_all(self, query: str, params: Tuple = None) -> Optional[List[Dict]]:
        """
        执行查询并返回所有结果
        
        Args:
            query: SQL查询语句
            params: 参数元组
            
        Returns:
            List[Dict]: 查询结果列表，失败返回None
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"查询错误: {e}")
            return None
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Dict]:
        """
        执行查询并返回单条结果
        
        Args:
            query: SQL查询语句
            params: 参数元组
            
        Returns:
            Dict: 单条查询结果，失败返回None
        """
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"查询错误: {e}")
            return None
    
    def insert(self, table: str, data: Dict) -> Optional[int]:
        """
        插入单条数据
        
        Args:
            table: 表名
            data: 数据字典 {字段名: 值}
            
        Returns:
            int: 插入的行ID，失败返回None
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, tuple(data.values()))
            if not self.autocommit:
                self.connection.commit()
            
            return self.cursor.lastrowid
            
        except Error as e:
            print(f"插入数据错误: {e}")
            if not self.autocommit:
                self.connection.rollback()
            return None
    
    def insert_many(self, table: str, data_list: List[Dict]) -> Optional[int]:
        """
        批量插入数据
        
        Args:
            table: 表名
            data_list: 数据字典列表
            
        Returns:
            int: 受影响的行数，失败返回None
        """
        if not data_list:
            return 0
            
        try:
            columns = ', '.join(data_list[0].keys())
            placeholders = ', '.join(['%s'] * len(data_list[0]))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            values = [tuple(data.values()) for data in data_list]
            self.cursor.executemany(query, values)
            
            if not self.autocommit:
                self.connection.commit()
                
            return self.cursor.rowcount
            
        except Error as e:
            print(f"批量插入错误: {e}")
            if not self.autocommit:
                self.connection.rollback()
            return None
    
    def update(self, table: str, data: Dict, condition: str, condition_params: Tuple = None) -> Optional[int]:
        """
        更新数据
        
        Args:
            table: 表名
            data: 要更新的数据 {字段名: 新值}
            condition: WHERE条件
            condition_params: 条件参数
            
        Returns:
            int: 受影响的行数，失败返回None
        """
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            
            params = tuple(data.values()) + (condition_params or ())
            self.cursor.execute(query, params)
            
            if not self.autocommit:
                self.connection.commit()
                
            return self.cursor.rowcount
            
        except Error as e:
            print(f"更新数据错误: {e}")
            if not self.autocommit:
                self.connection.rollback()
            return None
    
    def delete(self, table: str, condition: str, params: Tuple = None) -> Optional[int]:
        """
        删除数据
        
        Args:
            table: 表名
            condition: WHERE条件
            params: 条件参数
            
        Returns:
            int: 受影响的行数，失败返回None
        """
        try:
            query = f"DELETE FROM {table} WHERE {condition}"
            self.cursor.execute(query, params or ())
            
            if not self.autocommit:
                self.connection.commit()
                
            return self.cursor.rowcount
            
        except Error as e:
            print(f"删除数据错误: {e}")
            if not self.autocommit:
                self.connection.rollback()
            return None
    
    def begin_transaction(self):
        """开始事务"""
        self.connection.autocommit = False
    
    def commit(self):
        """提交事务"""
        self.connection.commit()
        self.connection.autocommit = True
    
    def rollback(self):
        """回滚事务"""
        self.connection.rollback()
        self.connection.autocommit = True
    
    def get_table_list(self) -> Optional[List[str]]:
        """获取所有表名"""
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            return [table[f'Tables_in_{self.database}'] for table in tables]
        except Error as e:
            print(f"获取表列表错误: {e}")
            return None
    
    def get_table_schema(self, table: str) -> Optional[List[Dict]]:
        """获取表结构"""
        try:
            self.cursor.execute(f"DESCRIBE {table}")
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取表结构错误: {e}")
            return None

    # 使用上下文管理器，支持with语句
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

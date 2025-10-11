import React, { useState } from 'react';
import { Layout, Menu, theme, ConfigProvider } from 'antd';
import {
    PieChartOutlined,
    BarChartOutlined,
    LineChartOutlined,
    UserOutlined,
    DashboardOutlined,
} from '@ant-design/icons';
import SalesChart from './components/SalesChart';
import ProductRanking from './components/ProductRanking';
import UserBehavior from './components/UserBehavior';
import SalesTrend from './components/SalesTrend';
import './App.css';

const { Header, Sider, Content } = Layout;

const App = () => {
    const [collapsed, setCollapsed] = useState(false);
    const [selectedMenu, setSelectedMenu] = useState('1');
    
    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();

    const menuItems = [
        {
            key: '1',
            icon: <BarChartOutlined />,
            label: 'Sales Analysis',
        },
        {
            key: '2',
            icon: <DashboardOutlined />,
            label: 'Product Ranking',
        },
        {
            key: '3',
            icon: <UserOutlined />,
            label: 'User Behavior',
        },
        {
            key: '4',
            icon: <LineChartOutlined />,
            label: 'Sales Trend',
        },
    ];

    const renderContent = () => {
        switch (selectedMenu) {
            case '1':
                return <SalesChart />;
            case '2':
                return <ProductRanking />;
            case '3':
                return <UserBehavior />;
            case '4':
                return <SalesTrend />;
            default:
                return <SalesChart />;
        }
    };

    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#1890ff',
                },
            }}
        >
            <Layout style={{ minHeight: '100vh' }}>
                <Sider 
                    collapsible 
                    collapsed={collapsed} 
                    onCollapse={(value) => setCollapsed(value)}
                    theme="dark"
                >
                    <div className="app-logo">
                        {collapsed ? 'DV' : 'Data Visualization'}
                    </div>
                    <Menu
                        theme="dark"
                        defaultSelectedKeys={['1']}
                        mode="inline"
                        items={menuItems}
                        onClick={({ key }) => setSelectedMenu(key)}
                    />
                </Sider>
                <Layout>
                    <Header
                        style={{
                            padding: '0 24px',
                            background: colorBgContainer,
                            boxShadow: '0 1px 4px rgba(0,21,41,0.08)',
                        }}
                    >
                        <h1 style={{ 
                            margin: 0, 
                            fontSize: '20px',
                            fontWeight: '600',
                            color: '#1890ff'
                        }}>
                            Business Analytics Dashboard
                        </h1>
                    </Header>
                    <Content
                        style={{
                            margin: '24px 16px',
                            padding: 24,
                            minHeight: 280,
                            background: colorBgContainer,
                            borderRadius: borderRadiusLG,
                        }}
                    >
                        {renderContent()}
                    </Content>
                </Layout>
            </Layout>
        </ConfigProvider>
    );
};

export default App;
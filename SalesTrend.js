import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Alert, Button, Row, Col, Statistic } from 'antd';
import { ReloadOutlined, RiseOutlined, ShoppingOutlined } from '@ant-design/icons';
import axios from 'axios';

const SalesTrend = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSalesTrend = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get('http://localhost:5000/api/sales-trend');
            setChartData(response.data);
        } catch (err) {
            setError('Failed to fetch sales trend data');
            console.error('Error fetching sales trend:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSalesTrend();
    }, []);

    const getOption = () => {
        if (!chartData) return {};

        return {
            title: {
                text: 'Sales Trend Analysis',
                left: 'center',
                textStyle: {
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['Daily Sales', 'Daily Orders'],
                top: '10%'
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                top: '20%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: chartData.dates,
                axisLabel: {
                    formatter: function(value) {
                        return value.split('-').slice(1).join('/');
                    }
                }
            },
            yAxis: [
                {
                    type: 'value',
                    name: 'Sales Amount ($)',
                    position: 'left',
                    axisLabel: {
                        formatter: '${value}'
                    }
                },
                {
                    type: 'value',
                    name: 'Order Count',
                    position: 'right'
                }
            ],
            series: [
                {
                    name: 'Daily Sales',
                    type: 'line',
                    data: chartData.sales,
                    smooth: true,
                    itemStyle: {
                        color: '#ee6666'
                    },
                    lineStyle: {
                        width: 3
                    },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0,
                            y: 0,
                            x2: 0,
                            y2: 1,
                            colorStops: [{
                                offset: 0, color: 'rgba(238, 102, 102, 0.6)'
                            }, {
                                offset: 1, color: 'rgba(238, 102, 102, 0.1)'
                            }]
                        }
                    },
                    yAxisIndex: 0
                },
                {
                    name: 'Daily Orders',
                    type: 'bar',
                    data: chartData.orders,
                    itemStyle: {
                        color: '#5470c6',
                        opacity: 0.7
                    },
                    yAxisIndex: 1
                }
            ]
        };
    };

    const totalSales = chartData ? 
        chartData.sales.reduce((sum, sales) => sum + sales, 0) : 0;
    const totalOrders = chartData ? 
        chartData.orders.reduce((sum, orders) => sum + orders, 0) : 0;

    if (loading) {
        return (
            <Card title="Sales Trend Analysis">
                <div style={{ textAlign: 'center', padding: '50px' }}>
                    <Spin size="large" />
                    <div style={{ marginTop: '16px' }}>Loading sales trend data...</div>
                </div>
            </Card>
        );
    }

    if (error) {
        return (
            <Card 
                title="Sales Trend Analysis"
                extra={
                    <Button 
                        icon={<ReloadOutlined />} 
                        onClick={fetchSalesTrend}
                    >
                        Retry
                    </Button>
                }
            >
                <Alert message={error} type="error" showIcon />
            </Card>
        );
    }

    return (
        <Card 
            title="Sales Trend Analysis"
            extra={
                <Button 
                    icon={<ReloadOutlined />} 
                    onClick={fetchSalesTrend}
                    loading={loading}
                >
                    Refresh
                </Button>
            }
            bordered={false}
        >
            <Row gutter={16} style={{ marginBottom: 24 }}>
                <Col span={8}>
                    <Statistic
                        title="Total Sales"
                        value={totalSales}
                        precision={2}
                        prefix="$"
                        valueStyle={{ color: '#3f8600' }}
                        prefix={<RiseOutlined />}
                    />
                </Col>
                <Col span={8}>
                    <Statistic
                        title="Total Orders"
                        value={totalOrders}
                        prefix={<ShoppingOutlined />}
                    />
                </Col>
                <Col span={8}>
                    <Statistic
                        title="Tracking Days"
                        value={chartData.dates.length}
                    />
                </Col>
            </Row>
            <ReactECharts 
                option={getOption()} 
                style={{ height: 500 }}
                opts={{ renderer: 'svg' }}
            />
        </Card>
    );
};

export default SalesTrend;
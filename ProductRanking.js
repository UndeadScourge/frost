import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Alert, Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const ProductRanking = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchProductRanking = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get('http://localhost:5000/api/product-ranking');
            setChartData(response.data);
        } catch (err) {
            setError('Failed to fetch product ranking data');
            console.error('Error fetching product ranking:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProductRanking();
    }, []);

    const getOption = () => {
        if (!chartData) return {};

        return {
            title: {
                text: 'Top 10 Products by Sales',
                left: 'center',
                textStyle: {
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: function (params) {
                    const data = params[0];
                    return `
                        ${data.name}<br/>
                        Sales: $${data.value.toLocaleString()}<br/>
                        Orders: ${chartData.counts[data.dataIndex]}
                    `;
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                name: 'Sales Amount ($)',
                axisLabel: {
                    formatter: '${value}'
                }
            },
            yAxis: {
                type: 'category',
                data: chartData.products,
                inverse: true
            },
            series: [
                {
                    name: 'Sales',
                    type: 'bar',
                    data: chartData.sales,
                    itemStyle: {
                        color: function(params) {
                            const colorList = [
                                '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
                                '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#c23531'
                            ];
                            return colorList[params.dataIndex];
                        }
                    },
                    label: {
                        show: true,
                        position: 'right',
                        formatter: '${c}'
                    }
                }
            ]
        };
    };

    if (loading) {
        return (
            <Card title="Product Ranking">
                <div style={{ textAlign: 'center', padding: '50px' }}>
                    <Spin size="large" />
                    <div style={{ marginTop: '16px' }}>Loading product ranking...</div>
                </div>
            </Card>
        );
    }

    if (error) {
        return (
            <Card 
                title="Product Ranking"
                extra={
                    <Button 
                        icon={<ReloadOutlined />} 
                        onClick={fetchProductRanking}
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
            title="Top Products Sales Ranking"
            extra={
                <Button 
                    icon={<ReloadOutlined />} 
                    onClick={fetchProductRanking}
                    loading={loading}
                >
                    Refresh
                </Button>
            }
            bordered={false}
        >
            <ReactECharts 
                option={getOption()} 
                style={{ height: 500 }}
                opts={{ renderer: 'svg' }}
            />
        </Card>
    );
};

export default ProductRanking;
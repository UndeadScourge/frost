import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Alert, Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const SalesChart = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSalesData = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get('http://localhost:5000/api/sales-data');
            setChartData(response.data);
        } catch (err) {
            setError('Failed to fetch sales data');
            console.error('Error fetching sales data:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSalesData();
    }, []);

    const getOption = () => {
        if (!chartData) return {};

        return {
            title: {
                text: 'Sales Analysis by Category and Region',
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
                    let result = `${params[0].axisValue}<br/>`;
                    params.forEach(param => {
                        result += `${param.seriesName}: $${param.value.toLocaleString()}<br/>`;
                    });
                    return result;
                }
            },
            legend: {
                data: chartData.categories,
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
                data: chartData.regions
            },
            yAxis: {
                type: 'value',
                name: 'Sales Amount ($)',
                axisLabel: {
                    formatter: '${value}'
                }
            },
            series: chartData.series.map(series => ({
                ...series,
                itemStyle: {
                    borderRadius: [2, 2, 0, 0]
                }
            }))
        };
    };

    if (loading) {
        return (
            <Card title="Sales Analysis">
                <div style={{ textAlign: 'center', padding: '50px' }}>
                    <Spin size="large" />
                    <div style={{ marginTop: '16px' }}>Loading sales data...</div>
                </div>
            </Card>
        );
    }

    if (error) {
        return (
            <Card 
                title="Sales Analysis"
                extra={
                    <Button 
                        icon={<ReloadOutlined />} 
                        onClick={fetchSalesData}
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
            title="Sales Analysis by Category and Region"
            extra={
                <Button 
                    icon={<ReloadOutlined />} 
                    onClick={fetchSalesData}
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

export default SalesChart;
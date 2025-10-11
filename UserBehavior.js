import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Alert, Button, Row, Col, Statistic } from 'antd';
import { ReloadOutlined, UserOutlined, ClockCircleOutlined } from '@ant-design/icons';
import axios from 'axios';

const UserBehavior = () => {
    const [chartData, setChartData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchUserBehavior = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await axios.get('http://localhost:5000/api/user-behavior');
            setChartData(response.data);
        } catch (err) {
            setError('Failed to fetch user behavior data');
            console.error('Error fetching user behavior:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUserBehavior();
    }, []);

    const getOption = () => {
        if (!chartData) return {};

        return {
            title: {
                text: 'User Behavior Analytics',
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
                data: ['Action Count', 'Average Duration (seconds)'],
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
                data: chartData.actions
            },
            yAxis: [
                {
                    type: 'value',
                    name: 'Action Count',
                    position: 'left'
                },
                {
                    type: 'value',
                    name: 'Duration (seconds)',
                    position: 'right'
                }
            ],
            series: [
                {
                    name: 'Action Count',
                    type: 'bar',
                    data: chartData.counts,
                    itemStyle: {
                        color: '#5470c6'
                    },
                    label: {
                        show: true,
                        position: 'top'
                    }
                },
                {
                    name: 'Average Duration (seconds)',
                    type: 'line',
                    yAxisIndex: 1,
                    data: chartData.durations,
                    itemStyle: {
                        color: '#91cc75'
                    },
                    lineStyle: {
                        width: 3
                    }
                }
            ]
        };
    };

    const totalActions = chartData ? chartData.counts.reduce((sum, count) => sum + count, 0) : 0;
    const averageDuration = chartData ? 
        Math.round(chartData.durations.reduce((sum, duration) => sum + duration, 0) / chartData.durations.length) : 0;

    if (loading) {
        return (
            <Card title="User Behavior Analytics">
                <div style={{ textAlign: 'center', padding: '50px' }}>
                    <Spin size="large" />
                    <div style={{ marginTop: '16px' }}>Loading user behavior data...</div>
                </div>
            </Card>
        );
    }

    if (error) {
        return (
            <Card 
                title="User Behavior Analytics"
                extra={
                    <Button 
                        icon={<ReloadOutlined />} 
                        onClick={fetchUserBehavior}
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
            title="User Behavior Analytics"
            extra={
                <Button 
                    icon={<ReloadOutlined />} 
                    onClick={fetchUserBehavior}
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
                        title="Total Actions"
                        value={totalActions}
                        prefix={<UserOutlined />}
                    />
                </Col>
                <Col span={8}>
                    <Statistic
                        title="Average Duration"
                        value={averageDuration}
                        suffix="seconds"
                        prefix={<ClockCircleOutlined />}
                    />
                </Col>
                <Col span={8}>
                    <Statistic
                        title="Action Types"
                        value={chartData.actions.length}
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

export default UserBehavior;
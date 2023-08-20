<script>
import { onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
    name: 'HeatmapChart',
    props: {
        hours: Array,
        days: Array,
        chartData: Array
    },
    data() {
        return {
            chartDataCopy: []
        };
    },
    mounted() {
        const chartDom = document.getElementById('chart');
        const myChart = echarts.init(chartDom);

        this.chartDataCopy = [...this.chartData];

        const option = {
            tooltip: {
                position: 'top'
            },
            grid: {
                height: '50%',
                top: '10%'
            },
            xAxis: {
                type: 'category',
                data: this.hours,
                splitArea: {
                    show: true
                }
            },
            yAxis: {
                type: 'category',
                data: this.days,
                splitArea: {
                    show: true
                }
            },
            visualMap: {
                min: 0,
                max: 10,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '15%'
            },
            series: [
                {
                    name: 'Punch Card',
                    type: 'heatmap',
                    data: this.chartDataCopy,
                    label: {
                        show: true
                    },
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    },
    watch: {
        chartData(newChartData) {
            this.chartDataCopy = [...newChartData];
        }
    }
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
<template>
    <div id="chart"></div>
    <!-- <div style="color:blue">点击下载预测结果文件</div> -->
</template>
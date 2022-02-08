import * as echarts from 'echarts';
import { useEffect, useState } from 'react';
import { Card, Row, Col } from 'antd'
import { getClusterList } from '@/services';
import { history } from 'umi';
import ArticalTable from './component/ArticalTable';
import './index.less';

const Detail = () => {
  const [list, setList] = useState([]);
  useEffect(() => {
    // 基于准备好的dom，初始化echarts实例
    const bar = echarts.init(document.getElementById('bar'));
    const pie = echarts.init(document.getElementById('pie'));
    const { id } = history.location.query;
    getClusterList({ id }).then(data => {
      console.log(data);
      setList(data.map(v => v.cluster_class));
      // 绘制图表 柱状图
      bar.setOption({
        title: {
          text: '文章分布'
        },
        tooltip: {
          formatter:function(params){
            console.log(params)
            const keyword = data[params.dataIndex].keyword_list.join(",")
            return `
              <div>class:${params.name};</div>
              <div>value:${params.value};</div>
              <p style="word-wrap: break-word;
              white-space: normal;
              word-break: break-all;">keyword:${keyword}</p>
            `
          },
          extraCssText:'width:300px;'
        },
        xAxis: {
          data: data.map(v => v.cluster_class)
        },
        yAxis: {},
        series: [
          {
            type: 'bar',
            data: data.map(v => v.count)
          }
        ]
      });
      // 绘制图表 柱状图
      pie.setOption({
        title: {
          text: '文章分布'
        },
        tooltip: {},
        legend: {
          orient: 'vertical',
          left: 'right'
        },
        series: [
          {
            type: 'pie',
            radius: '70%',
            data: data.map(v => ({
              value: v.count, name: v.cluster_class
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      });
    }).catch(err => console.log(err));

  }, [])

  return (
    <>
      <Row gutter={16}>
        <Col span={12}>
          <Card title="柱状图" style={{ width: "100%" }}>
            <div id="bar" className='detail'></div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="饼图" style={{ width: "100%" }}>
            <div id="pie" className='detail'></div>
          </Card>
        </Col>
      </Row>
      <Row gutter={16} style={{marginTop:"20px"}}>
        <Col span={24}>
          <Card title="文章列表" style={{ width: "100%" }}>
            <ArticalTable list={list} ></ArticalTable>
          </Card>
        </Col>
      </Row>
    </>

  )
}

export default Detail;

import * as echarts from 'echarts';
import { useEffect, useState } from 'react';
import { Card, Row, Col, Form, Select, Tag } from 'antd'
import { getClusterList } from '@/services';
import { history } from 'umi';
const { Option } = Select;
import ArticalTable from './component/ArticalTable';
import KeyWordList from './component/KeyWordList';
import Sankey from './component/Sankey';
import './index.less';
const { id } = history.location.query;


const Detail = () => {
  const [list, setList] = useState([]);
  const [years, setYears] = useState([]);
  const [curYear, setCurYear] = useState('');
  const [keyWordList, setKeyWordList] = useState([]);
  const [allData, setAllData] = useState();

  const [form] = Form.useForm();

  const composeData = (yearData) => {
    // 设置文章列表数据
    setList(yearData.data.map(v => v.cluster_class));
    // 设置关键词列表
    setKeyWordList(yearData.data.map(v => {
      return {
        class: v.cluster_class,
        keyWordList: v.keyword_list
      }
    }))
    const bar = echarts.init(document.getElementById('bar'));
    // 绘制图表 柱状图
    bar.setOption({
      title: {
        text: '文章分布'
      },
      tooltip: {
        formatter: function (params) {
          const keyword = yearData.data[params.dataIndex].keyword_list.join(",")
          return `
        <div>class:${params.name};</div>
        <div>value:${params.value};</div>
        <p style="word-wrap: break-word;
        white-space: normal;
        word-break: break-all;">keyword:${keyword}</p>
      `
        },
        extraCssText: 'width:300px;'
      },
      xAxis: {
        data: yearData.data.map(v => v.cluster_class)
      },
      yAxis: {},
      series: [
        {
          type: 'bar',
          data: yearData.data.map(v => v.count)
        }
      ]
    });
  }

  const onFormChange = ({ year }) => {
    setCurYear(year);
    const yearData = allData.find(v => v.year === year);
    composeData(yearData)
  };

  useEffect(() => {

    getClusterList({ id }).then(data => {
      //缓存所有数据
      setAllData(data)
      //设置所有年份列表
      setYears(data.map(v => v.year));
      //取出最近一年数据
      const lastYearData = data.at(-1);
      //设置年份筛选
      setCurYear(lastYearData.year)
      form.setFieldsValue({
        year: lastYearData.year
      })
      composeData(lastYearData)
    }).catch(err => console.log(err));

  }, [])

  return (
    <>
      <Row gutter={16} style={{ marginBottom: "20px" }}>
        <Col span={24}>
          <Card title="类别总览" style={{ width: "100%" }}>
            <Sankey ></Sankey>
          </Card>
        </Col>
      </Row>
      <Row gutter={16}>
        <Form
          layout="inline"
          form={form}
          onValuesChange={onFormChange}
          style={{ marginBottom: "20px" }}
        >
          <Form.Item label="年份：" name="year">
            <Select style={{ width: 120 }}>
              {years.length && years.map(v => (
                <Option value={v}>{v}</Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Row>
      <Row gutter={16} style={{ marginBottom: "20px" }}>
        <Col span={24}>
          <Card title="关键词列表" style={{ width: "100%" }}>
            <KeyWordList list={keyWordList} />
          </Card>
        </Col>
      </Row>
      <Row gutter={16}>
        <Col span={24}>
          <Card title="柱状图" style={{ width: "100%" }}>
            <div id="bar" className='detail'></div>
          </Card>
        </Col>
      </Row>
      <Row gutter={16} style={{ marginTop: "20px" }}>
        <Col span={24}>
          <Card title="词云图 & 文章列表" style={{ width: "100%" }}>
            <ArticalTable list={list} year={curYear}></ArticalTable>
          </Card>
        </Col>
      </Row>
    </>

  )
}

export default Detail;

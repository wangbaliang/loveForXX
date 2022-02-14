import { Table, Form, Select, Tag } from 'antd'
import { useEffect, useState } from 'react';
import { getClusterPaperList, url } from '@/services';
import { history } from 'umi';
const { Option } = Select;
const { id } = history.location.query;

const ArticalList = (props) => {
  const { list, year } = props;
  const [data, setData] = useState([]);
  const [clusterClass, setClusterClass] = useState();
  const [cloudChartUrl, setCloudChartUrl] = useState('');
  const [form] = Form.useForm();

  const columns = [
    {
      title: 'wos_doc_id',
      dataIndex: 'wos_doc_id',
      key: 'wos_doc_id',
      align: 'center'
    },
    {
      title: 'title',
      dataIndex: 'title',
      key: 'title',
      align: 'center'
    },
    {
      title: 'year',
      key: 'year',
      dataIndex: 'year',
      align: 'center',
    },
    {
      title: 'keyword',
      dataIndex: 'keyword',
      key: 'keyword',
      render: keyword => (
        <>
          {keyword.map(keyword => {
            let color = keyword.length > 5 ? 'geekblue' : 'green';
            return (
              <Tag color={color} key={keyword}>
                {keyword}
              </Tag>
            );
          })}
        </>
      ),
      align: 'center',
    },
    {
      title: 'abstract',
      key: 'abstract',
      dataIndex: 'abstract',
      align: 'center',
    }
  ];

  useEffect(() => {
    if (typeof (clusterClass) !== "undefined") {
      getClusterPaperList({ id, cluster_class: clusterClass, year }).then(data => {
        setData(data)
      }).catch(err => console.log(err))
      setCloudChartUrl(`${url}/keyword?id=${id}&year=${year}&cluster_class=${clusterClass}`)
    }
  }, [clusterClass, year])

  useEffect(() => {
    form.setFieldsValue({
      clusterClass: list[0]
    })
    setClusterClass(list[0]);
    if (year && list[0] && id) {
      setCloudChartUrl(`${url}/keyword?id=${id}&year=${year}&cluster_class=${list[0]}`)
    }
  }, [list, year])

  const onFormChange = ({ clusterClass }) => {
    setClusterClass(clusterClass);
  };

  return (
    <>
      <Form
        layout="inline"
        form={form}
        onValuesChange={onFormChange}
        style={{ marginBottom: "20px" }}
      >
        <Form.Item label="类别选择：" name="clusterClass">
          <Select style={{ width: 120 }}>
            {list.length && list.map(v => (
              <Option value={v}>{v}</Option>
            ))}
          </Select>
        </Form.Item>
      </Form>
      {
        cloudChartUrl && <iframe src={cloudChartUrl} frameborder="0" style={{ width: '100%', height: '400px' }}></iframe>
      }
      <Table columns={columns} dataSource={data} bordered rowKey="wos_doc_id" />
    </>
  )
}

export default ArticalList;

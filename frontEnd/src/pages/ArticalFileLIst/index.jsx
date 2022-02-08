import { Table, Space, Upload, message, Button } from 'antd'
import {
  CloseCircleOutlined,
  CheckCircleOutlined,
  LoadingOutlined,
  UploadOutlined
} from '@ant-design/icons';
import { useEffect, useState } from 'react';
import { getFileList, url } from '@/services';
import { history } from 'umi';

const ArticalFileList = () => {

  const [data, setData] = useState([]);

  const handleToDetail = (id) => {
    history.push(`/detail?id=${id}`);
  }

  const columns = [
    {
      title: 'id',
      dataIndex: 'id',
      key: 'id',
      align: 'center'
    },
    {
      title: 'status',
      dataIndex: 'status',
      key: 'status',
      align: 'center',
      render: (status) => {
        const res = {
          "-1": <CloseCircleOutlined style={{ color: "red" }} />,
          "0": <LoadingOutlined spin />,
          "1": <CheckCircleOutlined style={{ color: "green" }} />
        }
        return res[status];
      }
    },
    {
      title: 'upload_path',
      key: 'upload_path',
      dataIndex: 'upload_path',
      align: 'center',
    },
    {
      title: 'message',
      dataIndex: 'message',
      key: 'message',
      align: 'center',
    },
    {
      title: 'created_at',
      key: 'created_at',
      dataIndex: 'created_at',
      align: 'center',
    },
    {
      title: 'updated_at',
      key: 'updated_at',
      dataIndex: 'created_at',
      align: 'center',
    },
    {
      title: 'user_name',
      key: 'user_name',
      dataIndex: 'user_name',
      align: 'center',
    },
    {
      title: 'action',
      key: 'action',
      align: 'center',
      render: (text, record) => (
        <Space size="middle">
          <a onClick={() => handleToDetail(record.id)}>details</a>
        </Space>
      ),
    },
  ];

  useEffect(() => {
    getFileList().then(data => {
      setData(data)
    }).catch(err => console.log(err))
  }, [])

  const props = {
    name: 'file',
    action: `${url}/upload`,
    maxCount:1,
    showUploadList: false,
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        message.success(`${info.file.name}上传成功`);
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name}上传失败`);
      }
    },
  };

  return (
    <>
      <div style={{marginBottom:"20px", display:'flex', justifyContent: 'flex-end'}}>
        <Upload {...props} >
          <Button icon={<UploadOutlined />} type='primary'>上传文件包</Button>
        </Upload>
      </div>
      <Table columns={columns} dataSource={data} bordered rowKey="id" />
    </>

  )
}

export default ArticalFileList;

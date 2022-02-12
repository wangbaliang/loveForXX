import { List, Tag } from 'antd';

export default (props) => {
  const { list } = props;
  return (
    <List
      itemLayout="horizontal"
      dataSource={list}
      renderItem={item => (
        <List.Item>
          <List.Item.Meta
            title={<a>类别：{item.class}</a>}
            description={<>{
              item.keyWordList.length && item.keyWordList.map(v => (
                <Tag key={v}>
                  {v}
                </Tag>
              ))
            }</>}
          />
        </List.Item>
      )}
    />
  )
}

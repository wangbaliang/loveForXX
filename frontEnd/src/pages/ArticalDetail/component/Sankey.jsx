import { useEffect, useState } from 'react';
import { url } from '@/services';
import { history } from 'umi';

const ArticalList = (props) => {
  const [sankeyUrl, setSankeyUrl] = useState('');

  useEffect(() => {
    const { id } = history.location.query;
    setSankeyUrl(`${url}/sankey?id=${id}`)
  }, [])

  return (
    <>
      {
        sankeyUrl && <iframe src={sankeyUrl} frameborder="0" style={{ width: '1000px', height: '550px' }}></iframe>
      }
    </>
  )
}

export default ArticalList;

import { notification } from 'antd';
import {
  request
} from 'umi';

export const url = "http://101.201.199.130:5000";

const myRequest = (url, options) => {
  return new Promise((resolve, reject) => {
    request(url, options).then(res => {
      const {error_code, message, result} = res;
      if(error_code !== 0){
        notification.error({
          message:"ERROR",
          description:message,
        });
        reject(message);
      }else {
        resolve(result);
      }
    }).catch(err => reject(err));
  })
}
/** 获取文件包列表 */

export async function getFileList() {
  return myRequest(`${url}/fileList`, {
    method: 'GET',
  });
}

/** 根据文件包id获取聚类分布结果 */

// http: //101.201.199.130:5000/clusterList?id=3

export async function getClusterList(params) {
  return myRequest(`${url}/clusterList`, {
    method: 'GET',
    params,
  });
}

/** 根据文件包id和聚类的类别获取该类别的文章列表 */

// http: //101.201.199.130:5000/clusterPaperList?id=3&cluster_class=1

export async function getClusterPaperList(params) {
  return myRequest(`${url}/clusterPaperList`, {
    method: 'GET',
    params,
  });
}

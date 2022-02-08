export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './user/Login',
          },
        ],
      },
      {
        component: './404',
      },
    ],
  },
  {
    name: '文件包列表',
    icon: 'folder',
    path: '/list',
    component: './ArticalFileList',
  },
  {
    name: '文件包详情',
    path: '/detail',
    component: './ArticalDetail',
    hideInMenu:true,
  },
  {
    path: '/',
    redirect: '/list',
  },
  {
    component: './404',
  },
];

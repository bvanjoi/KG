import {
    //mainRoutes
    NotFound,

    //contentRoutes
    Introduce,
    Knowledge,
    Robot
} from '../views';



export const mainRoutes = [{
    pathname: '/404',
    title:'找不到页面',
    component: NotFound
}]

export const contentRoutes = [{
    pathname: '/introduce',
    title:'首页',
    component: Introduce
},{
    pathname: '/knowledge',
    title:'知识图谱',
    component: Knowledge
},{
    pathname: '/robot',
    title:'问答机器人',
    component: Robot
}]
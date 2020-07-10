import axios from 'axios';

const service = axios.create({
    baseURL: 'http://127.0.0.1:5000'
}); 

//获取 introduce 页的数据
export const getIntroduceData = ( ()=> {
    return service.post('/introduce');
})

// knowledge 页提交搜索框的关键字, 并返回数据
export const getKnowledgeData = ( ( keyValue )=> {
    return service.post('/knowledge', keyValue);
})

// robot 页提交搜索框的关键字, 并返回数据
export const getRobotData = ( ( sentence )=> {
    return service.post('/robot', sentence);
})
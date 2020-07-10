import React from 'react';
import echarts from 'echarts';

import { Input } from 'antd';

import './knowledge.css'

import { getKnowledgeData } from '../../requests'


class Knowledge extends React.Component{
    constructor(){
        super();
        this.relationAmount = React.createRef();
    }
    componentDidMount(){
        this.chart = echarts.init(this.relationAmount.current);
    }

    onSearchClick = ( keyValue ) => {
        keyValue = keyValue.trim()

        var categories = [];
        for (var i = 0; i < 50; i++) {
            categories[i] = {
                name: '类目' + i
            };
        }
        
        getKnowledgeData(keyValue)
            .then( (resp) => {
                console.log('knowledge:', resp)
                if( resp.data === "failed"){
                    alert('无此名词，换个名词试试吧！')
                    return 
                }
                const option = {
                    title: {
                        text: 'ONLY FOR TEST',
                        top: 'bottom',
                        left: 'right'
                    },
                    tooltip: {
                        trigger: 'none'
                    },
                    animationDuration: 1500,
                    animationEasingUpdate: 'quinticInOut',
                    series: [{
                        type: "graph",          // 系列类型:关系图
                        roam: false,             // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
                        focusNodeAdjacency: true,   // 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。[ default: false ]
                        force: {                // 力引导布局相关的配置项，力引导布局是模拟弹簧电荷模型在每两个节点之间添加一个斥力，每条边的两个节点之间添加一个引力，每次迭代节点会在各个斥力和引力的作用下移动位置，多次迭代后节点会静止在一个受力平衡的位置，达到整个模型的能量最小化。
                                                // 力引导布局的结果有良好的对称性和局部聚合性，也比较美观。
                            repulsion: 1000,            // [ default: 50 ]节点之间的斥力因子(关系对象之间的距离)。支持设置成数组表达斥力的范围，此时不同大小的值会线性映射到不同的斥力。值越大则斥力越大
                            edgeLength: [150, 100]      // [ default: 30 ]边的两个节点之间的距离(关系对象连接线两端对象的距离,会根据关系对象值得大小来判断距离的大小)，
                                                        // 这个距离也会受 repulsion。支持设置成数组表达边长的范围，此时不同大小的值会线性映射到不同的长度。值越小则长度越长。如下示例:
                                                        // 值最大的边长度会趋向于 10，值最小的边长度会趋向于 50      edgeLength: [10, 50]
                        },
                        //不知道为什么 layout 设置为 'none' 会报错？？
                        layout: "force",            // 图的布局。[ default: 'none' ]
                                                    // 'none' 不采用任何布局，使用节点中提供的 x， y 作为节点的位置。
                                                    // 'circular' 采用环形布局;'force' 采用力引导布局.
                        // 标记的图形
                        //symbol: "path://M19.300,3.300 L253.300,3.300 C262.136,3.300 269.300,10.463 269.300,19.300 L269.300,21.300 C269.300,30.137 262.136,37.300 253.300,37.300 L19.300,37.300 C10.463,37.300 3.300,30.137 3.300,21.300 L3.300,19.300 C3.300,10.463 10.463,3.300 19.300,3.300 Z",
                        // symbol: 'circle',
                        lineStyle: {
                            color: 'source',
                            curveness: 0
                        },
                        emphasis: {
                            lineStyle: {
                                width: 10
                            }
                        },
                        itemStyle: {
                            borderColor: '#fff',
                            borderWidth: 1,
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.3)'
                        },
                        data: resp.data.nodes,
                        categories: categories,
                        links: resp.data.links,
                        label: {//图形上的文本标签，可用于说明图形的一些数据信息
                            normal: {
                                show : true,//显示
                                position: 'right',//相对于节点标签的位置，默认在节点中间
                            },
                            position: 'right',
                            formatter: '{b}'
                        },
                        edgeLabel: {//线条的边缘标签
                            normal: {
                                show: true,
                                formatter: function (x) {
                                    return x.data.name;
                                }
                            }
                        }
                    }]
                }
                this.chart.setOption(option); 
            })
    }

    render(){
        return (
            <div>
                <Input.Search
                    className="search"
                    placeholder="请输入关键字"
                    onSearch={this.onSearchClick}
                    enterButton="Search"
                    size='large'
                />
                <div id='knowledge' ref={this.relationAmount}/>
            </div>
            
        )
    }
}

export default Knowledge;
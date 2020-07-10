import React from 'react';
import './introduce.less';

import echarts from 'echarts';
import { getIntroduceData } from '../../requests'

require('echarts-wordcloud')

class Introduce extends React.Component{
    constructor(){
        super();
        this.wordCloudAmount = React.createRef();
    }

    initIntroduceChart = () =>{
        this.chart = echarts.init(this.wordCloudAmount.current);

        getIntroduceData()
            .then( (resp) => {
                console.log('introduce:',resp)
             const option = {
                title: {
                    text: 'ONLY FOR TEST',
                    top: 'bottom',
                    left: 'right'
                },
                tooltip: {
                    trigger: 'none',
                },
                series: [{
                    type: "wordCloud",          // 系列类型:词云
                    data: resp.data,
                    gridSize: 2,
                    sizeRange: [12, 50],
                    rotationRange: [-90,90],
                    shape: 'circle',
                    left: 'center',
                    top: 'center',
                    right: null,
                    bottom: null,
                    textStyle: {
                        normal: {
                            color: function () {
                                return 'rgb(' + [
                                        Math.round(Math.random() * 255),
                                        Math.round(Math.random() * 255),
                                        Math.round(Math.random() * 255)
                                    ].join(',') + ')';
                            }
                        },
                        emphasis: {
                            shadowBlur: 10,
                            shadowColor: '#333'
                        }
                    }
                }]
            };
            this.chart.setOption(option); 
        })
    }

    componentDidMount(){
        this.initIntroduceChart();
    }

    render(){   
        return (
            <div id='introduce' ref={this.wordCloudAmount}/>
        )
    }
}

export default Introduce;
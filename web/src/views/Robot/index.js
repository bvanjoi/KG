import React from 'react';
import echarts from 'echarts';

import { getRobotData } from '../../requests'

import './robot.less';
import { Input, Button, Skeleton, Tag } from 'antd';

class Robot extends React.Component{
    constructor(props) {
        super( props)
        this.state = {
            inputText: '',
            loading: false,
            cutSentence: {},
            res: ''
        }
        this.graph = React.createRef()
    }

    hanldeInputChange = (event) => {
        this.setState( {
            inputText: event.target.value
        })
    }

    componentDidMount() {
        this.chart = echarts.init(this.graph.current);
    }

    uploadSentence = () => {
        this.setState({
            loading: true
        })

        var categories = [];
        for (var i = 0; i < 50; i++) {
            categories[i] = {
                name: '类目' + i
            };
        }

        getRobotData( this.state.inputText.trim())
            .then( (resp) => {
                console.log( 'robot: ', resp); 
                if( resp.data.graph.length > 0) {
                    this.setState({
                        loading: false,
                        cutSentence:resp.data,
                        res: resp.data.describe
                    })
                    
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
                            type: "graph",          
                            roam: true,             
                            focusNodeAdjacency: true,  
                            force: {                
                                repulsion: 1000,            
                                edgeLength: [150, 100]      
                            },
                            layout: "force",            
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
                            label: {
                                normal: {
                                    show : true,
                                    position: 'right',
                                },
                                position: 'right',
                                formatter: '{b}'
                            },
                            edgeLabel: {
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
                }
                else {
                    alert('没找到有价值的内容')
                }
            })
    }

    render(){
        return (
            <div id='outer'>
                <div className="window">
                    <div className='left'>
                        <div className='input'>
                            <Input.TextArea 
                                className='text'
                                autoSize={false}
                                rows={3}
                                placeholder='plase write here'
                                onChange = {this.hanldeInputChange}
                                />
                            <Button 
                                className='button'
                                onClick={ this.uploadSentence}
                            >
                            Click
                            </Button>
                        </div>
                        <div className="cut" id='cut'>
                            <Skeleton 
                            active
                            loading={this.state.loading}
                            />
                            {
                                JSON.stringify(this.state.cutSentence) === "{}" ? ''
                                :
                                <div>
                                    <p><Tag color="#2db7f5">原始句子</Tag>  {this.state.cutSentence['origin']}</p>
                                    <hr/>
                                    <p><Tag color="#179ec7">分词后</Tag>  {this.state.cutSentence['cut'].join(" ")}</p>
                                    <hr/>
                                    <p><Tag color="#108ee9">消除停顿词后</Tag>  {this.state.cutSentence['stopwords_cut'].join(" ")}</p>
                                    <hr/>
                                    <p><Tag color="#234781">{this.state.cutSentence['show_cut'].join(" ")}</Tag><p>{this.state.res}</p></p>
                                </div>
                            }
                        </div>
                    </div>
                    <div className='right'>
                        <div className='graph' ref={this.graph}>
                                <Skeleton
                                active
                                loading={this.state.loading}
                                />
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Robot;
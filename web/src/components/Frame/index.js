import React from 'react';
import { Layout, Menu, Button } from 'antd';
import { withRouter } from 'react-router-dom';

import logo from './logo.jpg';
import './frame.less'

@withRouter
class Frame extends React.Component{
    constructor(){
        super();
        this.state = {
            nodes: [],
            links: []
        }
    }
    onMenuClick = ({key}) => {
        this.props.history.push(key);
    };

    render(){
        return (
            <Layout className='page'>
                <Layout.Header className='header'>
                    <div className='logo'>
                        <img src={logo} alt="KGQA"/>
                    </div>
                    <Menu
                        className='menus'
                        theme='light'
                        mode='horizontal' 
                        onClick={this.onMenuClick}
                        selectedKeys={this.props.location.pathname}
                    >
                        {
                            this.props.menus.map( item => {
                                return (
                                    <Menu.Item key={item.pathname}>{item.title}</Menu.Item>
                                )
                            })
                        }
                    </Menu>
                </Layout.Header>

                <Layout.Content className='content'>
                    {this.props.children}
                </Layout.Content>

                <Layout.Footer className='footer'>
                    <Button href='https://github.com/bvanjoi/KG' target='_blank'>说明</Button>
                </Layout.Footer>
            </Layout>   
        )
    }
}

export default Frame;
import React from 'react';

import { Frame } from './components'
import { Switch, Redirect, Route } from 'react-router-dom';
import { contentRoutes } from './routes'

class App extends React.Component{
    render(){
        return (
            <Frame menus={contentRoutes}>
                <Switch>
                    {
                        contentRoutes.map( route => {
                            return ( 
                                <Route
                                    key={route.pathname}
                                    path={route.pathname}
                                    render={ (routeProps) => {
                                        return <route.component {...routeProps}/>
                                    }}
                            />)
                        })
                    }
                    <Redirect to='/introduce' from='/' exact/>
                    <Redirect to='/404'/>
                </Switch>
            </Frame>
        )
    }
}

export default App;
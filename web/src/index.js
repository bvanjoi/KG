import React from 'react';
import ReactDOM from 'react-dom';
import {HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

import App from './App';
import {mainRoutes} from './routes';

ReactDOM.render(
    <Router>
        <Switch>
            <Route path='/' component={App}/>
            {
                mainRoutes.map( route => {
                    return <Route key={route.pathname} path={route.pathname} component={route.component}/>
                })
            }
            <Redirect to='/introduce' from='/' exact/>
            <Redirect to='/404'/>
        </Switch>
    </Router>,
    document.getElementById('root')
)
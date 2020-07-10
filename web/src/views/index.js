import Loadable from 'react-loadable';

import {Loading} from '../components';

const NotFound = Loadable({
    loader: () => import('./NotFound'),
    loading: Loading
})

const Knowledge = Loadable({
    loader: () => import('./Knowledge'),
    loading: Loading
}) 

const Robot = Loadable({
    loader: () => import('./Robot'),
    loading: Loading
})

const Introduce = Loadable({
    loader: () => import('./Introduce'),
    loading: Loading
})

export {
    NotFound,

    Knowledge,
    Robot,
    Introduce
}
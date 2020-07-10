const {override,
    addLessLoader,
    fixBabelImports,
    addDecoratorsLegacy
} = require('customize-cra');

const modifyVars = require('./lessVars');

//从 customize-cra 中引入一些相关的方法
module.exports = override(
    addDecoratorsLegacy(),
    addLessLoader({
        javascriptEnabled: true,
        modifyVars
    }),
    fixBabelImports('import',{
        libraryName: 'antd',
        libraryDirector: 'es',
        style: true,
    })
);
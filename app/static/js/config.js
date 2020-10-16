// requirejs.config({
//     //Pass the top-level main.js/index.js require
//     //function to requirejs so that node modules
//     //are loaded relative to the top-level JS file.
//     baseUrl: 'js',
//     paths: {
//         query: "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js",
//         reformat: "https://cdn.jsdelivr.net/npm/json2csv"
//     },

//     nodeRequire: require
// });

// requirejs(['foo', 'bar'],
// function   (foo,   bar) {
//     //foo and bar are loaded according to requirejs
//     //config, but if not found, then node's require
//     //is used to load the module.
// });
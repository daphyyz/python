import plotly
plotly.offline.init_notebook_mode() 
plotly.offline.iplot({
"data": [{
    "x": [1, 2, 3],
    "y": [4, 2, 5]
}],
"layout": {
    "title": "hello world"
}
})
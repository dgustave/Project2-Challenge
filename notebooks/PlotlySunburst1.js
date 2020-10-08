Plotly.d3.csv('output_Final.csv', function(err, rows){
    function unpack(rows, key) {
    return rows.map(function(row) {return row[key]})
  }
  
    var data = [{
          type: "sunburst",
          maxdepth: 2,
          ids: unpack(rows, 'ids'),
          labels: unpack(rows, 'labels'),
          parents: unpack(rows, 'parents'),
          textposition: 'inside',
          insidetextorientation: 'radial'
    }]
   console.log(data)
    var layout = {margin: {l: 0, r: 0, b: 0, t:0}}
  
    Plotly.newPlot('tester', data, layout)
  })
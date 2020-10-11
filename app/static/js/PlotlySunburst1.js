Plotly.d3.csv('../../data/external/sunburst_scrape.csv', function(err, rows){
    function unpack(rows, key) {
    return rows.map(function(row) {return row[key]})
  }
  
    var data = [{
          type: "sunburst",
          maxdepth: 2,
          ids: unpack(rows, 'ids'),
          labels: unpack(rows, 'labels'),
          exploded: true,
          parents: unpack(rows, 'parents'),
          textposition: 'inside',
          insidetextorientation: 'radial',
          opacity: .8,
          "marker": {"line": {"width": 0.5,

                     "color" : "white"}},
                     
    leaf: {opacity: 0.4},
    leaves: {opacity: 0.4}
  }]
   console.log(data)
    var layout = {margin: {l: 10, r: 0, b: 0, t:0},
      paper_bgcolor: 'rgba(0,0,0,0)', 
      sunburstcolorway:[
        "#00A5E3","#8DD7BF","#FF96C5","#FF5768","#FFBF65",
        "#FC6238", "#FFD872","#F2D4CC","#E77577","#6C88C4", "C05780"
      ],}
  
    Plotly.newPlot('tester', data, layout)
  })
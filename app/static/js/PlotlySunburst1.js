Plotly.d3.csv('../../data/external/sunburst_scrape.csv', function(err, rows){
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
        "#636EFA","#EF553B","#00CC96","#AB63FA","#19D3F3",
        "#E763FA", "#FECB52","#FFA15A","#FF6692","#B6E880", "teal"
      ],}
  
    Plotly.newPlot('tester', data, layout)
  })
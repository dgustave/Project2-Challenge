d3.csv("../data/external/sp500.csv").then(function(data) {
    console.log(data[0]);
  });
// d3.csv('../../data/external/sp500.csv')
//     .then(makeChart);
  
//   function makeChart(sectors) {
//     var ctx = document.getElementById('myChart').getContext('2d');
//     var sp500 = sectors.map(function(d) {return d["S&P 500 & Sectors"]});
//     var change = sectorss.map(function(d) {return d["% Change"]});
//     var chart = new Chart(ctx, {
//       type: 'horizontalBar',
//       data: {
//         labels: sp500,
//         datasets: [
//           {
//             data: change 
//           }
//         ]
//       }
//     });
//   }
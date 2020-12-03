var table = new Tabulator("#example-table-theme", {
    height:"331px",
    layout:"fitColumns",
    tooltipsHeader: false,
    columns:[
        {title:"Name", field:"name", sorter:"string", width:150},
        {title:"Progress", field:"progress", sorter:"number", hozAlign:"right", formatter:"progress"},
        {title:"Gender", field:"gender", width:100, sorter:"string", cellClick:function(e, cell){alert("cell clicked - " + cell.getValue())}},
        {title:"Rating", field:"rating", formatter:"star", hozAlign:"center", width:100},
        {title:"Favourite Color", field:"col", width:100, sorter:"string"},
        {title:"Date Of Birth", field:"dob", width:100, sorter:"date", hozAlign:"center"},
        {title:"Driver", field:"car", hozAlign:"center", formatter:"tickCross", sorter:"boolean"},
    ],
});
mapboxgl.accessToken = 'pk.eyJ1IjoiZW5kcmVocCIsImEiOiJjamRsNmlvZjYwM3RqMnhwOGRneDhhc2ZkIn0.wVZHznNCtC5_gJAnLC2EJQ';

console.log('beg igjen')

var l = 0;
var v =[];
var i;
var Time;
var url; 

var epi_url;
var play = false;
var endTime = 700;
var speed = 10;
var title;
var epi_speed = 1;
var slider_end_time;
var filterlist;
var hidden_sensors = [];


var map = new mapboxgl.Map({
  container: 'map', // container element id
  style: 'mapbox://styles/mapbox/light-v9',
  center: [-98.2022, 16.6855], // initial map center in [lon, lat]
  zoom: 5.5,
  maxZoom: 8
});



map.on('load', function() {
    slider_end_time = document.getElementById('slider');
    
    
    document.querySelector('.new-data').addEventListener('click', function () {
    
    if (l > 0) {
    map.removeLayer('earthquake' + l);
    map.removeLayer('epicenter' + l)
    
    }
        
    l += 1
        

    epi_url = 'media/epicenter_' + title + '.geojson';
    
    //speed = document.getElementById('speed').value;
    epi_speed = document.getElementById('epi_speed').value;
    epi_delay = document.getElementById('epi_delay').value;
    
    
    console.log('legg til noe')
    add_data()
    
    });
    

document.querySelector('.update-layer').addEventListener('click', function () {
updateLayer(Time);
console.log('layer updated')
});
    
document.getElementById('slider').addEventListener('input', function(e) {
  Time = parseInt(e.target.value);
    i = Time;
  // update the map
  updateLayer(Time)  
});


document.querySelector('.btn-pause').addEventListener('click', function() { 
    if (l > 0) {
        pause();}});

document.querySelector('.btn-reset').addEventListener('click', function() {
    if (l > 0) {
    reset();}});

document.querySelector('.btn').addEventListener('click', function() {
    if (l > 0 && play == false ){
        play_b();
        document.querySelector('.btn').innerHTML= 'Pause'; //'<i class="ion-ios-plus-outline"></i>';
    }
    
    else if (l>0 && play == true){
		pause();
	   document.querySelector('.btn').innerHTML= 'Play';//'<i class="ion-ios-plus-outline"></i>';
	}});

});

function add_data() {
//setEndTime();
    map.addLayer({
      id: 'earthquake' + l,
      type: 'circle',
      source: {
        type: 'geojson',
        data: url, //replace this with the url of your own geojson
      },
      paint: {
        'circle-radius':
             
          [
            'interpolate',
          ['linear'],
          ['number', ['get', 'S_Gal']],
        0, 6,
        5, 16,
        10, 20,
        50, 25,
        100, 30
        ],
        
        'circle-color': [
          'interpolate',
          ['linear'],
          ['number', ['get', 'S_Gal']],
          0, '#000000',
          5, '#b8ecff',
          10,'#05bcff',
          15,'#2fff05',
          25,'#ffd505',
          50,'#ff9f05',
          75,'#ff6d05',
          100,'#ff0505',
          150,'#C70000'
            
          
        ],
        
        'circle-opacity': 0.8
      }
    }, 'admin-2-boundaries-dispute');
    
    map.addLayer({
      id: 'epicenter' + l,
      type: 'circle',
      source: {
        type: 'geojson',
        data: epi_url, //replace this with the url of your own geojson
      },
      paint: {
        'circle-radius': {
        'property': 'Rad',
            
        stops:[ 
            [{zoom: 0, value: 0}, 0],
            [{zoom:0, value:700}, 0],
            [{zoom:22, value:0}, 0],
            [{zoom: 22, value: 700}, 70000000*epi_speed],
            
            ],
        base: 2,
        },    
        
        'circle-stroke-width': 2,
        'circle-stroke-color': 'green',
        'circle-opacity': 0
      }
    });
    

	
    map.on('click', 'earthquake' + l, function (e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var serial_number = e.features[0].properties.Sn;
        var description = 
            '<button id = "hide_sensor" onclick = "fill_form(\'' + serial_number +'\' );"> Hide sensor </button>'
            ;
        
        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    })

reset();
};


function updateLayer(Time) {
    //map.setFilter('earthquake'+ l, ['==', ['number', ['get', 'Time']], Time]);
    filterlist = ['all', ['==', ['number', ['get', 'Time']], Time]]; 
    
    if (hidden_sensors.length > 0) {
        for (var i = 0; i<hidden_sensors.length; i++) {
        filterlist.push(['!=', ['number', ['get', 'Sn']], hidden_sensors[i]]) 
    }};
    
    //filterlist = ['all', ['==', ['number', ['get', 'Time']], Time], ['!=', ['number', ['get', 'Sn']], 1604396]];
    map.setFilter('earthquake' + l, filterlist);
    
    
    //map.setFilter('earthquake'+l, ['!=', ['number', ['get', 'Sn']], 1604396])
    
    if (Time >= epi_delay) {
    map.setFilter('epicenter'+ l, ['==', ['number', ['get', 'Time']], Time-epi_delay]);
    }
    else {
        map.setFilter('epicenter'+ l, ['==', ['number', ['get', 'Time']], 0]);
    }
    
        
    document.getElementById('active-hour').innerText = display_time(Time);

};

function play_b() {

if (play == false) {
v = [];

for (var j=0; j < endTime; j++) {
    
    v.push(setTimeout( function () {
        
        document.getElementById('slider').value=i;
        Time = i;
        
        i++;
        updateLayer(Time) }, j*1000/speed));
    }
    play = true;
}
    
};

function reset() { 
    
    pause();
    
    i = 0;
    document.getElementById('slider').value=i;
    Time = i;
    updateLayer(Time);
};

function pause() { 
    if (v.length > 0){
    for (var j = 0; j < v.length; j++){
          clearTimeout(v[j])}
    };
    play = false;
        
    };

function setEndTime() {
    $.getJSON(url, function (data) {
        var b = data.features.length;
        
        slider_end_time.max = data.features[b-1].properties['Time'];
        endTime = data.features[b-1].properties['Time'];    
    })
    
    };

	

    // Change the cursor to a pointer when the mouse is over the places layer.
    map.on('mouseenter', 'places', function () {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'places', function () {
        map.getCanvas().style.cursor = '';
    });
    
function display_time(Time) {
    var minutes   = Math.floor(Time / 60);
    var seconds = Time - (minutes * 60);

    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return minutes+':'+seconds;
};




function select_earthquake(e) {
    
    for (var i=0; i < document.getElementsByClassName('table_row').length; i++){
        //console.log(document.getElementsByClassName('table_row')[i].innerHTML)
        document.getElementsByClassName('table_row')[i].style.background = 'white';
        document.getElementsByClassName('table_row')[i].style.color = 'black';
        
    
    };
        
    e.style.background = 'black';
    e.style.color = 'white';
    old_title = title;
    title = e.getElementsByClassName('title')[0].innerText;
    
    if (old_title != title) {
        hidden_sensors = []
        title = e.getElementsByClassName('title')[0].innerText;
        url = 'media/edit_public_' + title + '.geojson';
        setEndTime();
    }
    
	document.getElementById('load').click();
}

function fill_form(number){
	
    console.log(number)
    pushAndUpdate(Number(number), clickToUpdate);
    console.log('pushet of opdatert')
    document.getElementsByClassName('mapboxgl-popup-close-button')[0].click()
};



function pushAndUpdate(number, update) {
    hidden_sensors.push(Number(number))
    update();
}

function clickToUpdate () {
    document.getElementById('update-layer').click();
    console.log('prøvde å klikke')
}


function export_function() {
    
    if (title == undefined){
            alert('No earthquake chosen')
        }
    
    else {
    var result = confirm('Are you sure you want to export?')
    if (result) {
        document.getElementById('title1').value = title; 
        document.getElementById('url').value = url; 
        document.getElementById('sn').value = hidden_sensors.join()
        document.getElementById('export').click();
    };
    };
}

function undo_function() {
    hidden_sensors.splice(-1,1)
    document.getElementById('update-layer').click();
}


function speed_x(e) {
    speed = Number(e.innerText.slice(1))
    //console.log(speed)
    for (var i = 0; i < document.getElementsByClassName('speed_col').length; i++) {
        document.getElementsByClassName('speed_col')[i].style.background = 'white';
        document.getElementsByClassName('speed_col')[i].style.color = 'black';
    };
    
    e.style.color='white';
    e.style.background='black';
    document.getElementById('play-btn').click();
    document.getElementById('play-btn').click();
};




/*
function remove_and_export(export_callback) {
    document.getElementById('remove').click(); 
    console.log('remove clicked')
    export_callback();
}

function export_callback() {
    document.getElementById('export').click();
    console.log('export clicked')
}
*/

mapboxgl.accessToken = 'pk.eyJ1IjoiZW5kcmVocCIsImEiOiJjamRsNmlvZjYwM3RqMnhwOGRneDhhc2ZkIn0.wVZHznNCtC5_gJAnLC2EJQ';

console.log('begynn igjen')
    
var l = 0;
var v =[];
var i;
var Time;
var url; //= mode + '_' + earthquakeDate;
var play = false;
var b;
var a;
var endTime = 700;
var speed = 10;
var title;
var epi_url;
var epi_info_url;
var epi_speed;
var epi_delay;
var slider_end_time;


    
var map = new mapboxgl.Map({
  container: 'map', // container element id
  style: 'mapbox://styles/mapbox/light-v9',
  center: [-98.2022, 16.6855], // initial map center in [lon, lat]
  zoom: 5.5,
  maxZoom: 9
});


map.on('load', function() {
    slider_end_time = document.getElementById('slider');
    document.querySelector('.new-data').addEventListener('click', function () {
    
    if (l > 0) {
    map.removeLayer('earthquake' + l);
    map.removeLayer('epicenter' + l)
    };  
    l += 1
    epi_url = 'media/epicenter_' + title + '.geojson';
    url = 'media/public_' + title + '.geojson';
    epi_info_url = 'media/epi_public_' + title + '.json'    
    
    getEpiInfo(epi_info_url)
    
    add_data()
    });
    
    
document.getElementById('slider').addEventListener('input', function(e) {
  Time = parseInt(e.target.value);
    i = Time;
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
    play_b();} else if (l>0 && play == true){
		pause();
	}});

});

function add_data() {
//setEndTime();
 
    map.addLayer({
      id: 'earthquake' + l,
      type: 'circle',
      source: {
        type: 'geojson',
        data: url, 
      },
      paint: {
        'circle-radius':
             
          [
            'interpolate',
          ['linear'],
          ['number', ['get', 'S_Gal']],
        0, 3,
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
        //'type': 'exponential',
        //stops: [[0,0],[22,5000000]],
        //base: 2
            
        //},
            
            
        stops:[ 
            [{zoom: 0, value: 0}, 0],
            [{zoom:0, value:700}, 0],
            [{zoom:22, value:0}, 0],
            [{zoom: 22, value: 700}, 70000000*epi_speed],
            
            ],
        base: 2,
        },
            
        /*'circle-radius':  
          ['interpolate',
          ['linear'],
          ['number', ['get', 'Rad']],
        0, 0,
        700, 700*epi_speed
        ],*/
        
        'circle-stroke-width': 2,
        'circle-stroke-color': 'green',
        'circle-opacity': 0
      }
    });
    
reset();
};


function updateLayer(Time) {
    map.setFilter('earthquake'+ l, ['==', ['number', ['get', 'Time']], Time+epi_delay]); 
    map.setFilter('epicenter'+ l, ['==', ['number', ['get', 'Time']], Time]);
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
        b = data.features.length;
        
        slider_end_time.max = data.features[b-1].properties['Time'];
        endTime = data.features[b-1].properties['Time'];    
    })
    
    };

function display_time(Time) {
    var minutes   = Math.floor(Time / 60);
    var seconds = Time - (minutes * 60);

    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return minutes+':'+seconds;
};


function getEpiInfo(epi_url) {
     epi_info = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': epi_url,
        'dataType': "json",
        'success': function (data) {
            epi_info = data;
        }
    });
    epi_speed = Number(epi_info.epi_speed);
    epi_delay = Number(epi_info.delay);
 };

function select_earthquake(e) {
    for (var i=0; i < document.getElementsByClassName('table_row').length; i++){
        document.getElementsByClassName('table_row')[i].style.background = 'white';
        document.getElementsByClassName('table_row')[i].style.color = 'black';
        /*
        document.getElementsByClassName('inner_row1')[i].style.background = 'white';
        document.getElementsByClassName('inner_row1')[i].style.color = 'black';
        document.getElementsByClassName('inner_row2')[i].style.background = 'white';
        document.getElementsByClassName('inner_row2')[i].style.color = 'black';
        */
    };
    
    e.style.background = 'black';
    e.style.color = 'white';
    e.getElementsByClassName('table_row')[0].style.background = 'black';
    e.getElementsByClassName('table_row')[1].style.background = 'black';
    e.getElementsByClassName('table_row')[0].style.color = 'white';
    e.getElementsByClassName('table_row')[1].style.color = 'white';
    //e.innerHTML.style.color = 'white';
    console.log(e.getElementsByClassName('table_row'))
    title = e.getElementsByClassName('title')[0].innerText;
    url = 'media/public_' + title + '.geojson';
    setEndTime();
    
    document.getElementById('load').click()
};

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

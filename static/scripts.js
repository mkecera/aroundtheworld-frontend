
// THIS IS THE FIRST MAP
// create map
var mymap = L.map('mapid').setView([11.8166, 122.0942], 8);

// attribution link
mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';

// add OpenStreetMap Tile layer
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
}).addTo(mymap);

// add markers
var locations = [
    ["LOCATION_1", 11.8166, 122.0942],
    ["LOCATION_2", 11.9804, 121.9189],
    ["LOCATION_3", 10.7202, 122.5621],
    ["LOCATION_4", 11.3889, 122.6277],
    ["LOCATION_5", 10.5929, 122.6325]
];
for (var i = 0; i < locations.length; i++) {
    marker = new L.marker([locations[i][1], locations[i][2]])
        .bindPopup("<b>" + locations[i][0] + "</b>")
        .addTo(mymap);
}


// THIS IS THE SECOND MAP
// create map
var mymap2 = L.map('mapid2').setView([11.8166, 122.0942], 8);

// attribution link
mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';

// add OpenStreetMap Tile layer
L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; ' + mapLink + ' Contributors',
    maxZoom: 18,
}).addTo(mymap2);

// add markers
var locations = [
    ["LOCATION_1", 11.8166, 122.0942],
    ["LOCATION_2", 11.9804, 121.9189],
    ["LOCATION_3", 10.7202, 122.5621],
    ["LOCATION_4", 11.3889, 122.6277],
    ["LOCATION_5", 10.5929, 122.6325]
];
for (var i = 0; i < locations.length; i++) {
    marker = new L.marker([locations[i][1], locations[i][2]])
        .bindPopup("<b>" + locations[i][0] + "</b>")
        .addTo(mymap2);
}
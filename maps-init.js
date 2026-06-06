/* Mapas offline Menorca — Leaflet + GeoJSON (sin tiles) */
(function () {
  'use strict';

  var COLORS = {
    sea: '#1a6b7c',
    sand: '#e8dfd0',
    pine: '#5a7d65',
    coral: '#c4785a',
    route: '#2d8fa3',
    zones: {
      norte: '#a8c5d4',
      sur: '#d4c4a8',
      este: '#b8d4c8',
      oeste: '#c8d4e8',
      centro: '#5a7d65'
    }
  };

  /* GeoJSON [lng, lat] */
  var ISLAND = {
    type: 'Feature',
    properties: { name: 'Menorca' },
    geometry: {
      type: 'Polygon',
      coordinates: [[
        [3.828, 40.008], [3.775, 39.968], [3.782, 39.912], [3.815, 39.868],
        [3.895, 39.845], [4.018, 39.852], [4.145, 39.878], [4.268, 39.905],
        [4.318, 39.948], [4.295, 40.018], [4.218, 40.078], [4.128, 40.098],
        [4.028, 40.088], [3.928, 40.062], [3.868, 40.038], [3.828, 40.008]
      ]]
    }
  };

  var ZONES = [
    { id: 'norte', label: 'Norte', color: COLORS.zones.norte, center: [4.045, 40.065] },
    { id: 'sur', label: 'Sur', color: COLORS.zones.sur, center: [3.870, 39.905] },
    { id: 'este', label: 'Este', color: COLORS.zones.este, center: [4.240, 39.875] },
    { id: 'oeste', label: 'Oeste', color: COLORS.zones.oeste, center: [3.820, 39.970] },
    { id: 'centro', label: 'Centro', color: COLORS.zones.centro, center: [4.050, 39.995] }
  ];

  var POIS = {
    mao: [4.2614, 39.8885],
    ciutadella: [3.8380, 40.0024],
    macarella: [3.7915, 39.9378],
    macarelleta: [3.7850, 39.9405],
    galdana: [3.9540, 39.9370],
    santCliment: [4.0980, 39.8970],
    mercadal: [4.0958, 39.9911],
    toro: [4.0217, 40.0372],
    ferreries: [4.0250, 39.9894],
    mitjana: [3.9367, 39.9433],
    pregonda: [4.0244, 40.0467],
    fornells: [4.0092, 40.0558],
    cavalleria: [4.0733, 40.0533],
    calaPorter: [4.1317, 39.8533],
    covaXoroi: [4.1350, 39.8450],
    puntaPrima: [4.1967, 39.8283],
    binissafuller: [4.2050, 39.8200],
    binibequerVell: [4.2183, 39.8183],
    calaBinibequer: [4.2217, 39.8150],
    salgar: [4.2333, 39.8083]
  };

  var DAYS = {
    day1: {
      color: COLORS.coral,
      points: [
        { ll: POIS.mao, name: 'Maó', n: 1 },
        { ll: POIS.santCliment, name: 'Sant Climent', n: 2 },
        { ll: POIS.galdana, name: 'Cala Galdana', n: 3 },
        { ll: POIS.macarella, name: 'Cala Macarella', n: 4 },
        { ll: POIS.macarelleta, name: 'Cala Macarelleta', n: 5 },
        { ll: POIS.ciutadella, name: 'Ciutadella', n: 6 }
      ]
    },
    day2: {
      color: COLORS.sea,
      points: [
        { ll: POIS.mao, name: 'Maó', n: 1 },
        { ll: POIS.mercadal, name: 'Es Mercadal', n: 2 },
        { ll: POIS.pregonda, name: 'Cala Pregonda', n: 3 },
        { ll: POIS.fornells, name: 'Fornells', n: 4 },
        { ll: POIS.cavalleria, name: 'Cap de Cavalleria', n: 5 }
      ]
    },
    day3: {
      color: COLORS.pine,
      points: [
        { ll: POIS.mao, name: 'Maó', n: 1 },
        { ll: POIS.mercadal, name: 'Es Mercadal', n: 2 },
        { ll: POIS.toro, name: 'Monte Toro', n: 3 },
        { ll: POIS.ferreries, name: 'Ferreries', n: 4 },
        { ll: POIS.mitjana, name: 'Cala Mitjana', n: 5 }
      ]
    },
    day4: {
      color: '#6b5a8a',
      points: [
        { ll: POIS.calaPorter, name: 'Cala en Porter', n: 1 },
        { ll: POIS.covaXoroi, name: "Cova d'en Xoroi", n: 2 },
        { ll: POIS.puntaPrima, name: 'Punta Prima', n: 3 },
        { ll: POIS.binissafuller, name: 'Binissafúller', n: 4 }
      ]
    },
    day5: {
      color: '#c4785a',
      points: [
        { ll: POIS.mao, name: 'Maó', n: 1 },
        { ll: POIS.binibequerVell, name: 'Binibèquer Vell', n: 2 },
        { ll: POIS.calaBinibequer, name: 'Cala Binibèquer', n: 3 },
        { ll: POIS.salgar, name: "S'Algar", n: 4 },
        { ll: POIS.mao, name: 'Maó (puerto)', n: 5 }
      ]
    }
  };

  var maps = {};
  var pending = [];

  function pinIcon(num, color) {
    return L.divIcon({
      className: 'map-pin-wrap',
      html: '<span class="map-pin" style="background:' + color + '">' + num + '</span>',
      iconSize: [30, 30],
      iconAnchor: [15, 15],
      popupAnchor: [0, -16]
    });
  }

  function baseMapOptions() {
    return {
      zoomControl: true,
      attributionControl: false,
      tap: true,
      touchZoom: true,
      bounceAtZoomLimits: false,
      preferCanvas: true,
      maxBounds: [[39.78, 3.72], [40.14, 4.36]],
      maxBoundsViscosity: 0.85
    };
  }

  function addIslandLayer(map) {
    L.geoJSON(ISLAND, {
      style: {
        fillColor: COLORS.sand,
        fillOpacity: 0.95,
        color: COLORS.sea,
        weight: 2,
        opacity: 0.9
      }
    }).addTo(map);
  }

  function addRoute(map, points, color) {
    var latlngs = points.map(function (p) { return [p.ll[1], p.ll[0]]; });
    L.polyline(latlngs, {
      color: color,
      weight: 4,
      opacity: 0.85,
      dashArray: '8 6',
      lineCap: 'round'
    }).addTo(map);
    points.forEach(function (p) {
      L.marker([p.ll[1], p.ll[0]], { icon: pinIcon(p.n, color) })
        .bindPopup('<strong>' + p.n + '.</strong> ' + p.name)
        .addTo(map);
    });
    map.fitBounds(L.latLngBounds(latlngs), { padding: [36, 36], maxZoom: 12 });
  }

  function initOverview() {
    var el = document.getElementById('map-overview');
    if (!el || maps.overview) return;

    var map = L.map(el, baseMapOptions()).setView([39.97, 4.05], 10);
    addIslandLayer(map);

    ZONES.forEach(function (z) {
      L.circleMarker([z.center[1], z.center[0]], {
        radius: 22,
        fillColor: z.color,
        fillOpacity: 0.55,
        color: COLORS.sea,
        weight: 1.5
      }).bindTooltip(z.label, { permanent: true, direction: 'center', className: 'zone-label' }).addTo(map);
    });

    Object.keys(POIS).forEach(function (key) {
      var ll = POIS[key];
      L.circleMarker([ll[1], ll[0]], {
        radius: 5,
        fillColor: COLORS.sea,
        fillOpacity: 0.9,
        color: '#fff',
        weight: 1.5
      }).addTo(map);
    });

    maps.overview = map;
    setTimeout(function () { map.invalidateSize(); }, 120);
  }

  var FULL_ROUTE = [
    { key: 'day1', label: 'D1 · Costa sur', color: COLORS.coral },
    { key: 'day2', label: 'D2 · Norte', color: COLORS.sea },
    { key: 'day3', label: 'D3 · Interior', color: COLORS.pine },
    { key: 'day4', label: 'D4 · Camí de Cavalls', color: '#6b5a8a' },
    { key: 'day5', label: 'D5 · Sureste', color: COLORS.route }
  ];

  function initFullRoute() {
    var el = document.getElementById('map-full-route');
    if (!el || maps.fullRoute) return;

    var map = L.map(el, baseMapOptions()).setView([39.97, 4.05], 10);
    addIslandLayer(map);

    var allLatLngs = [];

    FULL_ROUTE.forEach(function (entry) {
      var day = DAYS[entry.key];
      if (!day) return;

      var latlngs = day.points.map(function (p) { return [p.ll[1], p.ll[0]]; });
      allLatLngs = allLatLngs.concat(latlngs);

      L.polyline(latlngs, {
        color: entry.color,
        weight: 4,
        opacity: 0.88,
        dashArray: '8 6',
        lineCap: 'round'
      }).addTo(map);

      day.points.forEach(function (p) {
        L.marker([p.ll[1], p.ll[0]], { icon: pinIcon(p.n, entry.color) })
          .bindPopup('<strong>' + entry.label + '</strong><br>' + p.n + '. ' + p.name)
          .addTo(map);
      });
    });

    if (allLatLngs.length) {
      map.fitBounds(L.latLngBounds(allLatLngs), { padding: [44, 44], maxZoom: 11 });
    }

    maps.fullRoute = map;
    setTimeout(function () { map.invalidateSize(); }, 120);
  }

  function initDayMap(id, dayKey) {
    var el = document.getElementById(id);
    if (!el || maps[id]) return;

    var day = DAYS[dayKey];
    var map = L.map(el, baseMapOptions());
    addIslandLayer(map);
    addRoute(map, day.points, day.color);

    maps[id] = map;
    setTimeout(function () { map.invalidateSize(); }, 120);
  }

  function registerMap(id, dayKey) {
    pending.push({ id: id, dayKey: dayKey });
  }

  function bootMap(entry) {
    if (entry.id === 'map-overview') {
      initOverview();
    } else if (entry.id === 'map-full-route') {
      initFullRoute();
    } else {
      initDayMap(entry.id, entry.dayKey);
    }
  }

  function observeMaps() {
    if (!('IntersectionObserver' in window)) {
      pending.forEach(bootMap);
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var target = entry.target;
        var match = pending.find(function (p) { return p.id === target.id; });
        if (match) {
          bootMap(match);
          io.unobserve(target);
        }
      });
    }, { rootMargin: '80px', threshold: 0.05 });

    pending.forEach(function (p) {
      var el = document.getElementById(p.id);
      if (el) io.observe(el);
    });
  }

  registerMap('map-overview', null);
  registerMap('map-full-route', null);
  registerMap('map-day1', 'day1');
  registerMap('map-day2', 'day2');
  registerMap('map-day3', 'day3');
  registerMap('map-day4', 'day4');
  registerMap('map-day5', 'day5');

  function onReady() {
    observeMaps();
    window.addEventListener('orientationchange', function () {
      setTimeout(function () {
        Object.keys(maps).forEach(function (k) {
          if (maps[k]) maps[k].invalidateSize();
        });
      }, 300);
    });
    window.addEventListener('resize', function () {
      Object.keys(maps).forEach(function (k) {
        if (maps[k]) maps[k].invalidateSize();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();

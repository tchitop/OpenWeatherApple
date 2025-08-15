# app.py

# Importieren der notwendigen Flask- und Requests-Bibliotheken
from flask import Flask, jsonify, render_template_string
import requests

# Erstellen Sie eine Flask-Webserver-Instanz.
# Diese 'app'-Variable ist der Einstiegspunkt für Vercel.
app = Flask(__name__)

# Sie benötigen einen kostenlosen API-Schlüssel von OpenWeatherMap.
# Ersetzen Sie 'YOUR_API_KEY_HERE' durch Ihren echten Schlüssel.
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"

# Koordinaten für Apple Park in Cupertino, Kalifornien.
APPLE_PARK_LAT = 37.3346
APPLE_PARK_LON = -122.0090

# --------------------------------------------------------------------------------
# HTML-Vorlage
# Der gesamte HTML-Code, der vom Server bereitgestellt wird.
# --------------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0e1117">
<title>Gewitter-Zähler & Wetter · iPhone</title>
<link rel="manifest" href="data:application/manifest+json,{&quot;name&quot;:&quot;Gewitter-Zähler&quot;,&quot;short_name&quot;:&quot;Gewitter&quot;,&quot;display&quot;:&quot;standalone&quot;,&quot;background_color&quot;:&quot;#0e1117&quot;,&quot;theme_color&quot;:&quot;#0e1117&quot;,&quot;icons&quot;:[]}">
<style>
  :root{
    --bg:#0e1117; --panel:#121620; --panel2:#161b22;
    --accent:#7ee787; --accent2:#79c0ff; --text:#e6edf3; --muted:#9da7b3; --warn:#f2cc60; --danger:#ff7b72;
    --safe-inset-top: env(safe-area-inset-top);
    --safe-inset-bottom: env(safe-area-inset-bottom);
    --safe-inset-left: env(safe-area-inset-left);
    --safe-inset-right: env(safe-area-inset-right);
  }
  *{box-sizing:border-box; -webkit-tap-highlight-color:transparent}
  html,body{height:100%}
  body{
    margin:0; background:var(--bg); color:var(--text);
    font-family: ui-sans-serif, -apple-system, system-ui, Segoe UI, Roboto, Helvetica, Arial;
    padding-top: calc(12px + var(--safe-inset-top));
    padding-bottom: calc(12px + var(--safe-area-inset-bottom));
  }
  header{padding: 0 16px 10px}
  h1{margin:0; font-size: clamp(18px, 4.5vw, 26px); letter-spacing:.2px}
  .sub{color:var(--muted); font-size:.95rem}
  main{display:grid; gap:14px; padding: 0 16px; max-width: 820px; margin:0 auto}
  .card{
    background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
    border:1px solid rgba(255,255,255,.07);
    border-radius: 16px; padding: 12px;
    box-shadow: 0 8px 30px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.06);
  }
  .row{display:flex; align-items:center; gap:10px; flex-wrap:wrap}
  .controls{display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:12px}
  @media (min-width: 560px){ .controls{ grid-template-columns: repeat(3, 1fr);} }
  button{
    font-weight:700; font-size:1.05rem; padding:14px 16px; border-radius:14px; border:1px solid rgba(255,255,255,.12);
    background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02));
    color:var(--text); cursor:pointer; touch-action:manipulation;
  }
  button:active{transform: translateY(1px) scale(.995)}
  .accent{border-color: rgba(126,231,135,.6); box-shadow: 0 0 0 2px rgba(126,231,135,.15) inset}
  .accent2{border-color: rgba(121,192,255,.5); box-shadow: 0 0 0 2px rgba(121,192,255,.1) inset}
  .warn{border-color: rgba(242,204,96,.5)}
  .danger{border-color: rgba(255,123,114,.5)}
  .pill{display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px;
        background:rgba(121,192,255,.12); border:1px solid rgba(121,192,255,.28); font-weight:600}
  .muted{color:var(--muted)}
  .kbd{font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:.95em; padding:.1em .45em; border-radius:6px;
       border:1px solid rgba(255,255,255,.2); background:rgba(255,255,255,.06)}
  canvas{display:block; width:100%; height:auto; aspect-ratio:1/1}
  .two-col{display:grid; gap:12px}
  @media (min-width: 900px){ .two-col{ grid-template-columns: 420px 1fr; align-items:start} }
  table{width:100%; border-collapse:collapse; font-size:.95rem}
  th,td{padding:10px 8px; border-bottom:1px solid rgba(255,255,255,.07); text-align:left; white-space:nowrap}
  .table-wrap{overflow:auto; max-height:340px; border-radius:12px; border:1px solid rgba(255,255,255,.07)}
  footer{padding:12px 16px; text-align:center; color:var(--muted); font-size:.9rem}
  .map{
    width:100%; height:220px; border-radius:12px; border:1px solid rgba(255,255,255,.07);
    background: conic-gradient(from 0deg, rgba(121,192,255,.18), rgba(126,231,135,.18));
    position:relative; overflow:hidden;
  }
  .dot{position:absolute; width:14px; height:14px; border-radius:50%; background:#79c0ff; box-shadow:0 0 20px rgba(121,192,255,.6)}
  .toast{position:fixed; left:50%; transform:translateX(-50%); bottom: calc(20px + var(--safe-inset-bottom)); background:#1b2230; border:1px solid rgba(255,255,255,.12);
         border-radius:12px; padding:10px 14px; font-weight:600; z-index:9999}
</style>
</head>
<body>
  <header class="row" style="justify-content:space-between">
    <div>
      <h1>Gewitter-Zähler & Wetter <span class="sub">· iPhone</span></h1>
      <div class="sub">Touch-UI, offline · speichert Standort nur lokal.</div>
    </div>
    <span id="badge" class="pill">⚡ Kein aktives Gewitter</span>
  </header>

  <main class="two-col">
    <section class="card">
      <canvas id="dial" width="800" height="800" aria-label="Gewitter-Zähler"></canvas>

      <div class="controls">
        <button id="start" class="accent">Gewitter starten</button>
        <button id="end" class="warn">Beenden</button>
        <button id="flash" class="accent2" title="Bei Blitz tippen">⚡ Blitz</button>
        <button id="thunder" class="accent2" title="Bei Donner tippen">🔊 Donner</button>
        <button id="loc" title="Standort aktualisieren">📍 Standort</button>
        <button id="export">⬇️ CSV</button>
        <button id="reset" class="danger">Alles löschen</button>
      </div>

      <div class="sub" style="margin-top:10px">
        Shortcuts (Mac/Hardware-Tastatur): <span class="kbd">B</span> = Blitz, <span class="kbd">D</span> = Donner
      </div>
    </section>

    <section class="card">
      <h3 style="margin:6px 0 6px">Standort & Messungen</h3>
      <div id="locLine" class="sub">Standort: unbekannt – erlaube „Standort verwenden“.</div>
      <div class="map" id="mapBox" aria-label="Einfache Standortkarte">
        <div id="dot" class="dot" style="display:none"></div>
      </div>
      
      <!-- Container for weather data -->
      <div id="weather-info" class="sub" style="margin-top:10px;">
          <!-- Weather data will be inserted here dynamically -->
          Wetterdaten werden geladen...
      </div>

      <div id="stats" class="sub" style="margin-top:8px"></div>

      <div class="table-wrap" style="margin-top:10px">
        <table>
          <thead>
            <tr>
              <th>Zeit</th>
              <th>Ereignis</th>
              <th>Dauer (s)</th>
              <th>Entfernung (km)</th>
              <th>Lat</th>
              <th>Lon</th>
              <th>±m</th>
              <th>Storm-ID</th>
            </tr>
          </thead>
          <tbody id="log"></tbody>
        </table>
      </div>
    </section>
  </main>

  <footer>Zum Home-Bildschirm hinzufügen für Vollbild. Daten bleiben auf deinem Gerät.</footer>

  <div id="toast" class="toast" style="display:none"></div>

<script>
(function(){
  const DPR = Math.max(1, window.devicePixelRatio || 1);
  const W = 800, H = 800;
  const canvas = document.getElementById('dial');
  const ctx = canvas.getContext('2d');
  canvas.width = W * DPR; canvas.height = H * DPR; ctx.scale(DPR, DPR);

  const STORAGE_KEY = "gewitter-counter-iphone-v1";

  /*** STATE ***/
  let state = {
    stormsThisMonth: 0,
    activeStormId: null,
    measurements: [], // {t, type, deltaSec?, km?, stormId, lat?, lon?, acc?}
    pendingFlashAt: null,
    location: {lat:null, lon:null, acc:null, t:null},
    lastSaved: null
  };
  try{ const raw = localStorage.getItem(STORAGE_KEY); if (raw) state = JSON.parse(raw); }catch(e){}
  const save = () => { state.lastSaved = Date.now(); localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); render(); };

  /*** UI refs ***/
  const badge = document.getElementById('badge');
  const startBtn = document.getElementById('start');
  const endBtn = document.getElementById('end');
  const flashBtn = document.getElementById('flash');
  const thunderBtn = document.getElementById('thunder');
  const exportBtn = document.getElementById('export');
  const resetBtn = document.getElementById('reset');
  const locBtn = document.getElementById('loc');
  const stats = document.getElementById('stats');
  const logBody = document.getElementById('log');
  const locLine = document.getElementById('locLine');
  const toast = document.getElementById('toast');

  /*** Helpers ***/
  const round2 = x => Math.round(x*100)/100;
  const fmtTime = t => new Date(t).toLocaleString();
  function showToast(text){
    toast.textContent = text; toast.style.display = "block";
    setTimeout(()=> toast.style.display="none", 1600);
  }

  /*** Canvas Dial ***/
  const anim = { shown: 0 };
  function draw(){
    const cx = W/2, cy = H/2, r = 280;
    ctx.clearRect(0,0,W,H);
    // bg ring
    ctx.beginPath();
    const grad = ctx.createRadialGradient(cx,cy,0,cx,cy,r*1.1);
    grad.addColorStop(0,"rgba(126,231,135,.07)");
    grad.addColorStop(1,"rgba(126,231,135,.01)");
    ctx.fillStyle = grad; ctx.arc(cx,cy,r*1.25,0,Math.PI*2); ctx.fill();

    // base circle
    ctx.lineWidth = 18; ctx.strokeStyle = "rgba(255,255,255,.08)";
    ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();

    // progress
    const maxVisual = 20;
    const frac = Math.min(1, (anim.shown % (maxVisual+1)) / maxVisual);
    const ringGrad = ctx.createLinearGradient(cx-r,cy-r,cx+r,cy+r);
    ringGrad.addColorStop(0,"rgba(126,231,135,.9)");
    ringGrad.addColorStop(1,"rgba(121,192,255,.9)");
    ctx.strokeStyle = ringGrad; ctx.lineCap = "round";
    ctx.beginPath(); ctx.arc(cx,cy,r,-Math.PI/2,-Math.PI/2 + frac*Math.PI*2); ctx.stroke();

    // active glow
    if (state.activeStormId){
      ctx.shadowColor = "rgba(126,231,135,.6)"; ctx.shadowBlur = 24;
      ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();
      ctx.shadowBlur = 0;
    }
    // center text
    ctx.fillStyle = "#e6edf3"; ctx.textAlign="center"; ctx.textBaseline="middle";
    ctx.font = "700 92px system-ui,-apple-system,Segoe UI,Roboto";
    ctx.fillText(String(state.stormsThisMonth), cx, cy - 10);
    ctx.font = "600 20px system-ui,-apple-system,Segoe UI,Roboto";
    const hint = state.pendingFlashAt ? "Zähle bis Donner …" : (state.activeStormId ? "Bereit" : "Keine Session");
    ctx.fillStyle = state.pendingFlashAt ? "rgba(242,204,96,.95)" : "rgba(157,167,179,.95)";
    ctx.fillText("Gewitter diesen Monat", cx, cy + 36);
    ctx.fillText(hint, cx, cy + 64);
  }
  function animate(){
    const target = state.stormsThisMonth;
    anim.shown += (target - anim.shown) * 0.15;
    if (Math.abs(target - anim.shown) < 0.01) anim.shown = target;
    draw();
    requestAnimationFrame(animate);
  }
  animate();

  /*** LOCATION ***/
  let watchId = null;
  function updateLocLine(){
    if (state.location.lat==null){ locLine.textContent = "Standort: unbekannt – tippe „📍 Standort“ und erlaube Zugriff."; return; }
    const {lat,lon,acc,t} = state.location;
    locLine.textContent = `Standort: ${round2(lat)}°, ${round2(lon)}° (±${acc ?? "?"} m) · ${t ? new Date(t).toLocaleTimeString() : ""}`;
  }
  function placeDot(){
    const box = document.getElementById('mapBox');
    const dot = document.getElementById('dot');
    if (state.location.lat==null){ dot.style.display="none"; return; }
    // fake mini-map: place the dot proportionally within the box using normalized lat/lon
    // normalize lat [-90,90] -> y [0,1], lon [-180,180] -> x [0,1]
    const x = (state.location.lon + 180) / 360;
    const y = 1 - (state.location.lat + 90) / 180;
    const rect = box.getBoundingClientRect();
    const dx = Math.max(7, Math.min(rect.width - 7, x * rect.width));
    const dy = Math.max(7, Math.min(rect.height - 7, y * rect.height));
    dot.style.left = (dx - 7) + "px";
    dot.style.top = (dy - 7) + "px";
    dot.style.display = "block";
  }
  function requestLocation(){
    if (!('geolocation' in navigator)){ showToast("Kein Geolocation-Support"); return; }
    const opts = {enableHighAccuracy:true, maximumAge: 15000, timeout: 15000};
    // Start/refresh a watch for continuous updates (better UX on iPhone)
    if (watchId!=null){ navigator.geolocation.clearWatch(watchId); }
    watchId = navigator.geolocation.watchPosition((pos)=>{
      const {latitude, longitude, accuracy} = pos.coords;
      state.location = {lat: latitude, lon: longitude, acc: Math.round(accuracy), t: Date.now()};
      save();
      updateLocLine(); placeDot();
    }, (err)=>{
      console.warn(err);
      showToast(err.message || "Standortfehler");
      updateLocLine();
    }, opts);
    showToast("Standort wird aktualisiert …");
  }
  window.addEventListener('resize', placeDot);

  /*** Storm logic ***/
  function currentLocFields(){
    const {lat,lon,acc} = state.location || {};
    return {lat, lon, acc};
  }
  function startStorm(){
    if (state.activeStormId) return;
    const id = "S"+Date.now().toString(36);
    state.activeStormId = id;
    state.stormsThisMonth += 1;
    state.measurements.unshift({t:Date.now(), type:"storm_start", stormId:id, ...currentLocFields()});
    save(); showToast("Session gestartet");
  }
  function endStorm(){
    if (!state.activeStormId) return;
    state.measurements.unshift({t:Date.now(), type:"storm_end", stormId:state.activeStormId, ...currentLocFields()});
    state.activeStormId = null; state.pendingFlashAt = null;
    save(); showToast("Session beendet");
  }
  function flash(){
    if (!state.activeStormId){ startStorm(); }
    state.pendingFlashAt = Date.now();
    state.measurements.unshift({t:state.pendingFlashAt, type:"flash", stormId: state.activeStormId, ...currentLocFields()});
    save();
  }
  function thunder(){
    if (!state.pendingFlashAt) return;
    const t = Date.now();
    const deltaSec = (t - state.pendingFlashAt)/1000;
    const km = deltaSec / 3; // 3 s ≈ 1 km
    state.measurements.unshift({t, type:"thunder", deltaSec: round2(deltaSec), km: round2(km), stormId: state.activeStormId, ...currentLocFields()});
    state.pendingFlashAt = null;
    save();
  }

  /*** Events ***/
  startBtn.addEventListener('click', startStorm);
  endBtn.addEventListener('click', endStorm);
  flashBtn.addEventListener('click', flash);
  thunderBtn.addEventListener('click', thunder);
  exportBtn.addEventListener('click', ()=>{
    const rows = [["Zeit","Ereignis","Dauer (s)","Entfernung (km)","Lat","Lon","±m","Storm-ID"]];
    state.measurements.slice().reverse().forEach(m=>{
      rows.push([fmtTime(m.t), m.type, m.deltaSec ?? "", m.km ?? "", m.lat ?? "", m.lon ?? "", m.acc ?? "", m.stormId ?? ""]);
    });
    const csv = rows.map(r=>r.map(x => `"${String(x).replace(/"/g,'""')}"`).join(",")).join("\n");
    const blob = new Blob([csv], {type:"text/csv;charset=utf-8;"});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = "gewitter_messungen.csv"; a.click(); URL.revokeObjectURL(a.href);
  });
  resetBtn.addEventListener('click', ()=>{
    if (!confirm("Wirklich alle Daten löschen?")) return;
    state = {stormsThisMonth:0, activeStormId:null, measurements:[], pendingFlashAt:null, location:{lat:null,lon:null,acc:null,t:null}, lastSaved:null};
    save(); showToast("Zurückgesetzt");
  });
  locBtn.addEventListener('click', requestLocation);

  // Keyboard (for external keyboards on iPad/Mac)
  window.addEventListener('keydown', (e)=>{
    if (['INPUT','TEXTAREA'].includes((e.target&&e.target.tagName)||"")) return;
    const k = e.key.toLowerCase();
    if (k==='b') flash();
    if (k==='d') thunder();
  });

  /*** Render table & stats ***/
  function render(){
    badge.textContent = state.activeStormId ? ("⚡ Aktiv · " + state.activeStormId) : "⚡ Kein aktives Gewitter";
    // stats
    const total = state.measurements.filter(m=>m.type==="thunder").length;
    const avgKm = (()=>{
      const arr = state.measurements.filter(m=>typeof m.km === 'number').map(m=>m.km);
      if (!arr.length) return null;
      return round2(arr.reduce((a,b)=>a+b,0)/arr.length);
    })();
    stats.textContent = `Diesen Monat: ${state.stormsThisMonth} Gewitter · Messungen: ${total}` + (avgKm!=null ? ` · Ø Entfernung: ${avgKm} km` : "");
    // table
    logBody.innerHTML = "";
    state.measurements.forEach(m=>{
      const tr = document.createElement('tr');
      const td = v => { const c = document.createElement('td'); c.textContent = v; return c; };
      tr.appendChild(td(fmtTime(m.t)));
      tr.appendChild(td(m.type==='flash'?'Blitz':(m.type==='thunder'?'Donner':(m.type==='storm_start'?'Start':'Ende'))));
      tr.appendChild(td(m.deltaSec ?? ""));
      tr.appendChild(td(m.km ?? ""));
      tr.appendChild(td(m.lat!=null ? round2(m.lat): ""));
      tr.appendChild(td(m.lon!=null ? round2(m.lon): ""));
      tr.appendChild(td(m.acc ?? ""));
      tr.appendChild(td(m.stormId ?? ""));
      logBody.appendChild(tr);
    });
    updateLocLine(); setTimeout(placeDot, 0);
  }
  render();

  // Simple month rollover
  const last = state.lastSaved ? new Date(state.lastSaved) : null;
  if (last){
    const now = new Date();
    if (now.getMonth()!==last.getMonth() || now.getFullYear()!==last.getFullYear()){
      state.stormsThisMonth = 0; save();
    }
  }

  // Ask for location once on first load (non-blocking)
  setTimeout(()=>{ requestLocation(); }, 500);

  // --------------------------------------------------------------------------------
  // NEUER JAVASCRIPT-CODE für Wetterdaten
  // Dieser Code ruft die Wetterdaten vom Flask-Server ab und zeigt sie an.
  // --------------------------------------------------------------------------------
  async function fetchAndDisplayWeather() {
      const weatherInfoDiv = document.getElementById('weather-info');
      weatherInfoDiv.innerHTML = "Wetterdaten werden geladen...";
      try {
          // fetch vom `/weather` endpoint
          const response = await fetch('/weather');
          if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.error || 'Fehler beim Abrufen der Wetterdaten.');
          }
          const data = await response.json();
          weatherInfoDiv.innerHTML = `
              <strong>Wetterdaten für Apple Park:</strong><br>
              <strong>Ort:</strong> ${data.Ort}, ${data.Land}<br>
              <strong>Temperatur:</strong> ${data.Temperatur}<br>
              <strong>Beschreibung:</strong> ${data.Wetterbeschreibung}<br>
              <strong>Gefühlt:</strong> ${data.Gefühlte_Temperatur}<br>
              <strong>Luftfeuchtigkeit:</strong> ${data.Luftfeuchtigkeit}<br>
              <strong>Windgeschwindigkeit:</strong> ${data.Windgeschwindigkeit}
          `;
      } catch (error) {
          console.error(error);
          weatherInfoDiv.innerHTML = `
              <span style="color: var(--danger);">Fehler: ${error.message}</span>
              <br>
              Bitte stellen Sie sicher, dass Sie den OpenWeatherMap API-Schlüssel im Python-Skript
              aktualisiert haben.
          `;
      }
  }

  // Abrufen der Wetterdaten beim Laden der Seite
  document.addEventListener('DOMContentLoaded', fetchAndDisplayWeather);

})();
</script>
</body>
</html>
"""

# --------------------------------------------------------------------------------
# Flask-Endpunkte
# --------------------------------------------------------------------------------

@app.route("/")
def render_app():
    """
    Dieser Endpunkt stellt die HTML-Seite für die Benutzeroberfläche bereit.
    """
    return render_template_string(HTML_TEMPLATE)

@app.route("/weather")
def get_apple_weather():
    """
    Dieser Endpunkt ruft die aktuellen Wetterdaten für Apple Park ab und gibt sie als JSON-Daten zurück.
    """
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        # Überprüfen, ob der Benutzer einen API-Schlüssel bereitgestellt hat.
        return jsonify({"error": "Bitte ersetzen Sie 'YOUR_API_KEY_HERE' durch Ihren echten OpenWeatherMap API-Schlüssel."}), 500

    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={APPLE_PARK_LAT}&lon={APPLE_PARK_LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=de"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()

        main_weather = weather_data.get('main', {})
        weather_description = weather_data.get('weather', [{}])[0].get('description', 'Nicht verfügbar')
        
        formatted_weather = {
            "Ort": weather_data.get('name', 'Cupertino'),
            "Land": weather_data.get('sys', {}).get('country', 'USA'),
            "Temperatur": f"{main_weather.get('temp', 'N/A')} °C",
            "Gefühlte_Temperatur": f"{main_weather.get('feels_like', 'N/A')} °C",
            "Wetterbeschreibung": weather_description.capitalize(),
            "Luftfeuchtigkeit": f"{main_weather.get('humidity', 'N/A')}%",
            "Windgeschwindigkeit": f"{weather_data.get('wind', {}).get('speed', 'N/A')} m/s"
        }
        
        return jsonify(formatted_weather)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Fehler beim Abrufen der Wetterdaten: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Ein unerwarteter Fehler ist aufgetreten: {e}"}), 500

#!/usr/bin/env python3
"""Parchea la guía Menorca: Google Maps, carrusel de fotos y extras reales."""
import re
import urllib.parse
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent
SOURCE = BASE / "source.html"

from images_data import DAYS, FULL_GMAPS, MAINS, EXTRAS, all_photos  # noqa: E402

EXTRA_CSS = """
    .gallery-hint{font-size:.78rem;color:var(--text-muted);margin-bottom:.65rem}
    .photo-carousel{position:relative;margin:1rem 0;border-radius:var(--radius-sm);overflow:hidden;background:var(--white);border:1px solid var(--sand-dark);box-shadow:var(--shadow)}
    .carousel-viewport{overflow:hidden;touch-action:pan-y pinch-zoom}
    .carousel-track{display:flex;transition:transform .35s ease;will-change:transform}
    .carousel-slide{min-width:100%;margin:0;flex-shrink:0}
    .carousel-open{display:block;width:100%;border:none;padding:0;background:none;cursor:zoom-in}
    .carousel-open img{width:100%;height:220px;object-fit:cover;display:block}
    .carousel-slide figcaption{padding:.65rem 1rem .75rem;font-size:.82rem;color:var(--text-muted);text-align:center;line-height:1.4;border-top:1px solid var(--sand-dark);min-height:2.8rem}
    .carousel-controls{display:flex;align-items:center;justify-content:center;gap:.75rem;padding:.5rem .75rem .65rem;background:var(--white)}
    .carousel-prev,.carousel-next{width:2.25rem;height:2.25rem;border-radius:50%;border:1px solid var(--sand-dark);background:var(--white);color:var(--sea);font-size:1.25rem;line-height:1;cursor:pointer}
    .carousel-dots{display:flex;gap:.35rem;flex-wrap:wrap;justify-content:center;max-width:60%}
    .carousel-dot{width:7px;height:7px;border-radius:50%;border:none;padding:0;background:var(--sand-dark);cursor:pointer}
    .carousel-dot.is-active{background:var(--sea);transform:scale(1.2)}
    .map-stack{border-radius:var(--radius-sm);overflow:hidden;border:1px solid var(--sand-dark);box-shadow:var(--shadow);margin:1.5rem 0 0}
    .map-tabs{display:flex;background:var(--white);border-bottom:1px solid var(--sand-dark)}
    .map-tab{flex:1;padding:.65rem .5rem;border:none;background:transparent;font-size:.82rem;font-weight:600;color:var(--text-muted);cursor:pointer}
    .map-tab.is-active{color:var(--sea);box-shadow:inset 0 -2px 0 var(--sea)}
    .map-panel{display:none}
    .map-panel.is-active{display:block}
    .gmap-embed{width:100%;height:380px;border:0;display:block}
    .map-stack .leaflet-map{height:380px;margin:0;border:none;border-radius:0}
    .map-stack .map-caption{margin:0}
    .spot-img{width:96px;height:76px;flex-shrink:0;border-radius:8px;border:none;cursor:pointer;padding:0;overflow:hidden}
    .spot-img img{width:100%;height:100%;object-fit:cover;display:block}
    .lightbox{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;padding:1rem}
    .lightbox.is-open{display:flex}
    .lightbox-inner{max-width:min(96vw,1100px);width:100%;display:flex;flex-direction:column;align-items:center;position:relative}
    .lightbox-img{max-width:100%;max-height:72vh;object-fit:contain;border-radius:8px;touch-action:pinch-zoom}
    .lightbox-cap{color:#fff;margin-top:.75rem;font-size:.9rem;text-align:center;max-width:640px;padding:0 .5rem}
    .lightbox-close{position:absolute;top:-2.5rem;right:0;width:2.5rem;height:2.5rem;border:none;border-radius:50%;background:rgba(255,255,255,.15);color:#fff;font-size:1.4rem;cursor:pointer}
    .lightbox-nav{position:absolute;top:50%;transform:translateY(-50%);width:2.75rem;height:2.75rem;border:none;border-radius:50%;background:rgba(255,255,255,.2);color:#fff;font-size:1.5rem;cursor:pointer}
    .lightbox-prev{left:.25rem}.lightbox-next{right:.25rem}
    @media(max-width:640px){.gmap-embed,.map-stack .leaflet-map{height:280px}.carousel-open img{height:180px}}
"""

EXTRA_JS = """
(function(){
  'use strict';
  function qs(s,r){return (r||document).querySelector(s)}
  function qsa(s,r){return Array.from((r||document).querySelectorAll(s))}

  /* Carruseles por día */
  qsa('.photo-carousel').forEach(function(car){
    var track=qs('.carousel-track',car),slides=qsa('.carousel-slide',car),dots=qs('.carousel-dots',car);
    var idx=0,n=slides.length;
    if(!track||!n)return;
    slides.forEach(function(_,i){
      var d=document.createElement('button');
      d.type='button';d.className='carousel-dot'+(i===0?' is-active':'');d.setAttribute('aria-label','Foto '+(i+1));
      d.addEventListener('click',function(){go(i)});dots.appendChild(d);
    });
    function go(i){
      idx=(i+n)%n;
      track.style.transform='translateX('+(-idx*100)+'%)';
      qsa('.carousel-dot',car).forEach(function(d,j){d.classList.toggle('is-active',j===idx)});
      slides.forEach(function(s,j){s.classList.toggle('is-active',j===idx)});
    }
    var sx=0,dx=0;
    track.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    track.addEventListener('touchend',function(e){dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(idx+(dx<0?1:-1))});
    var prev=qs('.carousel-prev',car),next=qs('.carousel-next',car);
    if(prev)prev.addEventListener('click',function(){go(idx-1)});
    if(next)next.addEventListener('click',function(){go(idx+1)});
    qsa('.carousel-open',car).forEach(function(btn){
      btn.addEventListener('click',function(){
        var i=parseInt(btn.getAttribute('data-index'),10)||0;
        openLightbox(car.getAttribute('data-carousel'),i);
      });
    });
  });

  /* Pestañas mapa Google / offline */
  qsa('.map-stack').forEach(function(stack){
    qsa('.map-tab',stack).forEach(function(tab){
      tab.addEventListener('click',function(){
        var m=tab.getAttribute('data-map');
        qsa('.map-tab',stack).forEach(function(t){t.classList.toggle('is-active',t===tab)});
        qsa('.map-panel',stack).forEach(function(p){
          p.classList.toggle('is-active',p.classList.contains('map-panel--'+m));
        });
        if(m==='leaflet'){
          setTimeout(function(){
            if(window.L&&window.menorcaMaps){
              Object.keys(window.menorcaMaps).forEach(function(k){
                if(window.menorcaMaps[k])window.menorcaMaps[k].invalidateSize();
              });
            }
          },200);
        }
      });
    });
  });

  /* Lightbox con slide */
  var lb=document.getElementById('lightbox'),lbImg=lb&&qs('.lightbox-img',lb),lbCap=lb&&qs('.lightbox-cap',lb);
  var lbClose=lb&&qs('.lightbox-close',lb),lbPrev=lb&&qs('.lightbox-prev',lb),lbNext=lb&&qs('.lightbox-next',lb);
  var lbSet=[],lbIdx=0;
  function buildSets(){
    lbSet={};
    qsa('.photo-carousel').forEach(function(car){
      var id=car.getAttribute('data-carousel');
      lbSet[id]=qsa('.carousel-open',car).map(function(b){
        return{src:b.getAttribute('data-full'),cap:b.getAttribute('data-cap')||''};
      });
    });
  }
  function showLb(){
    if(!lb||!lbSet[lb.carouselId])return;
    var item=lbSet[lb.carouselId][lbIdx];
    if(!item)return;
    lbImg.src=item.src;lbImg.alt=item.cap;lbCap.textContent=item.cap;
  }
  window.openLightbox=function(id,i){
    buildSets();if(!lbSet[id]||!lbSet[id].length)return;
    lb.carouselId=id;lbIdx=i;showLb();lb.hidden=false;lb.classList.add('is-open');document.body.style.overflow='hidden';
  };
  function closeLb(){if(!lb)return;lb.classList.remove('is-open');lb.hidden=true;document.body.style.overflow='';lbImg.src=''}
  if(lbClose)lbClose.addEventListener('click',closeLb);
  if(lb)lb.addEventListener('click',function(e){if(e.target===lb)closeLb()});
  if(lbPrev)lbPrev.addEventListener('click',function(e){e.stopPropagation();lbIdx=(lbIdx-1+lbSet[lb.carouselId].length)%lbSet[lb.carouselId].length;showLb()});
  if(lbNext)lbNext.addEventListener('click',function(e){e.stopPropagation();lbIdx=(lbIdx+1)%lbSet[lb.carouselId].length;showLb()});
  document.addEventListener('keydown',function(e){
    if(!lb||!lb.classList.contains('is-open'))return;
    if(e.key==='Escape')closeLb();
    if(e.key==='ArrowLeft'&&lbPrev)lbPrev.click();
    if(e.key==='ArrowRight'&&lbNext)lbNext.click();
  });
  var lx=0;
  if(lb)lb.addEventListener('touchstart',function(e){lx=e.touches[0].clientX},{passive:true});
  if(lb)lb.addEventListener('touchend',function(e){
    var d=e.changedTouches[0].clientX-lx;if(Math.abs(d)<45)return;
    if(d<0&&lbNext)lbNext.click();else if(lbPrev)lbPrev.click();
  });

  /* Spot → abrir carrusel del día */
  qsa('.spot-img[data-carousel]').forEach(function(btn){
    btn.addEventListener('click',function(){
      openLightbox(btn.getAttribute('data-carousel'),parseInt(btn.getAttribute('data-index'),10)||0);
    });
  });
})();
"""

SPOT_LABEL_TO_KEY = {
    "Cala Macarelleta": "macarelleta",
    "Cala Macarella": "macarella",
    "Cala Galdana": "galdana",
    "Ciutadella": "ciutadella",
    "Cala Pregonda": "pregonda",
    "Fornells": "fornells",
    "Cap de Cavalleria": "cavalleria",
    "Es Mercadal": "mercadal",
    "Monte Toro": "toro",
    "Ferreries": "ferreries",
    "Cala Mitjana": "mitjana",
    "Cala en Porter": "cala_porter",
    "Cova d'en Xoroi": "cova_xoroi",
    "Punta Prima": "punta_prima",
    "Cala Binissafúller": "binissafuller",
    "Binibèquer Vell": "binibequer_vell",
    "Cala Binibèquer": "cala_binibequer",
    "S'Algar & Cales Coves": "salgar",
    "S'Algar": "salgar",
    "Maó (puerto)": "mao",
}


def gmaps_embed(stops):
    enc = [urllib.parse.quote_plus(s) for s in stops]
    if len(enc) == 1:
        return f"https://maps.google.com/maps?q={enc[0]}&z=11&output=embed"
    if len(enc) == 2:
        return f"https://maps.google.com/maps?saddr={enc[0]}&daddr={enc[1]}&dirflg=d&output=embed"
    mid = "+to:".join(enc[1:-1])
    return f"https://maps.google.com/maps?saddr={enc[0]}&daddr={mid}+to:{enc[-1]}&dirflg=d&output=embed"


def extra_url(file):
    p = file.rsplit(".", 1)
    thumb = f"{p[0]}_thumb.{p[1]}"
    return f"./images/{thumb}"


def photo_list(spot_keys):
    photos = []
    for key in spot_keys:
        m = MAINS[key]
        photos.append({
            "url": m["url"],
            "full": m["url"].replace("w=800", "w=1600"),
            "cap": m["cap"],
            "key": key,
        })
        for ex in EXTRAS.get(key, []):
            photos.append({
                "url": extra_url(ex["file"]),
                "full": f"./images/{ex['file']}",
                "cap": ex["cap"],
                "key": key,
            })
    return photos


def spot_index(day_spots, spot_key):
    photos = photo_list(day_spots)
    for i, p in enumerate(photos):
        if p["key"] == spot_key:
            return i
    return 0


def build_carousel(car_id, spot_keys):
    photos = photo_list(spot_keys)
    slides = []
    for i, p in enumerate(photos):
        slides.append(
            f'<figure class="carousel-slide{" is-active" if i == 0 else ""}">'
            f'<button type="button" class="carousel-open" data-index="{i}" data-full="{p["full"]}" data-cap="{p["cap"]}" aria-label="Ampliar foto {i+1}">'
            f'<img src="{p["url"]}" alt="{p["cap"]}" loading="lazy" decoding="async"></button>'
            f'<figcaption>{p["cap"]}</figcaption></figure>'
        )
    return (
        f'<p class="gallery-hint">Desliza o usa las flechas · Toca para ampliar con zoom</p>'
        f'<div class="photo-carousel" data-carousel="{car_id}">'
        f'<div class="carousel-viewport"><div class="carousel-track">{"".join(slides)}</div></div>'
        f'<div class="carousel-controls">'
        f'<button type="button" class="carousel-prev" aria-label="Anterior">‹</button>'
        f'<div class="carousel-dots" role="tablist"></div>'
        f'<button type="button" class="carousel-next" aria-label="Siguiente">›</button>'
        f'</div></div>'
    )


def build_map_stack(map_id, embed, caption):
    return f"""<div class="map-stack">
            <div class="map-tabs" role="tablist">
              <button type="button" class="map-tab is-active" data-map="google" role="tab">🗺️ Google Maps</button>
              <button type="button" class="map-tab" data-map="leaflet" role="tab">📍 Mapa offline</button>
            </div>
            <div class="map-panel map-panel--google is-active">
              <iframe class="gmap-embed" title="Ruta en Google Maps" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" src="{embed}"></iframe>
            </div>
            <div class="map-panel map-panel--leaflet">
              <div id="{map_id}" class="leaflet-map" role="img" aria-label="Mapa offline"></div>
            </div>
            <p class="map-caption">{caption}</p>
          </div>"""


def upgrade_spots(html, day_cfg):
    car_id = f"day{day_cfg['num']}"
    spots = day_cfg["spots"]

    def repl(m):
        label = m.group(1)
        body = m.group(2)
        key = SPOT_LABEL_TO_KEY.get(label.strip())
        if not key:
            return m.group(0)
        idx = spot_index(spots, key)
        url = MAINS[key]["url"]
        cap = MAINS[key]["cap"]
        img = (
            f'<button type="button" class="spot-img" data-carousel="{car_id}" data-index="{idx}" '
            f'aria-label="Ver fotos de {label}">'
            f'<img src="{url}" alt="{cap}" loading="lazy"></button>'
        )
        return f'<li class="spot-item">{img}{body}</li>'

    # Replace within each day-card - process per day section
    day_pattern = rf'(<p class="day-num">Día {day_cfg["num"]} ·.*?</article>)'
    dm = re.search(day_pattern, html, re.DOTALL)
    if not dm:
        return html
    section = dm.group(1)
    section_new = re.sub(
        r'<li class="spot-item">\s*<div class="spot-img"[^>]*aria-label="([^"]+)"[^>]*></div>\s*(<div class="spot-body">.*?</li>)',
        repl,
        section,
        flags=re.DOTALL,
    )
    return html.replace(section, section_new, 1)


def main():
    src = SOURCE if SOURCE.exists() else ROOT / "menorca-pwa" / "index.html"
    if not src.exists():
        raise SystemExit(f"No se encuentra fuente: {src}")
    html = src.read_text(encoding="utf-8")

    # CSS
    if ".photo-carousel" not in html:
        html = html.replace(
            "    .day-gallery {\n      display: flex;\n",
            "    .day-gallery { display: none !important;\n",
        )
        html = html.replace("    /* ── RESPONSIVE ── */", EXTRA_CSS + "\n    /* ── RESPONSIVE ── */")

    # Reemplazar galerías (5 días en orden)
    for day in DAYS:
        car = build_carousel(f"day{day['num']}", day["spots"])
        html = re.sub(r'<div class="day-gallery">.*?</div>', car, html, count=1, flags=re.DOTALL)

    # Mapas por día
    for day in DAYS:
        embed = gmaps_embed(day["gmaps"])
        stack = build_map_stack(day["map_id"], embed, "Ruta interactiva · Cambia a mapa offline sin conexión")
        html = re.sub(
            r'<div class="map-wrap">\s*<div id="' + day["map_id"] + r'" class="leaflet-map"[^>]*></div>\s*<p class="map-caption">[^<]*</p>\s*</div>',
            stack,
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = upgrade_spots(html, day)

    # Mapa ruta completa
    full_embed = gmaps_embed(FULL_GMAPS)
    full_stack = build_map_stack("map-full-route", full_embed, "~220 km · 5 días · Google Maps requiere conexión")
    html = re.sub(
        r'<div class="map-wrap map-wrap--fullroute">\s*<div id="map-full-route"[^>]*></div>\s*<p class="map-caption">[^<]*</p>\s*</div>',
        f'<div class="map-wrap map-wrap--fullroute">{full_stack}</div>',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Actualizar textos btn-map
    html = html.replace("📍 Ver ruta en Google Maps", "📍 Abrir ruta en app Google Maps")

    # Lightbox + JS
    if 'id="lightbox"' not in html:
        html = html.replace(
            "<script>\n(function () {\n  'use strict';\n  if ('serviceWorker' in navigator)",
            """<div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Galería ampliada">
    <div class="lightbox-inner">
      <button type="button" class="lightbox-close" aria-label="Cerrar">×</button>
      <button type="button" class="lightbox-prev" aria-label="Anterior">‹</button>
      <img class="lightbox-img" src="" alt="">
      <button type="button" class="lightbox-next" aria-label="Siguiente">›</button>
      <p class="lightbox-cap"></p>
    </div>
  </div>
<script>
""" + EXTRA_JS + """
</script>
<script>
(function () {
  'use strict';
  if ('serviceWorker' in navigator)""",
        )

    # Exponer maps para invalidateSize
    html = html.replace("  var maps = {};", "  var maps = {};\n  window.menorcaMaps = maps;")

    out = BASE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Written {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

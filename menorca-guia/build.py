#!/usr/bin/env python3
"""Genera guía Menorca: tira de fotos, lightbox, solo Google Maps."""
import re
import urllib.parse
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent
SOURCE = BASE / "source.html"

from images_data import DAYS, MAINS, EXTRAS  # noqa: E402

DAY_TAB_LABELS = {
    1: "D1 · Sur",
    2: "D2 · Norte",
    3: "D3 · Interior",
    4: "D4 · Cavalls",
    5: "D5 · Sureste",
}

EXTRA_CSS = """
    .gallery-hint{font-size:.78rem;color:var(--text-muted);margin-bottom:.65rem}
    .gallery-thumb{border:none;padding:0;background:none;cursor:zoom-in;flex-shrink:0;scroll-snap-align:start;border-radius:var(--radius-sm);overflow:hidden;box-shadow:var(--shadow);position:relative}
    .gallery-thumb::after{content:'🔍';position:absolute;right:.35rem;bottom:.3rem;font-size:.7rem;background:rgba(0,0,0,.45);color:#fff;padding:.12rem .3rem;border-radius:5px}
    .gallery-thumb img{height:130px;width:auto;min-width:200px;max-width:280px;object-fit:cover;display:block}
    .gmap-only .gmap-embed{width:100%;height:380px;border:0;display:block}
    .gmap-only .map-caption{margin:0}
    .full-routes-overview{border-radius:var(--radius-sm);overflow:hidden;border:1px solid var(--sand-dark);box-shadow:var(--shadow)}
    .route-day-tabs{display:flex;flex-wrap:wrap;background:var(--white);border-bottom:1px solid var(--sand-dark)}
    .route-day-tab{flex:1;min-width:4.5rem;padding:.6rem .35rem;border:none;background:transparent;font-size:.72rem;font-weight:600;color:var(--text-muted);cursor:pointer}
    .route-day-tab.is-active{color:var(--sea);box-shadow:inset 0 -2px 0 var(--sea);background:var(--sea-pale)}
    .route-day-panel{display:none}
    .route-day-panel.is-active{display:block}
    .route-day-panel .gmap-embed{width:100%;height:420px;border:0;display:block}
    .spot-img{width:96px;height:76px;flex-shrink:0;border-radius:8px;border:none;cursor:pointer;padding:0;overflow:hidden}
    .spot-img img{width:100%;height:100%;object-fit:cover;display:block}
    .lightbox{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;padding:1rem}
    .lightbox.is-open{display:flex}
    .lightbox-inner{max-width:min(96vw,1100px);width:100%;display:flex;flex-direction:column;align-items:center;position:relative}
    .lightbox-img{max-width:100%;max-height:72vh;object-fit:contain;border-radius:8px;touch-action:pinch-zoom}
    .lightbox-cap{color:#fff;margin-top:.75rem;font-size:.9rem;text-align:center;max-width:640px;padding:0 .5rem;line-height:1.45}
    .lightbox-close{position:absolute;top:-2.5rem;right:0;width:2.5rem;height:2.5rem;border:none;border-radius:50%;background:rgba(255,255,255,.15);color:#fff;font-size:1.4rem;cursor:pointer}
    .lightbox-prev,.lightbox-next{position:absolute;top:50%;transform:translateY(-50%);width:2.75rem;height:2.75rem;border:none;border-radius:50%;background:rgba(255,255,255,.2);color:#fff;font-size:1.5rem;cursor:pointer}
    .lightbox-prev{left:.25rem}.lightbox-next{right:.25rem}
    @media(max-width:640px){.gmap-only .gmap-embed,.route-day-panel .gmap-embed{height:280px}.gallery-thumb img{height:110px;min-width:160px}}
"""

EXTRA_JS = """
(function(){
  'use strict';
  function qs(s,r){return (r||document).querySelector(s)}
  function qsa(s,r){return Array.from((r||document).querySelectorAll(s))}

  /* Pestañas mapa ruta general por día */
  qsa('.full-routes-overview').forEach(function(box){
    qsa('.route-day-tab',box).forEach(function(tab){
      tab.addEventListener('click',function(){
        var d=tab.getAttribute('data-day');
        qsa('.route-day-tab',box).forEach(function(t){t.classList.toggle('is-active',t===tab)});
        qsa('.route-day-panel',box).forEach(function(p){
          p.classList.toggle('is-active',p.getAttribute('data-day')===d);
        });
      });
    });
  });

  /* Lightbox con slide */
  var lb=document.getElementById('lightbox'),lbImg=lb&&qs('.lightbox-img',lb),lbCap=lb&&qs('.lightbox-cap',lb);
  var lbClose=lb&&qs('.lightbox-close',lb),lbPrev=lb&&qs('.lightbox-prev',lb),lbNext=lb&&qs('.lightbox-next',lb);
  var lbSet={},lbId='',lbIdx=0;

  function buildSets(){
    lbSet={};
    qsa('[data-gallery-strip]').forEach(function(strip){
      var id=strip.getAttribute('data-gallery-strip');
      lbSet[id]=qsa('.gallery-thumb',strip).map(function(b){
        return{src:b.getAttribute('data-full'),cap:b.getAttribute('data-cap')||''};
      });
    });
  }

  function showLb(){
    if(!lb||!lbSet[lbId]||!lbSet[lbId][lbIdx])return;
    var item=lbSet[lbId][lbIdx];
    lbImg.src=item.src;lbImg.alt=item.cap;lbCap.textContent=item.cap;
  }

  window.openLightbox=function(id,i){
    buildSets();
    if(!lbSet[id]||!lbSet[id].length)return;
    lbId=id;lbIdx=i;showLb();
    lb.hidden=false;lb.classList.add('is-open');document.body.style.overflow='hidden';
  };

  function closeLb(){
    if(!lb)return;
    lb.classList.remove('is-open');lb.hidden=true;
    document.body.style.overflow='';if(lbImg)lbImg.src='';
  }

  qsa('.gallery-thumb').forEach(function(btn){
    btn.addEventListener('click',function(){
      openLightbox(btn.getAttribute('data-gallery'),parseInt(btn.getAttribute('data-index'),10)||0);
    });
  });

  qsa('.spot-img[data-gallery]').forEach(function(btn){
    btn.addEventListener('click',function(){
      openLightbox(btn.getAttribute('data-gallery'),parseInt(btn.getAttribute('data-index'),10)||0);
    });
  });

  if(lbClose)lbClose.addEventListener('click',closeLb);
  if(lb)lb.addEventListener('click',function(e){if(e.target===lb)closeLb()});
  if(lbPrev)lbPrev.addEventListener('click',function(e){e.stopPropagation();lbIdx=(lbIdx-1+lbSet[lbId].length)%lbSet[lbId].length;showLb()});
  if(lbNext)lbNext.addEventListener('click',function(e){e.stopPropagation();lbIdx=(lbIdx+1)%lbSet[lbId].length;showLb()});
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


def gmaps_menorca():
    return "https://maps.google.com/maps?q=Menorca,+Islas+Baleares,+Espa%C3%B1a&z=10&output=embed"


def extra_url(file):
    p = file.rsplit(".", 1)
    return f"./images/{p[0]}_thumb.{p[1]}"


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
    for i, p in enumerate(photo_list(day_spots)):
        if p["key"] == spot_key:
            return i
    return 0


def build_gallery_strip(gal_id, spot_keys):
    photos = photo_list(spot_keys)
    items = []
    for i, p in enumerate(photos):
        items.append(
            f'<button type="button" class="gallery-thumb" data-gallery="{gal_id}" data-index="{i}" '
            f'data-full="{p["full"]}" data-cap="{p["cap"]}" aria-label="Ampliar: {p["cap"]}">'
            f'<img src="{p["url"]}" alt="{p["cap"]}" loading="lazy" decoding="async"></button>'
        )
    return (
        '<p class="gallery-hint">Toca cualquier miniatura para ampliar · Desliza entre fotos en el zoom</p>'
        f'<div class="day-gallery" data-gallery-strip="{gal_id}">{"".join(items)}</div>'
    )


def build_gmap_wrap(embed, caption="Ruta interactiva en Google Maps"):
    return f"""<div class="map-wrap gmap-only">
            <iframe class="gmap-embed" title="Ruta en Google Maps" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" src="{embed}"></iframe>
            <p class="map-caption">{caption}</p>
          </div>"""


def build_full_routes_overview():
    tabs = []
    panels = []
    for day in DAYS:
        n = day["num"]
        active = " is-active" if n == 1 else ""
        tabs.append(
            f'<button type="button" class="route-day-tab{active}" data-day="{n}" role="tab">'
            f'{DAY_TAB_LABELS[n]}</button>'
        )
        embed = gmaps_embed(day["gmaps"])
        panels.append(
            f'<div class="route-day-panel{active}" data-day="{n}" role="tabpanel">'
            f'<iframe class="gmap-embed" title="Ruta día {n}" loading="lazy" allowfullscreen '
            f'referrerpolicy="no-referrer-when-downgrade" src="{embed}"></iframe></div>'
        )
    return (
        f'<div class="full-routes-overview">'
        f'<div class="route-day-tabs" role="tablist">{"".join(tabs)}</div>'
        f'{"".join(panels)}</div>'
    )


def upgrade_spots(html, day_cfg):
    gal_id = f"day{day_cfg['num']}"
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
            f'<button type="button" class="spot-img" data-gallery="{gal_id}" data-index="{idx}" '
            f'aria-label="Ver fotos de {label}">'
            f'<img src="{url}" alt="{cap}" loading="lazy"></button>'
        )
        return f"<li class=\"spot-item\">{img}{body}</li>"

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


def strip_leaflet(html):
    html = re.sub(
        r"\n    \.leaflet-pane,.*?(?=\n    \.map-wrap)",
        "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<script>\n/\* Leaflet 1\.9\.4.*?</script>\n\n",
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html


def inject_assets(html):
    if 'id="lightbox"' in html:
        return html
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
    return html


def main():
    src = SOURCE if SOURCE.exists() else ROOT / "menorca-pwa" / "index.html"
    html = src.read_text(encoding="utf-8")

    if ".gallery-thumb" not in html:
        html = html.replace("    /* ── RESPONSIVE ── */", EXTRA_CSS + "\n    /* ── RESPONSIVE ── */")

    html = strip_leaflet(html)

    html = html.replace(
        "Los cinco días en un solo mapa interactivo. Cada color es un día de ruta; toca los marcadores numerados para ver cada parada. Funciona offline en iPhone y iPad.",
        "Las cinco rutas en Google Maps centradas en Menorca. Elige un día en las pestañas para ver su recorrido interactivo.",
    )
    html = html.replace(
        "Menorca mide ~47 km de este a oeste y ~17 km de norte a sur. Mapa interactivo offline: pellizca para zoom, arrastra para mover. Sin conexión necesaria.",
        "Menorca mide ~47 km de este a oeste y ~17 km de norte a sur. Vista general en Google Maps.",
    )

    for day in DAYS:
        gal = build_gallery_strip(f"day{day['num']}", day["spots"])
        html = re.sub(r"<div class=\"day-gallery\">.*?</div>", gal, html, count=1, flags=re.DOTALL)

    for day in DAYS:
        embed = gmaps_embed(day["gmaps"])
        gmap = build_gmap_wrap(embed)
        html = re.sub(
            r'<div class="map-wrap">\s*<div id="' + day["map_id"] + r'" class="leaflet-map"[^>]*></div>\s*<p class="map-caption">[^<]*</p>\s*</div>',
            gmap,
            html,
            count=1,
            flags=re.DOTALL,
        )
        html = upgrade_spots(html, day)

    overview = build_full_routes_overview()
    html = re.sub(
        r'<div class="map-wrap map-wrap--fullroute">\s*<div id="map-full-route"[^>]*></div>\s*<p class="map-caption">[^<]*</p>\s*</div>',
        f'<div class="map-wrap map-wrap--fullroute">{overview}<p class="map-caption">Selecciona un día · Rutas interactivas en Menorca · ~220 km totales</p></div>',
        html,
        count=1,
        flags=re.DOTALL,
    )

    menorca_map = build_gmap_wrap(gmaps_menorca(), "Menorca — vista general (Google Maps)")
    html = re.sub(
        r'<div class="map-wrap map-wrap--overview">\s*<div id="map-overview"[^>]*></div>\s*<p class="map-caption">[^<]*</p>\s*</div>',
        menorca_map.replace("gmap-only", "gmap-only map-wrap--overview"),
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace("📍 Ver ruta en Google Maps", "📍 Abrir ruta en app Google Maps")
    html = html.replace("Funciona offline en iPhone y iPad", "Requiere conexión para mapas Google")
    html = inject_assets(html)

    out = BASE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Written {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

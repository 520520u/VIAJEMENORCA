"""Imágenes por sitio: principal Unsplash (sin cambiar) + extras reales (Commons, locales)."""

# Principal: se mantiene la foto Unsplash actual
MAINS = {
    "macarelleta": {
        "url": "https://images.unsplash.com/photo-1747752419876-50b8d12d68f2?w=800&q=80",
        "cap": "Cala Macarelleta — agua turquesa y rocas de piedra",
    },
    "macarella": {
        "url": "https://images.unsplash.com/photo-1651918858137-d3d484d35854?w=800&q=80",
        "cap": "Cala Macarella — la cala icónica del sur",
    },
    "galdana": {
        "url": "https://images.unsplash.com/photo-1592634186523-484938bc3c22?w=800&q=80",
        "cap": "Cala Galdana — bahía amplia entre pinos",
    },
    "ciutadella": {
        "url": "https://images.unsplash.com/photo-1663790161767-cba32a06bbfd?w=800&q=80",
        "cap": "Ciutadella — calles medievales y puerto",
    },
    "pregonda": {
        "url": "https://images.unsplash.com/photo-1692285629272-a4fb26a2bcc5?w=800&q=80",
        "cap": "Cala Pregonda — arena rojiza e isla central",
    },
    "fornells": {
        "url": "https://images.unsplash.com/photo-1670343587351-e5f98dfbea3e?w=800&q=80",
        "cap": "Fornells — pueblo marinero y caldereta",
    },
    "cavalleria": {
        "url": "https://images.unsplash.com/photo-1544572650-7e8d887baab6?w=800&q=80",
        "cap": "Cap de Cavalleria — faro sobre acantilados",
    },
    "mercadal": {
        "url": "https://images.unsplash.com/photo-1564087558267-9e36fae557b7?w=800&q=80",
        "cap": "Es Mercadal — corazón rural de la isla",
    },
    "toro": {
        "url": "https://images.unsplash.com/photo-1458628370679-1f7b2f6bd22b?w=800&q=80",
        "cap": "Monte Toro — punto más alto de Menorca",
    },
    "ferreries": {
        "url": "https://images.unsplash.com/photo-1568330265107-7dd078486284?w=800&q=80",
        "cap": "Ferreries — pueblo blanco del interior",
    },
    "mitjana": {
        "url": "https://images.unsplash.com/photo-1693910771501-f083fe7abd85?w=800&q=80",
        "cap": "Cala Mitjana — cala virgen entre acantilados",
    },
    "cala_porter": {
        "url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "cap": "Cala en Porter — acceso al Camí de Cavalls",
    },
    "cova_xoroi": {
        "url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80",
        "cap": "Cova d'en Xoroi — discoteca en la roca",
    },
    "punta_prima": {
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
        "cap": "Punta Prima — playa familiar del sureste",
    },
    "binissafuller": {
        "url": "https://images.unsplash.com/photo-1592634378917-49e37742ee21?w=800&q=80",
        "cap": "Cala Binissafúller — cala pequeña y tranquila",
    },
    "binibequer_vell": {
        "url": "https://images.unsplash.com/photo-1598345042882-4448d0ed51de?w=800&q=80",
        "cap": "Binibèquer Vell — laberinto blanco junto al mar",
    },
    "cala_binibequer": {
        "url": "https://images.unsplash.com/photo-1592634214635-d4ae889d9621?w=800&q=80",
        "cap": "Cala Binibèquer — cala de pescadores",
    },
    "salgar": {
        "url": "https://images.unsplash.com/photo-1747752419876-50b8d12d68f2?w=800&q=80",
        "cap": "S'Algar — aguas cristalinas del sureste",
    },
    "mao": {
        "url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80",
        "cap": "Maó — uno de los puertos naturales más grandes del mundo",
    },
}

# Extras: descargados de Wikimedia → ./images/{key}_eN.jpg
EXTRAS = {
    "macarelleta": [
        {"file": "macarelleta_e1.jpg", "cap": "Cala Macarelleta — vista desde el sendero (Wikimedia)"},
    ],
    "macarella": [
        {"file": "macarella_e1.jpg", "cap": "Cala Macarella — bahía completa (Wikimedia)"},
    ],
    "galdana": [
        {"file": "galdana_e1.jpg", "cap": "Cala Galdana desde el mirador (Wikimedia)"},
    ],
    "ciutadella": [
        {"file": "ciutadella_e1.jpg", "cap": "Ciutadella y su puerto (Wikimedia)"},
        {"file": "ciutadella_e2.jpg", "cap": "Catedral de Ciutadella — interior (Wikimedia)"},
    ],
    "pregonda": [
        {"file": "pregonda_e1.jpg", "cap": "Cala Pregonda — paisaje rojizo (Wikimedia)"},
        {"file": "pregonda_e2.jpg", "cap": "La Pregonda desde el camino (Wikimedia)"},
    ],
    "fornells": [
        {"file": "fornells_e1.jpg", "cap": "Bahía de Fornells (Wikimedia)"},
    ],
    "cavalleria": [
        {"file": "cavalleria_e1.jpg", "cap": "Faro de Cavalleria (Wikimedia)"},
        {"file": "cavalleria_e2.jpg", "cap": "Acantilados de Cavalleria (Wikimedia)"},
    ],
    "mercadal": [
        {"file": "mercadal_e1.jpg", "cap": "Es Mercadal — centro del municipio (Wikimedia)"},
    ],
    "toro": [
        {"file": "toro_e1.jpg", "cap": "Camino al Monte Toro (Wikimedia)"},
        {"file": "toro_e2.jpg", "cap": "Vistas desde El Toro (Wikimedia)"},
    ],
    "ferreries": [
        {"file": "ferreries_e1.jpg", "cap": "Ferreries — calles del pueblo (Wikimedia)"},
    ],
    "mitjana": [
        {"file": "mitjana_e1.jpg", "cap": "Cala Mitjana — agua turquesa (Wikimedia)"},
        {"file": "mitjana_e2.jpg", "cap": "Entrada a Cala Mitjana (Wikimedia)"},
    ],
    "cala_porter": [
        {"file": "cala_porter_e1.jpg", "cap": "Cala en Porter — acantilados (Wikimedia)"},
    ],
    "cova_xoroi": [
        {"file": "cova_xoroi_e1.jpg", "cap": "Cova d'en Xoroi desde el mar (Wikimedia)"},
    ],
    "punta_prima": [
        {"file": "punta_prima_e1.jpg", "cap": "Playa de Punta Prima (Wikimedia)"},
    ],
    "binissafuller": [
        {"file": "binissafuller_e1.jpg", "cap": "Cala Binissafúller (Wikimedia)"},
    ],
    "binibequer_vell": [
        {"file": "binibequer_e1.jpg", "cap": "Binibèquer — arquitectura blanca (Wikimedia)"},
        {"file": "binibequer_e2.jpg", "cap": "Binibeca Vell — calles junto al mar (Wikimedia)"},
    ],
    "cala_binibequer": [
        {"file": "binibequer_e2.jpg", "cap": "Cala Binibèquer — barcas de pesca (Wikimedia)"},
    ],
    "salgar": [
        {"file": "salgar_e1.jpg", "cap": "Cala Alcalfar — sureste de Menorca (Wikimedia)"},
    ],
    "mao": [
        {"file": "mao_e1.jpg", "cap": "Puerto de Maó (Wikimedia)"},
        {"file": "mao_e2.jpg", "cap": "Bahía de Maó — vista histórica (Wikimedia)"},
    ],
}

# URLs remotas para descargar extras (Commons)
REMOTE = {
    "macarelleta_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Cala_Macarelleta_%2829504027804%29.jpg",
    "macarella_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/2/24/Cala_Macarella.jpg",
    "galdana_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Cala_Galdana%2C_Menorca.jpg",
    "ciutadella_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/45/Ciutadella_in_Menorca.jpg",
    "ciutadella_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/6/60/Cathedral_de_Menorca_Innen_1.jpg",
    "pregonda_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/06/Cala_Pregonda%2C_Menorca_-_50245703838.jpg",
    "pregonda_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/84/Benimel_La_Pregonda_%28263820141%29.jpeg",
    "fornells_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Bay_of_Fornells%2C_Minorca.jpg",
    "cavalleria_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Cavalleria_lighthouse.jpg",
    "cavalleria_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/52/2007_06_28_-_Far_de_Cavalleria_00_%287381726180%29.jpg",
    "mercadal_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Christmas_in_Es_Mercadal_%28Es_Mercadal%29.jpg",
    "toro_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/5/55/View_from_El_Toro.jpg",
    "toro_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/41/Holiday_in_Menorca_May_June_2013_%288948147885%29.jpg",
    "ferreries_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Ferreries-JoanHuguet.jpg",
    "mitjana_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/80/Cala_Mitjana%2C_Menorca_-_50127521481.jpg",
    "mitjana_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/10/Cala_Mitjana_03.jpg",
    "cala_porter_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/3/33/Cala%27n_Porter_%28Menorca%29.JPG",
    "cova_xoroi_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Calan_n_Porter%2C_Cueva_d%27en_Xoroi_-_panoramio.jpg",
    "punta_prima_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b6/Playa_de_Punta_Prima.jpg",
    "binissafuller_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Binissafuller.jpg",
    "binibequer_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/47/Beca.jpg",
    "binibequer_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Binibeca_Vell%2C_Menorca.jpg",
    "salgar_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/01/Cala_Alcalfar_%28T%C3%A9rmino_municipal_de_Sant_Lluis_-_Menorca%29.jpg",
    "mao_e1.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Puerto_de_Ma%C3%B3_20221230_001.jpg",
    "mao_e2.jpg": "https://upload.wikimedia.org/wikipedia/commons/c/cd/A_draught_of_the_town_and_harbour_of_Mahon_%28BM_Y%2C4.89%29.jpg",
}

DAYS = [
    {
        "num": 1,
        "spots": ["macarelleta", "macarella", "galdana", "ciutadella"],
        "gmaps": ["Maó, Menorca", "Cala Macarelleta, Menorca", "Cala Macarella, Menorca", "Ciutadella de Menorca"],
        "map_id": "map-day1",
        "day_key": "day1",
    },
    {
        "num": 2,
        "spots": ["pregonda", "fornells", "cavalleria", "mercadal"],
        "gmaps": ["Maó, Menorca", "Cala Pregonda, Es Mercadal, Menorca", "Fornells, Menorca", "Cap de Cavalleria, Menorca"],
        "map_id": "map-day2",
        "day_key": "day2",
    },
    {
        "num": 3,
        "spots": ["toro", "mercadal", "ferreries", "mitjana"],
        "gmaps": ["Maó, Menorca", "Monte Toro, Menorca", "Ferreries, Menorca", "Cala Mitjana, Ferreries, Menorca"],
        "map_id": "map-day3",
        "day_key": "day3",
    },
    {
        "num": 4,
        "spots": ["cala_porter", "cova_xoroi", "punta_prima", "binissafuller"],
        "gmaps": ["Cala en Porter, Menorca", "Cova d'en Xoroi, Menorca", "Punta Prima, Menorca", "Cala Binissafúller, Menorca"],
        "map_id": "map-day4",
        "day_key": "day4",
    },
    {
        "num": 5,
        "spots": ["binibequer_vell", "cala_binibequer", "salgar", "mao"],
        "gmaps": ["Maó, Menorca", "Binibèquer Vell, Menorca", "Cala Binibèquer, Menorca", "S'Algar, Menorca", "Maó, Menorca"],
        "map_id": "map-day5",
        "day_key": "day5",
    },
]

FULL_GMAPS = [
    "Maó, Menorca", "Cala Macarella, Menorca", "Ciutadella de Menorca",
    "Cala Pregonda, Menorca", "Fornells, Menorca",
    "Monte Toro, Menorca", "Cala Mitjana, Menorca",
    "Cala en Porter, Menorca", "Binibèquer Vell, Menorca",
]


def all_photos(spot_keys):
    """Lista de {url, full, cap} — principal primero, luego extras."""
    photos = []
    for key in spot_keys:
        m = MAINS[key]
        photos.append({"url": m["url"], "full": m["url"].replace("w=800", "w=1600"), "cap": m["cap"]})
        for ex in EXTRAS.get(key, []):
            path = f"./images/{ex['file']}"
            photos.append({"url": path, "full": path, "cap": ex["cap"]})
    return photos

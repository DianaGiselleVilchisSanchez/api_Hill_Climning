from flask import Flask, render_template, request, jsonify
import math
import random
import os

app = Flask(__name__)

# Coordenadas fijas
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord_local):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord_local[ciudad1], coord_local[ciudad2])
    total += distancia(coord_local[ruta[-1]], coord_local[ruta[0]])
    return total

def hill_climbing(ciudades):
    coord_local = {c: coord[c] for c in ciudades}
    ruta = list(coord_local.keys())
    random.shuffle(ruta)

    mejora = True
    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta, coord_local)
        for i in range(len(ruta)):
            if mejora:
                break
            for j in range(len(ruta)):
                if i != j:
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp, coord_local)
                    if dist < dist_actual:
                        mejora = True
                        ruta = ruta_tmp
                        break
    return ruta, evalua_ruta(ruta, coord_local)

@app.route('/')
def index():
    return render_template('index.html', ciudades=coord.keys())

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    ciudades_seleccionadas = data.get('ciudades', [])
    
    if not ciudades_seleccionadas:
        return jsonify({'error': 'No seleccionaste ciudades'}), 400

    ruta, distancia_total = hill_climbing(ciudades_seleccionadas)
    return jsonify({
        'ruta': ruta,
        'distancia': round(distancia_total, 2)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

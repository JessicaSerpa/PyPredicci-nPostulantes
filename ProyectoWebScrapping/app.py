from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Leer y combinar los CSV de unmsm al inicio
df_2023 = pd.read_csv("data/ingresantes_unmsm_2023-2.csv")
df_2024_1 = pd.read_csv("data/ingresantes_unmsm_2024-1.csv")
df_2024_2 = pd.read_csv("data/ingresantes_unmsm_2024-2.csv")

df_2023["Periodo"] = "2023-2"
df_2024_1["Periodo"] = "2024-1"
df_2024_2["Periodo"] = "2024-2"

df_total = pd.concat([df_2023, df_2024_1, df_2024_2], ignore_index=True)
df_total.fillna("", inplace=True)

# Datos villarreal
dfv_2023 = pd.read_csv("data/ingresantes_unfv_2023-2.csv")
dfv_2024_1 = pd.read_csv("data/ingresantes_unfv_2024-1.csv")
dfv_2024_2 = pd.read_csv("data/ingresantes_unfv_2024-2.csv")

dfv_2023["Periodo"] = "2023-2"
dfv_2024_1["Periodo"] = "2024-1"
dfv_2024_2["Periodo"] = "2024-2"

dfv_total = pd.concat([dfv_2023, dfv_2024_1, dfv_2024_2], ignore_index=True)
dfv_total.fillna("", inplace=True)

# Datos Uni
dfu_2023 = pd.read_csv("data/ingresantes_uni_2023-2.csv")
dfu_2024_1 = pd.read_csv("data/ingresantes_uni_2024-1.csv")
dfu_2024_2 = pd.read_csv("data/ingresantes_uni_2024-2.csv")

dfu_2023["Periodo"] = "2023-2"
dfu_2024_1["Periodo"] = "2024-1"
dfu_2024_2["Periodo"] = "2024-2"

dfu_total = pd.concat([dfu_2023, dfu_2024_1, dfu_2024_2], ignore_index=True)
dfu_total.fillna("", inplace=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/UNMSM")
def home():
    # Filtrar solo los que alcanzaron vacante en 2024-2
    df_filtrado = df_total[
        (df_total["Periodo"] == "2024-2") &
        (df_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]

    # Crear resumen de puntajes por carrera
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )

    # Enviamos el resumen al HTML
    return render_template("sanmarcos.html", resumen=resumen)


@app.route("/UNFV")
def unfv():
    # Filtrar solo los que alcanzaron vacante en 2024-2
    df_filtrado = dfv_total[
        (dfv_total["Periodo"] == "2024-2") &
        (dfv_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]

    # Crear resumen de puntajes por carrera
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )

    # Enviamos el resumen al HTML
    return render_template("villarreal.html", resumen=resumen)

@app.route("/UNI")
def uni():
    # Filtrar solo los que alcanzaron vacante en 2024-2
    df_filtrado = dfu_total[
        (dfu_total["Periodo"] == "2024-2") &
        (dfu_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]

    # Crear resumen de puntajes por carrera
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )

    # Enviamos el resumen al HTML
    return render_template("uni.html", resumen=resumen)


@app.route("/data-sanmarcos")
def dataSanMarcos():
    draw = request.args.get("draw", type=int)
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    search_value = request.args.get("search[value]", "")
    periodo_filtro = request.args.get("periodo", "2024-2")

    # Filtrar por periodo y búsqueda
    df_filtrado = df_total[df_total["Periodo"] == periodo_filtro]

    if search_value:
        df_filtrado = df_filtrado[df_filtrado.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    total = df_filtrado.shape[0]
    data = df_filtrado.iloc[start:start + length].to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    })

@app.route("/data-uni")
def dataUni():
    draw = request.args.get("draw", type=int)
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    search_value = request.args.get("search[value]", "")
    periodo_filtro = request.args.get("periodo", "2024-2")

    # Filtrar por periodo y búsqueda
    df_filtrado = dfu_total[dfu_total["Periodo"] == periodo_filtro]

    if search_value:
        df_filtrado = df_filtrado[df_filtrado.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    total = df_filtrado.shape[0]
    data = df_filtrado.iloc[start:start + length].to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    })

@app.route("/data-villarreal")
def dataVillarreal():
    draw = request.args.get("draw", type=int)
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    search_value = request.args.get("search[value]", "")
    periodo_filtro = request.args.get("periodo", "2024-2")

    # Filtrar por periodo y búsqueda
    df_filtrado = dfv_total[dfv_total["Periodo"] == periodo_filtro]

    if search_value:
        df_filtrado = df_filtrado[df_filtrado.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    total = df_filtrado.shape[0]
    data = df_filtrado.iloc[start:start + length].to_dict(orient="records")

    return jsonify({
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data
    })

@app.route("/predecir_carrera")
def predecir_carrera():
    try:
        puntaje = float(request.args.get("puntaje"))
    except:
        return jsonify({"error": "Puntaje inválido", "carreras": []})

    # Usar resumen del último periodo
    df_filtrado = df_total[
        (df_total["Periodo"] == "2024-2") & 
        (df_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]

    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
    )
    posibles = resumen[resumen["Puntaje_Min"] <= puntaje].sort_values("Puntaje_Min")
    # Puedes limitar a las 5 carreras más cercanas, si quieres
    carreras = posibles.to_dict(orient="records")
    # Opcional: cambia el nombre de columnas para JS (sin espacios)
    for c in carreras:
        c["Escuela_Profesional"] = c.pop("Escuela Profesional")
        c["Puntaje_Min"] = round(c["Puntaje_Min"],2)
    return jsonify({"carreras": carreras})


if __name__ == "__main__":
    app.run(debug=True)

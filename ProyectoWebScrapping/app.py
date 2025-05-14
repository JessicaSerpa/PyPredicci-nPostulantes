from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Leer y combinar todos los CSV al inicio
df_2023 = pd.read_csv("data/ingresantes_unmsm_2023-2.csv")
df_2024_1 = pd.read_csv("data/ingresantes_unmsm_2024-1.csv")
df_2024_2 = pd.read_csv("data/ingresantes_unmsm_2024-2.csv")

df_2023["Periodo"] = "2023-2"
df_2024_1["Periodo"] = "2024-1"
df_2024_2["Periodo"] = "2024-2"

df_total = pd.concat([df_2023, df_2024_1, df_2024_2], ignore_index=True)
df_total.fillna("", inplace=True)

@app.route("/")
def home():
    return render_template("sanmarcos.html")  # Nuevo template para server-side

@app.route("/data")
def data():
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

if __name__ == "__main__":
    app.run(debug=True)

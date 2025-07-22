from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import landscape

import pandas as pd
import os

app = Flask(__name__)

# Obtener ruta base del archivo actual
base_path = os.path.dirname(__file__)

# Función auxiliar para generar la ruta completa a los CSV
def ruta_csv(nombre_archivo):
    return os.path.join(base_path, "data", nombre_archivo)

# Leer y combinar los CSV de UNMSM
df_2023 = pd.read_csv(ruta_csv("ingresantes_unmsm_2023-2.csv"))
df_2024_1 = pd.read_csv(ruta_csv("ingresantes_unmsm_2024-1.csv"))
df_2024_2 = pd.read_csv(ruta_csv("ingresantes_unmsm_2024-2.csv"))

df_2023["Periodo"] = "2023-2"
df_2024_1["Periodo"] = "2024-1"
df_2024_2["Periodo"] = "2024-2"

df_total = pd.concat([df_2023, df_2024_1, df_2024_2], ignore_index=True)
df_total.fillna("", inplace=True)

# Datos UNFV
dfv_2023 = pd.read_csv(ruta_csv("ingresantes_unfv_2023-2.csv"))
dfv_2024_1 = pd.read_csv(ruta_csv("ingresantes_unfv_2024-1.csv"))
dfv_2024_2 = pd.read_csv(ruta_csv("ingresantes_unfv_2024-2.csv"))

dfv_2023["Periodo"] = "2023-2"
dfv_2024_1["Periodo"] = "2024-1"
dfv_2024_2["Periodo"] = "2024-2"

dfv_total = pd.concat([dfv_2023, dfv_2024_1, dfv_2024_2], ignore_index=True)
dfv_total.fillna("", inplace=True)

# Datos UNI
dfu_2023 = pd.read_csv(ruta_csv("ingresantes_uni_2023-2.csv"))
dfu_2024_1 = pd.read_csv(ruta_csv("ingresantes_uni_2024-1.csv"))
dfu_2024_2 = pd.read_csv(ruta_csv("ingresantes_uni_2024-2.csv"))

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
    df_filtrado = df_total[
        (df_total["Periodo"] == "2024-2") &
        (df_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )
    return render_template("sanmarcos.html", resumen=resumen)

@app.route("/UNFV")
def unfv():
    df_filtrado = dfv_total[
        (dfv_total["Periodo"] == "2024-2") &
        (dfv_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )
    return render_template("villarreal.html", resumen=resumen)

@app.route("/UNI")
def uni():
    df_filtrado = dfu_total[
        (dfu_total["Periodo"] == "2024-2") &
        (dfu_total["Observaciones"].str.contains("ALCANZO", na=False, case=False))
    ]
    resumen = (
        df_filtrado.groupby("Escuela Profesional")
        .agg(Puntaje_Min=("Puntaje final", "min"), Puntaje_Max=("Puntaje final", "max"))
        .reset_index()
        .sort_values("Puntaje_Max", ascending=False)
        .to_dict(orient="records")
    )
    return render_template("uni.html", resumen=resumen)

@app.route("/data-sanmarcos")
def dataSanMarcos():
    draw = request.args.get("draw", type=int)
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    search_value = request.args.get("search[value]", "")
    periodo_filtro = request.args.get("periodo", "2024-2")

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
    carreras = posibles.to_dict(orient="records")
    for c in carreras:
        c["Escuela_Profesional"] = c.pop("Escuela Profesional")
        c["Puntaje_Min"] = round(c["Puntaje_Min"], 2)

    return jsonify({"carreras": carreras})



@app.route("/exportar-excel/<universidad>")
def exportar_excel(universidad):
    from flask import send_file
    import io
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill

    periodo = request.args.get("periodo", "2024-2")
    search = request.args.get("search", "")

    if universidad == "UNMSM":
        df = df_total
    elif universidad == "UNI":
        df = dfu_total
    elif universidad == "UNFV":
        df = dfv_total
    else:
        return "Universidad no válida", 400

    df = df[df["Periodo"] == periodo]
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    wb = Workbook()
    ws = wb.active
    ws.title = "Ingresantes"

    # Estilos de cabecera
    bold_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    center_align = Alignment(horizontal="center")

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        ws.append(row)
        if r_idx == 1:
            for cell in ws[r_idx]:
                cell.font = bold_font
                cell.fill = header_fill
                cell.alignment = center_align

    # Activar filtro de columnas
    ws.auto_filter.ref = ws.dimensions

    # ➕ ANCHOS FIJOS por columna
    anchos_columnas = {
        "A": 12,  # Código
        "B": 18,  # Apellidos
        "C": 18,  # Nombres
        "D": 25,  # Escuela Profesional
        "E": 18,  # Puntaje final
        "F": 18,  # Mérito Alcanzado
        "G": 24,  # Observaciones
        "H": 18,  # Periodo
        "I": 25,  # Escuela Segunda Opción
    }
    for col, width in anchos_columnas.items():
        ws.column_dimensions[col].width = width

    # Guardar en memoria
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name="ingresantes_filtrados.xlsx"
    )

@app.route("/exportar-pdf/<universidad>")
def exportar_pdf(universidad):
    from flask import send_file
    import io
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    periodo = request.args.get("periodo", "2024-2")
    search = request.args.get("search", "")

    if universidad == "UNMSM":
        df = df_total
    elif universidad == "UNI":
        df = dfu_total
    elif universidad == "UNFV":
        df = dfv_total
    else:
        return "Universidad no válida", 400

    df = df[df["Periodo"] == periodo] 
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    # Creamos el buffer PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # Título
    title = Paragraph(f"<b>Reporte de Ingresantes UNMSM - Periodo: {periodo}</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Datos como tabla
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle

    # Estilo para encabezados con wrap
    header_style = ParagraphStyle(name="HeaderStyle", alignment=1, fontSize=8, textColor=colors.white, fontName="Helvetica-Bold")

    headers = [Paragraph(col, header_style) for col in df.columns]
    data = [headers] + df.astype(str).values.tolist()


    normal_style = ParagraphStyle(name="Normal", fontSize=8, leading=10)

    # Convertir los valores a string y usar Paragraph en campos largos
    def procesar_fila(row):
        nueva_fila = []
        for i, cell in enumerate(row):
            texto = str(cell)
            if i in [1, 2, 3, 6, 8]:  # columnas propensas a ser largas
                nueva_fila.append(Paragraph(texto, normal_style))
            else:
                nueva_fila.append(texto)
        return nueva_fila

    data = [data[0]] + [procesar_fila(row) for row in data[1:]]


    # Crear tabla
    col_widths = [60, 90, 90, 100, 60, 50, 90, 45, 110]  # Ajusta según columnas visibles

    table = Table(data, repeatRows=1, colWidths=col_widths)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('WORDWRAP', (0, 0), (-1, 0), 'CJK'),  # Wrap en encabezado
    ]))


    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"ingresantes_{universidad}_{periodo}.pdf", mimetype='application/pdf')



if __name__ == "__main__":
    app.run(debug=True)

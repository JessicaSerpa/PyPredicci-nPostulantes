import plotly.express as px

fig = px.bar(x=["A", "B", "C"], y=[1, 3, 2], title="Test")
fig.write_image("test.png")
print("✅ Imagen de prueba guardada")

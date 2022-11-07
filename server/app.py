from flask import Flask, render_template
import pandas as pd
import json
import matplotlib.pyplot as plt
rutaprincipal = "C:/Users/Usuario/Documents/CALA-Analytics";
nombredearchivo = "/ejercicio1_b1.xlsx";
carga = pd.read_excel(rutaprincipal + nombredearchivo); #concatenar  rutas de base de datos
datos = pd.DataFrame(carga) # cargar los datos en un data frame
datos.head()
datos1 = datos.iloc[:,0:4]
datos2 = datos1.dropna(); ## Eliminar valores nan
base1 = datos2.drop_duplicates(subset=["id"]); # Eliminar valores repetidos
base1 = base1.iloc[:,1:4]
base2 = pd.read_table('C:/Users/Usuario/Documents/CALA-Analytics/ejercicio1_b2.txt',)
calculo = pd.DataFrame({'EDAD': [- int(base2.iloc[0,3][6:10]) + 2014, - int(base2.iloc[1,3][6:10]) + 2014, - int(base2.iloc[2,3][6:10]) + 2014, - int(base2.iloc[3,3][6:10]) + 2014, - int(base2.iloc[4,3][6:10]) + 2014, - int(base2.iloc[5,3][6:10]) + 2014]}) ##Calcula edad de los clientes
base2 = pd.concat([base2, calculo], axis = 1) ##Ingresar calculo a la base de datos
base2['NOMBRECOMPLETO'] = base2.NOMBRE.str.cat(base2.APELLIDO, sep=' ') ##Unir variable nombre con apellido
cruce = pd.merge(base2,base1, left_on="CEDULA", right_on="cc_cliente"); ## Cruzar base de datos con identificación del cliente
cruce = cruce.rename(columns={'numero de pedido':'PEDIDO'})
cruce = cruce.rename(columns={'Tipo de pedido':'TIPO'})
cruce["NOMBRECOMPLETO"]= cruce["NOMBRECOMPLETO"].str.capitalize();
cruce = cruce.iloc[:,0:8]
result = cruce.to_json(orient="records")
parsed = json.loads(result)
app = Flask(__name__,template_folder="template")
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/api")
def get():
    return result
@app.route("/pedidos")
def datos():
    return render_template("pedidos.html", tabla = parsed, long = len(parsed))
@app.route("/graficos")
def grafi():
    plt.bar(cruce.iloc[:,5], cruce.iloc[:,6])
    x = plt.show()
    return render_template("graficos.html", x=x)
    
if __name__ == "__main__":
    app.run(debug=True)



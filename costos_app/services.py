import requests
from datetime import datetime, timedelta

def obtener_precio_real_nordpool_lituania():
    try:
        # Definimos el rango de fecha de hoy para traer los precios comerciales por hora
        hoy = datetime.now().strftime('%Y-%m-%d')
        mañana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # URL de la API pública de Elering para el mercado Nord Pool
        url = f"https://dashboard.elering.ee/api/nps/price?start={hoy}T00:00:00Z&end={mañana}T00:00:00Z"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print("No se pudo conectar con la API de Elering. Usando fallback corporativo.")
            return 0.18  # Tarifa promedio comercial de contingencia
            
        datos = response.json()
        
        # Buscamos el bloque de datos específico para Lituania ('lt')
        precios_lituania = datos.get('data', {}).get('lt', [])
        
        if not precios_lituania:
            return 0.18
            
        # La API devuelve el precio por cada hora del día en EUR/MWh (Megavatio-hora)
        # Tomamos el precio de la última hora registrada como referencia
        ultimo_precio_mwh = precios_lituania[-1].get('price')
        
        # PASO DE INGENIERÍA FINANCIERA: 
        # La API entrega EUR/MWh. Para pasarlo a Kilovatio-hora (kWh), dividimos entre 1000.
        precio_kwh_mayorista = float(ultimo_precio_mwh) / 1000.0
        
        # IMPORTANTE: El precio mayorista de la bolsa no incluye los costos de red locales (peajes/distribución).
        # En Lituania, para una tarifa comercial real, se le suma un aproximado de €0.10 por costos de distribución de la VERT.
        precio_final_comercial = precio_kwh_mayorista + 0.10
        
        print(f"¡Dato Real de Nord Pool extraído! Precio final comercial: €{round(precio_final_comercial, 4)}/kWh")
        return round(precio_final_comercial, 4)
        
    except Exception as e:
        print(f"Error al consultar la base de datos de Nord Pool: {e}")
        return 0.18
    

if __name__=='__main__':
    obtener_precio_real_nordpool_lituania()
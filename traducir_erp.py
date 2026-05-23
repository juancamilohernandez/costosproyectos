# traducir_erp.py
import os
import polib
from deep_translator import GoogleTranslator

def traducir_archivo_po(ruta_origen, ruta_destino, idioma_destino):
    if not os.path.exists(ruta_origen):
        print(f"❌ No se encontró el archivo base en: {ruta_origen}")
        return

    print(f"✨ Procesando idioma: [{idioma_destino}]...")
    
    po = polib.pofile(ruta_origen)
    traductor = GoogleTranslator(source='es', target=idioma_destino)
    traducidos = 0

    for entry in po:
        # Solo traducimos si el msgid existe y si el msgstr está completamente vacío
        if entry.msgid and not entry.msgstr:
            try:
                texto_traducido = traductor.translate(entry.msgid)
                
                # 🔥 VALIDACIÓN CLAVE: Solo guardar si Google realmente devolvió texto
                if texto_traducido:
                    print(f"   -> Traduciendo: '{entry.msgid}' -> '{texto_traducido}'")
                    entry.msgstr = str(texto_traducido) # Nos aseguramos de que sea un String válido
                    
                    if 'fuzzy' in entry.flags:
                        entry.flags.remove('fuzzy')
                    traducidos += 1
                else:
                    print(f"   ⚠️ Google devolvió vacío para: '{entry.msgid}'")
                    entry.msgstr = "" # Lo dejamos vacío temporalmente para no estallar polib
                    
            except Exception as e:
                print(f"   ⚠️ Error al traducir '{entry.msgid}': {e}")
                entry.msgstr = ""
        
    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
    
    # Intentar guardar el archivo de manera segura
    try:
        po.save(ruta_destino)
        print(f"✅ ¡Éxito! Se tradujeron {traducidos} etiquetas en: {ruta_destino}\n")
    except Exception as e:
        print(f"❌ Error crítico al guardar el archivo {ruta_destino}: {e}\n")

def main():
    RUTA_BASE_ES = 'locale/es/LC_MESSAGES/django.po'
    
    IDIOMAS_MAPA = {
        'es': 'es',
        'fi': 'fi',
        'et': 'et',
        'lt': 'lt',
        'lv': 'lv',
        'da': 'da',
        'de': 'de',
        'de-ch': 'de',
        'fr-ch': 'fr',
        'it-ch': 'it',
    }
    
    for django_locale, google_code in IDIOMAS_MAPA.items():
        if django_locale == 'es':
            continue
        ruta_salida = f'locale/{django_locale}/LC_MESSAGES/django.po'
        traducir_archivo_po(RUTA_BASE_ES, ruta_salida, google_code)

    print("🚀 [PROCESO TERMINADO] Ejecuta ahora 'python3 manage.py compilemessages'")

if __name__ == '__main__':
    main()
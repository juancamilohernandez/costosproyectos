import urllib.parse  # 🚀 IMPORTACIÓN OBLIGATORIA PARA CODIFICAR EL CSS/JS DINÁMICO
from django.contrib import admin
from .models import Pais, Rol, Empleado, Proyecto, AsignacionProyecto, FacturaFija, ActivoFijo, PresupuestoProyecto, PoliticaContratacion, RegistroEnergia
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

# Configuración global del encabezado del Admin
admin.site.site_header = "ERP FinTech - Panel de Control Financiero"
admin.site.site_title = "Auditoría NIC 16 / NIIF 16"
admin.site.index_title = "Gestión de Costos ABC & Presupuestos"

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_iso', 'salario_minimo', 'tasa_patronal_estandar', 'tasa_patronal_temporal')
    search_fields = ('nombre', 'codigo_iso')
    list_filter = ('codigo_iso',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre_cargo', 'tipo_contable')
    list_filter = ('tipo_contable',)
    search_fields = ('nombre_cargo',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'pais', 'tipo_contrato', 'salario_bruto_mensual', 'email_corporativo')
    list_filter = ('pais', 'tipo_contrato', 'rol__tipo_contable')
    search_fields = ('nombre', 'email_corporativo', 'rol__nombre_cargo')
    raw_id_fields = ('rol', 'pais') # Evita desplegables lentos si hay miles de filas
    
    # Agrupamos los campos estéticamente con fieldsets colapsables
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'email_corporativo', 'pais', 'rol')
        }),
        ('Detalles de Contratación & Nómina', {
            'fields': ('tipo_contrato', 'salario_bruto_mensual'),
        }),
        ('Historial / Provisiones NIIF (Lectura)', {
            'classes': ('collapse',), # Se puede colapsar en la interfaz
            'fields': ('costo_seguridad_social_mes', 'provision_prestaciones_mes'),
        }),
    )

class PresupuestoInline(admin.StackedInline):
    model = PresupuestoProyecto
    can_delete = False
    verbose_name_plural = 'Presupuesto Asignado (Techos Financieros)'

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio')
    search_fields = ('nombre',)
    inlines = [PresupuestoInline] # Permite editar el presupuesto directamente dentro del Proyecto

@admin.register(PresupuestoProyecto)
class PresupuestoProyectoAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'limite_costos', 'limite_gastos', 'presupuesto_total', 'actualizado_en')
    search_fields = ('proyecto__nombre',)

@admin.register(AsignacionProyecto)
class AsignacionProyectoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'proyecto', 'horas_dedicadas', 'mes_ano', 'costo_imputado_al_proyecto', 'responsable_proyecto')
    list_filter = ('mes_ano', 'proyecto')
    search_fields = ('empleado__nombre', 'proyecto__nombre')
    raw_id_fields = ('empleado', 'proyecto', 'responsable_proyecto', 'jefe_inmediato')

@admin.register(FacturaFija)
class FacturaFijaAdmin(admin.ModelAdmin):
    list_display = ('proveedor_o_concepto', 'monto', 'mes_ano', 'clasificacion', 'proyecto')
    list_filter = ('clasificacion', 'mes_ano', 'proyecto')
    search_fields = ('proveedor_o_concepto',)

@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ('nombre_activo', 'tipo_activo', 'empleado_asignado', 'valor_adquisicion', 'depreciacion_mensual', 'es_leasing')
    list_filter = ('tipo_activo', 'es_leasing')
    search_fields = ('nombre_activo',)
    
    fieldsets = (
        ('Identificación del Activo', {
            'fields': ('nombre_activo', 'tipo_activo', 'empleado_asignado')
        }),
        ('Métricas NIC 16 (Propiedad, Planta y Equipo)', {
            'fields': ('valor_adquisicion', 'vida_util_meses', 'fecha_adquisicion')
        }),
        ('Bloque NIIF 16 (Arrendamientos / Leasing)', {
            'classes': ('collapse',),
            'fields': ('es_leasing', 'tasa_interes_mensual', 'canon_mensual')
        }),
    )


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Preferencias de Idioma Internacional (ERP)'

# Desenlazamos el UserAdmin por defecto de Django para registrar el nuestro vitaminado
admin.site.unregister(User)

@admin.register(User)
class PersonalizadoUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)
    
    # 🎯 EL ESCUDO REPARADOR: Aquí integramos las sugerencias para salvar los íconos
    class Media:
        # Usamos inyección de CSS para indicarle al motor de renderizado que aísle el comportamiento de los símbolos
        css = {
            'all': (
                'data:text/css,' + urllib.parse.quote('''
                /* Evitamos que Google Translate altere o intente procesar las fuentes tipográficas de iconos */
                .material-icons, 
                .icon, 
                [class^="icon-"], 
                [class*=" icon-"],
                #branding h1, 
                #header,
                .notranslate {
                    unicode-bidi: isolate !important;
                }
                
                .material-icons, .icon, [class^="icon-"], [class*=" icon-"] {
                    content: attr(data-icon) !important;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                }
                ''')
            ,)
        }
        
        # Inyectamos el JavaScript dinámico que busca los elementos y les pone el atributo anti-traducción en caliente
        js = (
            'data:text/javascript,(' + urllib.parse.quote('''
            function() {
                document.addEventListener("DOMContentLoaded", function() {
                    // Detectamos los elementos que Django usa para los logos y barras de herramientas
                    var iconos = document.querySelectorAll('.material-icons, .icon, [class^="icon-"], [class*=" icon-"], #branding h1 a');
                    
                    iconos.forEach(function(el) {
                        // Le añadimos la clase nativa que el plugin de Chrome respeta para saltarse la traducción
                        el.classList.add('notranslate');
                        el.setAttribute('translate', 'no');
                    });
                    
                    console.log("🔒 Filtros anti-traducción acoplados con éxito a la botonera del admin.");
                });
            }
            ''') + ')();',
        )

# Registros faltantes menores para que no se quede nada por fuera
admin.site.register(PoliticaContratacion)
admin.site.register(RegistroEnergia)


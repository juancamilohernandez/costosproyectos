from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from decimal import Decimal
from django.db.models import Sum  # <--- 1. IMPORTAMOS EL SUMADOR DE DJANGO
from django.utils.translation import get_language  # <--- IMPORTANTE PARA LA REDIRECCIÓN DE IDIOMAS
from .models import Empleado, Proyecto, AsignacionProyecto, FacturaFija, ActivoFijo
from .forms import EmpleadoForm, AsignacionProyectoForm, ProyectoForm, FacturaFijaForm, ActivoFijoForm


@login_required
@never_cache
def registrar_empleado(request):
    """
    Vista corregida: No asignamos costo_total_mes directamente 
    porque es una @property (propiedad calculada en el modelo).
    """
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            
            salario = Decimal(str(empleado.salario_bruto_mensual))
            pais = empleado.pais
            
            # 1. Determinar tasa patronal según el contrato
            if empleado.tipo_contrato == 'FIJO':
                tasa_seguridad_social = Decimal(str(pais.tasa_patronal_temporal))
            else:
                tasa_seguridad_social = Decimal(str(pais.tasa_patronal_estandar))
            
            # 2. CÁLCULOS FINANCIEROS
            # Guardamos la Seguridad Social del mes
            empleado.costo_seguridad_social_mes = float(salario * tasa_seguridad_social)
            
            # Guardamos las Provisiones NIIF (21.83%)
            tasa_provisiones_niif = Decimal('0.2183')
            empleado.provision_prestaciones_mes = float(salario * tasa_provisiones_niif)
            
            # !!! ELIMINAMOS LA LÍNEA QUE CAUSABA EL ERROR !!!
            # No tocamos empleado.costo_total_mes porque el modelo ya lo calcula solo.
            
            # Guardamos el registro en la base de datos
            empleado.save()
            
            messages.success(request, f"¡Empleado {empleado.nombre} registrado con éxito con provisiones NIIF!")
            return redirect('registrar_empleado')
    else:
        form = EmpleadoForm()
        
    empleados = Empleado.objects.all().order_by('-id')[:5]
    
    return render(request, 'costos_app/registrar_empleado.html', {
        'form': form, 
        'empleados': empleados
    })

@login_required
@never_cache
def asignar_proyecto(request):
    proyecto_form = ProyectoForm()
    asignacion_form = AsignacionProyectoForm()

    if request.method == 'POST':
        if 'btn_proyecto' in request.POST:
            proyecto_form = ProyectoForm(request.POST)
            if proyecto_form.is_valid():
                proyecto_form.save()
                messages.success(request, "¡Proyecto creado con éxito!")
                return redirect('asignar_proyecto')

        elif 'btn_asignacion' in request.POST:
            asignacion_form = AsignacionProyectoForm(request.POST)
            if asignacion_form.is_valid():
                asignacion = asignacion_form.save(commit=False)
                
                # REGLA DE TRES PARA EL COSTO INDIVIDUAL DE LA ASIGNACIÓN:
                empleado = asignacion.empleado
                costo_total_empleado = Decimal(str(empleado.costo_total_mes))
                horas_laborales_mes = Decimal('160.0')
                horas_dedicadas = Decimal(str(asignacion.horas_dedicadas))
                
                # Valor de una hora real del empleado * horas dedicadas a este proyecto
                valor_hora_real = costo_total_empleado / horas_laborales_mes
                asignacion.costo_imputado_al_proyecto = float(valor_hora_real * horas_dedicadas)
                
                asignacion.save()
                messages.success(request, f"¡Horas de {empleado.nombre} prorrateadas con éxito!")
                return redirect('asignar_proyecto')

    # =====================================================================
    # 📊 MATEMÁTICA DEL PRORRATEO REAL POR PROYECTO (COSTO ABC ACCUMULADO)
    # =====================================================================
    proyectos_lista = Proyecto.objects.all().order_by('-id')
    proyectos_con_costo = []

    for proyecto in proyectos_lista:
        asignaciones_proyecto = AsignacionProyecto.objects.filter(proyecto=proyecto)
        
        totales = asignaciones_proyecto.aggregate(
            total_horas=Sum('horas_dedicadas'),
            total_costo=Sum('costo_imputado_al_proyecto')
        )
        
        horas_totales = totales['total_horas'] or 0
        costo_total_real = totales['total_costo'] or 0.0

        proyectos_con_costo.append({
            'id': proyecto.id,
            'nombre': proyecto.nombre,
            'descripcion': proyecto.descripcion,
            'horas_totales': horas_totales,
            'costo_total_real': costo_total_real,
        })

    asignaciones_recientes = AsignacionProyecto.objects.all().select_related('empleado', 'proyecto').order_by('-id')

    return render(request, 'costos_app/asignar_proyecto.html', {
        'proyecto_form': proyecto_form,
        'asignacion_form': asignacion_form,
        'proyectos_prorrateados': proyectos_con_costo,
        'asignaciones': asignaciones_recientes
    })

@login_required
@never_cache
def dashboard_financiero(request):
    """Dashboard Ejecutivo de Margen de Contribución Total con Absorción de Depreciación (NIC 16)"""
    
    # =====================================================================
    # 🛡️ ESCUDO DE IDIOMA PARA REDIRECCIÓN POST-LOGIN
    # =====================================================================
    # Capturamos el código de idioma que guardó la cookie/sesión en el login (es, en, de, pl, etc.)
    idioma_actual = get_language()
    
    # Si el usuario entra a '/dashboard/' a secas sin prefijo, lo obligamos a ir a la URL con idioma
    if not request.path.startswith(f'/{idioma_actual}/'):
        return redirect(f'/{idioma_actual}/dashboard/')
    # =====================================================================

    # 1. MANO DE OBRA DIRECTA (Roles tipo COSTO)
    empleados_costo = Empleado.objects.filter(rol__tipo_contable='COSTO')
    total_mano_obra_directa = sum(e.costo_total_mes for e in empleados_costo)

    # 2. FACTURAS DE COSTO OPERATIVO (AWS, Internet de producción, etc.)
    facturas_costo = FacturaFija.objects.filter(clasificacion='COSTO_OPERATIVO')
    total_facturas_costo = sum(f.monto for f in facturas_costo)

    # 3. DEPRECIACIÓN TOTAL DE ACTIVOS EN OPERACIÓN (Costo Operativo Oculto)
    activos_en_operacion = ActivoFijo.objects.filter(empleado_asignado__rol__tipo_contable='COSTO')
    total_depreciacion_operativa = sum(a.depreciacion_mensual for a in activos_en_operacion)

    # TOTAL BOLSA OPERATIVA GLOBAL (MOD + Infraestructura + Desgaste de Equipos)
    total_costo_operativo_global = total_mano_obra_directa + total_facturas_costo + total_depreciacion_operativa

    # 4. BOLSA DE GASTOS DE ADMINISTRACIÓN (Personal Administrativo + Facturas Soporte + Depreciación Admin)
    empleados_gasto = Empleado.objects.filter(rol__tipo_contable='GASTO')
    total_nomina_gasto = sum(e.costo_total_mes for e in empleados_gasto)
    
    facturas_gasto = FacturaFija.objects.filter(clasificacion='GASTO_ADMIN')
    total_facturas_gasto = sum(f.monto for f in facturas_gasto)
    
    activos_en_gasto = ActivoFijo.objects.filter(empleado_asignado__rol__tipo_contable='GASTO') or ActivoFijo.objects.filter(empleado_asignado__isnull=True)
    total_depreciacion_gasto = sum(a.depreciacion_mensual for a in activos_en_gasto)
    
    total_gastos_administracion_global = total_nomina_gasto + total_facturas_gasto + total_depreciacion_gasto

    # 5. ABSORCIÓN EN PROYECTOS (Prorrateo ABC de Nómina + Depreciación de sus Herramientas)
    proyectos_lista = Proyecto.objects.all()
    proyectos_resumen = []
    total_costo_imputado_proyectos = 0

    for proyecto in proyectos_lista:
        asignaciones = AsignacionProyecto.objects.filter(proyecto=proyecto).select_related('empleado')
        
        horas_totales_proyecto = 0
        costo_nomina_proyecto = 0
        costo_depreciacion_proyecto = 0

        for asig in asignaciones:
            horas_totales_proyecto += asig.horas_dedicadas
            costo_nomina_proyecto += float(asig.costo_imputado_al_proyecto)
            
            empleado = asig.empleado
            activos_empleado = empleado.activos.all()
            depreciacion_mensual_empleado = sum(act.depreciacion_mensual for act in activos_empleado)
            
            proporcion_uso = float(asig.horas_dedicadas) / 160.0
            costo_depreciacion_proyecto += float(depreciacion_mensual_empleado) * proporcion_uso

        costo_total_proyecto = costo_nomina_proyecto + costo_depreciacion_proyecto
        total_costo_imputado_proyectos += costo_total_proyecto

        # --- Recuperar Presupuesto Asignado ---
        presupuesto_total = 0.0
        porcentaje_consumo = 0.0
        alerta_status = 'success'

        if hasattr(proyecto, 'presupuesto'):
            presupuesto_total = float(proyecto.presupuesto.presupuesto_total)
            if presupuesto_total > 0:
                porcentaje_consumo = (costo_total_proyecto / presupuesto_total) * 100
                
                if porcentaje_consumo >= 100:
                    alerta_status = 'danger'
                elif porcentaje_consumo >= 80:
                    alerta_status = 'warning'

        participacion = 0.0
        if total_costo_operativo_global > 0:
            participacion = (costo_total_proyecto / float(total_costo_operativo_global)) * 100

        proyectos_resumen.append({
            'nombre': proyecto.nombre,
            'descripcion': proyecto.descripcion,
            'horas': horas_totales_proyecto,
            'costo_nomina': costo_nomina_proyecto,
            'costo_depreciacion': costo_depreciacion_proyecto,
            'costo_real': costo_total_proyecto,
            'participacion': participacion,
            'presupuesto_total': presupuesto_total,         
            'porcentaje_consumo': porcentaje_consumo,       
            'alerta_status': alerta_status                  
        })

    mano_obra_ociosa = max(0.0, float(total_costo_operativo_global) - total_costo_imputado_proyectos)

    return render(request, 'costos_app/dashboard.html', {
        'total_mod': total_mano_obra_directa,
        'total_facturas_costo': total_facturas_costo,
        'total_depreciacion_op': total_depreciacion_operativa,
        'total_costo_operativo': total_costo_operativo_global,
        'total_gastos_admin': total_gastos_administracion_global,
        'total_proyectos': total_costo_imputado_proyectos,
        'mano_obra_ociosa': mano_obra_ociosa,
        'proyectos': proyectos_resumen,
    })


@login_required
@never_cache
def registrar_factura(request):
    """Vista para registrar y listar los costos y gastos fijos (Arriendos, AWS, etc.)"""
    form = FacturaFijaForm()
    
    if request.method == 'POST':
        form = FacturaFijaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Factura/Costo fijo registrado exitosamente!")
            return redirect('registrar_factura')
            
    facturas = FacturaFija.objects.all().order_by('-id')
    return render(request, 'costos_app/registrar_factura.html', {
        'form': form,
        'facturas': facturas
    })


@login_required
@never_cache
def registrar_activo(request):
    """Vista para el registro y auditoría contable de Activos Fijos (NIC 16) y Leasing (NIIF 16)"""
    form = ActivoFijoForm()
    
    if request.method == 'POST':
        form = ActivoFijoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Activo fijo registrado con éxito bajo políticas NIC 16 / NIIF 16!")
            return redirect('registrar_activo')
            
    activos = ActivoFijo.objects.all().select_related('empleado_asignado').order_by('-id')
    return render(request, 'costos_app/registrar_activo.html', {
        'form': form,
        'activos': activos
    })
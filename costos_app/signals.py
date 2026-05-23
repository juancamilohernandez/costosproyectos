from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import FacturaFija, Empleado, AsignacionProyecto

@receiver(post_save, sender=FacturaFija)
def alertar_desviacion_presupuestal_optima(sender, instance, created, **kwargs):
    """
    Motor Avanzado de Notificaciones Segmentadas: Envía alertas críticas 
    ÚNICAMENTE al ecosistema responsable del proyecto (Líder, Jefe, Analista y CEO).
    """
    proyecto = getattr(instance, 'proyecto', None)
    
    if proyecto and hasattr(proyecto, 'presupuesto'):
        presupuesto = proyecto.presupuesto
        
        # 1. Cálculo del Costo Real Actual (Nómina + NIC 16)
        costo_real_total = 0.0
        asignaciones = AsignacionProyecto.objects.filter(proyecto=proyecto).select_related('empleado', 'responsable_proyecto', 'jefe_inmediato')
        
        for asig in asignaciones:
            costo_real_total += float(asig.costo_imputado_al_proyecto)
            if asig.empleado:
                depr_mes = sum(float(act.depreciacion_mensual) for act in asig.empleado.activos.all())
                costo_real_total += depr_mes * (float(asig.horas_dedicadas) / 160.0)
            
        # Sumamos facturas asociadas al proyecto
        facturas_proyecto = FacturaFija.objects.filter(proyecto=proyecto)
        costo_real_total += sum(float(f.monto) for f in facturas_proyecto)

        presupuesto_techo = float(presupuesto.presupuesto_total)
        
        if presupuesto_techo > 0:
            porcentaje_consumo = (costo_real_total / presupuesto_techo) * 100
            
            # Disparar alerta si pasa del 90% de consumo
            if porcentaje_consumo >= 90:
                
                # --- MATRIZ DE RESPONSABILIDAD SEGMENTADA ---
                correos_objetivo = []
                
                # A. Correos de la operación directa (Líder y Jefe inmediato asignados)
                for asig in asignaciones:
                    if asig.responsable_proyecto and hasattr(asig.responsable_proyecto, 'email_corporativo') and asig.responsable_proyecto.email_corporativo:
                        correos_objetivo.append(asig.responsable_proyecto.email_corporativo)
                    if asig.jefe_inmediato and hasattr(asig.jefe_inmediato, 'email_corporativo') and asig.jefe_inmediato.email_corporativo:
                        correos_objetivo.append(asig.jefe_inmediato.email_corporativo)
                
                # B. Filtro Corporativo Seguro: Traemos los empleados y buscamos el rol de forma segura
                todos_los_empleados = Empleado.objects.exclude(email_corporativo__isnull=True).exclude(email_corporativo='')
                 
                for emp in todos_los_empleados:
                     # Convertimos el rol a texto string para que sirva tanto si es CharField como ForeignKey __str__
                     rol_str = str(emp.rol).upper()
                     if 'CEO' in rol_str or 'COSTOS' in rol_str or 'PRESUPUESTO' in rol_str or 'TI' in rol_str:
                         correos_objetivo.append(emp.email_corporativo)
                
                # Limpiar duplicados y correos vacíos
                correos_finales = list(set([email for email in correos_objetivo if email]))
                
                # 3. Envío del Correo si hay destinatarios válidos
                if correos_finales:
                    asunto = f"⚠️ [CONTROL DE PRESUPUESTO] Desviación Financiera - Proyecto: {proyecto.nombre}"
                    
                    status = "LÍMITE EXCEDIDO 🚨" if porcentaje_consumo >= 100 else "ZONA CRÍTICA DE CONTROL ⚠️"
                    
                    mensaje = f"""
                    Atención Equipo de Control de Proyectos,
                    
                    El ERP ha detectado una desviación en los techos de gasto asignados. Las áreas no operativas (Jurídica, Marketing, Gestión Humana) han sido omitidas de esta alerta.
                    
                    RESUMEN FINANCIERO EJECUTIVO:
                    --------------------------------------------------
                    Proyecto: {proyecto.nombre}
                    Evaluación: {status}
                    Presupuesto Máximo Aprobado: ${presupuesto_techo:,.2f}
                    Costo Imputado Acumulado: ${costo_real_total:,.2f}
                    Eficiencia de Consumo: {porcentaje_consumo:.2f}%
                    --------------------------------------------------
                    
                    IMPACTO DE LA ÚLTIMA FACTURA PROCESADA:
                    Proveedor/Concepto: {instance.proveedor_o_concepto or 'Gasto Operativo'}
                    Valor: ${instance.monto:,.2f}
                    Clasificación Contable: {instance.get_clasificacion_display()}
                    
                    ACCIÓN REQUERIDA:
                    El Responsable Principal del Proyecto y el Analista de Presupuestos asignado deben conciliar las horas registradas y las facturas en el Dashboard de inmediato.
                    
                    Sistemas de Información y Costos ABC.
                    """
                    
                    send_mail(
                        subject=asunto,
                        message=mensaje,
                        from_email='alertas-erp@tuempresa.com',
                        recipient_list=correos_finales,
                        fail_silently=True,
                    )
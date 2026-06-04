from django.db import models  # Importación crucial para usar las consultas Q e __icontains
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import FacturaFija, Empleado, AsignacionProyecto
from django.conf import settings
import threading  # LIBRERÍA NATIVA DE PYTHON PARA CONCURRENCIA ASÍNCRONA
import logging

# Configuramos un logger para registrar fallos en la consola de Render sin romper la app
logger = logging.getLogger(__name__)


def enviar_alerta_email_async(asunto, mensaje, remitente, destinatarios):
    """
    Función trabajadora (Worker) ejecutada en un hilo secundario independiente.
    Aísla la latencia y bloqueos de red del servidor SMTP de Gmail.
    """
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=remitente,
            recipient_list=destinatarios,
            fail_silently=True,  # Doble protección silenciosa ante fallos de conexión
        )
        logger.info(f"📧 [Threading] Alerta de presupuesto enviada con éxito a: {destinatarios}")
    except Exception as e:
        logger.error(f"❌ [Threading] Error crítico en el hilo de envío de correo SMTP: {str(e)}")


# 🔥 LA SOLUCIÓN: El decorador ahora escucha AMBOS modelos. 
# Se activa al guardar una FacturaFija O al prorratear una AsignacionProyecto.
@receiver(post_save, sender=FacturaFija)
@receiver(post_save, sender=AsignacionProyecto)
def alertar_desviacion_presupuestal_optima(sender, instance, created, **kwargs):
    """
    Motor Avanzado de Notificaciones Segmentadas: Envía alertas críticas 
    ÚNICAMENTE al ecosistema responsable del proyecto (Líder, Jefe, Analista y CEO).
    Se ejecuta dinámicamente al actualizar costos fijos o al prorratear mano de obra.
    """
    # Identificamos el proyecto dinámicamente según el modelo que disparó la señal
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
                    if asig.responsable_proyecto and getattr(asig.responsable_proyecto, 'email_corporativo', None):
                        correos_objetivo.append(asig.responsable_proyecto.email_corporativo)
                    if asig.jefe_inmediato and getattr(asig.jefe_inmediato, 'email_corporativo', None):
                        correos_objetivo.append(asig.jefe_inmediato.email_corporativo)
                
                # B. Filtro Corporativo Seguro (Optimizado a nivel Base de Datos - Case Insensitive)
                empleados_clave = Empleado.objects.exclude(
                    email_corporativo__isnull=True
                ).exclude(
                    email_corporativo=''
                ).filter(
                    models.Q(rol__icontains='CEO') | 
                    models.Q(rol__icontains='COSTOS') | 
                    models.Q(rol__icontains='PRESUPUESTO') | 
                    models.Q(rol__icontains='TI')
                )
                
                for emp in empleados_clave:
                    correos_objetivo.append(emp.email_corporativo)
                
                # Limpiar duplicados y correos vacíos
                correos_finales = list(set([email for email in correos_objetivo if email]))
                
                # 3. Envío del Correo mediante Desacoplamiento de Hilos (Asíncrono)
                if correos_finales:
                    asunto = f"⚠️ [CONTROL DE PRESUPUESTO] Desviación Financiera - Proyecto: {proyecto.nombre}"
                    status = "LÍMITE EXCEDIDO 🚨" if porcentaje_consumo >= 100 else "ZONA CRÍTICA DE CONTROL ⚠️"
                    
                    # Identificamos el detonante en el cuerpo del correo para que sea más informativo
                    detonante = "Prorrateo de Mano de Obra" if sender == AsignacionProyecto else "Registro de Factura Fija"
                    
                    mensaje = f"""
                    Atención Equipo de Control de Proyectos,
                    
                    El ERP ha detectado una desviación en los techos de gasto asignados mediante el proceso de: {detonante}.
                    
                    RESUMEN FINANCIERO EJECUTIVO:
                    --------------------------------------------------
                    Proyecto: {proyecto.nombre}
                    Evaluación: {status}
                    Presupuesto Máximo Aprobado: ${presupuesto_techo:,.2f}
                    Costo Imputado Acumulado: ${costo_real_total:,.2f}
                    Eficiencia de Consumo: {porcentaje_consumo:.2f}%
                    --------------------------------------------------
                    
                    ACCIÓN REQUERIDA:
                    El Responsable Principal del Proyecto y el Analista de Presupuestos asignado deben conciliar las horas registradas y las facturas en el Dashboard de inmediato.
                    
                    Sistemas de Información y Costos ABC.
                    """
                    
                    # CREACIÓN Y DELEGACIÓN DEL PROCESO AL HILO EN PARALELO
                    hilo_email = threading.Thread(
                        target=enviar_alerta_email_async,
                        args=(asunto, mensaje, settings.EMAIL_HOST_USER, correos_finales)
                    )
                    hilo_email.start()
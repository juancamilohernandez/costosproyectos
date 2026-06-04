from django import forms
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.mail import send_mail  # <--- SE INCLUYE LA IMPORTACIÓN PARA EL ENVÍO DE EMAIL REAL
from decimal import Decimal
from .models import Empleado, PoliticaContratacion, ActivoFijo, FacturaFija, Proyecto, AsignacionProyecto, PresupuestoProyecto
from django.utils.translation import gettext_lazy as _

class EmpleadoForm(forms.ModelForm):
    duracion_contrato_meses = forms.IntegerField(
        required=False,
        label=_("Duración del contrato (Meses)"),
        help_text=_("Requerido si el contrato es a Término Fijo"),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12'})
    )

    class Meta:
        model = Empleado
        fields = [
            'nombre', 'pais', 'rol', 'tipo_contrato', 
            'salario_bruto_mensual', 'duracion_contrato_meses'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'salario_bruto_mensual': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pais = cleaned_data.get('pais')
        tipo_contrato = cleaned_data.get('tipo_contrato')
        duracion = cleaned_data.get('duracion_contrato_meses')

        if pais and tipo_contrato:
            politica = PoliticaContratacion.objects.filter(pais=pais, tipo_contrato=tipo_contrato).first()
            if politica:
                if tipo_contrato == 'FIJO' and politica.duracion_maxima_meses:
                    if not duracion:
                        self.add_error('duracion_contrato_meses', 'Para contratos fijos en este país, debes especificar la duración.')
                    elif duracion > politica.duracion_maxima_meses:
                        raise forms.ValidationError(
                            f"Alerta Legal: La legislación de {pais.nombre} prohíbe contratos a "
                            f"término fijo mayores a {politica.duracion_maxima_meses} meses."
                        )
        return cleaned_data


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: App Bancaria'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Breve descripción del proyecto...'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AsignacionProyectoForm(forms.ModelForm):
    class Meta:
        model = AsignacionProyecto
        fields = ['empleado', 'proyecto', 'horas_dedicadas', 'mes_ano']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'proyecto': forms.Select(attrs={'class': 'form-select'}),
            'horas_dedicadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 80'}),
            'mes_ano': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2026-05'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'empleado' in self.fields:
            # Trae Nombre - Cargo (usando el campo nombre_cargo de tu FK Rol)
            self.fields['empleado'].label_from_instance = lambda obj: f"{obj.nombre} - {obj.rol.nombre_cargo if obj.rol else 'Sin Cargo'}"

    # =====================================================================
    # 🔒 CANDADO DE CONTROL PRESUPUESTAL EN TIEMPO REAL (HARD STOP) + EMAIL ASÍNCRONO
    # =====================================================================
    def clean(self):
        cleaned_data = super().clean()
        proyecto = cleaned_data.get('proyecto')
        empleado = cleaned_data.get('empleado')
        horas_dedicadas = cleaned_data.get('horas_dedicadas')

        if proyecto and empleado and horas_dedicadas:
            # 1. Traer el presupuesto asignado al proyecto de forma segura
            # Usamos la relación directa reverse o el atributo si existe
            try:
                from decimal import Decimal
                from django.db.models import Sum
                from django.conf import settings
                import threading
                
                # Para evitar fallos de ObjectDoesNotExist, usamos getattr seguro o filter.first()
                presupuesto_obj = getattr(proyecto, 'presupuesto', None)
                
                if not presupuesto_obj:
                    raise forms.ValidationError(
                        f"🛑 CONTROL DE AUDITORÍA: El proyecto '{proyecto.nombre}' no tiene una tabla de "
                        f"presupuesto asignada en el sistema. El CEO debe inicializar su presupuesto primero."
                    )
                
                limite_mano_obra = Decimal(str(presupuesto_obj.limite_costos))
                
            except Exception as e:
                # Si falla cualquier lectura del presupuesto, levantamos el error visible en el formulario
                raise forms.ValidationError(
                    f"🛑 ERROR DE CONFIGURACIÓN: No se pudo verificar el presupuesto del proyecto. "
                    f"Detalles técnicos: {str(e)}"
                )

            # 2. Replicar la regla de tres para calcular el costo proyectado
            costo_total_empleado = Decimal(str(empleado.costo_total_mes))
            horas_laborales_mes = Decimal('160.0')
            horas_nuevas = Decimal(str(horas_dedicadas))
            
            valor_hora_real = costo_total_empleado / horas_laborales_mes
            nuevo_costo_imputado = valor_hora_real * horas_nuevas

            # 3. Sumar el histórico real acumulado en la base de datos
            totales = AsignacionProyecto.objects.filter(proyecto=proyecto).aggregate(
                total_costo=Sum('costo_imputado_al_proyecto')
            )
            
            # Protección contra nulos convirtiendo estrictamente a Decimal
            costo_acumulado_actual = Decimal(str(totales['total_costo'] or '0.0'))

            # 4. Evaluación del Techo Financiero (Hard Stop)
            if (costo_acumulado_actual + nuevo_costo_imputado) > limite_mano_obra:
                
                # --- LOGICA INTEGRADA ASÍNCRONA: PREPARACIÓN DEL CORREO ---
                email_ceo = "camilohnz78@gmail.com"
                asunto_correo = f"🚨 ALERTA FINANCIERA: Presupuesto Agotado en Proyecto - {proyecto.nombre}"
                
                cuerpo_mensaje = (
                    f"Estimado Gerente / CEO,\n\n"
                    f"El ERP de Costos ha bloqueado un intento de registro que desborda las métricas de planeación presupuestal.\n\n"
                    f"📊 DETALLES DE LA AUDITORÍA:\n"
                    f"• Proyecto: {proyecto.nombre}\n"
                    f"• Límite para Costos Directos: ${limite_mano_obra:,.2f}\n"
                    f"• Costo histórico acumulado: ${costo_acumulado_actual:,.2f}\n"
                    f"• Costo que se intentó cargar: ${nuevo_costo_imputado:,.2f}\n"
                    f"• Déficit proyectado evitado: ${(costo_acumulado_actual + nuevo_costo_imputado) - limite_mano_obra:,.2f}\n"
                    f"• Colaborador que generaba el costo: {empleado.nombre}\n\n"
                    f"🔐 ACCIÓN DEL SISTEMA: Se aplicó un Hard Stop preventivo. Para desbloquear este proyecto, "
                    f"debe ingresar al módulo administrativo de Presupuestos y autorizar una adición de capital.\n\n"
                    f"Atentamente,\n"
                    f"Sistema Automático de Auditoría NIC 16 / NIIF 16"
                )

                # Definimos una función interna rápida para que corra en el fondo sin trabar el formulario
                def enviar_correo_formulario_async():
                    try:
                        send_mail(
                            subject=asunto_correo,
                            message=cuerpo_mensaje,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[email_ceo],
                            fail_silently=True,  # Si Gmail tarda, Django no se detiene
                        )
                    except Exception as mail_err:
                        print(f"❌ Falló el envío en segundo plano del formulario: {mail_err}")

                # DESPACHAMOS EL CORREO A UN HILO INDEPENDIENTE EN MILISEGUNDOS
                hilo_auditoria = threading.Thread(target=enviar_correo_formulario_async)
                hilo_auditoria.start()

                # Lanzamos inmediatamente la excepción en la pantalla (Hard Stop visual instantáneo)
                raise forms.ValidationError(
                    f"🛑 BLOQUEO DE COSTOS: La asignación de horas supera el límite financiero del proyecto. "
                    f"Acumulado actual: ${costo_acumulado_actual:,.2f} | Nuevo costo a imputar: ${nuevo_costo_imputado:,.2f} | "
                    f"Límite de Costos Directos permitido: ${limite_mano_obra:,.2f}."
                )

        return cleaned_data

class FacturaFijaForm(forms.ModelForm):
    class Meta:
        model = FacturaFija
        fields = ['proveedor_o_concepto', 'monto', 'mes_ano', 'clasificacion']
        widgets = {
            'proveedor_o_concepto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: AWS Servidores'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1500000'}),
            'mes_ano': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2026-05'}),
            'clasificacion': forms.Select(attrs={'class': 'form-select'}),
        }


class ActivoFijoForm(forms.ModelForm):
    class Meta:
        model = ActivoFijo
        fields = [
            'nombre_activo', 'tipo_activo', 'empleado_asignado', 
            'valor_adquisicion', 'vida_util_meses', 'fecha_adquisicion', 
            'es_leasing', 'tasa_interes_mensual', 'canon_mensual'
        ]
        widgets = {
            'nombre_activo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: MacBook Pro M3 #04'}),
            'tipo_activo': forms.Select(attrs={'class': 'form-select'}),
            'empleado_asignado': forms.Select(attrs={'class': 'form-select'}), 
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control'}),
            'vida_util_meses': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_adquisicion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'es_leasing': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'tasa_interes_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'canon_mensual': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'empleado_asignado' in self.fields:
            # Trae Nombre - Cargo (usando el campo nombre_cargo de tu FK Rol)
            self.fields['empleado_asignado'].label_from_instance = lambda obj: f"{obj.nombre} - {obj.rol.nombre_cargo if obj.rol else 'Sin Cargo'}"
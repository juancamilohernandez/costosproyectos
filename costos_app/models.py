from django.db import models
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # 🚀 LA HERRAMIENTA MÁGICA
from django.contrib.auth.models import User
import datetime

class Pais(models.Model):
    """Guarda las reglas fiscales y macroeconómicas de cada país."""
    nombre = models.CharField(_('Nombre del País'), max_length=50, unique=True)
    codigo_iso = models.CharField(_('Código ISO (2 letras)'), max_length=3, unique=True)  
    tasa_patronal_estandar = models.DecimalField(_('Tasa Patronal Estándar (%)'), max_digits=5, decimal_places=4)  
    tasa_patronal_temporal = models.DecimalField(_('Tasa Patronal Temporal (%)'), max_digits=5, decimal_places=4)  
    salario_minimo = models.DecimalField(_('Salario Mínimo'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Países")

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"


class Rol(models.Model):
    """Cargos dinámicos (Costo Directo vs Gasto Administrativo)."""
    TIPO_CONTABLE_CHOICES = [
        ('COSTO', _('Costo (Mano de Obra Directa / Operación)')),
        ('GASTO', _('Gasto (Administrativo / Ventas)')),
    ]
    nombre_cargo = models.CharField(_('Nombre del Cargo'), max_length=100, unique=True)
    descripcion = models.TextField(_('Descripción'), blank=True, null=True)
    tipo_contable = models.CharField(_('Tipo Contable'), max_length=5, choices=TIPO_CONTABLE_CHOICES, default='COSTO')

    class Meta:
        verbose_name = _("Rol / Cargo")
        verbose_name_plural = _("Roles / Cargos")

    def __str__(self):
        return f"{self.nombre_cargo} ({self.get_tipo_contable_display()})"


class Empleado(models.Model):
    """Nómina de la empresa vinculada a una jurisdicción (País) y a un Rol."""
    TIPO_CONTRATO_CHOICES = [
        ('INDEFINIDO', _('Término Indefinido')),
        ('FIJO', _('Término Fijo / Obra')),
    ]

    nombre = models.CharField(_('Nombre Completo'), max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='empleados', verbose_name=_('País'))
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, related_name='empleados', verbose_name=_('Rol / Cargo'))
    salario_bruto_mensual = models.DecimalField(_('Salario Bruto Mensual'), max_digits=10, decimal_places=2)
    tipo_contrato = models.CharField(_('Tipo de Contrato'), max_length=10, choices=TIPO_CONTRATO_CHOICES, default='INDEFINIDO')
    fecha_ingreso = models.DateField(_('Fecha de Ingreso'), auto_now_add=True)
    costo_seguridad_social_mes = models.FloatField(_('Costo Seguridad Social Mes'), default=0.0)
    provision_prestaciones_mes = models.FloatField(_('Provisión Prestaciones Mes'), default=0.0)
    email_corporativo = models.EmailField(
        _('Correo Corporativo'),
        blank=True, 
        null=True, 
        help_text=_("Correo oficial para notificaciones del ERP")
    )

    class Meta:
        verbose_name = _("Empleado")
        verbose_name_plural = _("Empleados")

    def __str__(self):
        return f"{self.nombre} - {self.pais.codigo_iso}"

    @property
    def costo_seguridad_social_patronal(self):
        base_calculo = max(self.salario_bruto_mensual, self.pais.salario_minimo)
        if self.tipo_contrato == 'FIJO':
            tasa = self.pais.tasa_patronal_temporal
        else:
            tasa = self.pais.tasa_patronal_estandar
        return base_calculo * tasa

    @property
    def costo_total_mes(self):
        return self.salario_bruto_mensual + self.costo_seguridad_social_patronal


class Proyecto(models.Model):
    """--- MODELO UNIFICADO DE PROYECTO ---"""
    nombre = models.CharField(_('Nombre del Proyecto'), max_length=150)
    descripcion = models.TextField(_('Descripción'), blank=True, null=True)
    fecha_inicio = models.DateField(_('Fecha de Inicio'), null=True, blank=True)
    kwh_estimados_mes = models.DecimalField(
        _('kWh Estimados Mes'),
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text=_("Consumo proyectado de energía al mes en kWh")
    )

    class Meta:
        verbose_name = _("Proyecto")
        verbose_name_plural = _("Proyectos")

    def __str__(self):
        return self.nombre


class RegistroEnergia(models.Model):
    """Registra las facturas reales de energía bajo NIIF."""
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='consumos_energia', verbose_name=_('País'))
    mes = models.IntegerField(_('Mes'))  
    año = models.IntegerField(_('Año'))  
    total_kwh_consumidos_real = models.DecimalField(_('Total kWh Consumidos Real'), max_digits=12, decimal_places=2)
    costo_total_recibo = models.DecimalField(_('Costo Total Recibo'), max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _("Registro de Energía")
        verbose_name_plural = _("Registros de Energía")

    def __str__(self):
        return f"Recibo {self.pais.nombre} - Mes {self.mes}/{self.año}"
    

class PoliticaContratacion(models.Model):
    """Parametriza las leyes laborales específicas de cada país."""
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='politicas_contratacion', verbose_name=_('País'))
    
    TIPO_CONTRATO_CHOICES = [
        ('INDEFINIDO', _('Término Indefinido')),
        ('FIJO', _('Término Fijo / Obra')),
    ]
    tipo_contrato = models.CharField(
        _('Tipo de Contrato'),
        max_length=10, 
        choices=TIPO_CONTRATO_CHOICES, 
        help_text=_("El tipo de contrato al que se le aplicará esta norma legal")
    )
    duracion_maxima_meses = models.IntegerField(
        _('Duración Máxima (Meses)'),
        blank=True, 
        null=True, 
        help_text=_("Duración máxima permitida por ley. Dejar vacío si no aplica.")
    )
    periodo_prueba_maximo_meses = models.IntegerField(
        _('Periodo Prueba Máximo (Meses)'),
        default=3,
        help_text=_("Meses máximos de prueba permitidos por la legislación local.")
    )
    porcentaje_maximo_nomina = models.DecimalField(
        _('Porcentaje Máximo Nómina (%)'),
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text=_("Límite de empleados con este contrato.")
    )
    observacion_legal = models.TextField(
        _('Observación Legal'),
        blank=True, 
        null=True, 
        help_text=_("Notas o textos legales adicionales sobre las condiciones de despido o preaviso.")
    )

    class Meta:
        verbose_name = _("Política de Contratación")
        verbose_name_plural = _("Políticas de Contratación")
        unique_together = ('pais', 'tipo_contrato')

    def __str__(self):
        return f"Política {self.pais.nombre} - {self.get_tipo_contrato_display()}"


class AsignacionProyecto(models.Model):
    """Tabla intermedia para el costo por horas de un empleado en múltiples proyectos"""
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name=_('Colaborador')) 
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name=_('Unidad de Negocio / Proyecto'))
    horas_dedicadas = models.FloatField(_('Horas Dedicadas en el Mes'))
    mes_ano = models.CharField(_('Periodo Contable (Mes/Año)'), max_length=7) 
    responsable_proyecto = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyectos_a_cargo',
        verbose_name=_('Responsable del Proyecto'),
        help_text=_("El líder, director de TI o responsable principal de la ejecución")
    )
    jefe_inmediato = models.ForeignKey(
        Empleado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinados_proyecto',
        verbose_name=_('Jefe Inmediato'),
        help_text=_("Jefe directo del área o supervisor inmediato de la asignación")
    )
    costo_imputado_al_proyecto = models.FloatField(_('Costo Imputado al Proyecto'), default=0.0)

    class Meta:
        verbose_name = _("Asignación de Proyecto")
        verbose_name_plural = _("Asignaciones a Proyectos")

    def __str__(self):
        return f"{self.empleado.nombre} -> {self.proyecto.nombre} ({self.horas_dedicadas} hrs)"
    

class FacturaFija(models.Model):
    """Registro de costos y gastos fijos mensuales (AWS, Internet, Arriendos)."""
    TIPO_CLASIFICACION_CHOICES = [
        ('COSTO_OPERATIVO', _('Costo Operativo (AWS, GitHub, Licencias core)')),
        ('GASTO_ADMIN', _('Gasto Administrativo (Papelería, Arriendos)')),
    ]

    proyecto = models.ForeignKey(
        Proyecto, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='facturas',
        verbose_name=_('Proyecto'),
        help_text=_("Seleccione el proyecto si este costo/gasto es imputable directamente a él")
    )
    proveedor_o_concepto = models.CharField(_('Proveedor o Concepto'), max_length=150, help_text=_("Ej: AWS Server, Claro Internet"))
    monto = models.DecimalField(_('Monto'), max_digits=12, decimal_places=2)
    mes_ano = models.CharField(_('Mes/Año'), max_length=7, help_text=_("Formato: AAAA-MM"))
    clasificacion = models.CharField(_('Clasificación'), max_length=20, choices=TIPO_CLASIFICACION_CHOICES, default='COSTO_OPERATIVO')
    fecha_registro = models.DateField(_('Fecha de Registro'), auto_now_add=True)

    class Meta:
        verbose_name = _("Factura Fija")
        verbose_name_plural = _("Facturas y Costos Fijos")

    def __str__(self):
        return f"{self.proveedor_o_concepto} - ${self.monto} ({self.mes_ano})"


class ActivoFijo(models.Model):
    """Control de Propiedad, Planta y Equipo (NIC 16) y Arrendamientos (NIIF 16)."""
    TIPO_ACTIVO_CHOICES = [
        ('COMPUTO', _('Equipo de Cómputo y Tecnología (Computadores, Servidores)')),
        ('MUEBLES', _('Muebles y Enseres (Escritorios, Sillas)')),
        ('COMUNICACION', _('Equipos de Comunicación (Teléfonos corporativos)')),
    ]

    empleado_asignado = models.ForeignKey(
        Empleado, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='activos',
        verbose_name=_('Empleado Asignado'),
        help_text=_("Empleado que tiene en su poder el activo para operar")
    )
    nombre_activo = models.CharField(_('Nombre del Activo'), max_length=150, help_text=_("Ej: MacBook Pro, Silla Ergonómica"))
    tipo_activo = models.CharField(_('Tipo de Activo'), max_length=20, choices=TIPO_ACTIVO_CHOICES)
    valor_adquisicion = models.DecimalField(_('Valor de Adquisición'), max_digits=12, decimal_places=2, help_text=_("Valor histórico de compra"))
    vida_util_meses = models.IntegerField(_('Vida Útil (Meses)'), help_text=_("Vida útil estimada en meses"))
    fecha_adquisicion = models.DateField(_('Fecha de Adquisición'), help_text=_("Fecha en la que se compró o inició el contrato"))
    
    es_leasing = models.BooleanField(default=False, verbose_name=_("¿Es financiado mediante Leasing? (NIIF 16)"))
    tasa_interes_mensual = models.DecimalField(_('Tasa Interés Mensual'), max_digits=5, decimal_places=4, default=0.0000, help_text=_("Tasa de interés mensual del leasing"))
    canon_mensual = models.DecimalField(_('Canon Mensual'), max_digits=12, decimal_places=2, default=0.00, help_text=_("El pago mensual fijo al banco"))

    class Meta:
        verbose_name = _("Activo Fijo")
        verbose_name_plural = _("Propiedad, Planta y Equipo")

    def __str__(self):
        return f"{self.nombre_activo} ({self.get_tipo_activo_display()})"

    @property
    def depreciacion_mensual(self):
        if self.vida_util_meses > 0:
            return self.valor_adquisicion / Decimal(str(self.vida_util_meses))
        return Decimal('0.00')


class PresupuestoProyecto(models.Model):
    """Control de Techos de Gasto y Presupuesto Asignado por Proyecto."""
    proyecto = models.OneToOneField(
        Proyecto, 
        on_delete=models.CASCADE, 
        related_name='presupuesto',
        verbose_name=_('Proyecto'),
        help_text=_("Proyecto al que se le asigna este techo financiero")
    )
    limite_costos = models.DecimalField(_('Límite de Costos Directos'), max_digits=12, decimal_places=2, default=0.00)
    limite_gastos = models.DecimalField(_('Límite de Gastos Indirectos'), max_digits=12, decimal_places=2, default=0.00)
    fecha_aprobacion = models.DateField(_('Fecha de Aprobación'), auto_now_add=True)
    actualizado_en = models.DateTimeField(_('Actualizado en'), auto_now=True)

    class Meta:
        verbose_name = _("Presupuesto de Proyecto")
        verbose_name_plural = _("Presupuestos de Proyectos")

    def __str__(self):
        return f"Presupuesto {self.proyecto.nombre}"

    @property
    def presupuesto_total(self):
        return self.limite_costos + self.limite_gastos

    def clean(self):
        from .models import AsignacionProyecto
        proyecto = self.proyecto
        asignaciones = AsignacionProyecto.objects.filter(proyecto=proyecto)
        
        costo_real_actual = 0.0
        for asig in asignaciones:
            costo_real_actual += float(asig.costo_imputado_al_proyecto)
            if asig.empleado:
                activos = asig.empleado.activos.all()
                depr_mes = sum(float(act.depreciacion_mensual) for act in activos)
                proporcion = float(asig.horas_dedicadas) / 160.0
                costo_real_actual += depr_mes * proporcion

        if float(self.presupuesto_total) < costo_real_actual:
            raise ValidationError(
                _("🚨 ¡PRESUPUESTO ABSURDO! El costo real mínimo actual de este proyecto es mayor al techo asignado.")
            )


class PerfilUsuario(models.Model):
    """Extiende el usuario del sistema para permitir personalización de idioma."""
    IDIOMAS_CHOICES = [
        ('en', _('English')),
        ('es', _('Español')),
        ('et', _('Eesti (Estonia)')),
        ('fi', _('Suomi (Finlandia)')),
        ('lt', _('Lietuvių (Lituania)')),
        ('da', _('Dansk (Danés)')),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name=_('Usuario'))
    idioma_preferido = models.CharField(
        _('Idioma Preferido'),
        max_length=5, 
        choices=IDIOMAS_CHOICES, 
        default='en',
        help_text=_("Seleccione el idioma nativo para la interfaz del ERP")
    )

    class Meta:
        verbose_name = _("Perfil de Usuario")
        verbose_name_plural = _("Perfiles de Usuarios")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
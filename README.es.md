# 🚀 ERP de Control de Costos ABC y Gestión de Proyectos Multi-Región

<p align="left">
  <strong>Choose your language / Seleccione su idioma:</strong><br>
  🇺🇸 <a href="README.md">English (Primary)</a> | 
  🇪🇸 <a href="README.es.md">Español</a> | 
  🇩🇪 <a href="README.de.md">Deutsch</a> | 
  🇵🇱 <a href="README.pl.md">Polski</a> | 
  🇫🇮 <a href="README.fi.md">Suomi</a> | 
  🇪🇪 <a href="README.et.md">Eesti</a> | 
  🇱🇹 <a href="README.lt.md">Lietuvių</a> | 
  🇱🇻 <a href="README.lv.md">Latviešu</a> | 
  🇩🇰 <a href="README.da.md">Dansk</a> | 
  🇳🇴 <a href="README.no.md">Norsk</a> | 
  🇸🇪 <a href="README.sv.md">Svenska</a>
</p>

---

Un núcleo de Sistema de Planificación de Recursos Empresariales (ERP) de nivel corporativo, diseñado para la asignación estratégica de costos, costeo basado en actividades (Costo ABC) para mano de obra directa y control automatizado de presupuestos. Este sistema modela dinámicamente la macroeconomía de Europa del Norte, las estructuras corporativas digitales del Báltico y los estrictos estándares internacionales de contabilidad (NIIF / NIC 16 / NIIF 16).

## 🌍 Enfoque Arquitectónico: Europa del Norte y Países Bálticos
A diferencia de los softwares empresariales genéricos, este ERP está construido desde cero para manejar las realidades financieras y multi-jurisdiccionales de Alemania, Polonia, los países nórdicos y los estados bálticos:
* **Cumplimiento Fiscal Localizado:** Procesamiento dinámico de las estructuras de impuestos patronales del estado (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) y salarios mínimos legales mapeados directamente según los límites del país (`Pais`).
* **Restricciones de Ley Laboral:** Control y aplicación automatizada de duraciones máximas de contratos, límites en los tipos de contratación y periodos de prueba (`PoliticaContratacion`) adaptados a las legislaciones laborales europeas.
* **Arquitectura Multi-Idioma (i18n):** Soporte nativo y selección de interfaz para los idiomas `es`, `en`, `fi`, `et`, `lt`, `lv`, `da`, `de`, `no`, `sv` y `pl` mediante las cadenas de traducción de Django.

## 📊 Módulos Core Técnicos y Financieros

### 1. Costeo Basado en Actividades (Costo ABC) Estricto
Seguimiento en tiempo real de la mano de obra directa (`COSTO`) frente a los gastos administrativos (`GASTO`). El sistema divide los costos utilizando cargos corporativos (`Rol`) y prorratea dinámicamente el valor exacto de las horas reales en función de variables de matriz complejas derivadas del salario bruto mensual del empleado (`salario_bruto_mensual`) junto con sus provisiones NIIF y prestaciones sociales legales.

### 2. Control Transaccional Intermedio (`AsignacionProyecto`)
Gestiona la distribución de horas de los colaboradores a través de múltiples unidades operativas de negocio. Funciona como un escudo financiero estructural; inspecciona la disponibilidad de fondos (`PresupuestoProyecto`) y valida el costo individual de la asignación mediante lógica en el backend antes de que cualquier transacción impacte las capas de la base de datos.

### 3. Depreciación de Activos y Arrendamientos (Cumplimiento NIC 16 / NIIF 16)
Controla Propiedad, Planta y Equipo (`ActivoFijo`), admitiendo tanto compras históricas como modelos de arrendamiento financiero corporativo (Leasing). La arquitectura absorbe automáticamente los gastos de depreciación mensual dentro de los proyectos operativos activos según la proporción exacta de horas dedicadas por el empleado que utiliza el activo.

### 4. Motor Avanzado de Señales y Alertas (`signals.py`)
Un bucle de comunicación de alta precisión posterior al guardado (`post_save`) que monitorea las desviaciones de costos. Calcula los costos acumulados (Nómina + Facturas Fijas + Desgaste de Activos) y dispara correos electrónicos automáticos en tiempo real cuando un proyecto alcanza o supera sus techos financieros. Se dirige exclusivamente al ecosistema directo del proyecto (Líder, Jefe Inmediato, Analistas Financieros y CEO) para eliminar el ruido de notificaciones corporativas.

## 🛠️ Tecnologías Utilizadas
* **Backend:** Python 3.x / Django Framework
* **Base de Datos:** PostgreSQL (Listo para producción)
* **Internacionalización:** Django i18n (`gettext_lazy`)

## 💻 Instalación Rápida y Configuración Local

1. **Clonar el repositorio:**
```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
   cd TU_REPOSITORIO
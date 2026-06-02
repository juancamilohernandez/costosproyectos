# 🚀 Multi-Regional ABC Costing & IFRS Compliance ERP

### 🌍 Live Application Deployment
➔ **[Click here to access the Live Demo](https://costosproyectos.onrender.com/)**

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

---

An advanced, enterprise-grade ERP core module engineered for strategic cost allocation, Activity-Based Costing (ABC) for direct labor, and automated budget enforcement. This system natively models Northern European macroeconomics, Baltic digital corporate structures, and strict international accounting standards (IFRS / NIC 16 / NIIF 16).

## 🌍 Northern Europe & Baltic Architectural Focus
Unlike generic corporate software, this ERP is built from the ground up to handle multi-jurisdictional financial realities across Germany, Poland, the Nordics, and the Baltic states:
* **Localized Fiscal Compliance:** Dynamic processing of state patronal tax structures (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) and statutory minimum wages mapped directly by country bounds (`Pais`).
* **Labor Policy Constraints:** Automated enforcement of maximum contract durations, limits on contract types, and probation periods (`PoliticaContratacion`) matching European employment laws.
* **Multi-Language Architecture (i18n):** Native support for `de`, `pl`, `fi`, `et`, `lt`, `en`, and `es` via Django locale middleware strings.

## 📊 Core Financial & Technical Modules

### 1. Strict Activity-Based Costing (ABC)
Real-time tracking of direct labor (`COSTO`) versus administrative expenses (`GASTO`). The system splits costs using corporate roles (`Rol`) and dynamically prorates exact hourly costs based on complex matrix variables derived from the employee's gross monthly salary (`salario_bruto_mensual`) and statutory NIIF social and payroll provisions.

### 2. Intermediate Transactional Control (`AsignacionProyecto`)
Manages employee hourly allocations across multiple operational business units. It acts as a structural financial shield; it inspects fund availability (`PresupuestoProyecto`) and calculates individual allocation costs via backend validation logic before any transaction touches the database layers.

### 3. Asset Depreciation & Leases (NIC 16 / NIIF 16 Compliance)
Tracks Property, Plant, and Equipment (`ActivoFijo`), supporting both historical acquisitions and corporate leasing models. The architecture automatically absorbs monthly depreciation expenses into active operational projects based on the precise hours dedicated by the employee using the asset.

### 4. Segmented Alert Engine (`signals.py`)
A high-precision post-save communication loop that monitors cost deviations. It calculates cumulative costs (Labor + Fixed Invoices + Asset Wear) and fires automated email alerts when a project hits or exceeds its financial ceilings. It targets exclusively the project's direct ecosystem (Líder, Jefe Inmediato, Financial Analysts, and CEO) to eliminate corporate notification noise.

## 🛠️ Tech Stack
* **Backend:** Python 3.x / Django Framework
* **Database:** PostgreSQL (Production-ready)
* **Internationalization:** Django i18n (`gettext_lazy`)

## 💻 Quick Installation & Local Setup

1. **Clone the repository:**
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
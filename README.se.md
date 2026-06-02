# 🚀 Multiregionalt ERP för ABC-kalkylering & IFRS-efterlevnad

### 🌍 Live-applikationsdriftsättning
➔ **[Klicka här för att komma till Live-demot](https://costosproyectos.onrender.com/)**

---

### Välj språk / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](#)

An avancerad ERP-kärnmodul i enterprise-klass utvecklad för strategisk kostnadsallokering, aktivitetsbaserad kalkylering (ABC) för direkt arbetskraft och automatiserad budgetkontroll. Detta system modellerar nativt nordeuropeisk makroekonomi, baltiska digitala företagsstrukturer och strikta internationella redovisningsstandarder (IFRS / IAS 16 / IFRS 16).

🌍 Arkitektoniskt fokus på Nordeuropa & Baltikum
Till skillnad från generisk företagsmjukvara är detta ERP byggt från grunden för att hantera finansiella realiteter i flera jurisdiktioner i Tyskland, Polen, Norden och Baltikum:
* **Lokaliserad skatteefterlevnad:** Dynamisk bearbetning av statliga arbetsgivaravgiftsstrukturer (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) och lagstadgade minimilöner mappade direkt efter landsgränser (`Pais`).
* **Arbetsmarknadspolitiska begränsningar:** Automatiserad tillämpning av maximala avtalstider, gränser för kontraktstyper och provanställningar (`PoliticaContratacion`) som matchar europeisk arbetsrätt.
* **Flerspråkig arkitektur (i18n):** Nativt stöd för de, pl, fi, et, lt, en och es via Djangos locale-middleware.

📊 Finansiella & tekniska kärnmoduler

1. Strikt aktivitetsbaserad kalkylering (ABC)
Spårning i realtid av direkt arbetskraft (`COSTO`) kontra administrativa kostnader (`GASTO`). Systemet delar upp kostnader med hjälp av företagsroller (`Rol`) och fördelar dyna-miskt exakta timkostnader baserat på komplexa matrisvariabler härledda från medarbetarens bruttomånadslön (`salario_bruto_mensual`) och lagstadgade NIIF-sociala avsättningar.

2. Mellanliggande transaktionskontroll (AsignacionProyecto)
Hanterar anställdas timallokeringar över flera operativa affärsenheter. Det fungerar som en strukturell finansiell sköld; det kontrollerar tillgången på medel (`PresupuestoProyecto`) och beräknar individuella allokeringskostnader via backend-valideringslogik innan någon transaktion rör databaslagren.

3. Tillgångsavskrivningar & leasing (Efterlevnad av IAS 16 / IFRS 16)
Spårar materiella anläggningstillgångar (`ActivoFijo`) och stödjer både historiska förvärv och företagsleasingmodeller. Arkitekturen absorberar automatiskt månatliga avskrivningskostnader i aktiva operativa projekt baserat på de exakta timmar som dedikerats av medarbetaren som använder tillgången.

4. Segmenterad larmmotor (signals.py)
En post-save-kommunikationsloop med hög precision som övervakar kostnadsavvikelser. Den beräknar kumulativa kostnader (Arbetskraft + Fasta fakturor + Slitage på tillgångar) och utlöser automatiska e-postvarningar när ett projekt når eller överskrider sina finansiella tak. Den riktar sig exklusivt till projektets direkta ekosystem (Líder, Jefe Inmediato, finansiella analytiker och VD) för att eliminera brus i företagets aviseringar.

🛠️ Teknikstack
* **Backend:** Python 3.x / Django Framework
* **Databas:** PostgreSQL (Redo för produktion)
* **Internationalisering:** Django i18n (gettext_lazy)

💻 Snabbinstallation & lokal konfiguration
1. Klona arkivet:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
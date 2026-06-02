# 🚀 Multiregional ABC-omkostningsregnskab & IFRS-overholdelses ERP

### 🌍 Live Applikationsdistribution
➔ **[Klik her for at få adgang til Live Demo](https://costosproyectos.onrender.com/)**

---

### Vælg sprog / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](#) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Et avanceret ERP-kernemodul i enterprise-klassen udviklet til strategisk omkostningsallokering, aktivitetsbaseret omkostningsregnskab (ABC) for direkte arbejdskraft og automatiseret budgethåndhævelse. Dette system modellerer indfødt nordeuropæisk makroøkonomi, baltiske digitale virksomhedsstrukturer og strenge internationale regnskabsstandarder (IFRS / IAS 16 / IFRS 16).

🌍 Arkitektonisk fokus på Nordeuropa og Baltikum
I modsætning til generisk virksomhedssoftware er denne ERP bygget fra bunden til at håndtere finansielle realiteter på tværs af Tyskland, Polen, Norden og de baltiske stater:
* **Lokaliseret skattemæssig overholdelse:** Dynamisk behandling af statslige arbejdsgiverafgiftsstrukturer (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) og lovbestemte mindstelønninger kortlagt direkte efter landegrænser (`Pais`).
* **Arbejdspolitiske begrænsninger:** Automatiseret håndhævelse af maksimale kontraktvarigheder, grænser for kontrakttyper og prøvetider (`PoliticaContratacion`) i overensstemmelse med europæisk arbejdsret.
* **Flersproget arkitektur (i18n):** Indfødt support til de, pl, fi, et, lt, en og es via Djangos locale-middleware.

📊 Finansielle og tekniske kjernemoduler

1. Streng aktivitetsbaseret omkostningsregnskab (ABC)
Sanntidssporing af direkte arbejdskraft (`COSTO`) versus administrative omkostninger (`GASTO`). Systemet opdeler omkostninger ved hjælp af virksomhedsroller (`Rol`) og beregner nøjagtige timeomkostninger dynamisk basert på komplekse matrixvariabler afledt af medarbejderens bruttomånedsløn (`salario_bruto_mensual`) og lovbestemte NIIF-sociale hensættelser.

2. Mellemliggende transaktionskontrol (AsignacionProyecto)
Administrerer medarbejdernes timeallokeringer på tværs af flere operationelle forretningsenheder. Det fungerer som et strukturelt økonomisk skjold; det kontrollerer tilgængeligheden af midler (`PresupuestoProyecto`) og beregner individuelle allokeringsomkostninger via backend-valideringslogik, før nogen transaktion berører databaselagene.

3. Aktivafskrivning og leasing (Overholdelse af IAS 16 / IFRS 16)
Spore materielle anlægsaktiver (`ActivoFijo`), der understøtter både historiske opkøb og leasingmodeller. Arkitekturen absorberer automatisk månedlige afskrivningsomkostninger i aktive operationelle projekter baseret på de nøjagtige timer dedikeret af den medarbejder, der bruger aktivet.

4. Segmenteret alarmmotor (signals.py)
En post-save kommunikationssløjfe med høj præcision, der overvåger omkostningsafvigelser. Den beregner kumulative omkostninger (arbejdskraft + faste fakturaer + aktivslid) og udløser automatiske e-mail-advarsler, når et projekt når eller overskrider sine økonomiske lofter. Det retter sig udelukkende mod projektets direkte økosystem (Líder, Jefe Inmediato, finansanalytikere og administrerende direktør) for at eliminere unødvendig støj i virksomhedsmeddelelser.

🛠️ Teknologistak
* **Backend:** Python 3.x / Django Framework
* **Database:** PostgreSQL (Klar til produktion)
* **Internationalisering:** Django i18n (gettext_lazy)

💻 Hurtig installation og lokalt regi
1. Klon arkivet:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
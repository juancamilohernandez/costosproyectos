# 🚀 Multiregional ABC-kostnadsregnskap & IFRS-samsvars ERP

### 🌍 Live Applikasjonsdistribuering
➔ **[Klikk her for å få tilgang til Live Demo](https://costosproyectos.onrender.com/)**

---

### Velg språk / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](#) | 🇸🇪 [Svenska](README.se.md)

En avansert ERP-kjernemodul i enterprise-klassen utviklet for strategisk kostnadsallokering, aktivitetsbasert kostnadsregnskap (ABC) for direkte arbeidskraft, og automatisert budsjetthåndhevelse. Dette systemet modellerer nativt nordeuropeisk makroøkonomi, baltiske digitale selskapsstrukturer og strenge internasjonale regnskapsstandarder (IFRS / IAS 16 / IFRS 16).

🌍 Arkitektonisk fokus på Nord-Europa og Baltikum
I motsetning til generisk bedriftsprogramvare, er denne ERP-en bygget fra grunnen av for å håndtere finansielle realiteter på tvers av Tyskland, Polen, Norden og de baltiske statene:
* **Lokalisert skattemessig samsvar:** Dynamisk behandling av statlige arbeidsgiveravgiftsstrukturer (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) og lovfestede minstelønninger kartlagt direkte etter landegrenser (`Pais`).
* **Arbeidspolitiske begrensninger:** Automatisert håndhevelse av maksimale kontraktsvarigheter, grenser for kontraktstyper og prøvetider (`PoliticaContratacion`) i samsvar med europeisk arbeidsrett.
* **Flerspråklig arkitektur (i18n):** Nativ støtte for de, pl, fi, et, lt, en og es via Djangos locale-middleware.

📊 Finansielle og tekniske kjernemoduler

1. Streng aktivitetsbasert kostnadsregnskap (ABC)
Sanntidssporing av direkte arbeidskraft (`COSTO`) versus administrative utgifter (`GASTO`). Systemet deler kostnader ved hjelp av bedriftsroller (`Rol`) og beregner nøyaktige timekostnader dynamisk basert på komplekse matrisevariabler avledet fra ansattes brutto månedslønn (`salario_bruto_mensual`) og lovfestede NIIF-sosiale avsetninger.

2. Mellomliggende transaksjonskontroll (AsignacionProyecto)
Administrerer ansattes timeallokeringer på tvers av flere operative forretningsenheter. Det fungerer som et strukturelt økonomisk skjold; det kontrollerer tilgjengeligheten av midler (`PresupuestoProyecto`) og beregner individuelle allokeringskostnader via backend-valideringslogikk før noen transaksjon berører databaselagene.

3. Eiendomsavskrivning og leieavtaler (Samsvar med IAS 16 / IFRS 16)
Sporer varige driftsmidler (`ActivoFijo`), og støtter både historiske oppkjøp og bedriftsleasingmodeller. Arkitekturen absorberer automatisk månedlige avskrivningskostnader i aktive operative prosjekter basert på de nøyaktige timene dedikert av den ansatte som bruker eiendelen.

4. Segmentert varslingsmotor (signals.py)
En post-save kommunikasjonsløkke med høy presisjon som overvåker kostnadsavvik. Den beregner kumulative kostnader (arbeid + faste fakturaer + slitasje på eiendeler) og utløser automatiske e-postvarsler når et prosjekt når eller overskrider sine økonomiske tak. Den retter seg utelukkende mot prosjektets direkte økosystem (Líder, Jefe Inmediato, finansanalytikere og administrerende direktør) for å eliminere unødvendig støy i bedriftsvarslinger.

🛠️ Teknologistakk
* **Backend:** Python 3.x / Django Framework
* **Database:** PostgreSQL (Klar for produksjon)
* **Internationalisering:** Django i18n (gettext_lazy)

💻 Hurtiginstallasjon og lokalt oppsett
1. Klon arkivet:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
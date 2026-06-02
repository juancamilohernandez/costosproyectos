# 🚀 Multiregionales ABC-Costing & IFRS-Compliance ERP

### 🌍 Live-Anwendungsbereitstellung
➔ **[Klicken Sie hier, um auf die Live-Demo zuzugreifen](https://costosproyectos.onrender.com/)**

---

### Sprache wählen / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](#) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Ein hochentwickeltes ERP-Kernmodul für Unternehmen, das für die strategische Kostenallokation, die prozessorientierte Kostenrechnung (ABC) für direkte Arbeitskräfte und die automatisierte Budgetkontrolle entwickelt wurde. Dieses System bildet die makroökonomischen Gegebenheiten Nordeuropas, die digitalen Unternehmensstrukturen des Baltikums und die strengen internationalen Rechnungslegungsstandards (IFRS / IAS 16 / IFRS 16) nativ ab.

🌍 Architekturfokus Nordeuropa & Baltikum
Im Gegensatz zu generischer Unternehmenssoftware wurde dieses ERP von Grund auf für die komplexen steuerlichen Realitäten in Deutschland, Polen, den nordischen Ländern und den baltischen Staaten entwickelt:
* **Lokale Steuereinhaltung:** Dynamische Verarbeitung staatlicher Arbeitgeberabgabenstrukturen (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) und gesetzlicher Mindestlöhne, die direkt über Ländergrenzen (`Pais`) abgebildet werden.
* **Arbeitsrechtliche Einschränkungen:** Automatische Durchsetzung von maximalen Vertragslaufzeiten, Beschränkungen der Vertragsarten und Probezeiten (`PoliticaContratacion`) gemäß europäischem Arbeitsrecht.
* **Mehrsprachige Architektur (i18n):** Native Unterstützung für de, pl, fi, et, lt, en und es über Django-Locale-Middleware-Strings.

📊 Kernmodule für Finanzen & Technik

1. Strikte prozessorientierte Kostenrechnung (ABC)
Echtzeit-Erfassung von direkter Arbeit (`COSTO`) im Vergleich zu Verwaltungskosten (`GASTO`). Das System trennt die Kosten nach Unternehmensrollen (`Rol`) und berechnet die exakten Stundensätze dynamisch auf Basis komplexer Matrixvariablen, die aus dem Bruttomonatsgehalt des Mitarbeiters (`salario_bruto_mensual`) und den gesetzlichen NIIF-Sozial- und Gehaltsrückstellungen abgeleitet werden.

2. Intermediäre Transaktionskontrolle (AsignacionProyecto)
Verwaltet die stündlichen Zuweisungen von Mitarbeitern über mehrere operative Geschäftseinheiten hinweg. Es fungiert als struktureller finanzieller Schutzschild; es prüft die Mittelverfügbarkeit (`PresupuestoProyecto`) und berechnet die individuellen Zuweisungskosten über eine Backend-Validierungslogik, bevor eine Transaktion die Datenbankebenen erreicht.

3. Anlagenabschreibung & Leasing (IFRS / IAS 16 Konformität)
Verfolgt Sachanlagen (`ActivoFijo`) und unterstützt sowohl historische Anschaffungen als auch Corporate-Leasing-Modelle. Die Architektur rechnet monatliche Abschreibungen automatisch in aktive operative Projekte ein, basierend auf den genauen Stunden, die der Mitarbeiter mit der Anlage verbracht hat.

4. Segmentierte Alert-Engine (signals.py)
Eine hochpräzise Post-Save-Kommunikationsschleife, die Kostenabweichungen überwacht. Sie berechnet kumulierte Kosten (Arbeit + feste Rechnungen + Anlagenverschleiß) und sendet automatische E-Mail-Warnungen, wenn ein Projekt seine finanzielle Obergrenze erreicht oder überschreitet. Sie filtert Benachrichtigungen gezielt für das direkte Projekt-Ökosystem (Líder, Jefe Inmediato, Finanzanalysten und CEO), um Unternehmens-Spam zu vermeiden.

🛠️ Tech-Stack
* **Backend:** Python 3.x / Django Framework
* **Datenbank:** PostgreSQL (Produktionsbereit)
* **Internationalisierung:** Django i18n (gettext_lazy)

💻 Schnellinstallation & lokales Setup
1. Klonen Sie das Repository:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
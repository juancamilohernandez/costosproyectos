# 🚀 Wieloregionalny system ERP Rachunku Kosztów Działań (ABC) i Zgodności z IFRS

### 🌍 Wdrożenie aplikacji produkcyjnej
➔ **[Kliknij tutaj, aby uzyskać dostęp do wersji demonstracyjnej na żywo](https://costosproyectos.onrender.com/)**

---

### Wybierz język / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](#) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Zaawansowany moduł główny systemu ERP klasy korporacyjnej, zaprojektowany z myślą o strategicznej alokacji kosztów, rachunku kosztów działań (ABC) dla pracy bezpośredniej oraz automatycznym egzekwowaniu budżetu. System natywnie modeluje makroekonomię Europy Północnej, cyfrowe struktury korporacyjne w krajach bałtyckich oraz rygorystyczne międzynarodowe standardy rachunkowości (IFRS / IAS 16 / IFRS 16).

🌍 Architektura zorientowana na Europę Północną i kraje bałtyckie
W przeciwieństwie do generycznego oprogramowania korporacyjnego, ten system ERP został zbudowany od podstaw z myślą o obsłudze wielojurysdykcyjnych realiów finansowych w Niemczech, Polsce, krajach nordyckich i bałtyckich:
* **Zlokalizowana zgodność fiskalna:** Dynamiczne przetwarzanie państwowych struktur podatków pracodawcy (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) oraz ustawowych płac minimalnych mapowanych bezpośrednio według granic krajów (`Pais`).
* **Ograniczenia polityki pracy:** Automatyczne egzekwowanie maksymalnego czasu trwania umów, limitów typów umów oraz okresów próbnych (`PoliticaContratacion`) zgodnie z europejskim prawem pracy.
* **Architektura wielojęzyczna (i18n):** Natywne wsparcie dla de, pl, fi, et, lt, en i es za pośrednictwem ciągów middleware lokalizacji Django.

📊 Główne moduły finansowe i techniczne

1. Rygorystyczny Rachunek Kosztów Działań (ABC)
Śledzenie w czasie rzeczywistym pracy bezpośredniej (`COSTO`) w porównaniu z kosztami administracyjnymi (`GASTO`). System dzieli koszty przy użyciu ról korporacyjnych (`Rol`) i dynamicznie rozlicza dokładne koszty godzinowe w oparciu o złożone zmienne macierzowe pochodzące z miesięcznego wynagrodzenia brutto pracownika (`salario_bruto_mensual`) oraz ustawowych przepisów płacowych i socjalnych NIIF.

2. Pośrednia kontrola transakcyjna (AsignacionProyecto)
Zarządza godzinowymi alokacjami pracowników w wielu operacyjnych jednostkach biznesowych. Działa jako strukturalna tarcza finansowa; sprawdza dostępność środków (`PresupuestoProyecto`) i oblicza indywidualne koszty alokacji za pomocą logiki walidacji backendu, zanim jakakolwiek transakcja trafi do warstw bazy danych.

3. Amortyzacja aktywów i leasing (Zgodność z IAS 16 / IFRS 16)
Śledzi rzeczowe aktywa trwałe (`ActivoFijo`), obsługując zarówno historyczne przejęcia, jak i modele leasingu korporacyjnego. Architektura automatycznie absorbuje miesięczne koszty amortyzacji w aktywnych projektach operacyjnych na podstawie dokładnych godzin dedykowanych przez pracownika korzystającego z zasobu.

4. Segmentowany silnik alertów (signals.py)
Precyzyjna pętla komunikacyjna po zapisaniu (post-save), która monitoruje odchylenia kosztów. Oblicza koszty skumulowane (robocizna + stałe faktury + zużycie aktywów) i uruchamia automatyczne alerty e-mail, gdy projekt osiągnie lub przekroczy swój pułap finansowy. Kieruje reklamy wyłącznie do bezpośredniego ekosystemu projektu (Líder, Jefe Inmediato, analitycy finansowi i CEO), aby wyeliminować szum informacyjny w korporacji.

🛠️ Stos technologiczny
* **Backend:** Python 3.x / Django Framework
* **Baza danych:** PostgreSQL (Gotowa do produkcji)
* **Międzynarodowienie:** Django i18n (gettext_lazy)

💻 Szybka instalacja i konfiguracja lokalna
1. Sklonuj repozytorium:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
# 🚀 Alueellinen ABC-kustannuslaskenta & IFRS-yhteensopiva ERP

### 🌍 Live-sovelluksen käyttöönotto
➔ **[Klikkaa tästä päästäksesi Live-demoon](https://costosproyectos.onrender.com/)**

---

### Valitse kieli / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](#) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Edistynyt, yritystason ERP-core-moduuli, joka on suunniteltu strategiseen kustannusten kohdistamiseen, toimintoperusteiseen kustannuslaskentaan (ABC) suoralle työvoimalle ja automatisoidulle budjetin valvonnalle. Järjestelmä mallintaa Pohjois-Euroopan talousrakenteita, Baltian digitaalisia yritysrakenteita ja kansainvälisiä tilinpäätösstandardeja (IFRS / IAS 16 / IFRS 16).

🌍 Pohjois-Euroopan ja Baltian arkkitehtuurifokus
Toisin kuin yleiset yritysohjelmistot, tämä ERP on rakennettu alusta alkaen käsittelemään monen lainkäyttöalueen taloudellisia todellisuuksia Saksassa, Puolassa, Pohjoismaissa ja Baltiassa:
* **Lokalisoitu verotuksen noudattaminen:** Työnantajamaksujen (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) ja lakisääteisten vähimmäispalkkojen dynaaminen käsittely maakohtaisten rajojen mukaan (`Pais`).
* **Työvoimapolitiikan rajoitukset:** Työsopimusten enimmäiskeston, sopimustyyppien rajoitusten ja koeaikojen (`PoliticaContratacion`) automaattinen valvonta Euroopan työlainsäädännön mukaisesti.
* **Monikielinen arkkitehtuuri (i18n):** Natiivi tuki kielille de, pl, fi, et, lt, en ja es Djangon locale-väliohjelmiston kautta.

📊 Keskeiset taloudelliset ja tekniset moduulit

1. Tiukka toimintoperusteinen kustannuslaskenta (ABC)
Suoran työvoiman (`COSTO`) ja hallintokulujen (`GASTO`) reaaliaikainen seuranta. Järjestelmä jakaa kustannukset yritysroolien (`Rol`) mukaan ja laskee dynaamisesti tarkan tuntikustannuksen työntekijän kuukausipalkan (`salario_bruto_mensual`) ja lakisääteisten NIIF-sosiaali- ja palkkavarausten perusteella.

2. Välitapahtumien valvonta (AsignacionProyecto)
Hallitsee työntekijöiden tuntiresurssien jakamista useille toiminnallisille liiketoimintayksiköille. Se toimii rakenteellisena taloudellisena suojana; se tarkistaa varojen saatavuuden (`PresupuestoProyecto`) ja laskee yksittäiset allokaatiokustannukset backend-validointilogiikan kautta ennen kuin mikään tapahtuma tallennetaan tietokantaan.

3. Omaisuuden poistot ja vuokrasopimukset (IAS 16 / IFRS 16 -yhteensopivuus)
Seuraa aineellista käyttöomaisuutta (`ActivoFijo`) tukemalla sekä historiallisia hankintoja että leasingmalleja. Arkkitehtuuri kohdistaa kuukausittaiset poistokustannukset automaattisesti aktiivisille projekteille sen mukaan, kuinka monta tuntia työntekijä on käyttänyt kyseistä omaisuutta.

4. Segmentoitu hälytysmoottori (signals.py)
Erittäin tarkka post-save-viestintäsilmukka, joka valvoo kustannuspoikkeamia. Se laskee kumulatiiviset kustannukset (työvoima + kiinteät laskut + omaisuuden kuluminen) ja lähettää automaattisia sähköpostihälytyksiä, kun projekti saavuttaa taloudellisen kattonsa. Se kohdistuu yksinomaan projektin suoraan ekosysteemiin (Líder, Jefe Inmediato, talousanalyytikot ja toimitusjohtaja) organisaation taustamelun vähentämiseksi.

🛠️ Teknologiapino
* **Backend:** Python 3.x / Django Framework
* **Tietokanta:** PostgreSQL (Tuotantovalmis)
* **Kansainvälistyminen:** Django i18n (gettext_lazy)

💻 Pikainstallaatio & Paikallinen asennus
1. Kloonaa repositorio:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
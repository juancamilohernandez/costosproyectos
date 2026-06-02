# 🚀 Regioonidevaheline ABC-põhine kulude arvestuse ja IFRS-i vastavuse ERP

### 🌍 Rakenduse reaalajas demo
➔ **[Reaalajas demo vaatamiseks klõpsake siin](https://costosproyectos.onrender.com/)**

---

### Vali keel / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](#) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Täiustatud ettevõttetaseme ERP-tuumikmoodul, mis on loodud strateegiliseks kulude jaotamiseks, tegevuspõhiseks kulude arvestuseks (ABC) otsese tööjõu puhul ja eelarve automaatseks täitmiseks. Süsteem modelleerib natiivselt Põhja-Euroopa makromajandust, Baltikumi digitaalsete ettevõtete struktuure ja rangeid rahvusvahelisi finantsaruandlusstandardeid (IFRS / IAS 16 / IFRS 16).

🌍 Põhja-Euroopa ja Baltikumi arhitektuuriline fookus
Erinevalt üldisest korporatiivsest tarkvarast on see ERP loodud maast madalast, et tulla toime mitme jurisdiktsiooni finantsreaalsusega Saksamaal, Poolas, Põhjamaades ja Baltikumis:
* **Lokaliseeritud fiskaalvastavus:** Riiklike patrooni maksustruktuuride (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) ja seadusjärgsete miinimumpalkade dünaamiline töötlemine, mis on kaardistatud otse riigipiiride järgi (`Pais`).
* **Tööpoliitika piirangud:** Lepingu maksimaalse kestuse, lepingutüüpide piirangute ja katseaegade (`PoliticaContratacion`) automaatne täitmine vastavalt Euroopa tööhõiveseadustele.
* **Mitmekeelne arhitektuur (i18n):** Natiivne tugi de, pl, fi, et, lt, en ja es keartele Django locale vahetarkvara stringide kaudu.

📊 Peamised finants- ja tehnilised moodulid

1. Range tegevuspõhine kulude arvestus (ABC)
Otsese tööjõu (`COSTO`) ja halduskulude (`GASTO`) reaalajas jälgimine. Süsteem jagab kulud ettevõtte rollide (`Rol`) abil ja jaotab dünaamiliselt täpsed tunnitasud, mis põhinevad töötaja igakuisest brutopalgast (`salario_bruto_mensual`) ja seadusjärgsetest NIIF-i sotsiaal- ja palgaeranditest tuletatud keerulistel maatriksmuutujatel.

2. Vahepealne tehingute kontroll (AsignacionProyecto)
Haldab töötajate töötundide jaotamist mitme tegevusüksuse vahel. See toimib struktuurse finantskilbina; see kontrollib vahendite olemasolu (`PresupuestoProyecto`) ja arvutab individuaalsed jaotuskulud backend-valideerimisloogika abil enne, kui mis tahes tehing puudutab andmebaasi kihte.

3. Varade kulum ja rendilepingud (IAS 16 / IFRS 16 vastavus)
Jälgib materiaalsest põhivara (`ActivoFijo`), toetades nii ajaloolisi soetusi kui ka korporatiivseid liisingumudeleid. Arhitektuur seab igakuised kulumid automaatselt aktiivsetele tegevusprojektidele, lähtudes varasid kasutava töötaja pühendatud töötundidest.

4. Segmenteeritud teavitussüsteem (signals.py)
Kõrge täpsusega salvestusjärgne suhtlusring, mis jälgib kulude hälbeid. See arvutab kumulatiivsed kulud (tööjõud + fikseeritud arved + varade kulumine) ja saadab automaatsed e-posti teavitused, kui projekt jõuab oma finantslagi piirini või ületab seda. See on suunatud eranditult projekti otsesele ökosüsteemile (Líder, Jefe Inmediato, finantsanalüütikud ja tegevjuht), et kõrvaldada ettevõtte teavituste müra.

🛠️ Tehnoloogiad
* **Backend:** Python 3.x / Django Framework
* **Andmebaas:** PostgreSQL (Produktsioonivalmis)
* **Rahvusvahelistumine:** Django i18n (gettext_lazy)

💻 Kiire paigaldus ja kohalik seadistus
1. Kloonige hoidla:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
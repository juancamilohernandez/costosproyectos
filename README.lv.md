# 🚀 Daudzreģionālais ABC pašizmaksas aprēķina un IFRS atbilstības ERP

### 🌍 Aktīva lietojumprogrammas izvietošana
➔ **[Noklikšķiniet šeit, lai piekļūtu Live Demo](https://costosproyectos.onrender.com/)**

---

### Izvēlieties valodu / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩🇪 [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](README.lt.md) | 🇱🇻 [Latviešu](#) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Uzlabots, uzņēmuma līmeņa ERP pamatmodulis, kas izstrādāts stratēģiskai izmaksu sadalei, uz darbībām balstītai izmaksu uzskaitei (ABC) tiešajam darbaspēkam un automatizētai budžeta izpildei. Šī sistēma natīvi modelē Ziemeļeiropas makroekonomiku, Baltijas digitālo uzņēmumu struktūras un stingrus starptautiskos grāmatvedības standartus (IFRS / IAS 16 / IFRS 16).

🌍 Ziemeļeiropas un Baltijas arhitektūras fokuss
Atšķirībā od vispārīgas korporatīvās programmatūras, šis ERP ir izveidots no pamatiem, lai risinātu vairāku jurisdikciju finanšu realitāti Vācijā, Polijā, Ziemeļvalstīs un Baltijas valstīs:
* **Lokalizēta fiskālā atbilstība:** Dinamiska valsts darba devēja nodokļu struktūru (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) un likumā noteikto minimālo algu apstrāde, kas kartēta tieši pa valstu robežām (`Pais`).
* **Darba politikas ierobežojumi:** Automātiska maksimālā līguma termiņa, līgumu veidu ierobežojumu un pārbaudes laiku (`PoliticaContratacion`) izpilde saskaņā ar Eiropas darba tiesību aktiem.
* **Daudzvalodu arhitektūra (i18n):** Integrēts de, pl, fi, et, lt, en un es valodu atbalsts, izmantojant Django locale starpprogrammatūru.

📊 Galvenie finanšu un tehniskie moduļi

1. Stingra uz darbībām balstīta izmaksu uzskaite (ABC)
Tiešā darbaspēka (`COSTO`) un administratīvo izdevumu (`GASTO`) izsekošana reāllaikā. Sistēma sadala izmaksas, izmantojot korporatīvās lomas (`Rol`), un dinamiski aprēķina precīzas stundas izmaksas, pamatojoties uz sarežģītiem matricas mainīgajiem, kas iegūti no darbinieka mēneša bruto algas (`salario_bruto_mensual`) un likumā noteiktajiem NIIF sociālajiem un algu uzkrājumiem.

2. Starpnieka darījumu kontrole (AsignacionProyecto)
Pārvalda darbinieku stundu sadalījumu vairākās operatīvās biznesa vienībās. Tas darbojas kā strukturāls finansiāls vairogs; pirms jebkurš darījums sasniedz datubāzes slāņus, tas pārbauda līdzekļu pieejamību (`PresupuestoProyecto`) un aprēķina individuālās sadales izmaksas, izmantojant backend validācijas loģiku.

3. Aktīvu nolietojums un noma (Atbilstība IAS 16 / IFRS 16)
Izseko pamatlīdzekļus (`ActivoFijo`), atbalstot gan vēsturiskos iegādes gadījumus, gan korporatīvās līzinga modeļus. Arhitektūra automātiski iekļauj ikmēneša nolietojuma izdevumus aktīvos darbības projektos, pamatojoties uz precīzām stundām, ko pavadījis darbinieks, kurš izmanto aktīvu.

4. Segmentēts brīdinājumu dzinējs (signals.py)
Augstas precizitātes post-save komunikācijas cilpa, kas uzrauga izmaksu novirzes. Tā aprēķina kumulatīvās izmaksas (darbaspēks + fiksētie rēķini + aktīvu nolietojums) un palaiž automatizētus e-pasta brīdinājumus, kad projekts sasniedz vai pārsniedz savus finansiālos griestus. Tas ir mērķēts tikai uz projekta tiešo ekosistēmu (Líder, Jefe Inmediato, finanšu analītiķi un izpilddirektors), lai novērstu korporatívos paziņojumu trokšņus.

🛠️ Tehnoloģiju kopums
* **Backend:** Python 3.x / Django Framework
* **Datubāze:** PostgreSQL (Gatavs ražošanai)
* **Starptautiskā izplatīšana:** Django i18n (gettext_lazy)

💻 Ātra uzstādīšana un vietējā konfigurācija
1. Klonējiet repozitoriju:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
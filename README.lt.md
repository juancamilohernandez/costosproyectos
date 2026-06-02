# 🚀 Kelių regionų ABC sąnaudų apskaitos ir IFRS atitikties ERP

### 🌍 Veikianti programos demonstracinė versija
➔ **[Spustelėkite čia, kad pasiektumėte Live Demo](https://costosproyectos.onrender.com/)**

---

### Pasirinkite kalbą / Choose your language:
🇺🇸 [English (Primary)](README.md) | 🇪🇸 [Español](README.es.md) | 🇩َهُ [Deutsch](README.de.md) | 🇵🇱 [Polski](README.pl.md) | 🇫🇮 [Suomi](README.fi.md) | 🇪🇪 [Eesti](README.et.md) | 🇱🇹 [Lietuvių](#) | 🇱🇻 [Latviešu](README.lv.md) | 🇩🇰 [Dansk](README.dk.md) | 🇳🇴 [Norsk](README.no.md) | 🇸🇪 [Svenska](README.se.md)

Pažangus, įmonės lygio ERP pagrindinis modulis, sukurtas strateginiam sąnaudų paskirstymui, veikla pagrįstų sąnaudų apskaitai (ABC) tiesioginiam darbui ir automatiniam biudžeto vykdymui. Ši sistema natūraliai modeliuoja Šiaurės Europos makroekonomiką, Baltijos šalių skaitmenines įmonių struktūras ir griežtus tarptautinius apskaitos standartus (IFRS / IAS 16 / IFRS 16).

🌍 Šiaurės Europos ir Baltijos šalių architektūrinis fokusas
Skirtingai nuo bendros įmonių programinės įrangos, ši ERP yra sukurta nuo pagrindų, kad atitiktų kelių jurisdikcijų finansinę realybę Vokietijoje, Lenkijoje, Šiaurės ir Baltijos šalyse:
* **Lokalizuotas mokesčių atitikimas:** Dinaminis valstybinių darbdavio mokesčių struktūrų (`tasa_patronal_estandar` vs `tasa_patronal_temporal`) ir nustatytų minimalių atlyginimų apdorojimas pagal šalių ribas (`Pais`).
* **Darbo politikos apribojimai:** Automatinis maksimalios sutarčių trukmės, sutarčių tipų apribojimų ir bandomųjų laikotarpių (`PoliticaContratacion`) vykdymas pagal Europos darbo įstatymus.
* **Daugiakalbė architektūra (i18n):** Integruotas de, pl, fi, et, lt, en ir es kalbų palaikymas per Django locale tarpinę programinę įrangą.

📊 Pagrindiniai finansiniai ir techniniai moduliai

1. Griežta veikla pagrįstų sąnaudų apskaita (ABC)
Tiesioginio darbo (`COSTO`) ir administracinių išlaidų (`GASTO`) sekimas realiuoju laiku. Sistema paskirsto sąnaudas naudodama įmonės vaidmenis (`Rol`) ir dinamiškai apskaičiuoja tikslias valandines sąnaudas, remdamasi sudėtingais matricos kintamaisiais, gautais iš darbuotojo mėnesinio bruto darbo užmokesčio (`salario_bruto_mensual`) ir įstatyminių NIIF socialinių atskaitymų.

2. Tarpinė sandorių kontrolė (AsignacionProyecto)
Valdo darbuotojų valandų paskirstymą keliuose veiklos padaliniuose. Tai veikia kaip struktūrinis finansinis skydas; prieš bet kokiam sandoriui pasiekiant duomenų bazės sluoksnius, ji patikrina lėšų prieinamumą (`PresupuestoProyecto`) ir apskaičiuoja individualias paskirstymo sąnaudas naudodama backend validavimo logiką.

3. Turto nusidėvėjimas ir nuoma (Atitiktis IAS 16 / IFRS 16)
Seka ilgalaikį materialųjį turtą (`ActivoFijo`), palaikydama tiek istorinius įsigijimus, tiek įmonių lizingo modelius. Architektūra automatiškai įtraukia kasmėnesines nusidėvėjimo išlaidas į aktyvius veiklos projektus, atsižvelgdama į tikslias darbuotojo, naudojančio turtą, valandas.

4. Segmentuotas įspėjimų variklis (signals.py)
Didelio tikslumo post-save komunikacijos ciklas, stebintis sąnaudų nukrypimus. Jis apskaičiuoja sukauptas sąnaudas (darbas + fiksuotos sąskaitos-faktūros + turto nusidėvėjimas) ir paleidžia automatinius įspėjimus el. paštu, kai projektas pasiekia arba viršija savo finansines lubas. Jis nukreiptas išskirtinai į tiesioginę projekto ekosistemą (Líder, Jefe Inmediato, finansų analitikai ir generalinis direktorius), kad pašalintų įmonės pranešimų triukšmą.

🛠️ Technologijų paketas
* **Backend:** Python 3.x / Django Framework
* **Duomenų bazė:** PostgreSQL (Paruošta gamybai)
* **Tarptautinimas:** Django i18n (gettext_lazy)

💻 Greitas įdiegimas ir vietinė sąranka
1. Klonuokite saugyklą:
```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
   cd YOUR_REPOSITORY
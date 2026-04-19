# Nokia Hackathon (early 2026)

**Általános információk:**

Minden feladatnak megvan a saját „munkaterülete” (workspace), saját feladatmappája. Kérjük, maradjatok ezekben a mappákban, amikor a megoldásokon dolgoztok. Ha valamilyen dependency-re szükségetek van, írjátok a _requirements.txt_ fájlba, és az automatikusan telepítve lesz, ha nem üres.
A pontokat először az alapján adjuk, hogy a feladatok helyesen és teljesen vannak-e megoldva. Ezután a megvalósítást, a funkcionalitást, a kód szépségét és olvashatóságát is figyelembe vesszük. Több fájlban is dolgozhattok, és használhattok absztrakciót is. A pontozásnál a harmadik és a negyedik feladat nehezebb, ezért ezek dupla pontot érnek.

**Mappastruktúra:**

- _input.txt_
- _main.py_, amely az automatizált tesztfuttató fő belépési pontja. Kérjük, ne távolítsátok el ezt a fájlt, és ne legyenek benne kötelező paraméterek. Kérjük, minden feladat megoldását printeljétek ki a console-ra.

**Futtatási szabályok:**

- A megoldások futási ideje feladatonként legfeljebb 5 másodperc lehet.
- Ne módosítsátok a `.github` mappát.
- Ne nevezzétek át és ne töröljétek a main.py fájlt.
- A leaderboard nem a végleges állást mutatja, csak a szórakoztatás céljából van ott. Minden eredményt egyénileg végig náünk és pontozunk a fentiekben meghatározottak alapján.

## 1. Mágikus számok

**Feladatmappa:**

`magic_numbers`

**Leírás:**

Nevezzük "mágikus számok"-nak azokat a pozitív egész számokat aminek számjegyeit ha visszafelé olvassuk akkor is ugyanannyi az értékük.
Mágikus szám például az `32123`, vagy a `4994`.

Bármely adott pozitív egész számra találd meg az adott számnál nagyobb, mégis a lehető legkisebb mágikus számot.

**Példák:**

- `next_magic_num(808) => 818`
- `next_magic_num(999) => 1001`
- `next_magic_num(2133) => 2222`

**Megkötés:**

- A megoldásnak tetszőlegesen nagy méretű bemenetekre is hatékonyan kell lefutnia.
- Ha csak sorban, egyesével megnézzük a következő számot és ellenőrizzük, hogy az mágikus szám-e az nem elég hatékony megoldás.

## 2. Törésteszt

**Feladatmappa:**

`drop_test`

**Leírás:**

Egy biciklire szerelhető GPS készüléket fejlesztő cégnél dolgozol, amely a készülékeik strapabíró kialakításáról ismert.
A marketing-osztály éppen egy szlogenen dolgozik a legújabb modellhez: „Képes túlélni egy K méteres esést!”.
Már csak azt kell tudniuk, hogy mekkora lehet a K legnagyobb lehetséges egész értéke, amit még valósan állíthatnak.
Valaki már leejtett egy készüléket 101 méterről, és az eltört.
Tehát a legnagyobb lehetséges érték valahol 0 és 100 között van.

Itt jössz te a képbe.
Meg kell találnod azt a K értéket, amelyre igaz, hogy a készülék nem törik el, ha K méterről ejtik le, viszont eltörik, ha K+1 méterről.
Ennél a feladatnál feltételezzük, hogy:

- a tesztek teljesen megbízhatóak, ezért egyetlen próba K, illetve K+1 méteren elegendő ennek megállapításához
- amíg a készülék túléli az esést, semmilyen sérülést nem szenved, tehát a következő tesztekhez újra felhasználható
- egy már eltört készülék leejtése viszont semmilyen információt nem ad

A főnököd ad egy prototípust és azt mondja, béreld ki a közeli 100 méteres tornyot és határozd meg K értékét.
A torony tulajdonosának tudnia kell, mennyi időre szeretnéd kibérelni a tornyot,
ezért tudnod kell, hogy legfeljebb hány próbára lesz szükség ahhoz, hogy meghatározd K-t.
Rájössz, hogy elég hosszú időre kell kibérelned a tornyot ahhoz, hogy 100 próbát is el lehessen végezni, minden szinten egyet.
Ez azért van, mert el kell végezni egy próbát 1 méteren, aztán 2 méteren és így tovább egészen 100 méterig...
Ha bármelyiket kihagyod, előfordulhat, hogy nem fogod pontosan tudni K értékét, mielőtt a készülék eltörik.
Ha pedig K = 100, akkor ez a stratégia 100 próbát igényel.

A főnök szerint túl drága lenne 100 tesztre kibérelni a tornyot,
szóval megkérdi: mi a maximális próbaszám, ha két prototípussal tesztelhetnél?
Némi számolás után rájössz, hogy a válasz 14.
Ha három készüléked lenne, akkor legfeljebb 9 próbára lenne szükség.

**Feladat:**

Adott N, a rendelkezésedre álló prototípusok száma, valamint H, a maximális magasság, amit tesztelni kell.
Határozd meg, hogy optimális stratégiát feltételezve legfeljebb hány próba szükséges K meghatározásához.
A megoldásnak kezelnie kell 999-es H értéket is.

**Példák:**

- `min_num_of_drops(1, 100) => 100`
- `min_num_of_drops(2, 100) => 14`
- `min_num_of_drops(3, 100) => 9`

## 3. Hálózati adapterek feldolgozása

**Feladatmappa:**

`ipconfig_parser`

**Leírás:**

A feladat célja, hogy a programod tudja automatikusan felismerni az egyes hálózati adapterek adatait egy ipconfig kimenetből, és ezekből kell egy jól strukturált JSON kimenetet készíteni.

**Elvárások:**

A scripted:

- olvassa be az összes mellékelt ipconfig kimeneti fájlt,
- azonosítsa bennük az egyes hálózati adaptereket,
- gyűjtse ki adapterenként a legfontosabb adatokat,
- az eredményt mentse JSON formátumban.

A hiányos értékek kerüljenek ugyanúgy feldolgozásra, a json-ben ilyen esetben üres string-et tárolj el.

**Megkötések:**

A megoldást Pythonban készítsd el.
Külső csomag használata nem kötelező, a feladat megoldható a Python beépített moduljaival is.
A JSON kiíráshoz használhatod a json modult.
A program tudjon több fájlt is feldolgozni egy futás alatt.

**Példa kimenet:**

Nem kötelező így kinéznie.

```json
[
  {
    "file_name": "ipconfig.log",
    "adapters": [
      {
        "adapter_name": "Ethernet adapter Ethernet 40",
        "description": "Intel(R) Ethernet Connection",
        "physical_address": "00-01-02-03-04-05",
        "dhcp_enabled": "Yes",
        "ipv4_address": "192.168.0.1",
        "subnet_mask": "255.255.255.0",
        "default_gateway": "192.168.0.100",
        "dns_servers": ["8.8.8.8", "8.8.4.4"]
      }
    ]
  }
]
```

## 4. Parkolás díjszámító

**Feladatmappa:**

`parking_calculator`

**Leírás:**

Készíts egy függvényt, amely kiszámolja egy autó parkolási díját a parkolóban eltöltött idő alapján.

**Díjszabás:**

- az első 30 perc ingyenes
- az ezt követő 3 órában a parkolás díja óránként 300 forint ami utána 500 forintra emelkedik
- 24 órára a parkolás díja egységesen 10000 forint

**Elvárások:**

A függvény kapja meg a belépés és a kilépés időpontját, majd ezek alapján határozza meg a fizetendő összeget.

- olvassa be a bemeneti adatokat
- számolja ki helyesen a parkolási díjat
- kezelje az esetleges hibás bemenetet
- írja ki a számított értéket egy fileba

Nem kötelező, de extra pont jár érte, ha az összegeket perc alapon is ki tudja számolni.

**Megkötések:**

A megoldást Pythonban készítsd el.
Külső csomag használata nem kötelező, a feladat megoldható a Python beépített moduljaival is.

**Fontos kérdések, amelyeket a programnak kezelnie kell:**

- Mi történik, ha az autó 30 órát marad a parkolóban?
- Mi történik, ha a kilépési idő korábbi, mint a belépési idő?

**Példa kimenetek:**

- 20 perc parkolás → 0 forint
- 2 óra parkolás → 600 forint
- 4 óra parkolás → 1400 forint
- 24 óra parkolás → 10000 forint

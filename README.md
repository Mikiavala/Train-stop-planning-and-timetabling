# Integrisano planiranje zaustavljanja vozova i izrada reda vožnje (TSP + TTP)

Ovaj repozitorijum sadrži kompletnu računarsku implementaciju celobrojnog linearnog programiranja (ILP) za integrisani problem planiranja zaustavljanja vozova (*Train Stop Planning*) i izrade reda vožnje (*Train Timetabling Problem*) u uslovima vremenski zavisne potražnje putnika.

Projekat je izrađen u okviru predmeta **Upravljanje železničkim saobraćajem i transportom** na Saobraćajnom fakultetu Univerziteta u Beogradu.

---

##  Rezime metodološkog pristupa

Model simultano optimizuje:
1. **Vremena dolazaka i polazaka vozova** po stanicama duž posmatranog železničkog koridora.
2. **Raspored zaustavljanja i preskakanja stanica** za svaki voz (binarna promenljiva $z_{i,j}$).
3. **Preraspodelu putničkih tokova** po vozovima uz uvažavanje maksimalnog kapaciteta vozila ($C_i$).

**Funkcija cilja:** Minimizacija ukupnog vremena putovanja i čekanja putnika na stanicama.  
**Ključna ograničenja:** Vremenska konzistentnost kretanja, tehnološke granice bavljenja u stanicama, minimalni bezbednosni razmak (headway) i kapacitet vozila.

---

##  Računarsko okruženje i biblioteke

Za pokretanje modela i reprodukciju rezultata potrebno je Python okruženje sa sledećim paketima:

- **Python:** 3.10+
- **PuLP:** `pip install pulp` (biblioteka za matematičko modelovanje)
- **CBC Solver:** Integrisan uz PuLP (COIN-OR Branch and Cut)
- **Matplotlib / Pandas:** Za obradu rezultata i crtanje dijagrama (opciono)

---

##  Uputstvo za pokretanje skripti

1. **Instalacija potrebnih biblioteka:**
   ```bash
   pip install pulp matplotlib pandas

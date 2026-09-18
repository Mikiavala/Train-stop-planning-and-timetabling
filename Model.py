import pulp
import Podaci as data

def resi_model_reda_voznje():
    # 1. Inicijalizacija problema (Minimizacija ukupnog vremena putovanja i čekanja)
    prob = pulp.LpProblem("Integrisani_TSP_TTP_Vremenski_Zavisna_Potraznja", pulp.LpMinimize)

    # 2. Uvoz skupova i parametara iz Podaci.py
    vozovi = data.vozovi
    stanice = data.stanice
    od_parovi = data.od_parovi
    vreme_voznje = data.vreme_voznje
    T_min = data.T_min
    T_max = data.T_max
    H = data.H
    Kapacitet_voza = data.Kapacitet_voza
    w_p = data.w_p
    w_c = data.w_c

    # 3. Promenljive odlučivanja
    z = pulp.LpVariable.dicts("Zaustavljanje", (vozovi, stanice[:-1]), cat='Binary')
    dolazak = pulp.LpVariable.dicts("Dolazak", (vozovi, stanice), lowBound=0, cat='Continuous')
    polazak = pulp.LpVariable.dicts("Polazak", (vozovi, stanice), lowBound=0, cat='Continuous')
    tok_putnika = pulp.LpVariable.dicts("TokPutnika", (vozovi, range(len(stanice)-1), od_parovi), lowBound=0, cat='Continuous')

    # 4. Funkcija cilja (Minimizacija vremena putovanja)
    ukupni_troskovi = pulp.lpSum(
        w_p * (polazak[v][w[1]] - dolazak[v][w[0]]) * tok_putnika[v][j][w]
        for v in vozovi for j, (pocetna, krajnja) in enumerate(zip(stanice[:-1], stanice[1:])) 
        for w in od_parovi if w[0] == pocetna and w[1] == krajnja
    )
    prob += ukupni_troskovi, "Minimizacija_Ukupnog_Vremena"

    # 5. Sistemska ograničenja

    # Ograničenje 1: Vremenska konzistentnost na stanici
    for v in vozovi:
        for j_idx, j in enumerate(stanice[:-1]):
            prob += polazak[v][j] == dolazak[v][j] + (T_min * z[v][j]), f"Konzistentnost_Stanice_{v}_{j}"

    # Ograničenje 2: Granice vremena zadržavanja
    for v in vozovi:
        for j in stanice[:-1]:
            prob += polazak[v][j] - dolazak[v][j] >= T_min * z[v][j], f"Min_Zadrzavanje_{v}_{j}"
            prob += polazak[v][j] - dolazak[v][j] <= T_max * z[v][j], f"Max_Zadrzavanje_{v}_{j}"

    # Ograničenje 3: Kretanje voza između susednih stanica
    for v in vozovi:
        for j_idx in range(len(stanice) - 1):
            trenutna_stanica = stanice[j_idx]
            sledeca_stanica = stanice[j_idx + 1]
            t_v = vreme_voznje[v][j_idx]
            prob += dolazak[v][sledeca_stanica] >= polazak[v][trenutna_stanica] + t_v, f"Kretanje_Vozova_{v}_{trenutna_stanica}_{sledeca_stanica}"

    # Ograničenje 4: Kapacitet voza na deonicama
    for v in vozovi:
        for j_idx in range(len(stanice) - 1):
            prob += pulp.lpSum(tok_putnika[v][j_idx][w] for w in od_parovi) <= Kapacitet_voza, f"Kapacitet_Ogranicenje_{v}_sekcija{j_idx}"

    # Ograničenje 5: Bezbednosni razmaci (Headway)
    for v_idx in range(len(vozovi) - 1):
        voz1 = vozovi[v_idx]
        voz2 = vozovi[v_idx + 1]
        for j in stanice:
            prob += dolazak[voz2][j] - dolazak[voz1][j] >= H, f"Headway_{voz1}_{voz2}_{j}"

    # 6. Pokretanje solvera (CBC)
    print("Pokretanje optimizacije modela...")
    prob.solve(pulp.PULP_CBC_CMD(msg=True, timeLimit=300, gapRel=0.01))

    # 7. Ispis statusa i rezultata
    print(f"\nStatus rešenja: {pulp.LpStatus[prob.status]}")
    print(f"Optimalna vrednost funkcije cilja: {pulp.value(prob.objective):.2f}")

    print("\n--- REZULTATI: Vremena dolazaka i odlazaka vozova ---")
    for v in vozovi:
        print(f"Voz {v}:")
        for j in stanice:
            print(f"  Stanica {j} -> Dolazak: {dolazak[v][j].varValue:.1f} min, Polazak: {polazak[v][j].varValue:.1f} min")

if __name__ == "__main__":
    resi_model_reda_voznje()
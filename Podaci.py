# Podaci.py - Ulazni podaci za integrisani model rasporeda vozova i zaustavljanja

# Skupovi
vozovi = ['Voz1', 'Voz2', 'Voz3', 'Voz4']
stanice = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']

# OD parovi (početna stanica, krajnja stanica)
od_parovi = [('S1', 'S6'), ('S1', 'S4'), ('S2', 'S6'), ('S3', 'S5')]

# Vremenski intervali
vremenski_intervali = [1, 2, 3]

# Vremena vožnje između susednih stanica za svaki voz (u minutima)
vreme_voznje = {v: {j: 12 for j in range(len(stanice)-1)} for v in vozovi}

# Parametri modela
T_min = 1   # Minimalno vreme zadržavanja
T_max = 3   # Maksimalno vreme zadržavanja
H = 3       # Minimalni bezbednosni razmak (Headway)
Kapacitet_voza = 350   # Maksimalni kapacitet voza

# Težinski koeficijenti u funkciji cilja
w_p = 1.0  # Težina vremena putovanja
w_c = 1.5  # Težina čekanja
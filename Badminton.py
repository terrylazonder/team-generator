import streamlit as st
import random

st.title("Padminton Team Generator")

# ✅ Zorg ervoor dat session state correct is geïnitialiseerd
if "players" not in st.session_state:
    st.session_state.players = []

if "generated_teams" not in st.session_state:
    st.session_state.generated_teams = ([], None)  # Teams, Overgebleven speler

# 🔹 Sidebar: Spelers toevoegen
with st.sidebar:
    st.header("Spelers toevoegen")
    name = st.text_input("Naam")
    rating = st.slider("Rating (1 = zwak, 5 = sterk)", 1, 5, 3)

    if st.button("Speler toevoegen"):
        if name:
            st.session_state.players.append({"naam": name, "rating": rating})
            st.rerun()

    if st.button("Reset spelers"):
        st.session_state.players = []
        st.rerun()

# ✅ Spelerslijst weergeven en aanwezigheidsselectie
st.subheader("Selecteer aanwezige spelers")
if st.session_state.players:
    aanwezig = {}
    for player in st.session_state.players:
        aanwezig[player["naam"]] = st.checkbox(f'{player["naam"]} (Rating: {player["rating"]})', value=True)

    aanwezige_spelers = [p for p in st.session_state.players if aanwezig[p["naam"]]]

    if len(aanwezige_spelers) < 4:
        st.warning("Minstens 4 spelers nodig om teams te maken!")
    else:
        # 🔹 Functie voor teams genereren
        def maak_teams(keuze):
            spelers = aanwezige_spelers.copy()

            if keuze == "eerlijk_mix":
                # Sorteer spelers op rating en splits in 2 groepen
                spelers.sort(key=lambda x: x["rating"], reverse=True)
                sterken = spelers[:len(spelers)//2]
                zwakken = spelers[len(spelers)//2:]
                random.shuffle(sterken)
                random.shuffle(zwakken)
                teams = list(zip(sterken, zwakken))

            elif keuze == "eerlijk_gelijk":
                # 🔹 Stap 1: Sorteer spelers op rating (hoog naar laag)
                spelers.sort(key=lambda x: x["rating"], reverse=True)

                # ✅ Stap 2: Split de groep in exact twee helften
                midden_index = len(spelers) // 2
                sterke_helft = spelers[:midden_index]  # Sterke spelers (4-5)
                zwakke_helft = spelers[midden_index:]  # Zwakke spelers (1-2)

                # ✅ Stap 3: Shuffle de groepen en verdeel correct
                random.shuffle(sterke_helft)
                random.shuffle(zwakke_helft)

                teams = []
                
                # ✅ Sterken tegen sterken
                for i in range(0, len(sterke_helft) - 1, 2):
                    teams.append((sterke_helft[i], sterke_helft[i + 1]))

                # ✅ Zwakken tegen zwakken
                for i in range(0, len(zwakke_helft) - 1, 2):
                    teams.append((zwakke_helft[i], zwakke_helft[i + 1]))

            else:  # Volledig random
                random.shuffle(spelers)
                teams = [(spelers[i], spelers[i + 1]) for i in range(0, len(spelers) - 1, 2)]
    
            # ✅ Controleer of er een speler overblijft
            overgebleven_speler = None
            if len(spelers) % 2 == 1:
                overgebleven_speler = spelers[-1]  # Laatste speler zonder team

            return teams, overgebleven_speler

        # 🔹 Knoppen om teams te genereren
        col1, col2, col3 = st.columns(3)
        
        if col1.button("Eerlijke teams (Mix goed/slecht)"):
            st.session_state.generated_teams = maak_teams("eerlijk_mix")
            st.rerun()

        if col2.button("Eerlijke teams (Goed vs Goed, Slecht vs Slecht)"):
            st.session_state.generated_teams = maak_teams("eerlijk_gelijk")
            st.rerun()

        if col3.button("Volledig random teams"):
            st.session_state.generated_teams = maak_teams("random")
            st.rerun()

        # ✅ Teams weergeven in een mooie layout
        st.subheader("Gegenereerde teams")

        teams, overgebleven_speler = st.session_state.generated_teams

        if teams:
            wedstrijd_teksten = [
                f"🎾 {team[0]['naam']} & {team[1]['naam']}  VS  {tegenstander[0]['naam']} & {tegenstander[1]['naam']}"
                for team, tegenstander in zip(teams[::2], teams[1::2])
            ]

            for wedstrijd in wedstrijd_teksten:
                st.markdown(f"### {wedstrijd}")

            # ✅ Laat de overgebleven speler zien (indien van toepassing)
            if overgebleven_speler:
                st.warning(f"⏳ {overgebleven_speler['naam']} wacht op de volgende ronde.")
        else:
            st.info("Nog geen teams gegenereerd. Klik op een knop om teams te maken!")
else:
    st.info("Voeg spelers toe in het zijmenu.")

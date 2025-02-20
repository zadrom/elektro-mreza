import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def inicijaliziraj_mrezu():
    G = nx.Graph()
    
    # Dodavanje trafostanica 35kV
    G.add_node("TS35kV 1", pos=(2, 5))
    G.add_node("TS35kV 2", pos=(6, 5))
    
    # Dodavanje trafostanica 10/0.4 kV
    positions = {
        "TS1": (3, 4), "TS2": (4, 4), "TS3": (5, 4),
        "TS4": (3, 3), "TS5": (4, 3), "TS6": (5, 3),
        "TS7": (3, 2), "TS8": (4, 2), "TS9": (5, 2)
    }
    for ts, pos in positions.items():
        G.add_node(ts, pos=pos)
    
    # Povezivanje trafostanica dalekovodima
    connections = [
        ("TS35kV 1", "TS1"), ("TS1", "TS2"), ("TS2", "TS3"),
        ("TS2", "TS4"), ("TS3", "TS6"),
        ("TS4", "TS5"), ("TS5", "TS6"),
        ("TS4", "TS7"), ("TS5", "TS9"),
        ("TS7", "TS8"), ("TS8", "TS9"), ("TS9", "TS35kV 2"),
        ("TS35kV 1", "TS7"), ("TS35kV 2", "TS6"), ("TS35kV 2", "TS9"),
        ("TS35kV 1", "TS4")
    ]
    
    for a, b in connections:
        G.add_edge(a, b, color='gray', style='solid')
    
    return G

def prikazi_mrezu(G):
    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = [G[u][v]['color'] for u, v in G.edges]
    
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, edge_color=edge_colors)
    st.pyplot(plt)

def simulacija():
    st.title("Simulacija elektroenergetske mreže")
    G = inicijaliziraj_mrezu()
    
    scenariji = {
        "D1": "Kvar na D1 (TS1-TS2)",
        "D7": "Kvar na D7 (TS3-TS6)",
        "D10": "Kvar na D10 (TS6-TS9)"
    }
    
    odabir = st.radio("Odaberite scenarij kvara:", list(scenariji.keys()))
    
    if st.button("Pokreni scenarij"):
        if odabir == "D1":
            st.write("Relejna zaštita u TS35kV 1 je aktivirala zaštitu.")
            G.remove_edge("TS1", "TS2")
            G.remove_edge("TS2", "TS3")
        elif odabir == "D7":
            st.write("Relejna zaštita u TS35kV 2 je aktivirala zaštitu.")
            G.remove_edge("TS3", "TS6")
        elif odabir == "D10":
            st.write("Kvar na D10, isključuje se veza TS6-TS9.")
            G.remove_edge("TS6", "TS9")
        
        prikazi_mrezu(G)

if __name__ == "__main__":
    simulacija()

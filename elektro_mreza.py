import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def inicijaliziraj_mrezu():
    G = nx.Graph()
    
    # Definicija trafostanica
    ts_positions = {
        "TS35kV 1": (2, 5), "TS35kV 2": (6, 5),
        "TS1": (3, 4), "TS2": (4, 4), "TS3": (5, 4),
        "TS4": (3, 3), "TS5": (4, 3), "TS6": (5, 3),
        "TS7": (3, 2), "TS8": (4, 2), "TS9": (5, 2)
    }
    
    # Početne boje trafostanica
    napajanje_1 = ["TS35kV 1", "TS1", "TS2", "TS3", "TS4", "TS5"]
    napajanje_2 = ["TS35kV 2", "TS6", "TS7", "TS8", "TS9"]
    
    for ts in napajanje_1:
        G.add_node(ts, pos=ts_positions[ts], color='blue', source='TS35kV 1')
    for ts in napajanje_2:
        G.add_node(ts, pos=ts_positions[ts], color='brown', source='TS35kV 2')
    
    # Definicija dalekovoda
    connections = {
        "D1": ("TS35kV 1", "TS1"), "D2": ("TS1", "TS2"), "D3": ("TS2", "TS3"), "D4": ("TS3", "TS35kV 2"),
        "D5": ("TS35kV 1", "TS4"), "D6": ("TS4", "TS5"), "D7": ("TS5", "TS6"), "D8": ("TS6", "TS35kV 2"),
        "D9": ("TS35kV 1", "TS7"), "D10": ("TS7", "TS8"), "D11": ("TS8", "TS9"), "D12": ("TS9", "TS35kV 2"),
        "D13": ("TS1", "TS4"), "D14": ("TS4", "TS2"), "D15": ("TS5", "TS9"), "D16": ("TS6", "TS9"), "D17": ("TS4", "TS7")
    }
    
    # Isključeni dalekovodi
    off_lines = {"D4", "D9", "D13", "D14", "D7", "D15", "D16", "D17"}
    
    for name, (a, b) in connections.items():
        color = 'lightblue' if name in off_lines else 'green'
        G.add_edge(a, b, label=name, color=color, status='off' if name in off_lines else 'on')
    
    return G, connections, off_lines

def prikazi_mrezu(G):
    plt.figure(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    node_colors = [G.nodes[n]['color'] for n in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=2000, font_size=10)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    st.pyplot(plt)

def simulacija():
    st.title("Simulacija elektroenergetske mreže")
    G, connections, off_lines = inicijaliziraj_mrezu()
    prikazi_mrezu(G)
    
    scenariji = {"D1": "Kvar na D1", "D2": "Kvar na D2", "D3": "Kvar na D3", "D5": "Kvar na D5", "D6": "Kvar na D6", 
                 "D7": "Kvar na D7", "D8": "Kvar na D8", "D10": "Kvar na D10", "D11": "Kvar na D11", "D12": "Kvar na D12"}
    
    izbor = st.selectbox("Odaberite scenarij kvara:", list(scenariji.keys()))
    
    if izbor:
        kvar_ts = []
        st.write(f"Aktivirala se zaštita, kvar na {izbor}.")
        kvar_vod = connections[izbor]
        G[kvar_vod[0]][kvar_vod[1]]['color'] = 'red'
        
        if izbor in {"D1", "D2", "D3"}:
            kvar_ts = ["TS1", "TS2", "TS3"]
        elif izbor in {"D5", "D6"}:
            kvar_ts = ["TS4", "TS5"]
        elif izbor in {"D7", "D8"}:
            kvar_ts = ["TS6", "TS9"]
        elif izbor in {"D10", "D11", "D12"}:
            kvar_ts = ["TS7", "TS8", "TS9"]
        
        for ts in kvar_ts:
            G.nodes[ts]['color'] = 'orange'
            G.nodes[ts]['source'] = 'none'
        
        prikazi_mrezu(G)
        
        alternativni_vod = st.selectbox("Odaberite alternativni dalekovod za uključivanje:", list(off_lines))
        
        if st.button("Uključi odabrani dalekovod"):
            if alternativni_vod in off_lines:
                a, b = connections[alternativni_vod]
                G[a][b]['color'] = 'green'
                off_lines.remove(alternativni_vod)
                st.write(f"Uključen dalekovod {alternativni_vod}.")
                
                # Ponovno dodavanje napajanja i bojenje stanica
                for ts in kvar_ts:
                    if nx.has_path(G, "TS35kV 1", ts):
                        G.nodes[ts]['source'] = 'TS35kV 1'
                        G.nodes[ts]['color'] = 'blue'
                    elif nx.has_path(G, "TS35kV 2", ts):
                        G.nodes[ts]['source'] = 'TS35kV 2'
                        G.nodes[ts]['color'] = 'brown'
                        
            else:
                st.write("Odabran dalekovod nije ispravan za uključivanje.")
            prikazi_mrezu(G)

if __name__ == "__main__":
    simulacija()

import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class TimelineVisualization:
    """
    Visualizes the artistic evolution timeline in different views:
      - Grid view for side-by-side comparison
      - Process path visualization (graph)
      - Detailed comparison view
    """
    def __init__(self, art_history):
        self.art_history = art_history
        self.df = self._create_dataframe()

    def _create_dataframe(self):
        """Convert art history list into a DataFrame for future use."""
        if not self.art_history:
            return pd.DataFrame()
        return pd.DataFrame([
            {
                'iteration': i,
                'modification_type': entry.get('modification_type', 'Initial Creation' if i == 0 else 'Unknown'),
                'concept': entry.get('concept', ''),
                'image_url': entry.get('image_url', ''),
                'feedback': entry.get('feedback', ''),
                'image_analysis': entry.get('image_analysis', ''),
                'timestamp': entry.get('timestamp', datetime.now().isoformat())
            }
            for i, entry in enumerate(self.art_history)
        ])

    def format_modification_type(self, idx, artwork):
        """Return a formatted modification type string."""
        mod_type = "Initial Creation" if idx == 0 else artwork.get("modification_type", "Unknown")
        return mod_type.replace("_", " ").title() if mod_type else "Unknown"

    def display_grid_view(self, default_columns=3):
        """Display artworks in a grid for quick comparison."""
        st.subheader("Artwork Evolution Grid")
        selected_iterations = st.multiselect(
            "Select iterations to compare:",
            options=list(range(len(self.art_history))),
            default=list(range(min(6, len(self.art_history)))),
            help="Choose which artwork iterations to display"
        )
        columns = st.slider("Columns", 1, 4, default_columns)
        show_details = st.checkbox("Show details", True)

        if not selected_iterations:
            selected_iterations = list(range(len(self.art_history)))
        rows = (len(selected_iterations) + columns - 1) // columns

        for r in range(rows):
            cols = st.columns(columns)
            for c in range(columns):
                idx = r * columns + c
                if idx < len(selected_iterations):
                    iteration_idx = selected_iterations[idx]
                    artwork = self.art_history[iteration_idx]
                    with cols[c]:
                        st.image(artwork["image_url"],
                                 caption=f"Iteration {iteration_idx}",
                                 use_container_width=True)
                        if show_details:
                            with st.expander("Details"):
                                st.write(f"**Strategy**: {self.format_modification_type(iteration_idx, artwork)}")
                                st.write("**Concept:**")
                                st.text_area("", value=artwork.get("concept", ""),
                                             height=100,
                                             label_visibility="collapsed",
                                             disabled=True)

    def display_comparison_view(self):
        """Display a side-by-side comparison of two iterations."""
        st.subheader("Detailed Comparison View")
        iter_a = st.selectbox(
            "First Iteration",
            options=list(range(len(self.art_history))),
            index=0,
            format_func=lambda i: f"Iteration {i}"
        )
        default_iter_b = min(len(self.art_history) - 1, 1)
        iter_b = st.selectbox(
            "Second Iteration",
            options=list(range(len(self.art_history))),
            index=default_iter_b,
            format_func=lambda i: f"Iteration {i}"
        )

        if iter_a == iter_b:
            st.warning("Please select two different iterations to compare.")
            return

        artwork_a, artwork_b = self.art_history[iter_a], self.art_history[iter_b]
        col1, col2 = st.columns(2)
        with col1:
            st.image(artwork_a["image_url"],
                     caption=f"Iteration {iter_a}",
                     use_container_width=True)
            st.write(f"**Strategy**: {self.format_modification_type(iter_a, artwork_a)}")
        with col2:
            st.image(artwork_b["image_url"],
                     caption=f"Iteration {iter_b}",
                     use_container_width=True)
            st.write(f"**Strategy**: {self.format_modification_type(iter_b, artwork_b)}")

        st.subheader("Concept Evolution")
        col1, col2 = st.columns(2)
        with col1:
            st.text_area(f"Concept (Iteration {iter_a})",
                         value=artwork_a.get("concept", ""),
                         height=200)
        with col2:
            st.text_area(f"Concept (Iteration {iter_b})",
                         value=artwork_b.get("concept", ""),
                         height=200)

        st.subheader("Feedback and Analysis")
        col1, col2 = st.columns(2)
        with col1:
            feedback_a = artwork_a.get("feedback", "")
            if feedback_a:
                st.text_area(f"Feedback (Iteration {iter_a})",
                             value=feedback_a,
                             height=200,
                             disabled=True)
            else:
                st.info(f"No feedback for Iteration {iter_a}")
        with col2:
            feedback_b = artwork_b.get("feedback", "")
            if feedback_b:
                st.text_area(f"Feedback (Iteration {iter_b})",
                             value=feedback_b,
                             height=200,
                             disabled=True)
            else:
                st.info(f"No feedback for Iteration {iter_b}")

    def display_process_path(self):
        """Visualize the artwork evolution as a directed graph."""
        st.subheader("Artistic Process Path")
        if len(self.art_history) <= 1:
            st.info("At least two iterations are needed to visualize a process path.")
            return

        G = nx.DiGraph()
        for i, artwork in enumerate(self.art_history):
            mod_type = self.format_modification_type(i, artwork)
            G.add_node(i, label=f"Iteration {i}", strategy=mod_type, image=artwork.get("image_url", ""))
            if i > 0:
                G.add_edge(i - 1, i)

        pos = {i: (i, 0) for i in range(len(self.art_history))}
        fig = go.Figure()
        # Add edges
        for start, end in G.edges():
            x0, y0 = pos[start]
            x1, y1 = pos[end]
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1],
                                     mode='lines',
                                     line=dict(color='gray', width=2),
                                     hoverinfo='none'))
        # Add nodes
        node_x, node_y, node_text, node_colors = [], [], [], []
        strategy_types = list({G.nodes[n]['strategy'] for n in G.nodes()})
        color_map = {strategy: px.colors.qualitative.Pastel1[i % len(px.colors.qualitative.Pastel1)]
                     for i, strategy in enumerate(strategy_types)}
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"Iteration: {node}<br>Strategy: {G.nodes[node]['strategy']}")
            node_colors.append(color_map[G.nodes[node]['strategy']])
        fig.add_trace(go.Scatter(x=node_x, y=node_y,
                                 mode='markers',
                                 marker=dict(size=30, color=node_colors, line=dict(width=2, color='Grey')),
                                 text=node_text,
                                 hoverinfo='text'))
        # Add labels and legend
        for node in G.nodes():
            x, y = pos[node]
            fig.add_annotation(x=x, y=y, text=str(node),
                               showarrow=False, font=dict(color='DarkSlateGrey', size=12))
        for strategy in strategy_types:
            fig.add_trace(go.Scatter(x=[None], y=[None],
                                     mode='markers',
                                     marker=dict(size=10, color=color_map[strategy]),
                                     name=strategy,
                                     showlegend=True))
        fig.update_layout(showlegend=True,
                          legend_title_text='Strategies',
                          hovermode='closest',
                          margin=dict(b=20, l=5, r=5, t=40),
                          xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          plot_bgcolor='#dcdaf4',
                          height=250)
        st.plotly_chart(fig, use_container_width=True)
        # Display thumbnails below the graph
        cols = st.columns(len(self.art_history))
        for i, (col, artwork) in enumerate(zip(cols, self.art_history)):
            with col:
                st.image(artwork["image_url"], caption=f"{i}", width=100)

    def display_main_interface(self):
        """Render the main interface with tabs for different visualizations."""
        st.title("Artistic Evolution Visualization")
        if not self.art_history:
            st.warning("No artwork history found. Create some art first!")
            return
        tabs = st.tabs(["Grid View", "Process Path", "Comparison View"])
        with tabs[0]:
            self.display_grid_view()
        with tabs[1]:
            self.display_process_path()
        with tabs[2]:
            self.display_comparison_view()

def visualize_art_history(art_history):
    """Wrapper to create and render the timeline visualization."""
    viz = TimelineVisualization(art_history)
    viz.display_main_interface()

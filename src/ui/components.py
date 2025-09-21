# src/ui/components.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

class PremiumComponents:
    def __init__(self):
        self.nvidia_green = '#76B900'
        self.google_blue = '#4285F4'
        
    def hero_header(self, title, subtitle):
        """Premium hero header with animations"""
        st.markdown(f"""
        <div class="main-header">
            <h1 style="margin:0; font-size:2.5rem; font-weight:700; 
                       background: linear-gradient(45deg, white, #E8EAED);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🏥 {title}
            </h1>
            <p style="margin:0.5rem 0 0 0; font-size:1.1rem; opacity:0.9;">
                {subtitle}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def performance_sidebar(self, metrics):
        """Live performance monitoring sidebar"""
        with st.sidebar:
            st.markdown("### 🚀 System Performance")
            
            # Memory usage with animated bar
            memory_percent = metrics.get('memory_percent', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h4>Memory Usage</h4>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {memory_percent}%"></div>
                </div>
                <p>{memory_percent:.1f}% ({metrics.get('memory_gb', 0):.1f} GB)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # CPU usage
            cpu_percent = metrics.get('cpu_percent', 0)
            st.metric(
                "CPU Usage",
                f"{cpu_percent:.1f}%",
                delta=f"{cpu_percent-50:.1f}%" if cpu_percent > 50 else None
            )
            
            # Model status
            st.success("✅ Models Loaded")
            st.info("🔄 CPU Optimized")
    
    def analysis_progress(self, progress_value, stage_name):
        """Animated analysis progress"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            "🔍 Loading medical image...",
            "🧠 AI model inference...",
            "📊 Analyzing results...",
            "📝 Generating insights...",
            "✅ Analysis complete!"
        ]
        
        import time
        for i, stage in enumerate(stages):
            progress_bar.progress((i + 1) / len(stages))
            status_text.text(stage)
            time.sleep(0.5)
            
        return True
    
    def confidence_display(self, predictions):
        """Display prediction confidence with visual bars"""
        st.markdown("### 🎯 Confidence Scores")
        
        for class_name, confidence in predictions.items():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.write(f"**{class_name}**")
            
            with col2:
                # Custom confidence bar
                bar_color = self.nvidia_green if confidence > 0.7 else self.google_blue
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); border-radius: 8px; overflow: hidden;">
                    <div style="width: {confidence*100}%; height: 25px; 
                               background: {bar_color}; border-radius: 8px;
                               display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-weight: bold;">{confidence:.1%}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def medical_image_viewer(self, image, overlay=None):
        """Advanced medical image viewer with overlays"""
        fig = go.Figure()
        
        # Base image
        fig.add_trace(go.Heatmap(
            z=image,
            colorscale='gray',
            showscale=False
        ))
        
        # Overlay (segmentation mask)
        if overlay is not None:
            fig.add_trace(go.Heatmap(
                z=overlay,
                colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(118,185,0,0.6)']],
                showscale=False
            ))
        
        fig.update_layout(
            title="Medical Image Analysis",
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

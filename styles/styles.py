style_global = """
<style>
/* Sidebar style */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #F5ADAD, #9271D3);
    color: white;
    font-family: 'Georgia';
}
[data-testid="stSidebar"] .css-17eq0hr a {
    color: #FFD700;
    font-size: 20px;
}
[data-testid="stSidebar"] .css-17eq0hr a:hover {
    color: #FFFFFF;
}
[data-testid="stSidebar"] h1 {
    color: white;
    font-size: 26px;
    font-weight: bold;
}

/* Global body and typography */
body {
    background-color: #f0f2f6;
    font-family: 'Helvetica Neue', Helvetica;
    color: #333;
}
h1 {
    text-align: center;
    color: #1A1A40;
    font-family: 'Georgia';
    font-size: 48px;
    margin-bottom: 10px;
}
h2, h3 {
    color: #1A1A40;
    font-weight: bold;
}
p {
    font-size: 16px;
    line-height: 1.6;
    color: #444;
}

/* Hero section for Home page */
.hero-section {
    background: linear-gradient(120deg, #F5ADAD, #9271D3);
    padding: 40px;
    border-radius: 10px;
    margin-bottom: 30px;
    color: white;
}

/* Text area styling */
.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #ccc;
    padding: 10px;
}

/* Spinner styling */
div.stSpinner {
    color: #2c3e50;
}
</style>
"""

style_custom = """
<style>
/* Strategy Cards Styling */
.strategy-description {
    background: linear-gradient(to top, rgba(238,174,202,0.15) 0%, rgba(148,187,233,0.15) 100%);
    border-radius: 12px;
    padding: 20px 25px;
    margin-top: 15px;
    border-left: 5px solid #8b6d8e;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.strategy-description:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.strategy-title {
    color: #8b6d8e;
    font-size: 1.4rem;
    margin-bottom: 12px;
    font-weight: 600;
    border-bottom: 1px solid rgba(146, 113, 211, 0.3);
    padding-bottom: 8px;
}

.strategy-content {
    color: #444;
    line-height: 1.6;
    font-size: 1.05rem;
}

.strategy-example {
    font-style: italic;
    margin-top: 10px;
    color: #555;
}

/* Artwork Display Styling */
.artwork-display {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.concept-display {
    border-radius: 10px;
    padding: 15px;
    height: 100%;
}

/* Evolution Timeline Styling */
.timeline-tabs .stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.timeline-tabs .stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #f0f0f0;
    border-radius: 8px 8px 0 0;
}

.timeline-tabs .stTabs [aria-selected="true"] {
    background-color: #1E88E5;
    color: white;
}
</style>
"""


style_buttons = """
<style>
/* Button styling */
button[kind="primary"] {
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    border: none;
    border-radius: 16px;
    padding: 0.8rem 1.5rem;
    margin-top: 1rem;
    transition: background 0.5s ease;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    text-decoration: none;
    display: inline-block;
}
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #F7C1C2, #B294DC);
    cursor: pointer;
}

button[kind="secondary"] {
    background-image: radial-gradient(circle, rgba(238,174,202,0.3) 0%, rgba(148,187,233,0.3) 100%);
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 10px;
    text-align: left;
    height: 120px;
    width: 100%;
    white-space: pre-wrap;
    transition: background 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 10px;
}

button[kind="secondary"]:hover {
    background: radial-gradient(circle, rgba(238,174,202,0.5) 0%, rgba(148,187,233,0.5) 100%);
}
</style>
"""
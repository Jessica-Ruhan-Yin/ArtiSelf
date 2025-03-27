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

/* Button style */
.cta-button, div.stButton > button {
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    margin-top: 1rem;
    transition: background 0.5s ease;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    text-decoration: none;
    display: inline-block;
}
.cta-button:hover, div.stButton > button:hover {
    background: linear-gradient(135deg, #F7C1C2, #B294DC);
    cursor: pointer;
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
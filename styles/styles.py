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

styles_home = """
<style>
.hero-section {
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    border-radius: 15px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.hero-section:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.hero-section::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
    transform: rotate(30deg);
}

.hero-title {
    color: white;
    font-size: 4rem;
    font-weight: 800;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease-out;
}

.hero-subtitle {
    color: white;
    font-size: 1.4rem;
    margin-bottom: 2rem;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.15);
    animation: fadeInUp 1.2s ease-out;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-top: 3rem;
    margin-bottom: 3rem;
}

.feature-card {
    background: linear-gradient(to bottom, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    text-align: center;
    height: 100%;
    backdrop-filter: blur(5px);
}

.feature-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.feature-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #333;
}

.feature-desc {
    color: #555;
    font-size: 1rem;
    line-height: 1.5;
}

.how-it-works-step {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 10px;
    background: linear-gradient(90deg, rgba(255,179,209,0.1) 0%, rgba(249,246,255,0.3) 100%);
}
.step-number {
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 15px;
    flex-shrink: 0;
}

.cta-button {
    background: linear-gradient(135deg, #9271D3, #F5ADAD);
    color: white;
    border: none;
    padding: 0.8rem 2rem;
    font-size: 1.2rem;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    display: inline-block;
    animation: pulse 2s infinite;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 7px 20px rgba(0, 0, 0, 0.25);
}

.testimonial-section {
    background: linear-gradient(to right, rgba(238,174,202,0.1), rgba(148,187,233,0.1));
    border-radius: 15px;
    padding: 2rem;
    margin-top: 2rem;
    position: relative;
}

.demo-section {
    margin-top: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.demo-container {
    position: relative;
    width: 100%;
    max-width: 800px;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.footer {
    margin-top: 3rem;
    text-align: center;
    padding: 1.5rem;
    color: #666;
    font-size: 0.9rem;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(146, 113, 211, 0.4);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(146, 113, 211, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(146, 113, 211, 0);
    }
}

.hidden {
    opacity: 0;
}

.show {
    opacity: 1;
    transition: all 1s;
}

/* Responsive adjustments */
@media (max-width: 992px) {
    .feature-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 3rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

create_artwork_styles = """
<style>
.artwork-container {
    background: linear-gradient(to right, rgba(238,174,202,0.1), rgba(148,187,233,0.1));
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.artwork-container:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    justify-content: center;
}

.concept-input {
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    padding: 1rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.concept-input:focus {
    border-color: #9271D3;
    box-shadow: 0 5px 15px rgba(146, 113, 211, 0.2);
}

.concept-container {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    height: 100%;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.image-container {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
}


.section-divider {
    height: 2px;
    background: linear-gradient(to right, rgba(238,174,202,0.3), rgba(148,187,233,0.3));
    margin: 2rem 0;
    border-radius: 2px;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    color: #9271D3;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fade-in {
    animation: fadeIn 0.8s ease-in;
}

.creative-tip {
    background: linear-gradient(135deg, rgba(245,173,173,0.1), rgba(146,113,211,0.1));
    border-left: 3px solid #9271D3;
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 0 10px 10px 0;
    font-style: italic;
    color: #555;
}
</style>
"""

collection_styles = """
<style>
.collection-card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.collection-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}
.collection-meta {
    color: #666;
    font-size: 0.8rem;
    margin-bottom: 10px;
}
.collection-desc {
    color: #333;
    font-size: 0.9rem;
    margin-bottom: 15px;
    max-height: 60px;
    overflow: hidden;
}
.collection-count {
    color: #9271D3;
    font-weight: 600;
    font-size: 0.9rem;
}
.thumbnail-container {
    display: flex;
    gap: 5px;
    margin-bottom: 15px;
    position: relative;
}
.thumbnail-container img {
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.evolution-arrow {
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    text-align: center;
    color: rgba(146, 113, 211, 0.7);
    font-size: 1.5rem;
    z-index: 2;
    pointer-events: none;
}
.delete-dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}
.delete-dialog {
    background: white;
    border-radius: 10px;
    padding: 20px;
    max-width: 500px;
    width: 90%;
    text-align: center;
}

/* Page Layout and General Styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.page-title {
    text-align: center;
    color: #1E293B;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Collection Grid Layout */
.collections-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

/* Collection Card Styling */
.collection-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    padding: 1.5rem;
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.collection-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.collection-card h4 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #1A365D;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.collection-meta {
    color: #64748B;
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
}

.collection-desc {
    color: #334155;
    font-size: 0.95rem;
    margin-bottom: 1rem;
    flex-grow: 1;
}

.collection-count {
    display: inline-block;
    background: #E2E8F0;
    color: #475569;
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* Thumbnail Styling */
.thumbnail-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    gap: 0.75rem;
    height: 160px; /* Fixed height for consistent thumbnail rows */
}

.thumbnail-image {
    flex: 1;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12);
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F8FAFC;
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.thumbnail-image img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    display: block;
}

.thumbnail-caption {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.3rem 0.5rem;
    text-align: center;
}

.evolution-arrow {
    color: #3B82F6;
    font-size: 1.75rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    flex-shrink: 0;
}


/* Empty State */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    background: #F8FAFC;
    border-radius: 12px;
    margin-top: 2rem;
}

.empty-state-icon {
    font-size: 3rem;
    color: #94A3B8;
    margin-bottom: 1rem;
}

.empty-state-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 0.5rem;
}

.empty-state-desc {
    color: #64748B;
    max-width: 500px;
    margin: 0 auto 1.5rem auto;
}
</style>
"""

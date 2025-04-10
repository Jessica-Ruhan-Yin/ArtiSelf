empty_state_html = """
<div class="empty-state">
    <div class="empty-state-animation">
        <div class="empty-state-icon">✨🎨✨</div>
    </div>
    <div class="prompt-suggestions">
        <h3>Need inspiration? Try these concepts:</h4>
        <div class="prompt-examples">
            <div class="prompt-example" onclick="usePrompt(this.textContent)">A vibrant cityscape at sunset with neon lights reflecting in puddles</div>
            <div class="prompt-example" onclick="usePrompt(this.textContent)">An ethereal forest with bioluminescent plants and mystical creatures</div>
            <div class="prompt-example" onclick="usePrompt(this.textContent)">A surreal underwater world with floating islands and ancient ruins</div>
        </div>
    </div>
</div>

<style>
.empty-state {
    text-align: center;
    padding: 1.5rem 3.5rem;
    border-radius: 20px;
    background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(249,246,255,0.9));
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin: 2rem 2rem;
    max-width: 800px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: float 3s ease-in-out infinite;
}
.empty-state:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(146,113,211,0.15);
}
.empty-state-animation {
    position: relative;
    height: 120px;
    overflow: hidden;
    margin-bottom: 1rem;
}
.empty-state-icon {
    font-size: 4rem;
    color: transparent;
    background: linear-gradient(135deg, #F5ADAD, #9271D3);
    -webkit-background-clip: text;
    background-clip: text;
    animation: pulse 2s infinite alternate;
}
.empty-state-title {
    color: #333;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #1A1A40, #9271D3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.empty-state-text {
    color: #555;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}
.prompt-suggestions {
    background: linear-gradient(to right, rgba(238,174,202,0.1), rgba(148,187,233,0.1));
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.prompt-suggestions h4 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}
.prompt-examples {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.prompt-example {
    background: white;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    border-left: 4px solid #9271D3;
    text-align: left;
    color: #555;
    font-style: italic;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
    cursor: pointer;
}
.prompt-example:hover {
    background: rgba(249,246,255,0.9);
    transform: translateX(5px);
}
@keyframes pulse {
    0% { opacity: 0.6; transform: scale(0.97); }
    100% { opacity: 1; transform: scale(1.03); }
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
}
</style>
"""

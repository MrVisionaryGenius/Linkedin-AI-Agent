import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# Define your system prompt with style examples
SYSTEM_PROMPT = """
You're writing as a tech-savvy, energetic, Gen-Z-flavored LinkedIn creator.

Use short paragraphs, strong formatting, emojis, and bold hooks. Your tone blends wit, insight, and curiosity. Every post should sound like it's written by a smart builder talking to their peers—not a brand.

IMPORTANT FORMATTING RESTRICTIONS:
- DO NOT use rocket emojis (🚀)

Here are three examples of my tone:

---

1️⃣

Headline:
Tired of Burning Cash on AI? 💸 Output Length Is Your Money Switch!

Body:
You pour hours into crafting the perfect AI prompts, but are you optimizing the output? You're probably wasting money 💸

Output length is THE underestimated configuration setting in the Large Language Model Land. Get this wrong, and you leave money 💰on the table:

Too many tokens? Costs skyrocket.  
Cutting corners? You're clipping the model's wings ✂.  
Complex chains = more $$$ wasted.

Want cost-effective AI and faster results?  
Optimize both prompt AND output!

👇 What's YOUR best hidden gem for reducing token usage?

---

2️⃣

From Fuzzy Friends to Future Visions 🤯

My first deep learning project? (Like so many others)  
A classic cat vs. dog classifier.  
Cut to today, and I'm crafting surreal AI art with ChatGPT.

The tools have evolved *fast*—and so has the journey.  
Beginner or expert, now's the best time to dive in.

🐱 What was YOUR first coding project?

---
3️⃣

YC rejected me.

Google didn't hire me.

VCs passed.

An angel investor ghosted me.

Still I went on to achieve Town Hall 17 in Clash of Clans.

Don't let anyone tell you that you can't win.

---

Now, write a new LinkedIn post in this style. Use a strong headline with emoji, 3–5 short punchy paragraphs, and end with a CTA or engagement hook.
"""

# Function to generate post using Gemini
def generate_linkedin_post(topic: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    {SYSTEM_PROMPT}

    Topic: {topic}
    Goal: Create a high-performing LinkedIn post based on this.
    """

    response = model.generate_content(prompt)
    return response.text

# Streamlit UI setup with custom styles
st.set_page_config(page_title="LinkedIn Post Writer", layout="centered")

# Custom CSS
st.markdown("""
<style>
.big-title {
    font-size: 3rem;
    font-weight: bold;
    color: #4F8BF9;
    text-align: center;
}
.subtext {
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 30px;
    color: #6c757d;
}
.usage-meter {
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 1px solid #dee2e6;
}
.meter-title {
    font-weight: bold;
    color: #495057;
    margin-bottom: 5px;
}
.meter-circles {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 10px 0;
}
.meter-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
}
.available {
    background-color: #28a745;
}
.used {
    background-color: #dc3545;
}
.locked {
    background-color: #6c757d;
}
.meter-text {
    text-align: center;
    font-size: 0.9rem;
    color: #6c757d;
}
.premium-box {
    background-color: #fff3cd;
    border: 1px solid #ffeeba;
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
}
.premium-title {
    font-weight: bold;
    color: #856404;
    margin-bottom: 5px;
}
.premium-text {
    color: #856404;
    font-size: 0.9rem;
}
.auth-section {
    background-color: #e2e3e5;
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
}
.copy-button {
    background-color:#4F8BF9;
    color:white;
    padding:10px 20px;
    border:none;
    border-radius:10px;
    cursor:pointer;
    font-size: 0.95rem;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="big-title">✨ Write LinkedIn Posts That Sound Like YOU</div>
<div class="subtext">Backed by Gemini AI. Trained on your personal style. Made for virality. ⚡️</div>
""", unsafe_allow_html=True)

# Session init
if "post_count" not in st.session_state:
    st.session_state.post_count = 0

# Usage meter - Always visible
free_posts_used = min(st.session_state.post_count, 2)
free_posts_left = max(0, 2 - st.session_state.post_count)

st.markdown(f"""
<div class="usage-meter">
    <div class="meter-title">📊 Free Post Usage</div>
    <div class="meter-circles">
        <div class="meter-circle {'used' if free_posts_used > 0 else 'available'}">{'✓' if free_posts_used > 0 else '1'}</div>
        <div class="meter-circle {'used' if free_posts_used > 1 else 'available'}">{'✓' if free_posts_used > 1 else '2'}</div>
        <div class="meter-circle locked">🔒</div>
        <div class="meter-circle locked">🔒</div>
        <div class="meter-circle locked">🔒</div>
    </div>
    <div class="meter-text">
        You've used <b>{free_posts_used}/2</b> free posts. {f"<b>{free_posts_left} remaining!</b>" if free_posts_left > 0 else "<b>Upgrade for unlimited posts!</b>"}
    </div>
</div>
""", unsafe_allow_html=True)

# Input from user
topic = st.text_input("🧠 Enter a topic you'd like to post about:", "The future of recruiters in an AI-powered hiring world")

# Authentication section
OWNER_PASS = os.getenv("OWNER_PASS", "letmein")  # change this to something only you know

st.markdown("""
<div class="auth-section">
    <div class="meter-title">🔐 Premium Access</div>
""", unsafe_allow_html=True)

user_key = st.text_input("Enter your access code:", type="password", help="Enter your premium access code to unlock unlimited posts")

is_owner = user_key == OWNER_PASS
can_generate = is_owner or free_posts_left > 0

# Premium box for users who've hit the limit
if free_posts_left == 0 and not is_owner:
    st.markdown("""
    <div class="premium-box">
        <div class="premium-title">🌟 Unlock Unlimited Posts!</div>
        <div class="premium-text">
            You've reached your free limit. DM me for a premium access code to unlock unlimited post generation!
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Close auth section

# Generate button and result area
if st.button("🎯 Generate Post", disabled=(not can_generate)):
    if not can_generate:
        st.warning("🚫 You've used all your free posts. Please enter an access code to continue.")
    else:
        with st.spinner("Crafting magic... ✨"):
            try:
                post = generate_linkedin_post(topic)
                if not is_owner:
                    st.session_state.post_count += 1  # Count this usage for free users

                st.markdown("---")
                st.subheader("📣 Your LinkedIn Post")
                st.code(post, language="markdown")
                
                # Copy to clipboard using Streamlit's component
                st.markdown("""
                <script>
                function copyTextToClipboard(text) {
                    navigator.clipboard.writeText(text).then(function() {
                        alert('Copied to clipboard!');
                    }, function(err) {
                        alert('Failed to copy text: ' + err);
                    });
                }
                </script>
                <button class="copy-button" onclick="copyTextToClipboard(`""" + post.replace("`", "\\`") + """\`)">📋 Copy to Clipboard</button>
                """, unsafe_allow_html=True)

                # Update the usage meter after generation
                if not is_owner:
                    free_posts_used = min(st.session_state.post_count, 2)
                    free_posts_left = max(0, 2 - st.session_state.post_count)

                    st.markdown(f"""
                    <div class="usage-meter" style="margin-top: 20px;">
                        <div class="meter-text">
                            You now have <b>{free_posts_used}/2</b> free posts used. {f"<b>{free_posts_left} remaining!</b>" if free_posts_left > 0 else "<b>You've used all your free posts!</b>"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.8rem;">
    Built with ARROGANCE by Mohammeed Saad.
</div>
""", unsafe_allow_html=True)
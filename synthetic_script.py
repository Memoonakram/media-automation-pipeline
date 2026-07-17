import streamlit as st
from huggingface_hub import InferenceClient
import io
from PIL import Image
from gtts import gTTS  # New robust TTS library

# --- Page Config & Styling ---
st.set_page_config(page_title="Generative Media Pipeline", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #FF4B4B; margin-bottom: 5px; }
    .subtitle { font-size: 1.1rem; color: #808495; margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 Generative Media Scripting Pipeline</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Professional studio-grade marketing script & asset generator powered by Open Source AI.</div>',
    unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.image("https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=50)
st.sidebar.title("Pipeline Settings")
# Ab token background secrets se automatically load hoga
hf_token = st.secrets["HF_TOKEN"]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Script Customization")
language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Roman Urdu", "Urdu (Urdu Script)", "Hindi"]
)
tone = st.sidebar.selectbox(
    "Select Tone",
    ["Exciting & Energetic", "Professional & Corporate", "Humorous & Funny", "Emotional & Touching"]
)

# --- Input Fields ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    product_name = st.text_input("📦 Product/Service Name", placeholder="e.g., Cake Shop")
with col_in2:
    target_audience = st.text_input("🎯 Target Audience", placeholder="e.g., Foodies")

# --- Session States ---
if "generated_script" not in st.session_state:
    st.session_state.generated_script = ""
if "generated_storyboard" not in st.session_state:
    st.session_state.generated_storyboard = ""
if "suggested_image_prompt" not in st.session_state:
    st.session_state.suggested_image_prompt = ""

# --- Stage 1: Script Generation ---
if st.button("🔥 Generate AI Script", type="primary"):
    if not hf_token:
        st.error("Please enter your Hugging Face Token in the sidebar first!")
    elif product_name and target_audience:
        with st.spinner("Llama Engine is crafting your customized script..."):
            try:
                # Direct client initialization with explicit endpoints to bypass auto-router logic
                client = InferenceClient(token=hf_token)

                prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
                You are a professional copywriter. Write the output in: {language} and tone: {tone}.<|eot_id|><|start_header_id|>user<|end_header_id|>
                Create a professional short-form video script (under 60 seconds) using the AIDA framework.

                Product/Service: {product_name}
                Target Audience: {target_audience}

                STRICT REQUIREMENTS:
                1. Write the script entirely in: {language}.
                2. Use this Tone: {tone}.

                Provide the output strictly divided into these sections:
                1. [ATTENTION HOOK - First 3 seconds]
                2. [INTEREST - Problem setup]
                3. [DESIRE - The solution and value proposition]
                4. [CALL TO ACTION - High converting ending]
                <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

                # Using text_generation explicitly targets the model without routing conflicts
                response = client.text_generation(
                    prompt,
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    max_new_tokens=500
                )
                st.session_state.generated_script = response
                st.success("Script generated successfully!")

            except Exception as e:
                st.error(f"Script Generation Error: {e}")
    else:
        st.error("Please fill in both fields!")

if st.session_state.generated_script:
    st.subheader(f"📝 Generated Script ({language} - {tone})")
    st.info(st.session_state.generated_script)

    # --- Stage 2: Storyboard Generation ---
    st.markdown("---")
    st.header("🎨 Stage 2: Media Asset & Storyboard Planner")

    if st.button("🎬 Generate Visual Storyboard"):
        with st.spinner("Analyzing script to design visual scenes & image prompts..."):
            try:
                client = InferenceClient(token=hf_token)

                storyboard_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
                You are a professional video producer. Create a structured storyboard.<|eot_id|><|start_header_id|>user<|end_header_id|>
                You are an expert Art Director. Analyze this script and create a structured storyboard.
                Provide:
                1. **Visual Description**
                2. **Camera Angle & Movement**
                3. **AI Image Prompt**: (Write ONLY one highly descriptive English prompt optimized for image generators, starting with 'AI Image Prompt: ...')
                4. **Audio & Sound Effects (SFX)**

                Script:
                {st.session_state.generated_script}
                <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

                response = client.text_generation(
                    storyboard_prompt,
                    model="meta-llama/Llama-3.3-70B-Instruct",
                    max_new_tokens=800
                )
                st.session_state.generated_storyboard = response

                lines = st.session_state.generated_storyboard.split('\n')
                for line in lines:
                    if "Prompt" in line or "prompt" in line:
                        st.session_state.suggested_image_prompt = line.split(":")[-1].strip().replace('"', '')
                        break
                if not st.session_state.suggested_image_prompt:
                    st.session_state.suggested_image_prompt = f"Cinematic shot of {product_name}, professional advertising photography, 8k resolution"

                st.success("Storyboard generated successfully!")

            except Exception as e:
                st.error(f"Storyboard Error: {e}")

if st.session_state.generated_storyboard:
    st.subheader("📋 Production Storyboard")
    st.write(st.session_state.generated_storyboard)

    # --- Stage 3: Live AI Asset Generation Hub ---
    st.markdown("---")
    st.header("🚀 Stage 3: Live AI Asset Generation Hub")
    st.write("Generate real media assets directly using open-source models!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Real-Time Scene Generator")
        custom_img_prompt = st.text_area("Adjust Image Generation Prompt",
                                         value=st.session_state.suggested_image_prompt)

        if st.button("🎨 Render Scene Image"):
            with st.spinner("Drawing your scene using FLUX..."):
                try:
                    img_client = InferenceClient(token=hf_token)
                    image = img_client.text_to_image(
                        custom_img_prompt,
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    st.image(image, caption="AI Generated Scene Visual", use_container_width=True)

                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="💾 Download Rendered Image",
                        data=buf.getvalue(),
                        file_name="generated_scene.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Image Generation Failed: {e}")

    with col2:
        st.subheader("🎙️ Real-Time Voiceover Generator (TTS)")
        # Clean formatting tags so the voice reads cleanly
        clean_text = st.session_state.generated_script.replace("[", "").replace("]", "").replace("**", "")
        st.text_area("Script text to convert into Audio", value=clean_text, height=120)

        if st.button("🔊 Generate Audio Voiceover"):
            with st.spinner("Converting text to speech via Google Engine..."):
                try:
                    # Dynamically adjust language for Google TTS
                    lang_code = 'en'
                    if language in ["Urdu (Urdu Script)", "Roman Urdu"]:
                        lang_code = 'ur'
                    elif language == "Hindi":
                        lang_code = 'hi'

                    # Generate audio block using gTTS locally
                    tts = gTTS(text=clean_text, lang=lang_code, slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)

                    # Streamlit Audio Player
                    st.audio(fp.read(), format="audio/mp3")
                    st.success("Voiceover generated successfully!")

                    st.download_button(
                        label="📥 Download Audio File",
                        data=fp.getvalue(),
                        file_name="voiceover.mp3",
                        mime="audio/mp3"
                    )
                except Exception as e:
                    st.error(f"TTS Generation Failed: {e}")

        # --- AI AVATAR INTEGRATION ---
        st.markdown("---")
        st.subheader("👤 AI Avatar Integration")
        st.write(
            "Want a talking digital human to read this script? You can generate video avatars using the prompt and script generated above!")
        st.info(
            "💡 **Pro-Tip for Avatar Video:** Use the Cleaned Script above, choose an avatar on platforms like **HeyGen**, **Synthesia** or **SadTalker**, paste the script, and merge it with the AI Image we rendered on the left!")

    st.markdown("---")
    st.download_button(
        label="📥 Download Full Production Brief (TXT)",
        data=f"=== SCRIPT ===\n{st.session_state.generated_script}\n\n=== STORYBOARD ===\n{st.session_state.generated_storyboard}",
        file_name="marketing_video_production_brief.txt",
        mime="text/plain"
    )
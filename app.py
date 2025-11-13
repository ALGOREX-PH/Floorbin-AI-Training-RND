import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Floorbin Design AI Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize session state
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

# Title and description
st.title("🎨 Floorbin Design Concept Generator")
st.markdown("### AI-Powered POS Display Design for IQOS TEREA Products")
st.markdown("---")

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key"
    )

    if api_key:
        openai.api_key = api_key
        st.success("API Key configured ✓")
    else:
        st.warning("Please enter your OpenAI API Key")

    st.markdown("---")

    # Model selection
    model = st.selectbox(
        "Model",
        ["gpt-image-1", "dall-e-3", "dall-e-2"],
        index=0,
        help="gpt-image-1 is OpenAI's latest image generation model"
    )

    # Image quality and size
    if model == "gpt-image-1":
        quality = st.selectbox("Quality", ["auto", "low", "medium", "high"], index=0,
                              help="auto = automatic quality selection based on prompt")
        size = st.selectbox("Size", ["1024x1024", "1792x1024", "1024x1792"], index=0)
    elif model == "dall-e-3":
        quality = st.selectbox("Quality", ["standard", "hd"], index=1)
        size = st.selectbox("Size", ["1024x1024", "1792x1024", "1024x1792"], index=0)
    else:
        quality = "standard"
        size = st.selectbox("Size", ["256x256", "512x512", "1024x1024"], index=2)

    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    This tool generates floorbin design concepts for IQOS TEREA products using OpenAI's image generation models.

    **Features:**
    - Product-specific customization
    - Brand guideline integration
    - Multiple design variations
    - Export capabilities
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Product Information")

    # Product details
    product_name = st.text_input(
        "Product Name",
        value="TEREA Clear Regular",
        help="Enter the TEREA product variant name"
    )

    product_flavor = st.text_input(
        "Flavor Profile",
        value="Refined, Clear, Subtle Lemon",
        help="Describe the flavor characteristics"
    )

    launch_date = st.text_input(
        "Launch Date (Optional)",
        value="",
        placeholder="e.g., October 27, 2025"
    )

    price = st.text_input(
        "Price (Optional)",
        value="",
        placeholder="e.g., ¥580"
    )

    st.markdown("---")

    st.header("Design Direction")

    # Creative mood
    creative_mood = st.multiselect(
        "Creative Mood",
        ["Indulging Pleasure", "Sophisticated", "Refined", "Bold", "Vibrant", "Minimalist", "Luxurious"],
        default=["Indulging Pleasure", "Refined"],
        help="Select the overall mood for the design"
    )

    # Color palette
    color_scheme = st.multiselect(
        "Color Palette",
        ["White & Black (High Contrast)", "Gold Accents", "Gradient Background",
         "Product Colors", "Bright & Colorful", "Monochrome", "Pastel Tones"],
        default=["White & Black (High Contrast)", "Gold Accents"],
        help="Select color themes based on TEREA guidelines"
    )

    # Design elements
    design_elements = st.multiselect(
        "Key Design Elements",
        ["3D Product Rendering", "Bold Typography", "Key Visual (KV)",
         "Smoke/Vapor Effects", "Geometric Shapes", "Product Photography",
         "Price Display", "Launch Date Badge"],
        default=["3D Product Rendering", "Bold Typography"],
        help="Select elements to include in the design"
    )

    # Historical reference
    historical_style = st.selectbox(
        "Historical Style Reference",
        ["None", "TEREA Oasis Pearl Style", "Black Ruby Menthol Style",
         "SENTIA Style", "Limited Edition Style", "Device Launch Style"],
        index=0,
        help="Reference past successful floorbin campaigns"
    )

with col2:
    st.header("Prompt Configuration")

    # Auto-generate prompt based on selections
    auto_prompt = f"""Create a professional retail floorbin display design for {product_name}.

Product Details:
- Flavor: {product_flavor}
{f"- Launch Date: {launch_date}" if launch_date else ""}
{f"- Price: {price}" if price else ""}

Design Direction:
- Mood: {", ".join(creative_mood)}
- Colors: {", ".join(color_scheme)}
- Key Elements: {", ".join(design_elements)}
{f"- Style Reference: {historical_style}" if historical_style != "None" else ""}

Requirements:
- High-end retail point-of-sale display
- IQOS ILUMA device aesthetic
- Premium tobacco product positioning
- Clean, modern, eye-catching design
- Suitable for Japanese retail environment
- 3D floorbin structure with product placement"""

    # Display auto-generated prompt
    st.text_area(
        "Auto-Generated Prompt",
        value=auto_prompt,
        height=200,
        help="This prompt is automatically generated from your selections"
    )

    # Allow custom modifications
    use_custom = st.checkbox("Use Custom Prompt", value=False)

    if use_custom:
        custom_prompt = st.text_area(
            "Custom Prompt",
            value=auto_prompt,
            height=200,
            help="Edit the prompt to your specific needs"
        )
        final_prompt = custom_prompt
    else:
        final_prompt = auto_prompt

    st.markdown("---")

    # Generation settings
    col_a, col_b = st.columns(2)

    with col_a:
        num_variations = st.number_input(
            "Number of Variations",
            min_value=1,
            max_value=4 if model == "dall-e-2" else 1,
            value=1,
            help="gpt-image-1 and DALL-E 3 only support 1 image per request"
        )

    with col_b:
        style = st.selectbox(
            "Style (DALL-E 3 only)",
            ["vivid", "natural"],
            index=0,
            help="vivid = hyper-real, natural = more realistic"
        ) if model == "dall-e-3" else "vivid"

# Generate button
st.markdown("---")

col_gen1, col_gen2, col_gen3 = st.columns([1, 2, 1])

with col_gen2:
    generate_button = st.button("🎨 Generate Floorbin Design", use_container_width=True, type="primary")

# Generation logic
if generate_button:
    if not api_key:
        st.error("❌ Please enter your OpenAI API Key in the sidebar")
    else:
        with st.spinner("🎨 Generating design concept... This may take 30-60 seconds..."):
            try:
                # Call OpenAI API
                if model == "gpt-image-1":
                    response = openai.images.generate(
                        model=model,
                        prompt=final_prompt,
                        size=size,
                        quality=quality,
                        n=1
                    )
                elif model == "dall-e-3":
                    response = openai.images.generate(
                        model=model,
                        prompt=final_prompt,
                        size=size,
                        quality=quality,
                        style=style,
                        n=1
                    )
                else:  # dall-e-2
                    response = openai.images.generate(
                        model=model,
                        prompt=final_prompt,
                        size=size,
                        n=num_variations
                    )

                # Store generated images
                st.session_state.generated_images = []

                for img_data in response.data:
                    # Check if response has URL or base64 data
                    img_url = getattr(img_data, 'url', None)
                    img_b64 = getattr(img_data, 'b64_json', None)

                    st.session_state.generated_images.append({
                        'url': img_url,
                        'b64_json': img_b64,
                        'revised_prompt': getattr(img_data, 'revised_prompt', None),
                        'product': product_name,
                        'model': model
                    })

                st.success(f"✅ Successfully generated {len(response.data)} design concept(s)!")

            except Exception as e:
                st.error(f"❌ Error generating image: {str(e)}")

# Display generated images
if st.session_state.generated_images:
    st.markdown("---")
    st.header("Generated Design Concepts")

    for idx, img_info in enumerate(st.session_state.generated_images):
        st.subheader(f"Concept {idx + 1}: {img_info['product']}")

        col_img, col_info = st.columns([2, 1])

        with col_img:
            # Download and display the image
            try:
                response = requests.get(img_info['url'])
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, use_container_width=True)
                else:
                    st.error(f"Failed to load image: Status {response.status_code}")
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")

        with col_info:
            st.markdown(f"**Model:** {img_info['model']}")

            if img_info['revised_prompt']:
                with st.expander("View Revised Prompt"):
                    st.write(img_info['revised_prompt'])

            # Download button
            try:
                response = requests.get(img_info['url'])
                if response.status_code == 200:
                    st.download_button(
                        label="📥 Download Image",
                        data=response.content,
                        file_name=f"floorbin_{img_info['product'].replace(' ', '_')}_{idx+1}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error preparing download: {str(e)}")

        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Floorbin Design AI Generator | Powered by OpenAI | Publicis AI Exploration</p>
</div>
""", unsafe_allow_html=True)

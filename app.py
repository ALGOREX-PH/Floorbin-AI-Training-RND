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

    # Reference image upload
    st.subheader("Product Reference Image")
    uploaded_file = st.file_uploader(
        "Upload Product Image (Optional)",
        type=["png", "jpg", "jpeg"],
        help="Upload a reference image of the product for visual context"
    )

    if uploaded_file is not None:
        reference_image = Image.open(uploaded_file)
        st.image(reference_image, caption="Reference Image", use_container_width=True)

    st.markdown("---")

    st.header("Design Direction")

    # Design Tone Selector
    design_tone = st.radio(
        "Overall Design Tone",
        ["Premium & Sophisticated", "Striking & Powerful", "Bold & Aggressive", "Minimal & Clean", "Vibrant & Energetic"],
        index=0,
        help="Choose the overall tone and energy of the floorbin design"
    )

    st.markdown("---")

    # Creative mood - auto-populate based on tone
    if design_tone == "Premium & Sophisticated":
        default_mood = ["Sophisticated", "Refined", "Luxurious"]
    elif design_tone == "Striking & Powerful":
        default_mood = ["Bold", "Indulging Pleasure", "Sophisticated"]
    elif design_tone == "Bold & Aggressive":
        default_mood = ["Bold", "Vibrant"]
    elif design_tone == "Minimal & Clean":
        default_mood = ["Minimalist", "Refined"]
    else:  # Vibrant & Energetic
        default_mood = ["Vibrant", "Bold", "Indulging Pleasure"]

    creative_mood = st.multiselect(
        "Creative Mood (Customizable)",
        ["Indulging Pleasure", "Sophisticated", "Refined", "Bold", "Vibrant", "Minimalist", "Luxurious"],
        default=default_mood,
        help="Fine-tune the mood - pre-populated based on your tone selection"
    )

    # Color palette
    color_scheme = st.multiselect(
        "Color Palette Presets",
        ["White & Black (High Contrast)", "Gold Accents", "Gradient Background",
         "Product Colors", "Bright & Colorful", "Monochrome", "Pastel Tones"],
        default=["White & Black (High Contrast)", "Gold Accents"],
        help="Select color theme presets or use custom colors below"
    )

    st.markdown("#### Custom Color Selection")

    col_color1, col_color2, col_color3 = st.columns(3)

    with col_color1:
        primary_color = st.color_picker(
            "Primary Color",
            value="#FFFFFF",
            help="Main background/panel color (default: white)"
        )

    with col_color2:
        accent_color = st.color_picker(
            "Accent Color",
            value="#D4AF37",
            help="Lighting/accent color (default: gold)"
        )

    with col_color3:
        base_color = st.color_picker(
            "Base Color",
            value="#000000",
            help="Base platform color (default: black)"
        )

    # Design elements
    design_elements = st.multiselect(
        "Key Design Elements",
        ["3D Product Rendering", "Bold Typography", "Key Visual (KV)",
         "Smoke/Vapor Effects", "Geometric Shapes", "Product Photography",
         "Price Display", "Launch Date Badge", "Tiered Display Structure", "Premium Lighting"],
        default=["3D Product Rendering", "Bold Typography", "Price Display", "Tiered Display Structure", "Premium Lighting"],
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

    # Generate tone-specific instructions
    if design_tone == "Premium & Sophisticated":
        tone_instructions = f"""sophisticated, high-end style with museum-quality presentation.

STRUCTURE & LAYOUT:
- Multi-tiered stepped display structure with 3-4 levels creating depth
- Each tier should be a clean platform/shelf at different heights
- Stepped/terraced design showing clear elevation between levels
- Elegant, refined structural design
- Base platform with premium finish

COLOR SCHEME & MATERIALS:
- Primary: Background panels in {primary_color} (hex color) with matte finish
- Accent: Edge lighting in {accent_color} (hex color) around each tier
- Base: Platform in {base_color} (hex color) and structural elements
- Price tags styled to complement the color scheme
- Premium, luxurious materials

LIGHTING & ATMOSPHERE:
- Professional studio lighting with soft shadows
- LED edge lighting in {accent_color} highlighting tier edges
- Premium lighting creating depth and dimension
- Dramatic but sophisticated lighting
- Clean neutral studio background"""

    elif design_tone == "Striking & Powerful":
        tone_instructions = """striking, powerful, and commanding presence.

STRUCTURE & LAYOUT:
- Bold, dynamic multi-level structure with dramatic height differences
- Angular, geometric tiers creating visual impact
- Strong vertical presence dominating the space
- Confident structural elements
- Dark base with strong contrast

COLOR SCHEME & MATERIALS:
- High-contrast color scheme with bold accents
- Dramatic lighting - bright spotlights or colored LED accents
- Mix of matte black and glossy finishes
- Metallic accents (silver, chrome, or bold gold)
- Strong visual contrast throughout

LIGHTING & ATMOSPHERE:
- Dramatic directional lighting creating strong shadows
- High-intensity spotlights on key products
- Colored accent lighting for impact
- Bold, theatrical atmosphere
- Dark or gradient background for drama"""

    elif design_tone == "Bold & Aggressive":
        tone_instructions = """bold, aggressive, and high-energy style.

STRUCTURE & LAYOUT:
- Dynamic, asymmetric structure with sharp angles
- Dramatic diagonal lines and bold geometric shapes
- Unconventional tier arrangements
- Edgy, attention-grabbing design
- Strong base with industrial elements

COLOR SCHEME & MATERIALS:
- Intense color combinations (black with neon, red, electric blue)
- Glossy, reflective surfaces
- Industrial materials mixed with premium finishes
- Sharp contrasts and bold patterns
- Vibrant accent colors

LIGHTING & ATMOSPHERE:
- Intense, high-contrast lighting
- Neon or colored LED strips for edge lighting
- Dramatic spotlights and shadows
- Energetic, dynamic feel
- Dark background with colored accents"""

    elif design_tone == "Minimal & Clean":
        tone_instructions = """minimal, clean, and ultra-refined style.

STRUCTURE & LAYOUT:
- Simple, elegant geometric forms
- Clean lines with minimal ornamentation
- 2-3 levels with clear separation
- Emphasis on negative space
- Pure white or neutral base

COLOR SCHEME & MATERIALS:
- Monochromatic or very limited color palette
- White, light gray, or soft neutrals
- Matte finishes throughout
- Subtle metal accents if any
- Clean, uncluttered aesthetic

LIGHTING & ATMOSPHERE:
- Soft, even lighting
- Minimal shadows
- Natural, clean atmosphere
- Pure white or very light gray background
- Focus on simplicity and clarity"""

    else:  # Vibrant & Energetic
        tone_instructions = """vibrant, energetic, and eye-catching style.

STRUCTURE & LAYOUT:
- Dynamic, playful multi-level design
- Curved or flowing tier arrangements
- Energetic, upward-moving composition
- Fun, engaging structural elements
- Colorful base elements

COLOR SCHEME & MATERIALS:
- Bright, saturated colors
- Gradient backgrounds and colored lighting
- Mix of glossy and matte finishes
- Colorful accent elements throughout
- Joyful, vibrant color palette

LIGHTING & ATMOSPHERE:
- Bright, colorful lighting
- Rainbow or multi-colored LED accents
- Cheerful, upbeat atmosphere
- Colorful gradient background
- Energetic, dynamic feel"""

    # Auto-generate prompt based on selections
    auto_prompt = f"""Create a premium 3D retail floorbin display for {product_name} in a {tone_instructions}

PRODUCT DISPLAY:
- Multiple {product_name} product boxes displayed prominently
- IQOS ILUMA device featured on one of the tiers
- Products arranged at varying angles for visual interest
- Clear product visibility from front view
- Flavor: {product_flavor}
{f"- Price displays showing: {price}" if price else "- Price tags prominently displayed"}
{f"- Launch Date: {launch_date}" if launch_date else ""}
- Additional color guidance: {", ".join(color_scheme)}
- Key elements to include: {", ".join(design_elements)}

TYPOGRAPHY & BRANDING:
- Large "TEREA" branding at top of display
- Product name "{product_name}" in bold typography
- Japanese text included for authenticity
- Flavor description in typography matching the tone
- Price displays in modern font

MOOD & STYLE:
- Overall mood: {", ".join(creative_mood)}
- Design tone: {design_tone}
- Japanese retail environment aesthetic
- IQOS ILUMA brand aesthetic
- Photorealistic 3D rendering quality
- Professional product photography style
{f"- Style reference: {historical_style}" if historical_style != "None" else ""}

TECHNICAL REQUIREMENTS:
- 3D rendered appearance with perfect perspective
- Photorealistic materials and textures
- Professional color grading
- Clean composition with proper negative space
- Suitable for Japanese retail environment
{"- IMPORTANT: Match the product design and colors from the reference image provided" if uploaded_file is not None else ""}

Design Approach: Create a display that embodies the {design_tone.lower()} aesthetic while maintaining the TEREA brand identity."""

    # Display auto-generated prompt
    st.text_area(
        "Auto-Generated Prompt",
        value=auto_prompt,
        height=350,
        help="This prompt is automatically generated from your selections"
    )

    # Allow custom modifications
    use_custom = st.checkbox("Use Custom Prompt", value=False)

    if use_custom:
        custom_prompt = st.text_area(
            "Custom Prompt",
            value=auto_prompt,
            height=350,
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
                        n=1,
                        response_format="url"
                    )
                else:  # dall-e-2
                    response = openai.images.generate(
                        model=model,
                        prompt=final_prompt,
                        size=size,
                        n=num_variations,
                        response_format="url"
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
                if img_info['url']:
                    # Handle URL-based response (DALL-E models)
                    response = requests.get(img_info['url'])
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, use_container_width=True)
                    else:
                        st.error(f"Failed to load image: Status {response.status_code}")
                elif img_info['b64_json']:
                    # Handle base64-encoded response (gpt-image-1)
                    image_data = base64.b64decode(img_info['b64_json'])
                    image = Image.open(BytesIO(image_data))
                    st.image(image, use_container_width=True)
                else:
                    st.error("No image data available")
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")

        with col_info:
            st.markdown(f"**Model:** {img_info['model']}")

            if img_info['revised_prompt']:
                with st.expander("View Revised Prompt"):
                    st.write(img_info['revised_prompt'])

            # Download button
            try:
                image_data = None
                if img_info['url']:
                    response = requests.get(img_info['url'])
                    if response.status_code == 200:
                        image_data = response.content
                elif img_info['b64_json']:
                    image_data = base64.b64decode(img_info['b64_json'])

                if image_data:
                    st.download_button(
                        label="📥 Download Image",
                        data=image_data,
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

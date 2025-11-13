# Floorbin Design AI Generator

AI-powered tool for generating Point-of-Sale (POS) floorbin design concepts for IQOS TEREA products using OpenAI's image generation models.

## Overview

This Streamlit application explores AI capabilities for producing low-mid fidelity floorbin design concepts, addressing the Publicis AI Exploration brief. The tool enables rapid concept generation while maintaining TEREA brand guidelines and learning from historical floorbin campaigns.

## Features

- **Product Customization**: Input specific product details (name, flavor, launch date, price)
- **Reference Image Upload**: Upload product images for visual reference and context
- **Design Tone Selection**: Choose from 5 distinct tones - Premium & Sophisticated, Striking & Powerful, Bold & Aggressive, Minimal & Clean, or Vibrant & Energetic
- **Creative Direction**: Select mood, color palette, and design elements based on TEREA brand guidelines
- **Historical Reference**: Apply styles from past successful campaigns (Oasis Pearl, Black Ruby, SENTIA, etc.)
- **AI-Powered Generation**: Use gpt-image-1, DALL-E 3, or DALL-E 2 for image generation
- **Multiple Variations**: Generate multiple design concepts (DALL-E 2 only)
- **Export Capabilities**: Download generated designs for presentations

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation

1. **Clone or navigate to the repository**:
   ```bash
   cd C:\Users\algor\Documents\Floorbin-Publicis-AI-Model-RND\Floorbin-AI-Training
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure your API key**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

   **Alternative**: You can also enter the API key directly in the app's sidebar.

## Usage

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**: The app will automatically open at `http://localhost:8501`

3. **Configure the app**:
   - Enter your OpenAI API key in the sidebar (if not using .env file)
   - Select your preferred model (gpt-image-1 is the default)
   - Choose image quality and size

4. **Input product information**:
   - Product name (e.g., "TEREA Clear Regular")
   - Flavor profile (e.g., "Refined, Clear, Subtle Lemon")
   - Optional: Launch date and price
   - Optional: Upload a reference image of the product

5. **Set design direction**:
   - **Choose overall design tone**: Premium & Sophisticated, Striking & Powerful, Bold & Aggressive, Minimal & Clean, or Vibrant & Energetic
   - Creative mood (auto-populated based on tone, customizable)
   - Color palette presets (e.g., "White & Black", "Gold Accents")
   - **Custom color pickers**: Choose exact colors for primary panels, accent lighting, and base platform
   - Key design elements (e.g., "3D Product Rendering", "Bold Typography")
   - Historical style reference (optional)

6. **Generate designs**:
   - Review the auto-generated prompt
   - Optionally customize the prompt
   - Click "Generate Floorbin Design"
   - Wait 30-60 seconds for generation

7. **Review and export**:
   - View generated concepts
   - Download images for your presentation

## Design Tone Options

The app offers five distinct design tones to match different campaign objectives:

### Premium & Sophisticated (Default)
- Museum-quality, luxury aesthetic
- Multi-tiered stepped structure with gold edge lighting
- Clean white/cream panels with black base
- Perfect for flagship products and high-end launches
- Similar to the reference floorbin design

### Striking & Powerful
- Bold, commanding presence with dramatic impact
- Angular geometric structures with strong vertical elements
- High-contrast lighting and metallic accents
- Ideal for making a strong statement in retail

### Bold & Aggressive
- High-energy, attention-grabbing design
- Sharp angles, asymmetric structures, dynamic forms
- Intense colors (neon accents, electric blue, red)
- Perfect for youth-oriented or limited edition launches

### Minimal & Clean
- Ultra-refined, simple elegance
- Clean geometric forms with emphasis on negative space
- Monochromatic palette, soft lighting
- Best for sophisticated, understated campaigns

### Vibrant & Energetic
- Bright, colorful, eye-catching
- Dynamic, playful structures with flowing forms
- Gradient backgrounds, multi-colored LED lighting
- Great for celebratory launches and festive campaigns

## Model Comparison

### gpt-image-1 (Default)
- **Pros**:
  - Latest OpenAI image generation model
  - High quality outputs
  - Better understanding of complex prompts
  - Accurate 3D representation
  - Flexible quality options (auto, low, medium, high)
  - Auto quality mode intelligently adjusts based on prompt
- **Cons**:
  - Only 1 image per request
  - Premium pricing

### DALL-E 3
- **Pros**:
  - High quality outputs
  - Better understanding of complex prompts
  - More accurate 3D representation
  - HD quality option
- **Cons**:
  - Only 1 image per request
  - Higher cost per image
  - Slower generation

### DALL-E 2
- **Pros**:
  - Generate up to 4 variations at once
  - Lower cost
  - Faster generation
- **Cons**:
  - Lower quality
  - Less accurate prompt interpretation

## Cost Considerations

OpenAI pricing (check https://openai.com/pricing for latest rates):
- **gpt-image-1**: Check OpenAI pricing page for current rates
- **DALL-E 3**:
  - Standard (1024x1024): $0.040 per image
  - HD (1024x1024): $0.080 per image
- **DALL-E 2**:
  - 1024x1024: $0.020 per image

## Use Case: AI Tool Exploration Brief

This tool addresses the key questions from the brief:

### 1. Which AI tools are best for floorbin design?
**gpt-image-1** and **DALL-E 3** show strong capability for:
- Understanding complex brand guidelines
- Generating retail-appropriate designs
- Maintaining visual consistency

### 2. Can AI understand 3D aspects in flat images?
**Yes, with proper prompting**:
- gpt-image-1 and DALL-E 3 can interpret 3D floorbin structures
- Requires detailed descriptions of spatial elements
- Best results with explicit "3D rendering" instructions

### 3. Pros and Cons

**Pros**:
- Rapid concept generation (minutes vs. days)
- Multiple variations quickly (with DALL-E 2)
- Reduces early-stage rendering costs
- Maintains brand consistency with proper prompts
- Can learn from historical examples through prompt engineering

**Cons**:
- Cannot perfectly replicate specific brand fonts
- Limited control over exact product placement
- Requires manual refinement for final production
- Text rendering can be inconsistent
- Cannot directly load/train on past floorbin files

## Project Structure

```
Floorbin-AI-Training/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .env                   # Your API key (gitignored)
└── README.md              # This file
```

## Tips for Best Results

1. **Be specific in product descriptions**: More detail = better results
2. **Upload reference images**: Provide product photos to help the AI understand colors, styling, and branding
3. **Reference brand guidelines**: Mention "TEREA style", "IQOS aesthetic"
4. **Specify 3D elements**: Explicitly request "3D floorbin structure"
5. **Iterate prompts**: Try variations of successful prompts
6. **Use high quality settings**: For gpt-image-1 use 'high' or 'auto', for DALL-E 3 use 'hd'
7. **Combine with manual design**: Use AI for ideation, refine manually

## Troubleshooting

### API Key Errors
- Ensure your API key is valid and has credits
- Check the key is correctly entered (no extra spaces)

### Generation Failures
- Try simplifying your prompt
- Reduce image size if timeout occurs
- Check OpenAI API status: https://status.openai.com

### Model Not Found Error
- If gpt-image-1 is not available on your account, switch to DALL-E 3
- Some models may require specific API access

### Slow Generation
- gpt-image-1 and DALL-E 3 HD can take 60+ seconds
- Use DALL-E 2 for faster iterations

## Next Steps

To create the Publicis-branded deck:
1. Generate multiple concepts for TEREA Clear Regular
2. Document the generation process (prompts, iterations)
3. Compare AI outputs vs. manual designs
4. Analyze time/cost savings
5. Recommend integration into current workflow

## Support

For issues or questions about:
- **The app**: Contact the development team
- **OpenAI API**: Visit https://platform.openai.com/docs
- **TEREA brand guidelines**: Refer to brand documentation

---

**Publicis AI Exploration | November 2024**

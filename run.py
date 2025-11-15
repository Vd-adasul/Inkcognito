#!/usr/bin/env python3
"""
Main execution file for the content generation and humanization pipeline.

Usage:
    python run.py "Your input prompt here"
"""
import sys
from src.generator import ContentGenerator
from src.humanizer import humanize_text
from config.config import DEFAULT_P_SYN, DEFAULT_P_TRANS


def main():
    """Main execution function."""
    # Check if prompt is provided
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as an argument.")
        print("Usage: python run.py \"Your input prompt here\"")
        sys.exit(1)
    
    # Get prompt from command line
    prompt = sys.argv[1]
    
    if not prompt.strip():
        print("Error: Prompt cannot be empty.")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 Content Generation & Humanization Pipeline")
    print("=" * 60)
    print(f"\n📝 Input Prompt: {prompt}\n")
    
    try:
        # Step 1: Generate content
        print("\n" + "=" * 60)
        print("PHASE 1: Content Generation")
        print("=" * 60)
        generator = ContentGenerator()
        generated_text = generator.generate(prompt)
        
        print(f"\n✅ Generated {len(generated_text.split())} words")
        
        # Step 2: Humanize the generated text
        print("\n" + "=" * 60)
        print("PHASE 2: Text Humanization")
        print("=" * 60)
        print("Applying humanization transformations...")
        humanized_text = humanize_text(
            generated_text,
            p_syn=DEFAULT_P_SYN,
            p_trans=DEFAULT_P_TRANS
        )
        
        print(f"✅ Humanized {len(humanized_text.split())} words")
        
        # Display final output
        print("\n" + "=" * 60)
        print("🎯 FINAL OUTPUT")
        print("=" * 60)
        print("\n" + humanized_text + "\n")
        print("=" * 60)
        print("✅ Process completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


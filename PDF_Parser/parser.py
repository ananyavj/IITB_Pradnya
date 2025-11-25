import fitz  # PyMuPDF
import os
import hashlib
import re

def extract_content(pdf_path, output_dir, images_dir):
    """
    Parses a PDF file and converts it to Markdown, extracting images and metadata.
    """
    doc = fitz.open(pdf_path)
    md_content = []
    metadata = {
        "title": doc.metadata.get("title", ""),
        "author": doc.metadata.get("author", ""),
        "page_count": len(doc),
        "headers": [],
        "footers": []
    }
    
    # Ensure directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(f"Processing: {pdf_path}")

    for page_num, page in enumerate(doc):
        page_height = page.rect.height
        
        # Heuristic for header/footer regions (top 5% and bottom 5%)
        header_threshold = page_height * 0.05
        footer_threshold = page_height * 0.95
        
        # Use "dict" with sort=True to get reading order
        blocks = page.get_text("dict", sort=True)["blocks"]

        for block in blocks:
            bbox = block["bbox"]
            y0, y1 = bbox[1], bbox[3]
            
            # Check for Header/Footer
            if y1 < header_threshold:
                # It's likely a header
                text = extract_text_from_block(block)
                if text.strip():
                    metadata["headers"].append({"page": page_num + 1, "text": text.strip()})
                continue
            elif y0 > footer_threshold:
                # It's likely a footer
                text = extract_text_from_block(block)
                if text.strip():
                    metadata["footers"].append({"page": page_num + 1, "text": text.strip()})
                continue

            # Process Text Block only (image extraction removed)
            if block["type"] == 0:  # text
                for line in block["lines"]:
                    line_text = ""
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        
                        # Check if it's a bullet point
                        is_bullet = len(text) <= 2 and text in ['•', '○', '■', '□', '-', '*', '>', '»']
                        font_size = span["size"]
                        
                        # Format based on type
                        if is_bullet:
                            line_text += f"{text} "
                        elif font_size > 14 and len(text) > 2:  # Headings (but not single chars)
                            line_text += f"## {text} "
                        elif font_size > 12 and len(text) > 2:
                            line_text += f"### {text} "
                        else:
                            line_text += f"{text} "
                    
                    if line_text.strip():
                        md_content.append(line_text.strip())

    # Post-processing: Filter metadata and merge lines
    final_lines = []
    current_paragraph = ""

    for line in md_content:
        stripped = line.strip()
        
        # Skip common metadata patterns (dates, page numbers, running headers)
        # Dates: 03/05/18, 3/5/18, etc.
        if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$', stripped):
            continue
        # Page numbers with section names: "2 EXEMPLAR PROBLEMS", "3 REAL NUMBERS"
        # Also handles leading spaces like " 2 EXEMPLAR PROBLEMS"
        if re.match(r'^\s*\d+\s+[A-Z][A-Z\s]+$', line) and len(stripped) < 40:
            continue
        # Section names with page numbers: "REAL NUMBERS 3", "EXEMPLAR PROBLEMS 2"
        if re.match(r'^\s*[A-Z][A-Z\s]+\d+\s*$', line) and len(stripped) < 40:
            continue
        

        
        # If it's a heading, flush and add
        if line.startswith("#"):
            if current_paragraph:
                final_lines.append(current_paragraph)
                current_paragraph = ""
            final_lines.append(f"\n{line}\n")
            continue

        # If it's a list item (bullet or numbered), start new paragraph
        if re.match(r'^(•|○|■|□|\d+\.|\([A-Z]\))', stripped):
            if current_paragraph:
                final_lines.append(current_paragraph)
                current_paragraph = ""
            current_paragraph = line
            continue

        # Merge logic
        if current_paragraph:
            # Check if previous line ends with sentence terminator or answer choice
            last_char = current_paragraph.strip()[-1] if current_paragraph.strip() else ''
            ends_with_terminator = last_char in ['.', '!', '?', ':']
            ends_with_choice = re.search(r'\([A-D]\)\s*$', current_paragraph.strip())
            starts_new_section = re.match(r'^(Sample Question|Solution|EXERCISE|Chapter|C HAPTER|\d+\.)', line)
            
            if ends_with_terminator or ends_with_choice or starts_new_section:
                final_lines.append(current_paragraph)
                current_paragraph = line
            else:
                # Merge with space
                current_paragraph += " " + line
        else:
            current_paragraph = line

    if current_paragraph:
        final_lines.append(current_paragraph)

    full_text = "\n\n".join(final_lines)
    
    # Remove Devanagari Unicode characters (U+0900 to U+097F)
    # This cleans up PDFs that have Hindi characters mixed in English text
    full_text = re.sub(r'[\u0900-\u097F]+', '', full_text)
    
    # Remove excessive blank lines
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    
    # Add Metadata Frontmatter
    frontmatter = "---\n"
    frontmatter += f"title: {metadata['title']}\n"
    frontmatter += f"page_count: {metadata['page_count']}\n"
    frontmatter += "---\n\n"
    
    final_output = frontmatter + full_text
    
    output_file = os.path.join(output_dir, f"{base_name}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_output)
        
    # Generate metadata JSON
    metadata_json = generate_metadata(base_name, full_text, metadata)
    metadata_file = os.path.join(r"c:\Projects\AI Aarohan - Copy\PDF_Parser\metadata", f"{base_name}.json")
    with open(metadata_file, "w", encoding="utf-8") as f:
        import json
        json.dump(metadata_json, f, indent=2, ensure_ascii=False)
    
    print(f"Done! Output saved to: {output_file}")
    print(f"Metadata saved to: {metadata_file}")
    return output_file

def generate_metadata(filename, content, pdf_metadata):
    """Generate metadata JSON from parsed content."""
    import json
    
    # Extract headings (lines starting with ## or ###)
    headings = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('##'):
            heading = stripped.replace('###', '').replace('##', '').strip()
            # Filter out invalid headings (chemical equations, too short, has arrows, etc.)
            if heading and len(heading) > 2 and '→' not in heading and '(' not in heading[:10]:
                # Further filter: must have alphabetic characters
                if any(c.isalpha() for c in heading):
                    headings.append(heading)
    
    # Determine subject from filename
    subject_map = {
        'math': 'Mathematics',
        'ganith': 'Mathematics',
        'science': 'Science',
        'vigyan': 'Science',
        'english': 'English',
        'hindi': 'Hindi',
        'social': 'Social Studies'
    }
    
    subject = "Unknown"
    for key, value in subject_map.items():
        if key.lower() in filename.lower():
            subject = value
            break
    
    # Extract unit number from filename
    unit_match = re.search(r'unit[\s_]?(\d+)', filename, re.IGNORECASE)
    unit = int(unit_match.group(1)) if unit_match else 1
    
    # Determine language
    language = "en"
    if any(hindi_word in filename.lower() for hindi_word in ['ganith', 'vigyan', 'hindi']):
        language = "hi"
    
    # Generate skills tags based on subject
    skills_tags = []
    if subject == "Mathematics":
        skills_tags = ["problem_solving", "numerical_reasoning", "logical_thinking"]
    elif subject == "Science":
        skills_tags = ["scientific_reasoning", "observation", "experimentation"]
    elif subject == "English":
        skills_tags = ["reading_comprehension", "vocabulary", "grammar"]
    
    metadata = {
        "lesson_id": f"{subject.lower()}_unit{unit}",
        "subject": subject,
        "unit": unit,
        "language": language,
        "source": "NCERT",
        "filename": filename,
        "page_count": pdf_metadata.get('page_count', 0),
        "headings": headings[:10],  # Limit to first 10 headings
        "skills_tags": skills_tags
    }
    
    return metadata

def extract_text_from_block(block):
    """Helper to extract raw text from a block."""
    text = ""
    if block["type"] == 0:
        for line in block["lines"]:
            for span in line["spans"]:
                text += span["text"] + " "
    return text

if __name__ == "__main__":
    # Configuration
    INPUT_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\input"
    OUTPUT_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\output"
    IMAGES_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\images"
    
    # Process all PDFs in input directory
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
    else:
        files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
        if not files:
            print("No PDF files found in input directory.")
        else:
            for f in files:
                pdf_path = os.path.join(INPUT_DIR, f)
                try:
                    extract_content(pdf_path, OUTPUT_DIR, IMAGES_DIR)
                except Exception as e:
                    print(f"Error processing {f}: {e}")

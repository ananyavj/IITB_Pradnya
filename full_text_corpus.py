"""
Script to create full_text_corpus.txt from markdown files
Input: .md files from FINAL_PARSED_FILES_AND_METADATA folder
Output: full_text_corpus.txt in the main project directory
"""
import os
from pathlib import Path

def create_full_text_corpus():
    """Concatenate all markdown files into full_text_corpus.txt"""
    
    # Define paths
    project_dir = Path(r"c:\Projects\AI Aarohan - Copy")
    input_dir = project_dir / "FINAL_PARSED FILES_AND_METADATA_"
    output_file = project_dir / "full_text_corpus.txt"
    
    # Get all markdown files
    md_files = sorted(input_dir.glob("*.md"))
    
    if not md_files:
        print("ERROR: No markdown files found in FINAL_PARSED_FILES_AND_METADATA!")
        return
    
    print(f"Found {len(md_files)} markdown files:")
    for md_file in md_files:
        print(f"  - {md_file.name}")
    
    # Concatenate all files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, md_file in enumerate(md_files):
            print(f"\nProcessing: {md_file.name}")
            
            # Read the content
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
            
            # Write separator and file info
            if i > 0:
                outfile.write("\n\n" + "="*80 + "\n")
            
            outfile.write(f"SOURCE FILE: {md_file.name}\n")
            outfile.write("="*80 + "\n\n")
            
            # Write the actual content
            outfile.write(content)
            
            print(f"  Added {len(content)} characters")
    
    # Print summary
    file_size = output_file.stat().st_size
    print(f"\n{'='*80}")
    print(f"SUCCESS: Created {output_file.name}")
    print(f"Location: {output_file}")
    print(f"Total size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
    print(f"Files concatenated: {len(md_files)}")
    print(f"{'='*80}")

if __name__ == "__main__":
    create_full_text_corpus()

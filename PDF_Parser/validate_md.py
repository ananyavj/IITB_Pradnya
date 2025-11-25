import os
import re
import json
from pathlib import Path

class MarkdownValidator:
    def __init__(self, output_dir, images_dir, metadata_dir):
        self.output_dir = output_dir
        self.images_dir = images_dir
        self.metadata_dir = metadata_dir
        self.validation_results = []
        
    def validate_all(self):
        """Validate all markdown files in the output directory."""
        print("=" * 80)
        print("MARKDOWN VALIDATION REPORT")
        print("=" * 80)
        
        md_files = [f for f in os.listdir(self.output_dir) if f.endswith('.md')]
        
        if not md_files:
            print("\n❌ No markdown files found in output directory!")
            return
        
        for md_file in md_files:
            self.validate_file(md_file)
        
        self.print_summary()
    
    def validate_file(self, filename):
        """Validate a single markdown file."""
        filepath = os.path.join(self.output_dir, filename)
        base_name = os.path.splitext(filename)[0]
        
        print(f"\n{'='*80}")
        print(f"📄 Validating: {filename}")
        print(f"{'='*80}")
        
        issues = []
        warnings = []
        successes = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Check frontmatter
            frontmatter_result = self.check_frontmatter(content)
            if frontmatter_result['status'] == 'error':
                issues.extend(frontmatter_result['issues'])
            elif frontmatter_result['status'] == 'warning':
                warnings.extend(frontmatter_result['warnings'])
            else:
                successes.append("✅ Frontmatter is valid")
            
            # 2. Check for image references
            image_result = self.check_images(content, base_name)
            issues.extend(image_result['issues'])
            warnings.extend(image_result['warnings'])
            if image_result['found_count'] > 0:
                successes.append(f"✅ Found {image_result['found_count']} image references, all images exist")
            
            # 3. Check metadata file exists
            metadata_result = self.check_metadata(base_name)
            if metadata_result['status'] == 'error':
                issues.append(metadata_result['message'])
            else:
                successes.append(metadata_result['message'])
            
            # 4. Check for common formatting issues
            format_result = self.check_formatting(content)
            warnings.extend(format_result['warnings'])
            if len(format_result['warnings']) == 0:
                successes.append("✅ No formatting issues detected")
            
            # 5. Check content statistics
            stats = self.get_statistics(content)
            successes.append(f"📊 Statistics: {stats['lines']} lines, {stats['words']} words, {stats['headings']} headings")
            
            # Print results
            if successes:
                print("\n✨ Successes:")
                for success in successes:
                    print(f"  {success}")
            
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"  {warning}")
            
            if issues:
                print("\n❌ Issues:")
                for issue in issues:
                    print(f"  {issue}")
            
            # Store validation result
            self.validation_results.append({
                'file': filename,
                'status': 'FAIL' if issues else ('WARNING' if warnings else 'PASS'),
                'issues': len(issues),
                'warnings': len(warnings),
                'stats': stats
            })
            
        except Exception as e:
            print(f"\n❌ Error reading file: {e}")
            self.validation_results.append({
                'file': filename,
                'status': 'ERROR',
                'issues': 1,
                'warnings': 0,
                'stats': {}
            })
    
    def check_frontmatter(self, content):
        """Check if frontmatter is properly formatted."""
        result = {'status': 'success', 'issues': [], 'warnings': []}
        
        # Check for frontmatter
        if not content.startswith('---'):
            result['status'] = 'error'
            result['issues'].append("Missing frontmatter at the beginning of file")
            return result
        
        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            result['status'] = 'error'
            result['issues'].append("Frontmatter is not properly closed with ---")
            return result
        
        frontmatter = parts[1].strip()
        
        # Check required fields
        required_fields = ['title', 'page_count']
        for field in required_fields:
            if f'{field}:' not in frontmatter:
                result['status'] = 'warning'
                result['warnings'].append(f"Missing recommended field in frontmatter: {field}")
        
        return result
    
    def check_images(self, content, base_name):
        """Check if all referenced images exist."""
        result = {'issues': [], 'warnings': [], 'found_count': 0}
        
        # Find all image references
        image_pattern = r'!\[.*?\]\((.*?)\)'
        image_refs = re.findall(image_pattern, content)
        
        for img_path in image_refs:
            result['found_count'] += 1
            # Convert relative path to absolute
            if img_path.startswith('images/'):
                img_filename = img_path.replace('images/', '')
                full_path = os.path.join(self.images_dir, img_filename)
                
                if not os.path.exists(full_path):
                    result['issues'].append(f"Referenced image not found: {img_filename}")
                
                # Check if image belongs to this markdown file
                if not img_filename.startswith(base_name):
                    result['warnings'].append(f"Image may not belong to this file: {img_filename}")
        
        return result
    
    def check_metadata(self, base_name):
        """Check if metadata JSON file exists and is valid."""
        metadata_file = os.path.join(self.metadata_dir, f"{base_name}.json")
        
        if not os.path.exists(metadata_file):
            return {
                'status': 'error',
                'message': f"❌ Metadata file not found: {base_name}.json"
            }
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Check required fields
            required_fields = ['lesson_id', 'subject', 'unit', 'language', 'source', 'filename']
            missing = [f for f in required_fields if f not in metadata]
            
            if missing:
                return {
                    'status': 'error',
                    'message': f"❌ Metadata missing fields: {', '.join(missing)}"
                }
            
            return {
                'status': 'success',
                'message': f"✅ Metadata file exists and is valid"
            }
            
        except json.JSONDecodeError:
            return {
                'status': 'error',
                'message': f"❌ Metadata file is not valid JSON"
            }
    
    def check_formatting(self, content):
        """Check for common formatting issues."""
        result = {'warnings': []}
        
        lines = content.split('\n')
        
        # Check for excessive blank lines
        blank_count = 0
        for i, line in enumerate(lines):
            if line.strip() == '':
                blank_count += 1
                if blank_count > 3:
                    result['warnings'].append(f"More than 3 consecutive blank lines at line {i+1}")
                    blank_count = 0  # Reset to avoid duplicate warnings
            else:
                blank_count = 0
        
        # Check for potential encoding issues
        if any(char in content for char in ['�', '�']):
            result['warnings'].append("Potential encoding issues detected (replacement characters found)")
        
        # Check for unbalanced parentheses in math expressions
        math_pattern = r'\([^)]*\([^)]*\)'
        if re.search(math_pattern, content):
            # This is just a simple heuristic
            open_count = content.count('(')
            close_count = content.count(')')
            if abs(open_count - close_count) > 5:  # Allow some difference
                result['warnings'].append(f"Potentially unbalanced parentheses: {open_count} open, {close_count} close")
        
        return result
    
    def get_statistics(self, content):
        """Get statistics about the content."""
        lines = content.split('\n')
        words = len(content.split())
        
        # Count headings
        headings = len(re.findall(r'^#+\s+', content, re.MULTILINE))
        
        # Count images
        images = len(re.findall(r'!\[.*?\]\(.*?\)', content))
        
        return {
            'lines': len(lines),
            'words': words,
            'headings': headings,
            'images': images
        }
    
    def print_summary(self):
        """Print overall summary."""
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}\n")
        
        total = len(self.validation_results)
        passed = sum(1 for r in self.validation_results if r['status'] == 'PASS')
        warnings = sum(1 for r in self.validation_results if r['status'] == 'WARNING')
        failed = sum(1 for r in self.validation_results if r['status'] in ['FAIL', 'ERROR'])
        
        print(f"Total files validated: {total}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"❌ Failed: {failed}\n")
        
        # Print table
        print(f"{'File':<30} {'Status':<10} {'Issues':<8} {'Warnings':<10} {'Lines':<8} {'Words':<8}")
        print("-" * 80)
        for result in self.validation_results:
            status_symbol = {
                'PASS': '✅',
                'WARNING': '⚠️ ',
                'FAIL': '❌',
                'ERROR': '❌'
            }.get(result['status'], '?')
            
            lines = result['stats'].get('lines', 0)
            words = result['stats'].get('words', 0)
            
            print(f"{result['file']:<30} {status_symbol} {result['status']:<8} {result['issues']:<8} {result['warnings']:<10} {lines:<8} {words:<8}")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    # Configuration
    OUTPUT_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\output"
    IMAGES_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\images"
    METADATA_DIR = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\metadata"
    REPORT_FILE = r"c:\Projects\AI Aarohan - Copy\PDF_Parser\validation_report.txt"
    
    # Redirect stdout to both console and file
    import sys
    from io import StringIO
    
    # Create a custom writer that writes to both stdout and file
    class TeeWriter:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()
    
    # Open report file
    with open(REPORT_FILE, 'w', encoding='utf-8') as report_file:
        original_stdout = sys.stdout
        sys.stdout = TeeWriter(original_stdout, report_file)
        
        try:
            # Run validation
            validator = MarkdownValidator(OUTPUT_DIR, IMAGES_DIR, METADATA_DIR)
            validator.validate_all()
            
            print("\n✨ Validation complete!")
            print(f"📄 Report saved to: {REPORT_FILE}")
        finally:
            sys.stdout = original_stdout

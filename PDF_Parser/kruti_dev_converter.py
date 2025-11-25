# Kruti Dev to Unicode Devanagari converter
# Maps Kruti Dev encoded ASCII characters to proper Unicode Devanagari

# Two/three character sequences (check these FIRST before single chars)
KRUTI_MULTI_CHAR = {
    # Three character
    'vks': 'ओ', 'vkS': 'औ', '.k': 'ण',
    'dks': 'को', 'dkks': 'को', 'dh': 'की',
    'कह': 'कह', 'gS': 'है', 'gSa': 'हैं',
    
    # Two character matras and combinations
    'ks': 'ो', 'kS': 'ौ', 'ksa': 'ों',
    'èkh': 'धी', 'îk': 'ध्या',
    '];': 'र्य', '¯': 'र्', '«': 'क्ष', '=': 'त्र',
    'K': 'ज्ञ', 'Ù': 'क्', 'ê': 'त्त',
    'vk': 'आ', 'bZ': 'ई', 'mQ': 'ऊ',
    'è;': 'ध्य', 'fn': 'दि', 'nh': 'दी',
    'rh': 'ती', 'jk': 'रा', 'js': 'रे',
    ';k': 'या', ';s': 'ये', 'kZ': 'र्ण',
    'gk': 'हा', 'gh': 'ही', 'gq': 'हु',
    'lh': 'सी', 'ls': 'से', 'lk': 'सा',
    'us': 'ने', 'uk': 'ना', 'uh': 'नी',
    'ds': 'के', 'dk': 'का', 'dh': 'की',
    'rk': 'ता', 'rh': 'ती', 'rs': 'ते',
    'esa': 'में', 'esa': 'मैं',
    'th': 'जी', 'tk': 'जा', 'ts': 'जे',
    'Qy': 'फल', 'ky': 'काल',
    'eku': 'मान', 'djsa': 'करें',
}

# Single character mappings
KRUTI_TO_UNICODE = {
    # Vowels
    'v': 'अ', 'V': 'आ', 'b': 'इ', 'B': 'ई', 'u': 'उ', 'U': 'ऊ',
    '^': 'ए', 'S': 'ऐ', ']': 'ऋ',
    
    # Consonants
    'd': 'क', 'D': 'ख', 'x': 'ग', 'X': 'घ', '³': 'ङ',
    'p': 'च', 'P': 'छ', 't': 'ज', 'T': 'झ', '¥': 'ञ',
    'V': 'ट', 'B': 'ठ', 'M': 'ड', '<': 'ढ', 
    'r': 'त', 'R': 'थ', 'n': 'द', 'N': 'ध', 'u': 'न',
    'i': 'प', 'I': 'फ', 'Q': 'फ', 'c': 'ब', 'C': 'भ', 'e': 'म',
    ';': 'य', 'j': 'र', 'y': 'ल', 'Y': 'ळ', 'o': 'व',
    "'": 'श', '"': 'ष', 'l': 'स', 'g': 'ह',
    
    # Matras (vowel signs)
    'k': 'ा', 'h': 'ि', 'H': 'ी', 'q': 'ु', 'Q': 'ू',
    '^': 'े', 's': 'े', 'S': 'ै',
    
    # Special characters
    '~': 'ं', '¡': 'ँ', '%': 'ः', '&': '्', '*': '्र',
    '+': 'ृ', 'Z': 'ञ', 'è': 'ध', 'W': 'ध',
    'A': '।', ',': ',',
    
    # Keep English chars and numbers as-is (handled separately)
}

# Extended mapping for common Kruti Dev word patterns
EXTENDED_PATTERNS = {
    # Common complete words
    'vè;k;': 'अध्याय',
    'okLrfod': 'वास्तविक',
    'la[;k': 'संख्या',
    'la[;k,¡': 'संख्याएँ',
    'la[;kvksa': 'संख्याओं',
    ';wfDyMh;': 'यूक्लिडीय',
    'foHkktu': 'विभाजन',
    'izesf;dk': 'प्रमेयिका',
    'iw.kk±d': 'पूर्णांक',
    'iw.kk±dksa': 'पूर्णांकों',
    'iw.kkZad': 'पूर्णांक',
    '/ukRed': 'धनात्मक',
    'vfLrRo': 'अस्तित्व',
    'vf}rh;': 'अद्वितीय',
    'izkIr': 'प्राप्त',
    'djus': 'करने',
    'djrs': 'करते',
    'djrk': 'करता',
    'djsa': 'करें',
    'fy,': 'लिए',
    'yhft,': 'लीजिए',
    'vkSj': 'और',
    'gS': 'है',
    'gSa': 'हैं',
    'gSaA': 'हैं।',
    'gks': 'हो',
    'ls': 'से',
    'ij': 'पर',
    'tks': 'जो',
    'dk': 'का',
    'dks': 'को',
    'dh': 'की',
    'osQ': 'के',
    'esa': 'में',
    'eq[;': 'मुख्य',
    'vo/kj.kk': 'अवधारणा',
    'vo/kj.kk,¡': 'अवधारणाएँ',
    'ifj.kke': 'परिणाम',
    ',sls': 'ऐसे',
    ',YxksfjFe': 'एल्गोरिथ्म',
    'pj.k': 'चरण',
    'iw.kZ': 'पूर्ण',
    'nks': 'दो',
    'fn,': 'दिए',
    'jgus': 'रहने',
    'larq\"V': 'संतुष्ट',
    'fd': 'कि',
    'eku': 'मान',
    'D;k': 'क्या',
    'D;ksaकि': 'क्योंकि',
    'dgrh': 'कहती',
    'vuqiz;ksx': 'अनुप्रयोग',
    'vHkkT;': 'अभाज्य',
    'vHkkT;ksa': 'अभाज्यों',
    'xq.kuiQy': 'गुणनफल',
    ':i': 'रूप',
    'O;Dr': 'व्यक्त',
    'kFkk': 'तथा',
    'vkus': 'आने',
    'Øeksa': 'क्रमों',
    'è;ku': 'ध्यान',
    'nsrs': 'देते',
    'gq,': 'हुए',
    'foHkkftr': 'विभाजित',
    'tgk¡': 'जहाँ',
    'vifjes;': 'अपरिमेय',
    'ifjes;': 'परिमेय',
    ';ksx': 'योग',
    'varj': 'अंतर',
    'HkkxiQy': 'भागफल',
    '\'kwU;srj': 'शून्येतर',
    'izdkj': 'प्रकार',
    'n\'keyo': 'दशमलव',
    'izlkj': 'प्रसार',
    'lkar': 'सांत',
    'vlkar': 'असांत',
    'vkorhZ': 'आवर्ती',
    'cgq': 'बहु',
    'fodYi': 'विकल्प',
    'fodYih;': 'विकल्पीय',
    'iz\'u': 'प्रश्न',
    'mÙkj': 'उत्तर',
    'lgh': 'सही',
    'pqfu,': 'चुनिए',
    'fuEufyf[kr': 'निम्नलिखित',
    'lekIr': 'समाप्त',
    'LFkku': 'स्थान',
    'gy': 'हल',
    'iz\'ukoyh': 'प्रश्नावली',
    'किlh': 'किसी',
    'oxZ': 'वर्ग',
    '?ku': 'घन',
    'le': 'सम',
    'fo\"ke': 'विषम',
    'lcls': 'सबसे',
    'cM+h': 'बड़ी',
    'Øe\'k%': 'क्रमशः',
    '\'ks\"kiQy': 'शेषफल',
    'izdज़': 'प्रकार',
    'ugha': 'नहीं',
    'vkSfpR;': 'औचित्य',
    'nhft,': 'दीजिए',
    'काj.k': 'कारण',
    'rdZ': 'तर्क',
    'lkFk': 'साथ',
    'laf{kIr': 'संक्षिप्त',
    'tc': 'जब',
    'Hkkx': 'भाग',
    'देus': 'देने',
    'केoy': 'केवल',
    'gks': 'हो',
    'ldrs': 'सकते',
    'ldrs': 'सकती',
    'vuqlkj': 'अनुसार',
    'vr%': 'अतः',
    'vad': 'अंक',
    'xq.ku[kaMu': 'गुणनखंडन',
    'bl': 'इस',
    'blfy,': 'इसलिए',
    'blके': 'इसके',
    'fdlh': 'किसी',
    'okyh': 'वाली',
    'laकेr': 'संकेत',
    'tkurs': 'जानते',
    'dYiuk': 'कल्पना',
    'djsa': 'करें',
    'i{k': 'पक्ष',
    'nk;k¡': 'दायां',
    'tcकि': 'जबकि',
    'fojks/kHkkl': 'विरोधाभास',
    'varfoZjks/': 'अंतर्विरोध',
    'n\'kkZb,': 'दर्शाइए',
    'fl¼': 'सिद्ध',
    'कीft,': 'कीजिए',
    'izR;sd': 'प्रत्येक',
    'kaS': 'कौन',
    ';qXe': 'युग्म',
    'lgvHkkT;': 'सहअभाज्य',
    'vkb,': 'आइए',
    'Kkr': 'ज्ञात',
    'परarq': 'परंतु',
    'iz;ksx': 'प्रयोग',
    'djus': 'करने',
    ',slh': 'ऐसी',
    'nwjh': 'दूरी',
    'पूर्ण': 'पूर्ण',
    'r;': 'तय',
    'djs': 'करे',
    'gj': 'हर',
    'fcuk': 'बिना',
    'yach': 'लंबी',
    'izfØ;k': 'प्रक्रिया',
    'कि,': 'किए',
    'dg': 'कह',
    'ldrs': 'सकते',
    'किUgha': 'किन्हीं',
    'nh?kZ': 'दीर्घ',
    'izfrn\'kZ': 'प्रतिदर्श',
    'pkj': 'चार',
    'vius': 'अपने',
    'काsbZ': 'कोई',
    'vFkkZr': 'अर्थात',
    'izdkj': 'प्रकार',
    'gesa': 'हमें',
    'izfØ;k': 'प्रक्रिया',
    'Hkktd': 'भाजक',
    'ok¡fNr': 'वांछित',
    'Lrj': 'स्तर',
    'O;fDr': 'व्यक्ति',
    'lkFk': 'साथ',
    'LFkku': 'स्थान',
    'pyuk': 'चलना',
    'izkjaHk': 'प्रारंभ',
    'dneksa': 'कदमों',
    'eki': 'माप',
    'buesa': 'इनमें',
    'U;wure': 'न्यूनतम',
    'pys': 'चले',
    'vadxf.kr': 'अंकगणित',
    'vk/kjHkwr': 'आधारभूत',
    'izes;': 'प्रमेय',
    'HkkT;': 'भाज्य',
    'Øekxr': 'क्रमागत',
    'dFku': 'कथन',
    'lR;': 'सत्य',
    'vlR;': 'असत्य',
    'fyf[k,': 'लिखिए',
    'izko`Qr': 'प्राकृत',
    'fHkUu': 'भिन्न',
    'Li\"V': 'स्पष्ट',
    'rkfd': 'ताकि',
    'परurq': 'परंतु',
    'vFkkZr~': 'अर्थात्',
    'izkr%dkyhu': 'प्रातःकालीन',
    'lSj': 'सैर',
    'le;': 'समय',
    'rhu': 'तीन',
    'vkorhZ': 'आवर्ती',
    'izdkj': 'प्रकार',
    'gksxh': 'होगी',
    'gksxk': 'होगा',
}

def convert_kruti_to_unicode(text):
    """
    Convert Kruti Dev encoded text to Unicode Devanagari.
    Returns original text if it doesn't appear to be Kruti Dev encoded.
    """
    # Quick check: if text already has Devanagari Unicode, return as-is
    if any('\u0900' <= char <= '\u097F' for char in text):
        return text
    
    # Check if text looks like Kruti Dev
    kruti_indicators = ['v', 'k', 'è', 'osQ', 'dk', 'gS', 'ls', 'dh', 'iz']
    if not any(indicator in text for indicator in kruti_indicators):
        return text
    
    # Split into words and convert only Kruti Dev words
    import re
    words = re.split(r'(\s+|[,.\(\);\[\]!?"])', text)
    result_words = []
    
    for word in words:
        if not word or word.isspace() or word in ',.(;)[]!?"':
            result_words.append(word)
            continue
            
        # Check if word looks like Kruti Dev (has Kruti patterns)
        is_kruti = any(indicator in word for indicator in ['v', 'k', 'è', 'dh', 'dk', 'ls', 'gS', 'iz', 'fd', 'tks'])
        
        # Also check if it's mostly English (has common English patterns)
        is_english = bool(re.match(r'^[A-Z][a-z]+$', word)) or word.isupper() or word in ['the', 'and', 'or', 'to', 'a', 'is', 'of', 'in', 'for', 'with']
        
        if is_kruti and not is_english:
            # Convert this word
            converted = []
            i = 0
            while i < len(word):
                matched = False
                
                # Try longer sequences first
                for length in [4, 3, 2]:
                    if i + length <= len(word):
                        substr = word[i:i+length]
                        if substr in KRUTI_MULTI_CHAR:
                            converted.append(KRUTI_MULTI_CHAR[substr])
                            i += length
                            matched = True
                            break
                
                if matched:
                    continue
                    
                # Single character conversion
                char = word[i]
                if char in KRUTI_TO_UNICODE:
                    converted.append(KRUTI_TO_UNICODE[char])
                else:
                    converted.append(char)
                i += 1
            
            result_words.append(''.join(converted))
        else:
            result_words.append(word)
    
    return ''.join(result_words)

def convert_with_patterns(text):
    """Enhanced conversion using common pattern matching."""
    
    # Protect image paths, URLs, and markdown links from conversion
    import re
    protected_patterns = []
    placeholder_map = {}
    
    # Find and protect markdown image syntax
    image_pattern = r'!\[Image:[^\]]+\]\([^\)]+\)'
    for match in re.finditer(image_pattern, text):
        placeholder = f"___IMAGE_PLACEHOLDER_{len(protected_patterns)}___"
        protected_patterns.append(match.group(0))
        placeholder_map[placeholder] = match.group(0)
    
    # Replace protected content with placeholders
    for i, pattern in enumerate(protected_patterns):
        placeholder = f"___IMAGE_PLACEHOLDER_{i}___"
        text = text.replace(pattern, placeholder)
    
    # First try direct pattern matching for complete words (longest first)
    patterns_sorted = sorted(EXTENDED_PATTERNS.items(), key=lambda x: len(x[0]), reverse=True)
    for kruti, unicode_text in patterns_sorted:
       # Only replace if surrounded by word boundaries
        text = re.sub(r'\b' + re.escape(kruti) + r'\b', unicode_text, text)
    
    # Then apply character-by-character conversion for remaining text
    text = convert_kruti_to_unicode(text)
    
    # Restore protected content
    for placeholder, original in placeholder_map.items():
        text = text.replace(placeholder, original)
    
    return text

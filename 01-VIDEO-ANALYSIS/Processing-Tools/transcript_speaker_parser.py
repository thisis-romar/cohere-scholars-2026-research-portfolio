import re

def parse_existing_transcript_with_speakers():
    """Parse the existing transcript file and add speaker identification"""
    
    # Read the existing transcript
    try:
        with open('transcript_ytdlp.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: transcript_ytdlp.txt not found!")
        return None
    
    # Extract the transcript portion (after the headers)
    transcript_start = content.find("TRANSCRIPT:")
    if transcript_start == -1:
        print("Error: Could not find transcript section!")
        return None
    
    transcript_text = content[transcript_start + len("TRANSCRIPT:"):]
    transcript_text = transcript_text.replace("="*30, "").strip()
    
    # Define speakers based on analysis
    speakers = [
        "**Sarah Hooker** (Host/Research Lead)",
        "**Marzia** (Research Team Member)", 
        "**Ahmed** (Research Team Member)",
        "**John** (Former Scholar, Research Engineer)"
    ]
    
    # Parse speaker segments
    segments = parse_speaker_segments(transcript_text, speakers)
    
    # Create markdown output
    markdown_content = create_markdown_transcript(segments)
    
    # Save the markdown file
    with open('transcript_speakers.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("✅ Speaker-identified transcript saved to: transcript_speakers.md")
    return markdown_content

def parse_speaker_segments(transcript_text, speakers):
    """Parse transcript into speaker segments"""
    
    segments = []
    
    # Find the start of each speaker based on content markers
    # Sarah's introduction
    sarah_intro = extract_text_until_marker(transcript_text, 0, ">> Uh yeah I think")
    if sarah_intro:
        timestamp = extract_first_timestamp(sarah_intro)
        segments.append({
            'speaker': speakers[0],
            'timestamp': timestamp,
            'text': clean_transcript_text(sarah_intro)
        })
    
    # Split by >> markers for other speakers
    speaker_parts = transcript_text.split('>> ')
    
    speaker_index = 1  # Start with Marzia (second speaker)
    
    for part in speaker_parts[1:]:  # Skip first empty part
        if part.strip():
            # Find where this speaker's text ends (next >> or end of text)
            speaker_text = part
            
            # Extract timestamp
            timestamp = extract_first_timestamp(speaker_text)
            
            # Clean the text
            clean_text = clean_transcript_text(speaker_text)
            
            if clean_text and len(clean_text.split()) > 5:  # Only include substantial segments
                segments.append({
                    'speaker': speakers[speaker_index % len(speakers)],
                    'timestamp': timestamp,
                    'text': clean_text
                })
                speaker_index += 1
    
    return segments

def extract_text_until_marker(text, start_pos, end_marker):
    """Extract text from start position until end marker"""
    end_pos = text.find(end_marker, start_pos)
    if end_pos == -1:
        return text[start_pos:].strip()
    return text[start_pos:end_pos].strip()

def extract_first_timestamp(text):
    """Extract the first timestamp from text"""
    timestamp_match = re.search(r'<(\d{2}:\d{2}:\d{2}\.\d{3})>', text)
    return timestamp_match.group(1) if timestamp_match else "00:00:00.000"

def clean_transcript_text(text):
    """Clean transcript text by removing timestamps and repetitions"""
    
    # Remove timestamp markers
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    
    # Remove speaker markers
    text = text.replace('>> ', '').strip()
    
    # Remove common auto-caption artifacts
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    # Split by periods and clean up repetitions
    parts = text.split('.')
    clean_parts = []
    
    for part in parts:
        part = part.strip()
        if len(part) < 5:  # Skip very short fragments
            continue
            
        # Remove repetitive patterns (common in auto captions where same phrase repeats 3 times)
        words = part.split()
        if len(words) > 6:
            # Check for pattern where same phrase repeats multiple times
            # Look for sequences that repeat within the same sentence
            cleaned_words = remove_internal_repetitions(words)
            part = ' '.join(cleaned_words)
        
        # Only add if it's not too similar to the last part
        if clean_parts:
            last_part = clean_parts[-1]
            similarity = calculate_similarity(part, last_part)
            if similarity < 0.7:  # Only add if less than 70% similar
                clean_parts.append(part)
        else:
            clean_parts.append(part)
    
    # Join and final cleanup
    result = '. '.join(clean_parts)
    
    # Remove common auto-caption artifacts
    result = result.replace('Kind: captions Language: en', '')
    result = re.sub(r'\s+', ' ', result).strip()
    
    if result and not result.endswith('.'):
        result += '.'
    
    return result

def remove_internal_repetitions(words):
    """Remove internal repetitions within a word sequence"""
    if len(words) < 6:
        return words
    
    # Look for patterns where sequences repeat (common in auto-captions)
    clean_words = []
    i = 0
    
    while i < len(words):
        # Look ahead to see if we have a repeating pattern
        found_repetition = False
        
        # Check for repetitions of 3-8 word sequences
        for seq_len in range(3, min(8, len(words) - i)):
            if i + seq_len * 2 <= len(words):
                seq1 = words[i:i + seq_len]
                seq2 = words[i + seq_len:i + seq_len * 2]
                
                # If sequences are identical, skip the repetition
                if seq1 == seq2:
                    clean_words.extend(seq1)
                    i += seq_len * 2  # Skip both sequences
                    found_repetition = True
                    break
        
        if not found_repetition:
            clean_words.append(words[i])
            i += 1
    
    return clean_words

def calculate_similarity(text1, text2):
    """Calculate similarity between two text strings"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def create_markdown_transcript(segments):
    """Create markdown formatted transcript"""
    
    markdown_lines = []
    
    # Header
    markdown_lines.append("# 🎥 Cohere Labs Research Scholar Program - Speaker Transcript\n")
    markdown_lines.append("**📺 Video**: What it takes to be a Cohere Labs Research Scholar")
    markdown_lines.append("**🔗 URL**: https://www.youtube.com/watch?v=EqbutUc5a_Q")
    markdown_lines.append("**⏱️ Duration**: 10:06")
    markdown_lines.append("**🏢 Channel**: Cohere")
    markdown_lines.append("\n---\n")
    
    # Table of Contents
    markdown_lines.append("## 📋 Speakers")
    markdown_lines.append("1. **Sarah Hooker** - Host/Research Lead at Cohere")
    markdown_lines.append("2. **Marzia** - Research Team Member")
    markdown_lines.append("3. **Ahmed** - Research Team Member") 
    markdown_lines.append("4. **John** - Former Scholar, Research Engineer")
    markdown_lines.append("\n---\n")
    
    # Transcript sections
    for i, segment in enumerate(segments, 1):
        # Convert timestamp for readability
        timestamp = segment['timestamp']
        time_parts = timestamp.split(':')
        if len(time_parts) == 3:
            hours, minutes, seconds = time_parts
            if hours == '00':
                display_time = f"{minutes}:{seconds.split('.')[0]}"
            else:
                display_time = timestamp
        else:
            display_time = timestamp
        
        markdown_lines.append(f"## {segment['speaker']}")
        markdown_lines.append(f"**⏰ {display_time}**\n")
        
        # Format text with proper paragraphs
        text = segment['text']
        if len(text) > 300:
            # Break long text into paragraphs
            paragraphs = break_into_paragraphs(text)
            for para in paragraphs:
                markdown_lines.append(para + "\n")
        else:
            markdown_lines.append(text + "\n")
        
        markdown_lines.append("---\n")
    
    return '\n'.join(markdown_lines)

def break_into_paragraphs(text, max_length=250):
    """Break long text into readable paragraphs"""
    sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
    paragraphs = []
    current_para = ""
    
    for sentence in sentences:
        if len(current_para + ' ' + sentence) > max_length and current_para:
            paragraphs.append(current_para.strip())
            current_para = sentence
        else:
            current_para += ' ' + sentence if current_para else sentence
    
    if current_para.strip():
        paragraphs.append(current_para.strip())
    
    return paragraphs

if __name__ == "__main__":
    result = parse_existing_transcript_with_speakers()
    if result:
        print("\n🎉 Successfully created speaker-identified transcript!")
        print("📄 File saved as: transcript_speakers.md")
        
        # Show a preview
        print("\n📖 Preview (first 500 characters):")
        print("=" * 50)
        print(result[:500] + "..." if len(result) > 500 else result)
    else:
        print("❌ Failed to process transcript")

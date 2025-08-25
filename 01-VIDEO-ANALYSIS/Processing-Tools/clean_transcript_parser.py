import re

def create_clean_speaker_transcript():
    """Create a properly cleaned speaker transcript from the raw transcript"""
    
    # Read the raw transcript
    try:
        with open('transcript_ytdlp.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: transcript_ytdlp.txt not found!")
        return None
    
    # Extract the transcript portion
    transcript_start = content.find("TRANSCRIPT:")
    if transcript_start == -1:
        print("Error: Could not find transcript section!")
        return None
    
    raw_transcript = content[transcript_start + len("TRANSCRIPT:"):]
    raw_transcript = raw_transcript.replace("="*30, "").strip()
    
    # Parse into clean speaker segments
    segments = parse_and_clean_segments(raw_transcript)
    
    # Create markdown
    markdown = create_final_markdown(segments)
    
    # Save
    with open('transcript_clean_speakers.md', 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print("✅ Clean speaker transcript saved to: transcript_clean_speakers.md")
    return markdown

def parse_and_clean_segments(raw_text):
    """Parse raw transcript into clean speaker segments"""
    
    # Define speakers
    speakers = {
        'sarah': "**Sarah Hooker** (Host/Research Lead)",
        'marzia': "**Marzia** (Research Team Member)", 
        'ahmed': "**Ahmed** (Research Team Member)",
        'john': "**John** (Former Scholar, Research Engineer)"
    }
    
    segments = []
    
    # Manually parse based on content analysis
    # Sarah's opening (from start until first >>)
    sarah_end = raw_text.find('>> Uh yeah I think')
    if sarah_end > 0:
        sarah_text = raw_text[:sarah_end]
        sarah_clean = extract_clean_speech(sarah_text, start_time="00:00:06.000")
        if sarah_clean:
            segments.append({
                'speaker': speakers['sarah'],
                'timestamp': '00:06',
                'text': sarah_clean
            })
    
    # Find Marzia's segment (first >> until Ahmed is mentioned)
    marzia_start = raw_text.find('>> Uh yeah I think')
    ahmed_start = raw_text.find('>> Um, for AI research')
    if marzia_start > 0 and ahmed_start > marzia_start:
        marzia_text = raw_text[marzia_start:ahmed_start]
        marzia_clean = extract_clean_speech(marzia_text)
        if marzia_clean:
            segments.append({
                'speaker': speakers['marzia'],
                'timestamp': '00:46',
                'text': marzia_clean
            })
    
    # Find Ahmed's segment
    ahmed_start = raw_text.find('>> Um, for AI research')
    john_start = raw_text.find('>> yeah I think there there are a couple')
    if ahmed_start > 0:
        if john_start > ahmed_start:
            ahmed_text = raw_text[ahmed_start:john_start]
        else:
            # Find another marker for Ahmed's end
            ahmed_end = raw_text.find('>> yeah and this is a good time')
            ahmed_text = raw_text[ahmed_start:ahmed_end] if ahmed_end > ahmed_start else raw_text[ahmed_start:ahmed_start+1000]
        
        ahmed_clean = extract_clean_speech(ahmed_text)
        if ahmed_clean:
            segments.append({
                'speaker': speakers['ahmed'],
                'timestamp': '01:48',
                'text': ahmed_clean
            })
    
    # Find John's segment
    john_start = raw_text.find('>> yeah I think there there are a couple')
    if john_start > 0:
        john_text = raw_text[john_start:john_start+2000]  # Take reasonable chunk
        john_clean = extract_clean_speech(john_text)
        if john_clean:
            segments.append({
                'speaker': speakers['john'],
                'timestamp': '02:47',
                'text': john_clean
            })
    
    # Additional segments can be added by finding more >> markers
    # For now, let's manually add the key insights from each speaker
    
    return segments

def extract_clean_speech(text_segment, start_time=None):
    """Extract clean speech from a text segment"""
    
    # Remove >> markers
    text = text_segment.replace('>> ', '').strip()
    
    # Remove timestamp markers
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    
    # Clean up common artifacts
    text = text.replace('Kind: captions Language: en', '')
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Process each sentence to remove repetitions
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 5:  # Skip very short fragments
            continue
        
        # Remove common repetition patterns
        words = sentence.split()
        clean_words = []
        
        i = 0
        while i < len(words):
            # Look for immediate repetitions (word word word)
            if i + 2 < len(words) and words[i] == words[i+1] == words[i+2]:
                clean_words.append(words[i])
                i += 3  # Skip the repetitions
            elif i + 1 < len(words) and words[i] == words[i+1]:
                clean_words.append(words[i])
                i += 2  # Skip one repetition
            else:
                clean_words.append(words[i])
                i += 1
        
        clean_sentence = ' '.join(clean_words)
        
        # Only add if it's not too similar to existing sentences
        is_duplicate = False
        for existing in clean_sentences:
            if calculate_similarity(clean_sentence.lower(), existing.lower()) > 0.8:
                is_duplicate = True
                break
        
        if not is_duplicate and len(clean_sentence.split()) > 3:
            clean_sentences.append(clean_sentence)
    
    # Join sentences
    result = '. '.join(clean_sentences)
    if result and not result.endswith('.'):
        result += '.'
    
    return result.strip()

def calculate_similarity(text1, text2):
    """Calculate word overlap similarity between two texts"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0

def create_final_markdown(segments):
    """Create the final markdown transcript"""
    
    markdown_lines = []
    
    # Header
    markdown_lines.append("# 🎥 Cohere Labs Research Scholar Program")
    markdown_lines.append("## Speaker-Identified Transcript\n")
    
    markdown_lines.append("**📺 Video**: What it takes to be a Cohere Labs Research Scholar")
    markdown_lines.append("**🔗 URL**: https://www.youtube.com/watch?v=EqbutUc5a_Q")
    markdown_lines.append("**⏱️ Duration**: 10:06")
    markdown_lines.append("**🏢 Channel**: Cohere\n")
    
    markdown_lines.append("---\n")
    
    # Speakers overview
    markdown_lines.append("## 👥 Speakers")
    markdown_lines.append("- **Sarah Hooker** - Research Lead at Cohere")
    markdown_lines.append("- **Marzia** - Research Team Member")
    markdown_lines.append("- **Ahmed** - Research Team Member") 
    markdown_lines.append("- **John** - Former Scholar, now Research Engineer\n")
    
    markdown_lines.append("---\n")
    
    # Add segments
    for segment in segments:
        markdown_lines.append(f"## {segment['speaker']}")
        markdown_lines.append(f"**⏰ {segment['timestamp']}**\n")
        
        # Format text nicely
        text = segment['text']
        if len(text) > 300:
            # Break into paragraphs
            paragraphs = break_into_paragraphs(text)
            for para in paragraphs:
                markdown_lines.append(para + "\n")
        else:
            markdown_lines.append(text + "\n")
        
        markdown_lines.append("---\n")
    
    # Add manual content for key insights (since auto-captions are messy)
    markdown_lines.append("## 🎯 Key Insights Summary\n")
    
    markdown_lines.append("### What Makes a Good Research Scholar")
    markdown_lines.append("- **Curiosity and passion** for learning")
    markdown_lines.append("- **Openness** to exploration and new ideas") 
    markdown_lines.append("- **Little research background required** - they want to help you get started")
    markdown_lines.append("- **Collaborative mindset** for working with mentors\n")
    
    markdown_lines.append("### Traits of Successful Researchers")
    markdown_lines.append("- **Asking the right questions** that challenge status quo")
    markdown_lines.append("- **Collaboration skills** across diverse teams") 
    markdown_lines.append("- **Perseverance** and learning from failures")
    markdown_lines.append("- **Building craft** through repetition and practice\n")
    
    markdown_lines.append("### Why Publishing Matters")
    markdown_lines.append("- **Open science** accelerates AI progress")
    markdown_lines.append("- **Entry points** for new researchers")
    markdown_lines.append("- **Two-way benefit** - more publishing leads to better research\n")
    
    return '\n'.join(markdown_lines)

def break_into_paragraphs(text, max_length=200):
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
    result = create_clean_speaker_transcript()
    if result:
        print("\n🎉 Successfully created clean speaker transcript!")
        print("📄 File saved as: transcript_clean_speakers.md")
        
        # Show preview
        print("\n📖 Preview:")
        print("=" * 50)
        lines = result.split('\n')
        for line in lines[:20]:  # Show first 20 lines
            print(line)
        if len(lines) > 20:
            print("...")
    else:
        print("❌ Failed to create transcript")

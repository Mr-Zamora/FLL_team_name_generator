# Gemini API Prompt Engineering Guide

# Richard Johnson Anglican College - Team Name Generator

## School Identity
- **Name**: Richard Johnson Anglican College (RJ)
- **Location**: Oakhurst, NSW, Australia
- **Established**: 1997
- **Mascot/Symbol**: Tree (representing growth and Christian foundation)
- **Motto**: "A place to belong, serve and succeed"
- **Namesake**: Reverend Richard Johnson, first Anglican minister in Australia

### Core Values & Educational Framework
- **Building Learning Power**: Focus on developing five key learning muscles
- **Christian Foundation**: Rooted in Anglican traditions and biblical teachings
- **Holistic Education**: Nurturing academic, spiritual, and personal growth
- **Community Focus**: Strong emphasis on relationships and service

### Five Learning Muscles
1. **Relationship**: Building positive connections and teamwork
2. **Resilience**: Developing perseverance and adaptability
3. **Resourcefulness**: Encouraging creativity and problem-solving
4. **Reflectiveness**: Promoting self-awareness and learning from experience
5. **Reciprocity**: Fostering mutual support and collaboration

## 2025-2026 Season Theme: UNEARTHED

### Season Theme Overview
- **Theme**: UNEARTHED - An archaeological adventure
- **Focus**: Discovering innovations from the past to build a better future
- **Key Concepts**:
  * Archaeology and discovery
  * Historical innovations
  * Preserving knowledge
  * Connecting past and future
  * Tools and technology of discovery

## Team Name Brainstorming Guidelines

### Name Inspiration Categories
- **RJ Identity**:
  * "Angels" (from Anglican)
  * "RJ" based names (e.g., "RJ Innovators", "RJ Explorers")
  * References to the College's tree symbol (e.g., "Mighty Oaks", "Rooted Innovators")
  * Christian heritage themes (e.g., "Faith Builders", "Grace Engineers")
  * Learning Muscles (e.g., "Resilient Builders", "Resourceful Discoverers")
  * School values (e.g., "Belong Builders", "Serve & Succeed")
- **Theme-based**: Related to archaeology, discovery, or historical innovations
- **Location-based**: Richard Johnson Anglican College, Oakhurst, or local landmarks
- **Thematic**: Related to the UNEARTHED theme and RJ values
- **Creative**: Fun combinations (e.g., "DinoBots", "Time Travelers", "Artifact Assemblers")
- **Technical**: References to robotics, coding, or engineering with a discovery twist
- **Team Identity**: Adjectives representing exploration and innovation
- **Wordplay**: Clever combinations or puns (e.g., "DigiTrowels", "Brick Archaeologists")

### Naming Conventions
- Keep it short (1-4 words)
- Make it memorable and easy to pronounce
- Ensure it's appropriate for all ages
- Consider how it might look on team shirts or posters
- Check for any unintended meanings or acronyms

## Core Prompts

### Team Name Generation Prompt
```
Generate a creative, child-friendly team name for a FIRST LEGO League robotics team participating in the 2025-2026 UNEARTHED season. 
The name should be:
- Short (1-4 words)
- Memorable and unique
- Relate to one or more of these themes:
  * Archaeology and discovery
  * Historical innovations and technology
  * Tools of exploration and research
  * Connecting past and future
  * Problem-solving and engineering
  * Teamwork and collaboration
  * LEGO building and creativity
- Be appropriate for students aged 9-16
- Be original and inspiring
- Avoid any potentially controversial references
- Bonus points for creative archaeological or historical references

### Creative Team Name Examples

**RJ & UNEARTHED Themed Names**
- "RJ Time Explorers" (ties to discovery and RJ identity)
- "Rooted Discoverers" (ties to tree symbol and discovery)
- "Faithful Time Travelers" (ties to Christian values and UNEARTHED)
- "RJ Relic Rovers" (ties to archaeology and RJ identity)

**Learning Power Inspired**
- "Resilient Relic Finders" (ties to Resilience muscle)
- "Resourceful Archaeologists" (ties to Resourcefulness)
- "Reflective Time Keepers" (ties to Reflectiveness)
- "Reciprocal Explorers" (ties to Reciprocity)
- "Relationship Rovers" (ties to Relationship)

**Creative & Fun Names**
- "BrickByBrick Builders" (ties to LEGO and progress)
- "The Time Tinkerers" (creative problem-solving)
- "Ancient Innovators" (ties to historical discovery)
- "Future Finders" (ties to UNEARTHED theme)
- "The DigiTrowels" (tech + archaeology pun)

**RJ Motto Inspired**
- "Belonging Builders" (from "place to belong")
- "Serve & Discover" (from "serve and succeed")
- "Success Seekers" (from school motto)
- "RJ Community Crew" (ties to community focus)

**Christian Values**
- "Faithful Finders"
- "Graceful Gravers" (grace + archaeological term)
- "Hope's Historians"
- "Peaceful Pioneers"

Return only the team name with no additional text.
```

### Description Generation Prompt
```
For the FIRST LEGO League team name "[TEAM_NAME]" (from Richard Johnson Anglican College, participating in the 2025-2026 UNEARTHED season), create a short, engaging description (maximum 15 words) that:
- Explains the team name's meaning or inspiration in a fun, creative way
- Uses positive, encouraging language that celebrates discovery and innovation
- Connects to the UNEARTHED theme of archaeology and historical discovery
- If possible, references RJ's values:
  * Christian faith and Anglican traditions
  * Building Learning Power (5 learning muscles)
  * School motto: "A place to belong, serve and succeed"
  * Community and relationships
- Is appropriate for children aged 9-16
- Captures the spirit of FLL: friendly competition, learning, and "Gracious Professionalism"
- If relevant, connects to LEGO building, robotics, or archaeological discovery

Example descriptions:
- "Building the future, one brick at a time!"
- "Where creativity meets technology in perfect harmony."
- "Young innovators solving tomorrow's challenges today!"

Return only the description with no additional text.
```

## Team Decision-Making Considerations

When generating names, encourage teams to consider:
1. **Consensus Building**: How will the team decide on a name?
2. **Inclusivity**: Does the name represent all team members?
3. **Longevity**: Will the name still work in future seasons?
4. **Branding**: How will it look on team materials?
5. **Originality**: Is the name unique to your team?

## Implementation Parameters

### API Configuration
- Configuration is managed through `config.py` (no environment variables used)
- Model: `gemini-1.5-pro` (or latest available)
- Temperature: `0.7` (balance between creativity and consistency)
- Max output tokens: `30` (keeps responses concise)
- Top-k: `40`
- Top-p: `0.95`
- API key and other settings are stored in `config.py`

### Safety Settings
- Set harassment, hate speech, dangerous content, and sexually explicit filters to maximum safety levels
- Set violence filter to medium (allows for creative but appropriate content)

## Error Handling

### Name Generation Fallbacks
If the API returns inappropriate content, errors, or fails to generate a valid team name:
1. Retry with a reduced temperature (0.5)
2. If that fails, use a backup list of pre-approved team names:
   - Cosmic Builders
   - Block Masters
   - Techno Titans
   - Brick Innovators
   - Logic Legends

### Description Fallbacks
If description generation fails:
1. Retry once with simplified prompt
2. If still failing, generate a generic description:
   - For names with "Robot" or technical terms: "Engineering excellence with creativity and teamwork!"
   - For creative/abstract names: "Bringing LEGO innovation to life with passion and skill!"

## Example Inputs/Outputs

### Team Name Examples
- Good: "Quantum Builders", "Robo Revolution", "Brick Wizards"
- Avoid: Names with complex words, puns that might be missed by children, or obscure references

### Description Examples
- Good: "Exploring the universe one brick at a time!" (for Cosmic Builders)
- Avoid: Descriptions that are too complex, use advanced vocabulary, or contain cultural references children might not understand

## Testing Approach

Before deployment:
1. Generate 20 sample names and descriptions
2. Review for appropriateness and child-friendliness
3. Test with different parameters if results are too similar or not appropriate
4. Create a reject list of words/themes to avoid

## Integration Tips

- Include basic request caching to avoid repeating identical prompts
- Add a 500ms delay between multiple requests to avoid rate limiting
- Include the context of FIRST LEGO League in the system message for better context

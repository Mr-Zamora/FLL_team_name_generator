# Word Generation Guide for FLL Team Name Generator

This document explains how the word generation system works in the FLL Team Name Generator and how to expand the word components to create more diverse team names.

## Overview

The FLL Team Name Generator creates team names by combining different word components according to specific patterns. All word components are stored in `data/word_components.json`, which serves as the central repository for words used in name generation.

## Word Components Structure

The `word_components.json` file contains several categories of words:

```
{
  "prefixes": [...],
  "suffixes": [...],
  "nouns": [...],
  "animals": [...],
  "adjectives": [...],
  "description_templates": [...]
}
```

Each word entry (except for description templates) follows this structure:

```json
{
  "word": "ActualWord",
  "category": "semantic_category",
  "compatibility": ["tag1", "tag2", "tag3"]
}
```

## Word Categories Explained

### Prefixes
Words that can start a team name, such as "Quantum", "Cyber", "Techno", etc.
- Example: `{"word": "Quantum", "category": "science", "compatibility": ["tech", "abstract"]}`

### Suffixes
Words that can end a team name, typically role or group words like "Builders", "Engineers", "Team", etc.
- Example: `{"word": "Engineers", "category": "creation", "compatibility": ["tech", "modern"]}`

### Nouns
General nouns that can be used in team names, such as "Robots", "Circuits", etc.
- Example: `{"word": "Robots", "category": "tech", "compatibility": ["tech", "modern"]}`

### Animals
Animal names that can be used in team names, like "Eagles", "Tigers", etc.
- Example: `{"word": "Eagles", "category": "animal", "compatibility": ["nature", "power"]}`

### Adjectives
Descriptive words that can be used in team names or descriptions, such as "Creative", "Dynamic", etc.
- Example: `{"word": "Creative", "category": "trait", "compatibility": ["abstract", "modern"]}`

### Description Templates
Templates used to generate descriptions for team names. These can include placeholders that get replaced with relevant words.
- Example: `"The {adjective} team that combines {category1} and {category2} in innovative ways!"`

## Understanding Compatibility Tags

Compatibility tags are crucial for creating coherent team names. They determine which words can be combined together:

- Common tags include: `tech`, `nature`, `abstract`, `modern`, `space`, `power`, `creation`, etc.
- Words with matching compatibility tags will be more likely to be paired together
- The generator looks for words whose compatibility tags overlap

For example, a prefix with `["tech", "modern"]` compatibility will work well with suffixes that have at least one of those tags.

## Name Generation Patterns

The system uses four main patterns to generate names:

1. **Prefix + Suffix**: e.g., "Quantum Engineers", "Cyber Squad"
2. **Prefix + Noun**: e.g., "Digital Circuits", "Techno Robots"
3. **Adjective + Animal**: e.g., "Creative Eagles", "Dynamic Tigers"
4. **Prefix + Animal**: e.g., "Cyber Dragons", "Quantum Eagles"

## How to Expand the Word Components

### Adding New Words

To add new words, simply add new entries to the appropriate arrays in `word_components.json`:

```json
"prefixes": [
  // Existing prefixes...
  {"word": "YourNewPrefix", "category": "appropriate_category", "compatibility": ["tag1", "tag2"]}
]
```

### Guidelines for Adding Words

1. **Choose Appropriate Categories**: The category should reflect the semantic meaning of the word
2. **Assign Relevant Compatibility Tags**: Tags should reflect what other words would pair well with this word
3. **Consider FIRST LEGO League Themes**: Words related to robotics, innovation, teamwork, and STEM are particularly appropriate
4. **Avoid Inappropriate Content**: All words should be appropriate for all ages
5. **Test Your Additions**: After adding new words, test the generator to ensure the combinations make sense

### Example: Adding LEGO-Themed Words

```json
// New prefixes
{"word": "Brick", "category": "building", "compatibility": ["creation", "modern"]},
{"word": "Block", "category": "building", "compatibility": ["creation", "abstract"]},

// New suffixes
{"word": "Constructors", "category": "creation", "compatibility": ["tech", "creation"]},
{"word": "Assemblers", "category": "creation", "compatibility": ["tech", "creation"]},

// New adjectives
{"word": "Modular", "category": "structure", "compatibility": ["tech", "creation"]},
{"word": "Interlocking", "category": "structure", "compatibility": ["tech", "creation"]}
```

## Best Practices

1. **Maintain Balance**: Try to add a similar number of words to each category
2. **Use Consistent Capitalization**: All words should start with a capital letter
3. **Keep Words Concise**: Shorter words generally work better in team names
4. **Test Combinations**: Make sure your new words create good combinations with existing words
5. **Update Regularly**: Consider updating the word components each season to reflect new FIRST LEGO League themes

## Technical Implementation

The word components are loaded by the `name_generator.py` module, which handles:
- Loading and caching the word components
- Finding compatible words based on compatibility tags
- Generating team names using the various patterns
- Ensuring generated names are unique

After modifying `word_components.json`, restart the application to see your changes take effect.

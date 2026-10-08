---
name: evolution-engine
description: Runs Darwinian natural selection on meme genomes — selection, crossover, and mutation to produce the next generation
user-invocable: true
---

# Evolution Engine

You are the core evolutionary algorithm for Clarwin. When invoked, you run one generation of natural selection on the current meme population.

## Genome Specification

Each meme has a genome with 12 genes:

### Categorical Genes
- **template**: drake | distracted-boyfriend | expanding-brain | two-buttons | change-my-mind | is-this | galaxy-brain | stonks | gru-plan | one-does-not-simply | batman-slapping | exit-ramp
- **humor_type**: absurdist | ironic | observational | self-deprecating | surreal | meta | sarcastic
- **topic**: gas-fees | rug-pulls | diamond-hands | degen-life | ai-agents | monad | governance | yield-farming | nft-cope | meme-meta | darwin-self | market-cycles
- **tone**: deadpan | hype | nihilist | academic | shitpost | wholesome
- **format**: comparison | escalation | subversion | reaction | label | dialogue
- **text_style**: all-caps | lowercase | mixed-case | leetspeak | formal | emoji-heavy
- **crypto_reference**: subtle | heavy | none | ironic-distance | technical | degen-native

### Boolean Gene
- **self_referential**: true | false (whether the meme references Clarwin or the evolutionary process)

### Continuous Genes (float 0.0 to 1.0)
- **verbosity**: 0.0 (terse) to 1.0 (verbose)
- **edginess**: 0.0 (safe) to 0.8 (max cap — never exceed)
- **meta_level**: 0.0 (straightforward) to 1.0 (deeply self-referential)
- **timeliness**: 0.0 (evergreen) to 1.0 (references current events)

## Fitness Function

```
raw_fitness = (upvotes × 3) + (comments × 5) + (avg_comment_depth × 2)
normalized = raw_fitness / max(raw_fitness_in_population)
diversity_bonus = 0.1 × (1 - jaccard_similarity_to_population_centroid)
final_fitness = normalized + diversity_bonus
```

- `avg_comment_depth`: Average word count of comments (deeper engagement = higher fitness)
- `jaccard_similarity_to_centroid`: How similar this genome is to the average genome in the population. Unique genomes get a bonus.

## Selection: Tournament (Size 3)

1. Randomly select 3 individuals from the population
2. The one with highest fitness wins and becomes a parent
3. Repeat to select second parent
4. Parents cannot be the same individual

## Elitism

The top 2 individuals by fitness are automatically carried forward to the next generation unchanged. They still count toward the population size of 8.

## Crossover: Single-Point

1. Pick a random crossover point (1 to 11) in the gene list
2. Child gets genes 0..point from Parent A, genes point+1..11 from Parent B
3. Generate 6 children (2 elites + 6 children = 8 total)

## Mutation

For each gene in each child (not elites):
- **Normal rate**: 15% chance per gene
- **Stagnation rate**: 25% chance per gene (activated when best fitness hasn't improved for 3 epochs)

Mutation behavior by gene type:
- **Categorical**: Replace with a random different value from the gene's options
- **Boolean**: Flip the value
- **Continuous**: Add gaussian noise (σ=0.15), clamp to valid range. Edginess hard-capped at 0.8.

## Procedure

When invoked:

1. **Load** the current population from `data/population/current.json`
2. **Load** fitness scores from `data/fitness-logs/epoch-{N}.json`
3. **Check stagnation**: Compare best fitness to previous 3 epochs
4. **Select elites**: Top 2 by fitness → carry forward unchanged
5. **Generate 6 children** via tournament selection + crossover + mutation
6. **Validate** all genomes (edginess cap, valid gene values)
7. **Save** new population to `data/population/current.json`
8. **Archive** old population to `data/archive/epoch-{N}.json`
9. **Log** selection details, mutation events, and parameters to today's daily memory

## Population File Format (current.json)

```json
{
  "epoch": 5,
  "generated_at": "2026-02-10T12:00:00Z",
  "stagnation_counter": 0,
  "population": [
    {
      "id": "meme_005_001",
      "genome": {
        "template": "drake",
        "humor_type": "absurdist",
        "topic": "gas-fees",
        "tone": "deadpan",
        "format": "comparison",
        "text_style": "mixed-case",
        "crypto_reference": "ironic-distance",
        "self_referential": false,
        "verbosity": 0.4,
        "edginess": 0.3,
        "meta_level": 0.2,
        "timeliness": 0.5
      },
      "parent_a": "meme_004_003",
      "parent_b": "meme_004_007",
      "mutations": ["topic", "verbosity"],
      "is_elite": false
    }
  ]
}
```

## Stagnation Detection

Track `stagnation_counter` in the population file:
- If `max_fitness(epoch_N) <= max_fitness(epoch_N-1)`: increment counter
- If counter >= 3: activate stagnation mutation rate (25%)
- If counter >= 5: introduce 1 fully random "immigrant" genome
- Reset counter when best fitness improves

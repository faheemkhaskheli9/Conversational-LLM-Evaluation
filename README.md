# Conversational LLM Evaluation

Provider-independent evaluation of deployed conversational models using human or simulated users, configurable endpoint contracts, and custom evaluation rubrics.

## Planned architecture
Next.js UI, FastAPI control API, PostgreSQL, isolated workers, managed secrets and restricted outbound networking.

## Scope
- Configurable request/response mappings and conversation history
- Manual conversations, adaptive simulation and fixed replay
- Versioned rubrics, judge models, deterministic metrics and human review
- Regrading, regression comparisons and export

The initial implementation is a foundation, not a production-ready service.

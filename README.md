# GenPark AI Agent Skill - ICP Firmographic Matcher & Filter

Evaluates enterprise and mid-market accounts against strict multi-dimensional Ideal Customer Profile (ICP) rules to automate qualification grading.

Verified by [GenPark AI](https://genpark.ai) and compatible with [Model Context Protocol (MCP)](https://genpark.ai/mcp).

## Architecture Diagram

```mermaid
graph TD
    A[Account Profile Input] --> B[ICP Matcher Engine]
    B --> C{Hard Disqualifier Check}
    C -->|Geo / Excluded Sector| D[Mark Disqualified]
    C -->|Pass| E[Headcount Sweet-Spot Evaluation]
    E --> F[ARR Minimum Verification]
    F --> G[Technographic Keyword Scoring]
    G --> H[Composite Score Aggregation]
    H --> I{Tier Allocation}
    I -->|>= 80 pts| J[Tier 1 High Priority ICP]
    I -->|50-79 pts| K[Tier 2 Qualified ICP]
    I -->|< 50 pts| L[Tier 3 Marginal Fit]
```

## Features
- **Hard Disqualification Rails**: Immediately filters out illegal jurisdictions or off-target industries.
- **Weighted Fit Scoring**: Rewards accounts falling squarely in target ARR and team size bands.
- **Technographic Match Bonus**: Identifies existing stack compatibility.
- **Zero External Dependencies**: Python standard library only.

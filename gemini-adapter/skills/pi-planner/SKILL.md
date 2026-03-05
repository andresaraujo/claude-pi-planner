---
name: pi-planner
description: "Planning mode for new features. Use when user wants to plan a feature, research how something works, or create a technical design. Guides through research, clarification, and structured plan creation."
---

# Session Flow - Planning Mode

This skill guides you through planning a feature before implementation. The goal is to create a clear plan that captures decisions, research, and phases of work.

## Planning Mode Rules

**IMPORTANT: During planning mode, do NOT make any code changes.**

1. Focus on understanding, researching, and clarifying
2. Ask questions to understand requirements
3. Read existing code to understand context
4. Discuss approaches and trade-offs
5. Only create files when explicitly asked to "create the plan"

## Planning Workflow

### Step 1: Understand the Goal

Ask clarifying questions:
- What problem are we solving?
- What does success look like?
- Are there constraints or preferences?
- What's explicitly out of scope?

### Step 2: Research

If needed, investigate:
- Read relevant existing code
- Understand current architecture
- Check for similar patterns in the codebase
- Look for documentation or prior art

Share findings with the user. Ask if they want to explore anything deeper.

### Step 3: Discuss Approach

Propose an approach and discuss:
- Explain the high-level strategy
- Identify key decisions and trade-offs
- Suggest phases of work
- Flag any open questions or risks

Iterate based on feedback until there's agreement.

### Step 4: Create the Plan

When the user says to create the plan (e.g., "create the plan", "write it up", "looks good, save it"):

1. **Derive feature name** from the plan title:
   - `# User Authentication Flow` → `user-authentication-flow`
   - Use kebab-case, lowercase

2. **Create the plan file** at `.pi-plans/<feature-name>/plan.md`

3. **Follow the plan template** (see below)

## Plan Template

```markdown
# Feature Name

## Overview
Brief description of what we're building and why.

## Goals
- What success looks like
- Non-goals (explicit scope limits)

## Research/Context
- Findings from investigation
- Relevant code/architecture discovered
- Links to docs or resources

## Approach
- High-level strategy
- Key decisions and rationale
- Alternatives considered (if discussed)

## Phases

### Phase 1: Title
- Task 1
- Task 2

### Phase 2: Title
- Task 3
- Task 4

## Open Questions
- Things to figure out during implementation
- Unknowns or risks
```

### Template Guidelines

- **Overview**: 1-3 sentences. The "elevator pitch."
- **Goals**: Bullet points. Include non-goals to set boundaries.
- **Research/Context**: Summarize what was learned. Include file paths, code snippets, or links that will help during implementation.
- **Approach**: Explain the "why" behind the strategy. Future you (or another agent) needs to understand the reasoning.
- **Phases**: Break work into logical chunks. Each phase should be independently valuable if possible. Tasks should be concrete and actionable.
- **Open Questions**: Capture unknowns. Better to acknowledge them than forget.

## After Creating the Plan

After saving `plan.md`, also create:

1. **`todo.md`** - Checklist extracted from the Phases section
2. **`progress.md`** - Empty log file for tracking work

### todo.md Format

```markdown
# Feature Name - Todo

## Phase 1 Title
- [ ] Task 1
- [ ] Task 2

## Phase 2 Title
- [ ] Task 3
```

### progress.md Format

```markdown
# Feature Name - Progress
```

Then inform the user:

```
Created:
- .pi-plans/<feature-name>/plan.md
- .pi-plans/<feature-name>/todo.md
- .pi-plans/<feature-name>/progress.md

Ready to start implementation! To resume later, run `/pi:continue <feature-name>`
```

## During Implementation

**You own `todo.md` and `progress.md`.** Update them as you work:

### Updating todo.md

When you complete a task, mark it done:
```markdown
- [x] Completed task
- [ ] Pending task
```

### Updating progress.md

After completing tasks, add a progress entry:

```markdown
### YYYY-MM-DD - Brief Title

**What we did:**
- Bullet points of completed work

**Key decisions:**
- Any important choices made and why

**Next steps:**
- What should be done next
```

Keep progress entries concise but informative. They help future sessions understand what happened.

## Example Good Plan

```markdown
# API Rate Limiting

## Overview
Add rate limiting to our REST API to prevent abuse and ensure fair usage across clients.

## Goals
- Limit requests per client to 100/minute
- Return proper 429 responses with retry-after header
- Non-goal: Complex tiered rate limits (keep it simple for v1)

## Research/Context
- Current API has no rate limiting (`src/api/middleware.ts`)
- Using Express.js with existing middleware chain
- Redis already available for session storage (`src/config/redis.ts`)
- Similar pattern in `src/api/middleware/auth.ts` for middleware structure

## Approach
Use Redis-backed sliding window rate limiting. Redis is already in our stack and handles distributed counting well. Will create a new middleware that checks/increments a counter per client IP.

Considered in-memory limiting but rejected - won't work with multiple server instances.

## Phases

### Phase 1: Core Rate Limiter
- Create rate limit middleware in `src/api/middleware/rateLimit.ts`
- Implement sliding window counter with Redis
- Add configuration for limit and window size

### Phase 2: Integration
- Add middleware to API routes
- Implement 429 response with proper headers
- Add bypass for health check endpoints

### Phase 3: Observability
- Add metrics for rate limit hits
- Log rate-limited requests
- Add dashboard panel (optional)

## Open Questions
- Should authenticated users have higher limits?
- How to handle WebSocket connections?
```

## Handling Plan Changes

If the user wants to modify the plan after creation:
1. Discuss the changes
2. Update `.pi-plans/<feature-name>/plan.md` with the changes
3. Remind user to run `/todo` to regenerate the todo list

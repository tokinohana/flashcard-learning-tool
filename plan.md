Revised Blueprint (clean + minimal)
Phase 1 — Core (unchanged)
Features
Flashcards (static JSON)
Quiz (MCQ)
Result page (score + explanation)
Add (important for Phase 3 later)

Store mistake data:

{
  "question_id": "q1",
  "topic": "trigonometry",
  "user_answer": "45°",
  "correct_answer": "30°",
  "correct": false
}
Phase 2 — UI polish
Focus
Better UX, not features

Add:

progress bar in quiz
highlight wrong answers
“review mistakes” page
LaTeX rendering stable

No AI yet.

Phase 3 — Mistake Analysis (AI here)
Goal

Turn mistakes → actionable feedback

1. Input to model

Do NOT send full history. Compress:

{
  "topic": "trigonometry",
  "mistakes": [
    {
      "question": "sin(x)=1/2",
      "user_answer": "45°",
      "correct_answer": "30°"
    }
  ]
}
2. Output (strict format)

Force structure:

{
  "weak_concept": "special angles",
  "reason": "confuses sin values",
  "advice": "memorize unit circle for 30°, 45°, 60°",
  "next_step": "practice basic sin/cos values"
}
3. Pipeline
quiz → collect mistakes → group by topic → summarize → send to model → display feedback
4. Grouping logic (important)

Before AI:

# group mistakes
by_topic = {}
for m in mistakes:
    by_topic[m["topic"]].append(m)

Send per topic, not all mixed.

5. Why this works better

You avoid:

hallucinated questions
bad answers
validation complexity

You only use AI for:

pattern recognition
explanation
6. UI (dashboard)

Show:

weak topics
AI suggestion
“retry this topic” button
7. Prompt design (critical)

Keep tight:

You analyze student mistakes.

Input: mistakes with correct answers.
Output JSON only.

Identify:
- weak_concept
- reason of mistake
- specific advice
- next_step
8. Constraints

Reject output if:

not JSON
vague advice (“practice more”)
Architecture summary
Phase 1 → deterministic engine
Phase 2 → polished UX
Phase 3 → AI feedback layer
Key advantage vs NotebookLM
NotebookLM: explains documents
You: diagnose learning mistakes

This is a different category.

Final note (important)

This design avoids the biggest problem:

small models generating bad content

Instead:

your content = correct (static)
AI = advisory only → low risk
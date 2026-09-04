# Two Answers

## What did you cut, and why?

I cut one major component, which is also the main weakness of this course: API calls to an AI provider. I had two primary concerns about using an API: cost and nondeterminism.

Cost would have been relatively easy to address. Google offers limited free access to Gemini Flash through its API, while Groq provides free access to some models with reasonable token-per-minute limits and performance.

The main concern was nondeterminism. In a course where students should receive the same results every time, compare their results with those of their peers, and revisit their work later, we need a stable baseline. If an AI model scored the cases as described in the course, its output could vary—even with a low temperature and a structured output schema like the one used here.

If the baseline were not stable across more than 100 runs, students could receive different results from one another or obtain different results when rerunning the script. Either case could break an otherwise correct solution. I considered that risk unacceptable because this topic can already be confusing, and inconsistent results would make the learning experience worse.

## Where is your course weakest?

As noted above, the course's main weakness is that it does not use a live AI provider. However, using AI output as the baseline was not necessary. I could have defined and hardcoded a deterministic baseline while also giving students the option to run a real model as they progressed through the course.

This would allow students to build and refine a rubric using real-world model outputs in a production-like setting. For example, after a human evaluator established the expected answers, students could run the LLM-as-a-judge evaluation several times, compare the results, and revise the rubric to improve consistency. They would effectively act as judges of the AI judge, following an evaluation-driven approach used in industry, including at [Airbnb](https://medium.com/airbnb-engineering/eval-driven-development-lessons-from-evaluating-genai-at-scale-e817e5ae5788).

Evaluation is essential for AI-based products and goes much deeper than the material covered here. A natural next step would be to explore additional evaluation frameworks and the scenarios in which each one is useful.

# Build us a course

**EducationPals · AI Engineer Intern · Take-home**

About **4 hours of your time**. The course itself should take a learner ~90 minutes. | 2 to 3 lessons | up to 5 sections each | one build-along per lesson | generated with AI | text only

---

Hi Felipe,

Thanks for applying to the AI Engineer Intern role. Below is the take-home. Reply with your zip to randeep@educationpals.ai (same address as Reply-To on this email).

---

## Why

Generating courses with agents is one of the foundations this company is built on, so we are asking you to do a small version of the real thing rather than a puzzle with nothing to do with the job.

Bring whichever AI tools you work best with. There is no version of this we would rather see done by hand, and how you work with a model is a good part of what we are reading.

---

## Pick one topic

All five are real holes in our catalog. We have 33 courses live and none of them cover these. Pick the one you’d most want to see in the catalog.

| Topic | Written for | Capstone the learner ends up holding |
| --- | --- | --- |
| **Evals and LLM-as-Judge** | Someone who shipped an AI feature and cannot tell if it is getting worse | A working grader printing real precision and recall |
| **Context Engineering** | Someone whose prompts work in testing and fail in production | A context assembly pipeline that beats naive stuffing at a fixed budget |
| **AI Cost Control and Model Routing** | Someone who just got a bill they cannot explain | A cascade router with a measured cost and quality curve |
| **Structured Outputs** | Someone whose pipeline breaks when the model returns prose instead of JSON | A schema-validated pipeline with a repair loop |
| **Running Models Locally** | Someone who cannot send their data to an API | A tiny OpenAI-compatible stub (no model weights in the zip) plus a measured quality note |

For **Running Models Locally**: do not ship weights. A stub endpoint and a short quality-gap note is enough. Zip must stay under 10 MB.

---

## Generate it with AI

**The course and the build-alongs must be generated with AI.** Not hand-written and polished with a model. Generated: your agent, your orchestration, your prompts.

Send that setup with the submission. It is the part we read most closely, and it is the closest thing here to the actual job.

---

## How to build it

**Start with the breaking points.** Where does a person actually get stuck on this topic? Where do they nod along and quietly lose the thread? Name at least three before you generate any content.

**Turn those into checkpoints.** A checkpoint is something the learner can now do and could not before. Name them before generating any content. Lessons are just containers for them.

**Design backwards from the capstone.** Cut it into two or three pieces where each is useful on its own, then write the lessons that produce them in order.

---

## Shape

| | |
| --- | --- |
| Sections per lesson | Up to 5 |
| A section | 2 to 3 minutes, 300 to 500 words, one idea |
| Checkpoints per lesson | 1 to 3 |
| Build-along | One, at the end of every lesson |

Each build-along produces a small artifact, and they compound: lesson one's output is lesson two's input, and the last one completes the capstone. Keep each under 20 minutes of learner time.

Plan on about ninety minutes end to end for the learner. Two lessons done properly beat three done thin, so take the two-lesson option if the capstone splits that way.

---

## Rules

- Text only. No video, no audio.
- Diagrams are a big plus. Inline HTML or SVG, not Mermaid. No raster images (PNG/JPEG); HTML/SVG diagrams count.
- Build-alongs are interactive: a CLI or notebook that prints a visible check at every step, built up incrementally rather than dropped in finished. A UI is not required.
- Nothing else. No flashcards, quizzes, or assessments.

**We will follow your build-alongs and try to reach the capstone. If we cannot, that is the end of the review.**

---

## How we run your submission

- Use your own API keys while you build.
- We grade `output/` first (what your code printed when you ran it). Include that folder.
- Code must be runnable offline for review: `README.md` says how (`python …`), and it should replay fixtures or cached results without a paid API call when we run it.
- Pin **Python 3.12**. Put deps in `requirements.txt`. Do not include `node_modules` or model weights in the zip.

---

## Send

One zip to randeep@educationpals.ai, subject line `AI Engineer Intern: [your name]`, by **Friday 5 Sep 2026, 11:59pm PT**. Under 10 MB, no dependencies we have to hunt for.

    lastname-firstname/
      README.md     checkpoints, capstone, how to run it
      course/       lessons, one file each
      build/        the code a learner produces, one folder per build-along
      output/       what that code actually printed when you ran it
      agent/        your config, orchestration, and prompts
      writeup.md    two answers, 150 words each

Send the code **and** the output it produced. We will run it ourselves and compare.

The two answers: **what you cut and why**, and **where your course is weakest**.

Your work stays yours. We will not put it in the catalog, and if we ever want to, we will come back and pay you for it.

If you need an accommodation to complete this, email us and we will sort it out.

---

## Graded

Whether the build-alongs reach the capstone. Whether the artifacts compound or restart each lesson. How you generated it, which is why the `agent/` folder matters as much as the course. Checkpoint structure. Prerequisite order, so lesson two never leans on something lesson one did not teach. Technical correctness, including keeping real industry vocabulary instead of inventing your own.

**Not graded:** writing quality, length, polish. A good model writes fluent lesson prose for anybody, so it tells us nothing about you.

---

Randeep

Founder and CEO, EducationPals

If you do not want further emails about this role, reply with the word unsubscribe.
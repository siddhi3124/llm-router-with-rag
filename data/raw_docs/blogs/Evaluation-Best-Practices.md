# Evaluation best practices

Source: https://developers.google.com/stax/best-practices
Retrieved on: March 2026

---

Stop "vibe testing" your LLMs. It's time for real evals.
If you're building with LLMs, you know the drill. You tweak a prompt, run it a few times, and... the output feels better. But is it actually better? You're not sure. So you keep tweaking, caught in a loop of "vibe testing" that feels more like art than engineering.

This uncertainty exists for a simple reason: unlike traditional software, AI models are non-deterministic. They don't always give the same output for the same input, which makes your usual unit tests insufficient for knowing if a change actually improved your results. On top of that, you have to wrangle datasets, manage API calls, parse outputs, and build a whole evaluation pipeline before you can even start testing.

To move past the vibes, we built Stax, a developer tool designed to take the headache out of LLM evaluation. We've leveraged the evaluation expertise from Google DeepMind and the experimental innovation from Google Labs to streamline the LLM evaluation lifecycle.

App builders need AI evals too
To know if your AI application really works for a specific use case, your own AI evals can be a critical tool. General benchmarks are generic tests measuring the model across a range of tasks, but they don't help you evaluate your AI stack based on your data and criteria.

Done right, evals can be a key differentiator, letting you codify your unique goal into your own reusable benchmark. Instead of spending hours "vibe testing" every time you try a new model or tweak a prompt, evals give you clear metrics to know what's actually better.

How to make good evals
Good evals can give you a clear sense of whether your AI application is actually behaving as intended, before it's shipped to real users where the stakes are high.

The first and most important step is defining your evaluation criteria: specific, measurable qualities you define that determine what "good" performance looks like. To come up with these criteria, it's helpful to consider:

Ideal behavior: How should your AI interact with users? (e.g., My AI tutor should never give away the answer to a homework problem.)
Business goals: What business outcomes are you trying to drive? (e.g., My customer support bot should help users resolve problems; I should have zero safety violations.)
Failure cases: What failure modes do you want to fix, based on production data or your own testing? (e.g., Summaries are too verbose; generated stories are not creative enough.)
With your criteria defined, the next step is to build a benchmark to test different versions of your AI on this criteria. This benchmark includes:

A dataset: A set of user prompts designed to test the evaluation criteria. You could write these yourself, pull them from production data, or even use an LLM to synthetically create them. Be sure to include the happy path, edge cases and adversarial examples. Stax gives you a centralized platform to manage and curate these datasets, turning them into a more reliable asset for your team.

An evaluator: This is the method used to score your AI's performance on the evaluation criteria. There are three common ways this is done:

Heuristic or code-based: These are simple, rule-based checks. They're helpful for objective, quantitative tasks where there's a clear right or wrong answer (e.g., does the output contain a specific keyword?; does it have the right number of tool calls?). They are a good starting point, but they can't measure subjective qualities like creativity or tone.
LLM-as-judge (aka autoraters): Here, an AI model is prompted to score output based on your evaluation criteria. While this is an effective method, the quality of the results depends entirely on the quality of your prompt and rubric. Stax has preloaded LLM evaluators that provide effective starting prompts and rubrics, though you should adapt them to your specific use case. To ensure alignment, manually rate a small sample set yourself and iterate on your autorater prompt until you agree with the scores.
Human raters: We've seen that developers often consider external human raters as the gold standard, but it's often slow, expensive, and hard to ensure consistency. Given that today's LLM autoraters are approaching human-level performance, they offer a faster, more scalable, and cost-effective way to perform evaluations.
In Stax, we make it easier to build datasets and evaluators and to seamlessly test any version of your AI against your unique evaluation criteria.

Some evals tips & tricks
Regression tests & challenge sets: Your evals should include regression tests to protect existing quality and challenge sets to drive future improvements. Regression tests prevent you from breaking what already works (e.g., always output valid JSON), while challenge sets target areas where you want your AI to get better.
Some evals are better than none: You don't need a perfect eval setup to get value. While the ideal is to have hundreds of prompts, covering all your key criteria, and perfectly aligned evaluators, that's rarely realistic. Instead, focus on getting more signal. An eval set with just ten high-quality prompts is infinitely more valuable than relying on vibe testing alone. Stax provides the framework to help turn those ten prompts into a real asset that you can expand on, helping you build the right evaluation habits from day one.
Human review (by the team) still matters: Don't abandon "vibe tests" altogether. Having your team use your AI product is still crucial for building intuition about what is and isn't working and what you should evaluate next. Instead of that feedback getting lost, use Stax to conduct these human reviews directly. This lets you save compelling examples and turn ad hoc 'vibe tests' into a structured, golden dataset.
Stop guessing, start evaluating
The era of crossing your fingers and shipping LLM features is over. It's time to treat them like other parts of your production stack: with rigorous testing and robust tooling. Stax gives you the power to better understand, iterate, and improve your LLM-powered features faster than ever.
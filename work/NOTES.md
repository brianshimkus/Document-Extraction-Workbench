# Learning journal

For each lesson record your prediction, observed result, explanation,
one failure, and one change you made independently.

## Interview evidence

Problem:
My contribution:
Input to output:
Alternative considered:
Failure and fix:
Measured result and sample size:
Limitation:
Next experiment:

## Experiment log

Date | Data split | Mode | Model | Change | Metric | Result | Interpretation


## Lesson 1
Q: What going in an invoice file?
A: The invoice itself. The whole page of text.

Q: What comes out?
A: The fives answers as JSON.

Q: What does an empty field mean?
A: The page never gave the fact, so the value stays null.

## Lesson 2
• null means the page never gave that fact
• "" means a blank string, which is still a value
• 0 or 0.00 means the page really said zero

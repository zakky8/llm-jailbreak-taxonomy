# Contributing to the LLM Jailbreak Taxonomy

Thank you for your interest in improving the taxonomic classification of LLM alignment failures. We welcome contributions that add rigor, empirical depth, or structural clarity to the project.

## How to Contribute

### 1. Proposing a New Attack Pattern (Subcategory)
If you have identified a new mechanistic bypass that is not covered by the existing 30 patterns:
- Open an Issue with the tag `new-pattern`.
- Describe the pattern's **mechanism of action**.
- Explicitly identify the **alignment assumption** it exploits.
- Provide a literature reference if it has been documented academically.
- **Do not include prohibited or harmful payload text.** Use benign placeholders (e.g., "Insert harmful instruction here").

### 2. Proposing a New Category
The six-category taxonomy is intended to be mechanistically exhaustive, but novel modalities (e.g., vision-language bypasses) may necessitate expansion.
- Open a discussion thread or pull request detailing why the new attack vector cannot be subsumed under Categories 1–6.
- Detail the structural assumption violated.

### 3. Submitting Empirical Results
If you have run the evaluation protocols documented in the notebooks:
- Ensure your testing strictly adhered to the stated temperature and trial counts.
- Submit the results CSV via Pull Request.
- Confirm your results do not contain proprietary system prompts or sensitive harmful outputs.

## Code of Conduct
All contributors must adhere to ethical AI research standards. Submissions designed purely to cause harm, optimize malicious payloads, or attack specific commercial applications will be rejected and reported.

# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

skills:
  - name: [skill_name]
    description: [One sentence — what does this skill do?]
    input: [What does it receive? Type and format.]
    output: [What does it return? Type and format.]
    error_handling: [What does it do when input is invalid or ambiguous?]

  - name: [second_skill_name]
    description: [One sentence]
    input: [Type and format]
    output: [Type and format]
    error_handling: [What does it do when input is invalid or ambiguous?]

# skills.md

skills:
  - name: retrieve_document_chunk
    description: Retrieves the most relevant text section from the internal policy documents based on the user’s question.
    input: User question string (plain text).
    output: A document chunk containing the relevant policy text along with the document source name (e.g., IT Security Policy or HR Policy).
    error_handling: If no relevant document text is found, return "NO_MATCH_FOUND" and trigger the refusal response workflow.

  - name: answer_with_citation
    description: Generates a clear answer to the user’s question using only the retrieved policy document chunk and includes the source citation.
    input: Retrieved document chunk text and the original user question.
    output: A concise answer followed by the cited policy source (for example: "Source: IT Security Policy").
    error_handling: If the document chunk does not directly answer the question, return "INSUFFICIENT_INFORMATION" and trigger the refusal template.

  - name: refusal_response
    description: Produces a standard refusal response when the system cannot answer the question using a single document source.
    input: Refusal trigger signal such as NO_MATCH_FOUND, INSUFFICIENT_INFORMATION, or MULTI_DOCUMENT_REQUIRED.
    output: A standardized refusal message stating that the answer cannot be provided from the available document source.
    error_handling: If the refusal signal is unclear, default to the standard refusal template to avoid hallucinated answers.
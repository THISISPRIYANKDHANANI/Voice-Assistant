def extract_subject_and_body(text):
    lines = text.strip().split("\n")
    subject = ""
    body_lines = []

    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line[len("subject:"):].strip()
        else:
            body_lines.append(line.strip())

    body = "\n".join(body_lines).strip()
    return subject or "No Subject", body

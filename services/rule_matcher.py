from sentence_transformers import SentenceTransformer, util
from models.compliance import NdpaRule
import torch

_model = None


def get_model():
    global _model
    if _model is None:
        print("Loading MiniLM model...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully.")
    return _model


def embed_sentences(sentences):
    model = get_model()
    embeddings = model.encode(sentences, convert_to_tensor=True)
    return embeddings


def find_best_match(rule_embedding, srs_embeddings, srs_sentences):
    similarities = util.pytorch_cos_sim(rule_embedding, srs_embeddings)[0]
    best_idx = torch.argmax(similarities).item()
    best_score = similarities[best_idx].item()
    best_sentence = srs_sentences[best_idx]
    return best_sentence, round(best_score, 4)


def classify_compliance(rule_type, similarity_score, matched_sentence):
    matched_lower = matched_sentence.lower()

    negative_phrases = [
        "does not", "do not", "no ", "not ", "never",
        "without", "lack", "missing", "absent",
        "no consent", "not required", "not implemented",
        "not collected", "not stored", "not encrypted",
        "not protected", "not provided", "not notified",
        "not allowed", "not available", "not supported"
    ]

    has_negation = any(phrase in matched_lower for phrase in negative_phrases)

    if similarity_score < 0.35:
        return "NOT ADDRESSED"

    if rule_type == "OBLIGATION":
        if has_negation:
            return "NON-COMPLIANT"
        elif similarity_score >= 0.55:
            return "COMPLIANT"
        else:
            return "NOT ADDRESSED"

    elif rule_type == "PROHIBITION":
        if has_negation:
            return "COMPLIANT"
        elif similarity_score >= 0.55:
            return "NON-COMPLIANT"
        else:
            return "NOT ADDRESSED"

    elif rule_type == "PERMISSION":
        return "COMPLIANT"

    return "NOT ADDRESSED"


def generate_recommendation(rule_text, status, rule_type):
    rule_lower = rule_text.lower()

    if status == "COMPLIANT":
        return "No action required. This requirement is satisfied."

    recommendations = {
        "consent": "Implement a clear consent mechanism such as a checkbox or popup that explicitly asks users for permission before collecting or processing their personal data.",
        "encrypt": "Apply encryption such as AES-256 for stored data and ensure all data in transit is protected using HTTPS or TLS.",
        "security": "Implement appropriate security measures including firewalls, access controls, and data protection protocols.",
        "breach": "Establish a data breach response plan that includes notifying the Nigeria Data Protection Commission and affected users within 72 hours of a breach.",
        "access": "Provide users with a mechanism to request access to their personal data, such as a profile settings page or data request form.",
        "delet": "Implement a data deletion feature that allows users to permanently delete their account and associated personal data.",
        "correct": "Provide users with the ability to update or correct their personal data through their account settings.",
        "transfer": "Ensure that any international data transfers include adequate safeguards such as data transfer agreements or storing data on Nigerian servers.",
        "retain": "Define and enforce a data retention policy that automatically deletes personal data when it is no longer needed.",
        "privacy policy": "Publish a clear and accessible privacy policy that explains what data is collected, how it is used, and the rights of users.",
        "data protection officer": "Appoint a Data Protection Officer (DPO) responsible for overseeing compliance with the NDPA 2023.",
        "impact": "Conduct a Data Protection Impact Assessment (DPIA) before processing any high-risk personal data.",
        "children": "Implement age verification mechanisms and obtain parental consent before collecting data from users under 18.",
        "access control": "Implement role-based access controls to ensure only authorised staff can access personal data.",
        "log": "Maintain audit logs of all access to personal data to support accountability and traceability.",
        "sensitive": "Obtain explicit consent before collecting or processing sensitive data such as health, biometric, or financial information.",
        "lawful": "Ensure every data processing activity has a documented lawful basis as required by the NDPA 2023.",
        "withdraw": "Provide users with a clear and easy way to withdraw their consent at any time."
    }

    for keyword, recommendation in recommendations.items():
        if keyword in rule_lower:
            return recommendation

    if rule_type == "OBLIGATION":
        return "Ensure this requirement is explicitly addressed in your software design and documented in your privacy policy."
    elif rule_type == "PROHIBITION":
        return "Remove or restrict this activity from your software to comply with the NDPA 2023."

    return "Review and address this requirement in line with the NDPA 2023 guidelines."


def run_compliance_check(srs_text, srs_sentences):
    rules = NdpaRule.query.all()

    if not rules:
        return None

    if not srs_sentences:
        return None

    print(f"Checking {len(rules)} rules against {len(srs_sentences)} SRS sentences...")

    rule_texts = [rule.rule_text for rule in rules]
    rule_embeddings = embed_sentences(rule_texts)
    srs_embeddings = embed_sentences(srs_sentences)

    results = []
    compliant_count = 0
    non_compliant_count = 0
    not_addressed_count = 0

    for i, rule in enumerate(rules):
        rule_embedding = rule_embeddings[i].unsqueeze(0)

        best_sentence, similarity_score = find_best_match(
            rule_embedding, srs_embeddings, srs_sentences
        )

        status = classify_compliance(
            rule.rule_type, similarity_score, best_sentence
        )

        recommendation = generate_recommendation(
            rule.rule_text, status, rule.rule_type
        )

        if status == "COMPLIANT":
            compliant_count += 1
        elif status == "NON-COMPLIANT":
            non_compliant_count += 1
        else:
            not_addressed_count += 1

        results.append({
            "rule_id": rule.id,
            "section": rule.section,
            "rule_text": rule.rule_text,
            "rule_type": rule.rule_type,
            "matched_sentence": best_sentence,
            "similarity_score": similarity_score,
            "status": status,
            "recommendation": recommendation
        })

    total_rules = len(rules)
    compliance_score = round((compliant_count / total_rules) * 100, 1) if total_rules > 0 else 0

    summary = {
        "compliance_score": compliance_score,
        "total_rules": total_rules,
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "not_addressed_count": not_addressed_count,
        "results": results
    }

    print(f"Compliance check complete. Score: {compliance_score}%")
    return summary
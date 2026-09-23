import json
import os

from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency
    genai = None


load_dotenv()


class AIEngine:
    """A lightweight AI-style classification layer for civic service issues."""

    keyword_map = {
        "Roads & Transport": [
            "road",
            "street",
            "pothole",
            "traffic",
            "signal",
            "crosswalk",
            "lane",
            "sidewalk",
            "asphalt",
            "curb",
        ],
        "Water & Sanitation": [
            "water",
            "drain",
            "sewer",
            "leak",
            "pipe",
            "waste",
            "garbage",
            "trash",
            "flood",
            "clog",
        ],
        "Public Safety": [
            "danger",
            "unsafe",
            "security",
            "lighting",
            "lamp",
            "dark",
            "fire",
            "hazard",
            "vandalism",
            "broken glass",
        ],
        "Housing & Community": [
            "housing",
            "building",
            "noise",
            "tenant",
            "community",
            "park",
            "playground",
            "garden",
        ],
    }

    def __init__(self):
        self.model = None
        api_key = os.getenv("GEMINI_API_KEY")
        if genai is not None and api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
            except Exception:  # pragma: no cover - safety fallback
                self.model = None

    def analyze_issue(self, title, description):
        if self.model is not None:
            try:
                return self._analyze_with_gemini(title, description)
            except Exception:
                pass

        combined = f"{title} {description}".lower()

        scores = {category: 0 for category in self.keyword_map}
        for category, keywords in self.keyword_map.items():
            for keyword in keywords:
                if keyword in combined:
                    scores[category] += 1

        category = max(scores, key=scores.get)
        if max(scores.values()) == 0:
            category = "General & Public Services"

        urgency = self._determine_urgency(combined)
        summary = (
            f"AI review suggests a {category.lower()} issue requiring {urgency.lower()} "
            f"attention. The reported concern is: {title.strip() or 'general civic issue'}"
        )

        return {"category": category, "urgency": urgency, "summary": summary}

    def _determine_urgency(self, text):
        high_risk = ["flood", "fire", "danger", "unsafe", "sewer", "breaks", "collapse", "leak"]
        medium_risk = ["road", "traffic", "lamp", "drain", "garbage", "noise"]

        if any(keyword in text for keyword in high_risk):
            return "High"
        if any(keyword in text for keyword in medium_risk):
            return "Medium"
        return "Low"

    def _analyze_with_gemini(self, title, description):
        prompt = f"""
You are CivicFix AI, an AI assistant that helps citizens structure and report civic problems.

Analyse the following civic complaint.

Title:
{title}

Description:
{description}

Return ONLY valid JSON with exactly these keys:
category, urgency, summary.
The values should be strings and urgency should be one of Low, Medium, High.
"""
        response = self.model.generate_content(prompt)
        response_text = response.text.strip()

        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        data = json.loads(response_text)
        return {
            "category": data.get("category") or "General & Public Services",
            "urgency": data.get("urgency") or "Medium",
            "summary": data.get("summary") or f"Issue reported: {title}",
        }


def analyze_complaint(issue, location):
    """Backwards-compatible helper for complaint analysis."""
    engine = AIEngine()
    result = engine.analyze_issue(issue, location)
    return {
        "category": result["category"],
        "severity": result["urgency"],
        "summary": result["summary"],
        "department": "Public Works",
        "complaint": issue,
        "missing_information": [],
    }

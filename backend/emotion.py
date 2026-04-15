from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

class EmotionDetector:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )

    def detect(self, text: str) -> dict:
        results = self.classifier(text)[0]
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        top = sorted_results[0]
        all_scores = {r["label"]: round(r["score"], 4) for r in sorted_results}

        return {
            "emotion": top["label"],
            "confidence": round(top["score"], 4),
            "all_scores": all_scores
        }

detector = EmotionDetector()

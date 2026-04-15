from transformers import pipeline
import warnings

warnings.filterwarnings("ignore")

classifier_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def detect(text):
    results = classifier_pipeline(text)[0]
    
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    top_emotion = sorted_results[0]
    
    all_scores_dict = {}
    for item in sorted_results:
        label = item["label"]
        score = item["score"]
        all_scores_dict[label] = round(score, 4)

    return {
        "emotion": top_emotion["label"],
        "confidence": round(top_emotion["score"], 4),
        "all_scores": all_scores_dict
    }

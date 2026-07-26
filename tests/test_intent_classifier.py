from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ai.intent_classifier import IntentClassifier


def test_trainer_search_query_is_classified_correctly() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("Who can teach Kubernetes?")
    assert intent.intent_type == "TRAINER_SEARCH"


def test_expert_search_query_is_classified_correctly() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("Who are the experts in Azure DevOps?")
    assert intent.intent_type == "EXPERT_SEARCH"


def test_course_search_query_is_classified_correctly() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("Show Terraform courses.")
    assert intent.intent_type == "COURSE_SEARCH"


def test_recommendation_query_is_classified_correctly() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("Recommend trainer for CRS001.")
    assert intent.intent_type == "TRAINER_RECOMMENDATION"
    assert intent.entity_code == "CRS001"


def test_trainer_profile_query_is_classified_correctly() -> None:
    classifier = IntentClassifier()
    intent = classifier.classify("Show profile for TRN001.")
    assert intent.intent_type == "TRAINER_PROFILE"
    assert intent.entity_code == "TRN001"

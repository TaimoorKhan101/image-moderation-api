import random
from typing import Dict
from app.models.moderation import ModerationResult, CategoryScore


class ModerationService:
    # Supported moderation categories
    CATEGORIES = {
        "explicit_nudity": "Sexually explicit content and nudity",
        "graphic_violence": "Violent, gory, or disturbing imagery",
        "hate_symbols": "Hate speech symbols and extremist imagery",
        "self_harm": "Content depicting self-harm or suicide",
        "spam_unwanted": "Spam, advertisements, or unwanted content"
    }

    # Threshold to determine if content is unsafe
    CONFIDENCE_THRESHOLD = 0.7

    async def analyze_image(
        self, file_content: bytes, filename: str, content_type: str
    ) -> ModerationResult:
        """
        Simulates image moderation by generating random confidence scores per category.
        """
        scores: Dict[str, float] = {
            category: round(random.uniform(0, 1), 2)
            for category in self.CATEGORIES
        }

        # Determine if the image is considered safe
        is_safe = all(confidence < self.CONFIDENCE_THRESHOLD for confidence in scores.values())

        return ModerationResult(
            is_safe=is_safe,
            scores=[
                CategoryScore(
                    category=category,
                    confidence=confidence
                ) for category, confidence in scores.items()
            ],
            filename=filename,
            content_type=content_type
        )

from typing import Iterable
from django.db import models
import re

class Source(models.Model):
    SOURCE_TYPES = {
        'PYQ': 'Previous Year',
        'ASN': 'Assignment',
        'MOD': 'Coaching Module',
        'TSR': 'Test Series',
        'BOOK': 'Book',
        'MISC': 'Miscellaneous',
    }

    name = models.CharField(max_length=300)
    source_type = models.CharField(max_length=300, choices=SOURCE_TYPES)

    def __str__(self) -> str:
        return '[' + self.source_type + '] ' + self.name

class Question(models.Model):
    QUESTION_TYPES = {
        "SCQ": "Single Correct Question",
        "MCQ": "Multiple Correct Question",
        "INT": "Integer Type Question",
        "NUM": "Numerical Type Question",
        "LONG": "Subjective Type Question",
        "FILL": "Fill in the Blank Question"
    }

    # Question info
    question_body = models.TextField(max_length=3000)
    question_type = models.CharField(choices=QUESTION_TYPES, default="SCQ", max_length=100)
    question_options = models.TextField(max_length=3000, null=True, blank=True)
    """
    Schema For Options
    --- option_index
    --- option_body
    --- is_correct
    """


    # Metadata
    sources = models.ManyToManyField(Source, null=True, blank=True)

    # Auto-generated
    search_text = models.TextField(max_length=2000, null=True, blank=True)
    display_text = models.TextField(max_length=3000, null=True, blank=True)
    display_image = models.TextField(max_length=3000, null=True, blank=True)
    display_body = models.TextField(max_length=3000, null=True, blank=True)

    def render_body(self):
        img_md_pattern = r"!\[(.*?)\]\((.*?)\)"

        self.display_body = re.sub(img_md_pattern, lambda match: f'<img src="{match.group(2)}" style="max-height:250px;" alt="{match.group(1)}">', self.question_body)
        self.display_body = re.sub(r'\n', '<br>', self.display_body)

        pattern = r'<img\s+[^>]*src="([^"]*)"[^>]*>'
        img_tags = re.findall(pattern, self.display_body)
        self.display_image = img_tags[0] if img_tags else None

        main_string_without_images = re.sub(pattern, '', self.display_body)
        self.display_text = main_string_without_images.strip().replace("<br>","").replace("–", "").strip() + "..."
    
    def __str__(self) -> str:
        return self.question_body[:50]+' ...'
    
    def save(self) -> None:
        self.render_body()
        return super().save()


class Solution(models.Model):
    SOLUTION_TYPES = {
        "IMG": "Image Only Solution",
        "VID": "Video Only Solution",
        "TXT": "Rich-Text Based Solution",
    }

    solution_type = models.CharField(max_length=100, choices=SOLUTION_TYPES)
    solution_media_source = models.URLField(blank=True, null=True)

    solution_body = models.TextField(max_length=3000, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

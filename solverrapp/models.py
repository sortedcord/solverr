from typing import Iterable
from django.db import models
import re

class Topic(models.Model):

    name = models.CharField(max_length=500)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def get_level(self):
        level = 0
        topic = self
        while topic.parent is not None:
            topic = topic.parent
            level += 1
        return level

    def __str__(self):
        return ("--"*self.get_level()) + self.name

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
    topics = models.ManyToManyField(Topic, null=True, blank=True)

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
        self.display_text = main_string_without_images.strip().replace("<br>","").replace("–", "").strip()

    def generate_search_text(self) -> str:
        to_null = r"""[ ,.`_'$^":{}()\[\]/]"""
        sym_replace = {
            'alpha':'α',
            'belong':'∈',
            'beta':'β',
            'infinity': '∞',
            'deg':'°',
            '!=':'≠',
            'greaterthanequal':'≥',
            'lessthanequal':'≤',
            'gamma':'γ',
            'delta':'Δ',
            'epsilon':'ε',
            'theta':'θ',
            'lambda':'λ',
            'mu':'μ',
            'pi':'π',
            'SIGMA':'Σ',
            'sigma':'σ',
            'OMEGA':'Ω',
            'omega':'ω',
            'int':'∫',
            'sum':'∑',
        }
        sanitized = re.sub(to_null, '', self.display_text.lower())
        self.search_text = sanitized

        for key, value in sym_replace.items():
            self.search_text.replace('\\'+key, value)
        print(self.search_text)
        return self.search_text

    def is_solved(self) -> bool:
        if Solution.objects.filter(question=self):
            return True
        else:
            return False


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
    solution_source = models.CharField(max_length=100, blank=True, null=True)

    solution_body = models.TextField(max_length=3000, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer = models.CharField(max_length=3000, blank=True, null=True)

    def generate_body(self):
        if not self.solution_body.startswith("$PROCESS"):
            return
        self.solution_body.replace("$PROCESS", '')

        if self.solution_type == 'IMG':
            self.solution_body = f"<img class='img-fluid' src='{self.solution_body}'>"
        elif self.solution_type == 'VID':
            if self.solution_body.endswith('.mp4') or self.solution_body.endswith('.webm') or self.solution_body.endswith('.mkv'):
                self.solution_body = f"<video class='img-fluid'><source src='{self.solution_body}'></video>"
            elif 'vimeo.com' in self.solution_body:
                video_id = self.solution_body.split("/")[-1].split('?')[0]
                self.solution_body = f"""
<div style="padding:56.25% 0 0 0;position:relative;">
<iframe src="https://player.vimeo.com/video/{video_id}?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write" style="position:absolute;top:0;left:0;width:100%;height:100%;border-radius:0.6rem;"></iframe>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>
                    """

    def save(self):
        self.generate_body()
        return super().save()


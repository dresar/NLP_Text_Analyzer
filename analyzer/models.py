from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TextAnalysis(models.Model):
    ANALYSIS_TYPES = [
        ('sentiment', 'Sentiment Analysis'),
        ('summary', 'Text Summarization'),
        ('ner', 'Named Entity Recognition'),
        ('classification', 'Text Classification'),
    ]
    
    title = models.CharField(max_length=200)
    text = models.TextField()
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES, default='sentiment')
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Text Analyses'
    
    def __str__(self):
        return self.title

class SavedTemplate(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    analysis_type = models.CharField(max_length=20, choices=TextAnalysis.ANALYSIS_TYPES, default='sentiment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    preferred_analysis_type = models.CharField(
        max_length=20, 
        choices=TextAnalysis.ANALYSIS_TYPES, 
        default='sentiment',
        blank=True
    )
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class AnalysisComment(models.Model):
    analysis = models.ForeignKey(TextAnalysis, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.analysis.title}"

class AnalysisTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class AnalysisTagging(models.Model):
    analysis = models.ForeignKey(TextAnalysis, on_delete=models.CASCADE, related_name='taggings')
    tag = models.ForeignKey(AnalysisTag, on_delete=models.CASCADE, related_name='analyses')
    
    class Meta:
        unique_together = ['analysis', 'tag']
    
    def __str__(self):
        return f"{self.analysis.title} - {self.tag.name}"

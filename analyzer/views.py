from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import TextAnalysis, SavedTemplate, UserProfile, AnalysisComment, AnalysisTag, AnalysisTagging
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileForm, SavedTemplateForm, TextAnalysisForm
import json

import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import re
import os

# Download NLTK data if not already downloaded
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    # Jika model tidak ditemukan, coba download
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

# Initialize NLTK's SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def home(request):
    """Home page view with text analysis form"""
    context = {
        'result': None,
        'analysis_type': 'sentiment',
    }
    
    # Get public analyses for showcase
    public_analyses = TextAnalysis.objects.filter(is_public=True).order_by('-created_at')[:5]
    context['public_analyses'] = public_analyses
    
    # Get saved templates if user is authenticated
    if request.user.is_authenticated:
        templates = SavedTemplate.objects.filter(user=request.user)
        context['templates'] = templates
    
    if request.method == 'POST':
        text = request.POST.get('text', '')
        analysis_type = request.POST.get('analysis_type', 'sentiment')
        save_analysis = request.POST.get('save_analysis') == 'on'
        title = request.POST.get('title', f'{analysis_type.capitalize()} Analysis')
        
        if text:
            if analysis_type == 'sentiment':
                result = analyze_sentiment(text)
            elif analysis_type == 'summary':
                result = summarize_text(text)
            elif analysis_type == 'ner':
                result = extract_entities(text)
            elif analysis_type == 'classification':
                result = classify_text(text)
            else:
                result = {'error': 'Invalid analysis type'}
                
            context['result'] = result
            context['text'] = text
            context['analysis_type'] = analysis_type
            
            # Save analysis if requested and user is authenticated
            if save_analysis and request.user.is_authenticated:
                analysis = TextAnalysis(
                    title=title,
                    text=text,
                    analysis_type=analysis_type,
                    result=result,
                    user=request.user
                )
                analysis.save()
                messages.success(request, 'Analysis saved successfully!')
                
                # Check for tags
                tags = request.POST.get('tags', '').split(',')
                for tag_name in tags:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = AnalysisTag.objects.get_or_create(name=tag_name)
                        AnalysisTagging.objects.create(analysis=analysis, tag=tag)
                
                return redirect('analysis_detail', pk=analysis.pk)
    
    return render(request, 'analyzer/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'analyzer/about.html')

@login_required
def dashboard(request):
    """User dashboard with saved analyses"""
    query = request.GET.get('q', '')
    analysis_type = request.GET.get('type', '')
    
    analyses = TextAnalysis.objects.filter(user=request.user)
    
    # Apply filters
    if query:
        analyses = analyses.filter(Q(title__icontains=query) | Q(text__icontains=query))
    
    if analysis_type:
        analyses = analyses.filter(analysis_type=analysis_type)
    
    # Pagination
    paginator = Paginator(analyses, 10)  # 10 analyses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'analysis_type': analysis_type,
        'analysis_types': TextAnalysis.ANALYSIS_TYPES,
    }
    
    return render(request, 'analyzer/dashboard.html', context)

@login_required
def analysis_detail(request, pk):
    """Detail view for a saved analysis"""
    analysis = get_object_or_404(TextAnalysis, pk=pk)
    
    # Check if user has permission to view
    if not analysis.is_public and analysis.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this analysis.")
    
    # Handle comments
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        if comment_text:
            AnalysisComment.objects.create(
                analysis=analysis,
                user=request.user,
                text=comment_text
            )
            messages.success(request, 'Comment added successfully!')
            return redirect('analysis_detail', pk=analysis.pk)
    
    context = {
        'analysis': analysis,
        'comments': analysis.comments.all(),
        'tags': [tagging.tag for tagging in analysis.taggings.all()],
    }
    
    return render(request, 'analyzer/analysis_detail.html', context)

@login_required
def delete_analysis(request, pk):
    """Delete a saved analysis"""
    analysis = get_object_or_404(TextAnalysis, pk=pk)
    
    # Check if user has permission to delete
    if analysis.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this analysis.")
    
    if request.method == 'POST':
        analysis.delete()
        messages.success(request, 'Analysis deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'analyzer/delete_analysis.html', {'analysis': analysis})

@login_required
def toggle_public(request, pk):
    """Toggle public/private status of an analysis"""
    if request.method == 'POST':
        analysis = get_object_or_404(TextAnalysis, pk=pk, user=request.user)
        analysis.is_public = not analysis.is_public
        analysis.save()
        
        status = 'public' if analysis.is_public else 'private'
        messages.success(request, f'Analysis is now {status}.')
        
        return redirect('analysis_detail', pk=analysis.pk)
    
    return redirect('dashboard')

@login_required
def save_template(request):
    """Save a text template for future use"""
    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        analysis_type = request.POST.get('analysis_type', 'sentiment')
        
        if name and text:
            template, created = SavedTemplate.objects.get_or_create(
                name=name,
                user=request.user,
                defaults={'text': text, 'analysis_type': analysis_type}
            )
            
            if not created:
                template.text = text
                template.analysis_type = analysis_type
                template.save()
                messages.success(request, 'Template updated successfully!')
            else:
                messages.success(request, 'Template saved successfully!')
        
        return redirect('home')
    
    return redirect('home')

@login_required
def delete_template(request, pk):
    """Delete a saved template"""
    template = get_object_or_404(SavedTemplate, pk=pk, user=request.user)
    
    if request.method == 'POST':
        template.delete()
        messages.success(request, 'Template deleted successfully!')
    
    return redirect('home')

@login_required
def get_template(request, pk):
    """Get a saved template as JSON"""
    template = get_object_or_404(SavedTemplate, pk=pk, user=request.user)
    
    data = {
        'text': template.text,
        'analysis_type': template.analysis_type
    }
    
    return JsonResponse(data)

@login_required
def profile(request):
    """User profile view and edit"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()
        
        # Update profile
        profile.bio = request.POST.get('bio', '')
        profile.preferred_analysis_type = request.POST.get('preferred_analysis_type', 'sentiment')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
        'analysis_types': TextAnalysis.ANALYSIS_TYPES,
    }
    
    return render(request, 'analyzer/profile.html', context)

def analyze_sentiment(text):
    """Analyze sentiment of the given text"""
    sentiment_scores = sia.polarity_scores(text)
    
    # Determine overall sentiment
    compound = sentiment_scores['compound']
    if compound >= 0.05:
        sentiment = 'positive'
        color_class = 'green'
    elif compound <= -0.05:
        sentiment = 'negative'
        color_class = 'red'
    else:
        sentiment = 'neutral'
        color_class = 'yellow'
    
    return {
        'sentiment': sentiment,
        'compound': compound,
        'positive': sentiment_scores['pos'],
        'negative': sentiment_scores['neg'],
        'neutral': sentiment_scores['neu'],
        'color_class': color_class,
    }

def summarize_text(text):
    """Summarize the given text"""
    # Basic extractive summarization
    sentences = sent_tokenize(text)
    
    # If text is short, return it as is
    if len(sentences) <= 3:
        return {'summary': text}
    
    # Process with spaCy for better analysis
    doc = nlp(text)
    
    # Calculate word frequencies
    word_frequencies = {}
    for word in doc:
        if not word.is_stop and not word.is_punct and not word.is_space:
            if word.lemma_ not in word_frequencies:
                word_frequencies[word.lemma_] = 1
            else:
                word_frequencies[word.lemma_] += 1
    
    # Normalize frequencies
    max_frequency = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in nlp(sentence):
            if word.lemma_ in word_frequencies:
                if i not in sentence_scores:
                    sentence_scores[i] = word_frequencies[word.lemma_]
                else:
                    sentence_scores[i] += word_frequencies[word.lemma_]
    
    # Get top 3 sentences or 30% of sentences, whichever is greater
    summary_length = max(3, int(len(sentences) * 0.3))
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:summary_length]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original position
    
    summary = ' '.join([sentences[i] for i, _ in top_sentences])
    
    return {
        'summary': summary,
        'original_length': len(text),
        'summary_length': len(summary),
        'reduction': round((1 - len(summary) / len(text)) * 100, 1) if len(text) > 0 else 0,
    }

def extract_entities(text):
    """Extract named entities from the given text"""
    doc = nlp(text)
    
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_,
            'description': spacy.explain(ent.label_),
        })
    
    # Group entities by type
    entity_groups = {}
    for entity in entities:
        if entity['label'] not in entity_groups:
            entity_groups[entity['label']] = []
        entity_groups[entity['label']].append(entity['text'])
    
    return {
        'entities': entities,
        'entity_groups': entity_groups,
        'entity_count': len(entities),
    }

def classify_text(text):
    """Classify text into predefined categories"""
    # Simple rule-based classification for demo purposes
    # In a real app, you would use a trained ML model
    
    text = text.lower()
    
    # Define some simple rules for classification
    categories = {
        'business': ['company', 'market', 'finance', 'stock', 'investment', 'profit', 'business', 'economy'],
        'technology': ['computer', 'software', 'hardware', 'app', 'programming', 'code', 'tech', 'ai', 'data'],
        'health': ['health', 'doctor', 'medicine', 'patient', 'hospital', 'disease', 'treatment', 'medical'],
        'education': ['school', 'student', 'teacher', 'learn', 'education', 'university', 'college', 'course'],
        'entertainment': ['movie', 'music', 'game', 'play', 'entertainment', 'film', 'actor', 'show', 'tv'],
    }
    
    # Count category matches
    category_scores = {category: 0 for category in categories}
    
    for category, keywords in categories.items():
        for keyword in keywords:
            # Use word boundary regex to match whole words
            matches = len(re.findall(r'\b' + keyword + r'\b', text))
            category_scores[category] += matches
    
    # Find the category with the highest score
    if sum(category_scores.values()) > 0:
        top_category = max(category_scores.items(), key=lambda x: x[1])
        confidence = top_category[1] / sum(category_scores.values()) if sum(category_scores.values()) > 0 else 0
        
        # If confidence is too low, mark as 'general'
        if confidence < 0.5 and top_category[1] < 3:
            predicted_category = 'general'
            confidence = 0
        else:
            predicted_category = top_category[0]
    else:
        predicted_category = 'general'
        confidence = 0
    
    return {
        'category': predicted_category,
        'confidence': round(confidence * 100, 1),
        'all_categories': category_scores,
    }

def register(request):
    """Register a new user"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Account created for {username}! You are now logged in.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """Login an existing user"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next page if specified
                next_page = request.POST.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """Logout the current user"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def custom_404(request, exception):
    """Custom 404 page handler"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 page handler"""
    return render(request, '500.html', status=500)


def custom_403(request, exception=None):
    """Custom 403 page handler"""
    return render(request, '403.html', status=403)

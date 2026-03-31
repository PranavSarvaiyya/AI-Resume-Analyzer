import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch
import re
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Initialize AI Client
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
client = None
if api_key:
    # Ensure any extra quotes around the API key from .env are removed
    clean_key = api_key.strip().strip("'").strip('"')
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = clean_key
    )

# Load model once at the top
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load Hard Skill Library dynamically from skills.json
SKILLS_FILE = os.path.join(os.path.dirname(__file__), 'skills.json')

def load_skills():
    if os.path.exists(SKILLS_FILE):
        with open(SKILLS_FILE, 'r') as f:
            return json.load(f)
    return []

TECH_LIBRARY = load_skills()

def get_semantic_match(resume_text, job_description):
    """Calculates overall contextual similarity."""
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(job_description, convert_to_tensor=True)
    score = util.pytorch_cos_sim(resume_emb, jd_emb)
    return round(float(score[0][0]) * 100, 2)

def update_skills_file(new_skills_list):
    """Adds newly detected skills recursively to the JSON file."""
    global TECH_LIBRARY
    added_any = False
    for skill in new_skills_list:
        skill_lower = skill.strip().lower()
        if skill_lower and skill_lower not in TECH_LIBRARY and len(skill_lower) > 1:
            TECH_LIBRARY.append(skill_lower)
            added_any = True
            
    if added_any:
        try:
            with open(SKILLS_FILE, 'w') as f:
                json.dump(TECH_LIBRARY, f, indent=4)
        except Exception as e:
            print(f"Skipping JSON update, Error: {e}")

def extract_new_skills_with_ai(text):
    """Uses LLM to detect unseen keywords (skills/tools) in JD/Resume."""
    try:
        if not client: return
        prompt = f"Extract a comma-separated list of ONLY technical skills, programming languages, tools, or frameworks from this text. Do not include soft skills. If none, return 'None'. Text: {text[:2000]}"
        completion = client.chat.completions.create(
            model="google/gemma-2-27b-it",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        response_text = completion.choices[0].message.content
        if response_text and response_text.strip().lower() != 'none':
            skills = [s.strip() for s in response_text.split(',')]
            update_skills_file(skills)
    except Exception as e:
        print(f"Error extracting skills: {e}")

def get_hard_skills_analysis(resume_text, job_desc):
    """Identifies missing and matching keywords."""
    # First, let AI scan and dynamically grow the TECH_LIBRARY dictionary
    extract_new_skills_with_ai(job_desc + " " + resume_text)
    
    resume_text = str(resume_text).lower()
    job_desc = str(job_desc).lower()

    # Find skills mentioned in JD
    required_in_job = [skill for skill in TECH_LIBRARY if re.search(r'\b' + re.escape(skill) + r'\b', job_desc)]
    
    if not required_in_job:
        return 0, [], []

    # Find which of those are in Resume
    found_in_resume = [skill for skill in required_in_job if re.search(r'\b' + re.escape(skill) + r'\b', resume_text)]
    
    missing_skills = list(set(required_in_job) - set(found_in_resume))
    match_ratio = (len(found_in_resume) / len(required_in_job)) * 100
    
    return round(match_ratio, 2), missing_skills, found_in_resume

def generate_tips(missing_skills):
    """Generates dynamic AI 'Improvisation' or advice based on gaps."""
    tips = []
    
    if not missing_skills:
        return ["✅ Your resume matches all detected technical keywords! Focus on quantifying achievements."]

    tips.append(f"👉 **Focus on adding these to your Tech Stack:** {', '.join([s.upper() for s in missing_skills])}")

    # AI-based drafting tips (using NVIDIA/Gemma)
    if client:
        try:
            prompt = f"The user is missing these technical skills from their resume: {', '.join(missing_skills)}. Keep it concise. For EACH skill independently, generate exactly ONE highly professional, actionable resume bullet point (drafting tip) that they could use if they learn it. Start each tip with '💡 **Drafting Tip ([Skill Name]):** '"
            completion = client.chat.completions.create(
                model="google/gemma-2-27b-it",
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                stream=False
            )
            response_text = completion.choices[0].message.content
            if response_text:
                for line in response_text.split('\n'):
                    if line.strip().startswith("💡") or line.strip().startswith("**"):
                        tips.append(line.strip())
            return tips
        except Exception as e:
            print(f"AI Tip Error: {e}")
            # Fallback to local hardcoded tips if AI fails

    # Fallback to old Logic-based advice
    if 'python' in missing_skills:
        tips.append("💡 **Drafting Tip:** 'Architected production-grade Python microservices, reducing deployment latency by 40%.'")
    
    if 'sql' in missing_skills:
        tips.append("💡 **Drafting Tip:** 'Optimized distributed SQL queries, cutting data retrieval costs by 25%.'")

    return tips

# Pura code khatam hone ke baad sabse aakhir mein:
print("Engine is Ready!")
tips = generate_tips(['docker', 'mongodb'])
print(tips)

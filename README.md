# 🚀 AI-Powered Resume Analyzer

An intelligent system that evaluates how well a candidate’s resume matches a specific job description — going beyond keyword matching to understand context, extract skills, and generate actionable improvements.

---

## 📈 Why This Project Matters

Most resume tools fail because they:

* Depend only on keyword matching
* Ignore context
* Provide no actionable feedback

This system solves that by combining:

* **Rule-based logic (ATS style)**
* **Deep semantic understanding**
* **Generative AI for improvement**
---

## 📌 Overview

This project is not just another ATS keyword matcher.

It combines **Natural Language Processing (NLP)** and **Generative AI** to:

* Measure resume-job fit accurately
* Identify missing skills
* Provide AI-generated suggestions to improve the resume

Instead of blindly matching keywords, the system understands **semantic meaning**, making it closer to how real recruiters evaluate profiles.

---

## 🧠 Core Features

### 🔍 Resume vs Job Description Matching

* Calculates how well a resume aligns with a given job description
* Generates a **match percentage score**
* Highlights missing and matched skills

---

### 🧾 Automatic Resume Parsing

* Extracts text from PDF resumes
* Cleans and processes raw content for analysis

---

### 🧩 Smart Skill Extraction (Self-Learning)

* Uses LLM to identify:

  * Technical Skills
  * Tools
  * Programming Languages
* Continuously improves by updating a dynamic skills dictionary

---

### ⚡ Semantic Matching (Context Awareness)

* Converts resume and job description into embeddings
* Uses cosine similarity to measure contextual alignment
* Recognizes related terms:

  * Example: *“Client Management” ≈ “Customer Relations”*

---

### 📊 ATS-Style Keyword Matching

* Detects exact skill matches using regex
* Generates:

  * Match score
  * Missing skills list

---

### ✍️ AI-Powered Resume Suggestions

* Generates professional bullet points for missing skills
* Helps users directly improve their resume content
* Focused on practical, job-ready improvements

---

## 🛠️ Tech Stack

| Category         | Tools Used                     |
| ---------------- | ------------------------------ |
| Frontend         | Streamlit                      |
| Language         | Python                         |
| NLP              | Sentence-Transformers (MiniLM) |
| LLM              | NVIDIA API (Gemma Model)       |
| PDF Processing   | pdfplumber                     |
| Data Processing  | pandas                         |
| Similarity       | sklearn (Cosine Similarity)    |
| Pattern Matching | Regex                          |

---

## ⚙️ System Workflow

1. User inputs:

   * Job Description (text)
   * Resume (PDF)

2. Resume is parsed and cleaned

3. AI extracts skills from:

   * Resume
   * Job Description

4. Matching is performed using:

   * Keyword-based comparison
   * Semantic similarity scoring

5. Output includes:

   * Match percentage
   * Missing skills
   * AI-generated resume improvement suggestions

---

## 🎯 Use Cases

* Students applying for internships
* Job seekers optimizing resumes
* Career switchers identifying skill gaps
* Recruiters doing quick screening


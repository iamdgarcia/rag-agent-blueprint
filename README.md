# RAG Agent Blueprint

A deployable template for a RAG (Retrieval-Augmented Generation) Agent based on the Agentic AI for Beginners course. This template implements "Chat with Your Docs" functionality.

## 🚀 Get Started

**Step 1 — Create your Netlify account:** [Register here](https://join.netlify.com/uk2itht31g7b) *(use this referral link to support the course)*

**Step 2 — Deploy:** Once registered, click below:

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/iamdgarcia/rag-agent-blueprint&affiliate=8mntz9z1uxdi-96ld6)

## What is a RAG Agent?

A RAG Agent combines retrieval and generation:
1. **Retrieve** - Search through documents to find relevant information
2. **Augment** - Use retrieved context to enhance the response
3. **Generate** - Produce accurate, context-aware answers

This pattern is covered in Module 2.2 and 2.3 of the Agentic AI for Beginners course.

## Features

- 📚 **Document Q&A** - Answer questions based on provided documents
- 🔍 **Semantic Search** - Find relevant content even with different wording
- 📖 **Context-Aware** - Uses retrieved information to generate accurate answers
- ⚡ **Netlify Functions** - Serverless backend for the agent logic
- 📚 **Course-Aligned** - Directly implements concepts from Modules 2.2-2.3
- 🚀 **One-Click Deploy** - Ready to deploy to Netlify with affiliate tracking

## How It Works

The RAG Agent follows this process:
1. **Receive Query** - User asks a question
2. **Search Knowledge Base** - Find relevant documents or passages
3. **Rank Results** - Prioritize most relevant information
4. **Augment Prompt** - Combine query with retrieved context
5. **Generate Answer** - Produce response using retrieved information
6. **Cite Sources** - Reference the documents used

## Included Implementation

- Python-based RAG Agent with semantic search
- Simple REST API endpoint (`/.netlify/functions/rag-agent`)
- Sample knowledge base about urban gardening
- HTML/JavaScript frontend for Q&A interface

## Accessing the API Directly

After deployment:
```
https://YOUR-SITE-NAME.netlify.app/.netlify/functions/rag-agent
```

### Request Format
```json
{
  "message": "Your question about the documents",
  "history": []
}
```

## Local Development

```bash
git clone https://github.com/iamdgarcia/rag-agent-blueprint.git
cd rag-agent-blueprint
pip install -r requirements.txt
python server.py
```

## Course Connection

This blueprint implements:
- **Module 2.2: Retrieval-Augmented Generation (RAG) Basics**
- **Module 2.3: Building a "Chat with Your Docs" Agent**
- Demonstrates semantic search and context augmentation

---

*Built with ❤️ for The Learning Curve community.*
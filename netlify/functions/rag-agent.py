import json
import re
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()

# Sample knowledge base (in production, use vector database)
KNOWLEDGE_BASE = {
    "urban_gardening": """
Urban gardening is a transformative practice that empowers city dwellers to cultivate their own fruits and vegetables. 
It significantly boosts local food security, particularly in food deserts where fresh produce is scarce.
Beyond enhancing access to nutritious food, urban gardening positively impacts the environment by transforming concrete jungles into lush green spaces.
This transformation helps mitigate the urban heat island effect, improves air quality, and creates habitats for pollinators and wildlife.
Urban gardening serves as a catalyst for community engagement, as shared gardening projects foster social interaction, cultural exchange, and a sense of collective responsibility.
The physical act of gardening offers substantial mental and physical health benefits, reducing stress and anxiety while promoting physical activity.
    """,
    "environmental_benefits": """
Urban gardening offers a multitude of environmental benefits. By increasing the number of plants, urban gardens play a crucial role in improving air quality.
They absorb carbon dioxide and release oxygen, helping to reduce urban air pollution.
These green spaces also serve as vital habitats for various species, supporting biodiversity by attracting essential pollinators like bees and butterflies.
Furthermore, urban gardens help combat the urban heat island effect through the cooling process of evapotranspiration and by providing shade.
They lower temperatures in densely built environments, making cities more comfortable during hot weather.
Additionally, urban gardening promotes sustainable waste management by encouraging composting.
    """,
    "health_benefits": """
Urban gardening provides access to fresh, organic produce, significantly enhancing dietary quality.
Community gardens have improved local residents' nutrition profiles, increasing their intake of essential vitamins and minerals.
The mental health benefits are profound - regular interaction with green spaces can substantially reduce stress and anxiety levels.
It improves overall mental well-being and alleviates symptoms of depression.
Urban gardening also promotes physical activity through tasks like planting, weeding, and harvesting.
This encourages movement, which helps combat obesity and related health issues.
    """,
    "community_impact": """
Urban gardening initiatives transform communities by enhancing cohesion and fostering collaboration among diverse groups.
These green spaces act as vibrant social hubs where residents exchange gardening tips, share resources, and forge lasting friendships.
They also serve as educational platforms, offering workshops on sustainable agriculture, nutrition, and environmental stewardship.
Urban gardens play a crucial role in increasing food security by providing a local source of fresh produce.
This is especially vital for low-income communities facing food deserts.
Involvement in these projects empowers individuals by equipping them with valuable skills in horticulture, project management, and teamwork.
    """,
    "starting_tips": """
To start an urban garden, begin by assessing your available space - whether it's a balcony, rooftop, or windowsill.
Consider factors such as sunlight, wind exposure, and accessibility.
Choose plants well-suited for urban environments - herbs, leafy greens, and compact vegetables are excellent choices as they thrive in containers.
Utilize vertical gardening techniques by incorporating wall planters, hanging pots, or trellises to optimize growing space.
Embrace sustainable practices by composting kitchen scraps for natural fertilizer, collecting rainwater for irrigation, and using organic pest control methods.
    """
}

class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    retrieved_documents: List[Dict[str, Any]]
    history: List[Dict[str, str]]

def retrieve_relevant_docs(query: str) -> List[Dict[str, Any]]:
    """Simple keyword-based retrieval (in production, use embeddings)"""
    query_lower = query.lower()
    results = []
    
    for doc_name, content in KNOWLEDGE_BASE.items():
        # Simple keyword matching
        query_words = set(query_lower.split())
        content_words = set(content.lower().split())
        matches = query_words.intersection(content_words)
        
        if matches:
            # Extract relevant sentences
            sentences = content.strip().split('. ')
            relevant_sentences = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(word in sentence_lower for word in matches):
                    relevant_sentences.append(sentence)
            
            if relevant_sentences:
                results.append({
                    "document": doc_name.replace('_', ' ').title(),
                    "relevance_score": len(matches),
                    "content": ' '.join(relevant_sentences[:3])  # Top 3 relevant sentences
                })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:3]  # Return top 3

def generate_rag_response(query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
    """Generate response using retrieved documents"""
    
    if not retrieved_docs:
        return f"I don't have specific information about '{query}' in my knowledge base. Could you try asking about urban gardening, environmental benefits, health benefits, community impact, or how to start an urban garden?"
    
    response = "Based on the documents I found:\n\n"
    
    for doc in retrieved_docs:
        response += f"**From: {doc['document']}**\n"
        response += f"{doc['content']}\n\n"
    
    response += "Would you like me to elaborate on any of these topics?"
    return response

def rag_agent_response(user_message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Main RAG agent response"""
    
    # 1. Retrieve relevant documents
    retrieved_docs = retrieve_relevant_docs(user_message)
    
    # 2. Generate response using retrieved context
    response = generate_rag_response(user_message, retrieved_docs)
    
    # 3. Update history
    updated_history = history.copy()
    updated_history.append({"role": "user", "content": user_message})
    updated_history.append({"role": "assistant", "content": response})
    
    return {
        "response": response,
        "retrieved_documents": retrieved_docs,
        "history": updated_history
    }

@app.get("/")
async def root():
    return {"message": "RAG Agent API is running", "documents": len(KNOWLEDGE_BASE)}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    try:
        result = rag_agent_response(
            user_message=chat_message.message,
            history=chat_message.history or []
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)
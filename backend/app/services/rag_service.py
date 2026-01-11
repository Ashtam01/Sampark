from ..database import supabase

def search_knowledge_base(query: str):
    """
    Simple search fallback. 
    In a full build, this would use vector embeddings.
    """
    try:
        # Simple text search if vector search isn't ready
        # Using Supabase's 'textSearch' if enabled, or just a dummy response for now
        return "I checked the manual, but since this is a prototype, I can't search PDF content yet. Please refer to mcd.gov.in."
    except Exception as e:
        print(f"RAG Error: {e}")
        return "Manual lookup failed."
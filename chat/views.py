from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Document, Query
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import SimpleVectorStore
from rest_framework.views import APIView
import os

class DocumentView(APIView):
    vector_store = SimpleVectorStore()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = None

    def post(self, request):
        files = request.FILES.getlist('files')
        for file in files:
            document = Document.objects.create(file=file)
            document_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
            documents = SimpleDirectoryReader(document_path).load_data()
            if not self.index:
                self.index = VectorStoreIndex(self.vector_store, self.storage_context)
            self.index.add_documents(documents)
        return Response({'message': 'Documents uploaded successfully'})

class QueryView(APIView):
    def post(self, request):
        query_text = request.data.get('query')
        if not DocumentView.index:
            return Response({'error': 'No documents indexed yet'}, status=status.HTTP_400_BAD_REQUEST)
        query_engine = DocumentView.index.as_query_engine()
        response = query_engine.query(query_text)
        if not response:
            return Response({'error': 'No response found for the query'}, status=status.HTTP_404_NOT_FOUND)
        Query.objects.create(text=query_text, response=str(response))
        return Response({'response': str(response)})
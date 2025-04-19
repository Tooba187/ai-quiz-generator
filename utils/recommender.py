from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class ResourceRecommender:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectorstore = None
        self.resources = []
    
    def add_resource(self, url):
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.split_documents(documents)
            
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(docs, self.embeddings)
            else:
                self.vectorstore.add_documents(docs)
            
            self.resources.append(url)
            return True
        except Exception as e:
            print(f"Error adding resource {url}: {e}")
            return False
    
    def recommend_resources(self, topic, num_recommendations=3):
        if self.vectorstore is None:
            return self._fallback_recommendations(topic, num_recommendations)
        
        try:
            docs = self.vectorstore.similarity_search(topic, k=num_recommendations)
            return [doc.metadata['source'] for doc in docs]
        except:
            return self._fallback_recommendations(topic, num_recommendations)
    
    def _fallback_recommendations(self, topic, num_recommendations):
        # Fallback to a simple web search if vector DB fails
        try:
            search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}+educational+site:youtube.com+OR+site:khanacademy.org+OR+site:edx.org"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href.startswith('/url?q='):
                    url = href.split('/url?q=')[1].split('&')[0]
                    if any(domain in url for domain in ['youtube.com', 'khanacademy.org', 'edx.org']):
                        links.append(url)
                        if len(links) >= num_recommendations:
                            break
            
            return links[:num_recommendations]
        except:
            return []

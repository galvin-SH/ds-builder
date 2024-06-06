import glob
import ollama
import chromadb
import codecs
path = './output/'
save_path = './output/newFolder/'
files = glob.glob(path + '*.txt')

# Read all files in the folder
# and save the content in a new file
with codecs.open(save_path + '/newFile.txt', 'w', encoding='utf-8') as outfile:
    for name in files:
        with open(name, 'r', encoding='utf-8') as infile:
            data = infile.read().encode('utf-8')
            outfile.write(data.decode('utf-8'))

# Read the new file and generate embeddings
documents = []
with open(save_path + '/newFile.txt', 'r', encoding='utf-8') as f:
    for line in f:
        documents.append(line.strip())
client = chromadb.Client()
collection = client.create_collection(name='docs')
# store each document in a vector embedding database
for i, d in enumerate(documents):
    response = ollama.embeddings(model="knowitall", prompt=d)
    embedding = response["embedding"]
    collection.add(
      ids=[str(i)],
      embeddings=[embedding],
      documents=[d]
    )

prompt = "Who is Yangyang in Wuthering Waves?"
# Generate embeddings for the prompt and retrieve the most similar documents
response = ollama.embeddings(model="knowitall", prompt=prompt)
results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=1
)

data = results['documents'][0][0]

# generate a response combining the prompt and the retrieved document
output = ollama.generate(
  model="knowitall",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)
print(prompt + '\n')
print(output['response'])
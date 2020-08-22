from newspaper import Article
import nltk

nltk.download('punkt')

url= 'https://www.nasdaq.com/news-and-insights'

article = Article(url, language="en") # en for English

article.download()
article.parse()
article.nlp()

print("Article Title:")
print(article.title) #prints the title of the article
print("\n")
print("Article Text:")
print(article.text) #prints the entire text of the article
print("\n")
print("Article Summary:")
print(article.summary) #prints the summary of the article
print("\n")
print("Article Keywords:")
print(article.keywords) #prints the keywords of the article

file1=open("NewsFile.txt", "w+")
file1.write("Title:\n")
file1.write(article.title)
file1.write("\n\nArticle Text:\n")
file1.write(article.text)
file1.write("\n\nArticle Summary:\n")
file1.write(article.summary)
file1.write("\n\n\nArticle Keywords:\n")
keywords='\n'.join(article.keywords)
file1.write(keywords)
file1.close()

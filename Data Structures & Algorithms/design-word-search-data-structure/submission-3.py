class WordDictionary:

    def __init__(self):
        self.words = {}



    def addWord(self, word: str) -> None:
        node = self.words
        for c in word:
            node = node.setdefault(c,{})
        node['*'] = True
            

    def search(self, word: str) -> bool:
        n = len(word)
        def dfs(node,i):
            if i == n:
                return "*" in node
            b = []
            if word[i] == ".":
                for c in node.keys():
                    if c != "*":
                        b.append(dfs(node[c],i+1))
                return any(b)
            else:
                return dfs(node[word[i]],i+1) if word[i] in node else False
        return dfs(self.words,0)
            

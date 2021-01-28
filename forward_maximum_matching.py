class Node:
    def __init__(self):
        self.next = {}
        self.is_word = False


class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        self._insert(self.root, word, 0)

    def _insert(self, node, word, d):
        if d == len(word):
            node.is_word = True
            return node
        c = word[d]
        if c not in node.next:
            node.next[c] = Node()
        node.next[c] = self._insert(node.next[c], word, d + 1)
        return node

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        x = self._search(self.root, word, 0)
        if x is None:
            return False
        return x.is_word is True

    def _search(self, node, word, d):
        if d == len(word):
            return node
        c = word[d]
        if c not in node.next:
            return None
        return self._search(node.next[c], word, d + 1)

    def startswith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        x = self._search(self.root, prefix, 0)
        if x is None:
            return False
        return True


class Tokenizer:
    def __init__(self, vocab_list):
        self.has_vocab = True
        if not vocab_list:
            self.has_vocab = False
        self.trie = Trie()
        for word in set(vocab_list):
            self.trie.insert(word)

    def forward_maximum_matching_cut(self, text):
        """
        return
            1. list: 分词结果（保留vocab的词不切分）
            2. 分词结果list中每个元素是否是vocab中的词

        example
            vocab = ['队友', '微软', '库克']
            text = '库克称微软公司是队友'

            return:
            tokens:  ['库克', '称', '微软', '公', '司', '是', '队友']
            is_word: [True, False, True, False, False, False, True]
        """
        if not self.has_vocab:
            return list(text), [False] * len(text)

        if not text:
            return [], []

        tokens = []
        is_word = []
        length = len(text)

        i = 0
        while i < length:
            node = self.trie.root
            j = i
            last_word_idx = -1  # 从位置i往后匹配，最长匹配词词尾的idx

            while j < length:
                c = text[j]
                if c not in node.next:
                    break
                node = node.next[c]
                if node.is_word:
                    last_word_idx = j
                j += 1

            if last_word_idx != -1:  # found
                tokens.append(text[i:last_word_idx+1])
                is_word.append(True)
                i = last_word_idx + 1
            else:  # not found
                tokens.append(text[i])
                is_word.append(False)
                i += 1
        assert len(tokens) == len(is_word)
        return tokens, is_word


if __name__ == '__main__':
    vocab = ['队友', '微软', '库克']
    text = '库克称微软公司是队友'
    tokenizer = Tokenizer(vocab)
    tokens, is_word = tokenizer.forward_maximum_matching_cut(text)
    print(tokens)
    print(is_word)



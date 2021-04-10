import os
import os.path
from transformers import AutoTokenizer, AutoModel


def download_from_huggingface(model_name, root_path):
    """
    1. 下载可能会失败，重试即可
    2. 程序会缓存之前下载过的内容
    :param model_name: from https://huggingface.co/models,
        e.g. download_from_huggingface('uer/chinese_roberta_L-2_H-128', '/Users/lilin/Desktop/temp1')
    :param root_path:
    :return:
    """
    path = os.path.join(root_path, model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(path)

    model = AutoModel.from_pretrained(model_name)
    model.save_pretrained(path)
    print(path, 'done.')


if __name__ == '__main__':
    download_from_huggingface('uer/chinese_roberta_L-2_H-128',
                              '/Users/lilin/data/pretrain-language-models/huggingface')
    download_from_huggingface('uer/chinese_roberta_L-2_H-768',
                              '/Users/lilin/data/pretrain-language-models/huggingface')
    download_from_huggingface('uer/chinese_roberta_L-4_H-256',
                              '/Users/lilin/data/pretrain-language-models/huggingface')
    download_from_huggingface('uer/chinese_roberta_L-4_H-768',
                              '/Users/lilin/data/pretrain-language-models/huggingface')


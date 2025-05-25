from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from tokenizers.processors import TemplateProcessing


def tokenizer(
    file_list,
    max_vocab_size: int = 2**15,
    min_frequency: int = 5,
    begin_token: str = "<|bos|>",
    end_token: str = "<|eos|>",
    padding_token: str = "<|pad|>",
    unknown_token: str = "<|unk|>",
    save_file: str = "tokenizer.json",
):
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.BpeTrainer(
        vocab_size=max_vocab_size,
        min_frequency=min_frequency,
        special_tokens=[begin_token, end_token, padding_token, unknown_token],
    )
    tokenizer.train(file_list, trainer=trainer)
    tokenizer.post_processor = TemplateProcessing(
        single=f"{begin_token} $A {end_token}",
        special_tokens=[
            (begin_token, tokenizer.token_to_id(begin_token)),
            (end_token, tokenizer.token_to_id(end_token)),
        ],
    )
    tokenizer.save(save_file)

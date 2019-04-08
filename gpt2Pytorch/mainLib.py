'''
    code by TaeHwan Jung(@graykode)
    Original Paper and repository here : https://github.com/openai/gpt-2
    GPT2 Pytorch Model : https://github.com/huggingface/pytorch-pretrained-BERT
'''

import os
import sys
import torch
import random
import argparse
import numpy as np
from gpt2Pytorch.GPT2.model import (GPT2LMHeadModel)
from gpt2Pytorch.GPT2.utils import load_weight
from gpt2Pytorch.GPT2.config import GPT2Config
from gpt2Pytorch.GPT2.sample import sample_sequence
from gpt2Pytorch.GPT2.encoder import get_encoder

def text_generator(state_dict, paragraph):
    os.chdir('gpt2Pytorch')
    #print(os.system("dir"))
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=False)
    parser.add_argument("--quiet", type=bool, default=True)
    parser.add_argument("--nsamples", type=int, default=1)
    parser.add_argument('--unconditional', action='store_true', help='If true, unconditional generation.')
    parser.add_argument("--batch_size", type=int, default=-1)
    parser.add_argument("--length", type=int, default=-1)
    parser.add_argument("--temperature", type=float, default=1) #default=0.7
    parser.add_argument("--top_k", type=int, default=40)        #default=60
    args = parser.parse_args()

    args.text = paragraph

    if args.quiet is False:
        print(args)
    #print(args.text)

    if args.batch_size == -1:
        args.batch_size = 1
    assert args.nsamples % args.batch_size == 0

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load Model
    enc = get_encoder()
    config = GPT2Config()
    model = GPT2LMHeadModel(config)
    model = load_weight(model, state_dict)
    model.to(device)
    model.eval()

    if args.length == -1:
        args.length = config.n_ctx // 2
    elif args.length > config.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % config.n_ctx)

    print(args.text)
    context_tokens = enc.encode(args.text)

    generated = 0
    for _ in range(args.nsamples // args.batch_size):
        out = sample_sequence(
            model=model, length=args.length,
            context=context_tokens  if not  args.unconditional else None,
            start_token=enc.encoder['<|endoftext|>'] if args.unconditional else None,
            batch_size=args.batch_size,
            temperature=args.temperature, top_k=args.top_k, device=device
        )
        out = out[:, len(context_tokens):].tolist()
        for i in range(args.batch_size):
            generated += 1
            text = enc.decode(out[i])
            if args.quiet is False:
                print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
            print(text)
            return text

def AIconverter(paragraph):
    if os.path.exists('gpt2Pytorch/gpt2-pytorch_model.bin'):
        state_dict = torch.load('gpt2Pytorch/gpt2-pytorch_model.bin', map_location='cpu' if not torch.cuda.is_available() else None)
        ret = text_generator(state_dict,paragraph)
    else:
        print('Please download gpt2-pytorch_model.bin')
        sys.exit()
    os.chdir("..")
    return ret

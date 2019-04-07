# Document-Enhancer

To get started:

install pytorch from here: https://pytorch.org/

Install dependencies:
`pip3 install tqdm regex==2017.4.5`

Clone gpt-2:
```git clone https://github.com/graykode/gpt-2-Pytorch && cd gpt-2-Pytorch```

Download the 117M model:
`curl --output gpt2-pytorch_model.bin https://s3.amazonaws.com/models.huggingface.co/bert/gpt2-pytorch_model.bin`

Test it out:
`python main.py --text "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him."`

from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from peft import PeftModel
import gc
import torch

model_name = "meta-llama/Llama-2-7b-chat-hf"
log_model_name = 'chrivasileiou/digitest'
subfolder = 'grpo_adapter'
adapter_name = 'grpo_adapter'
example_prompt = False

device = torch.device('cuda')
model = AutoModelForCausalLM.from_pretrained(model_name, 
                                             torch_dtype=torch.bfloat16, 
                                             device_map=device,
                                             attn_implementation="flash_attention_2",
                                             )
model.eval()
model = PeftModel.from_pretrained(model, 
                                  log_model_name, 
                                  subfolder=subfolder, 
                                  adapter_name=adapter_name)
model.set_adapter(adapter_name)
torch.cuda.empty_cache()
gc.collect()

tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=1280)
streamer = TextStreamer(tokenizer, skip_prompt=False, skip_special_tokens=True)

while True:
  user_prompt = input("Enter your prompt: ")
  if user_prompt.lower() == 'exit' or user_prompt.lower() == 'quit':
    break
  elif user_prompt.lower() == 'example':
    example_prompt = True
  elif user_prompt.lower() == 'model':
    print(model)
    continue

  if example_prompt:
    user_prompt = """Please formulate a test vector for the circuit "circuit_39868" to address the "sa0 _0007_" based on this netlist:
    ```
    module circuit_39868 ( _0000_,  _0001_,  _0002_,  _0003_, _0011_ );
    XNR2 _0004_ ( _0005_, _0001_, _0002_ );
    XOR2 _0006_ ( _0007_, _0000_, _0003_ );
    AN2 _0010_ ( _0011_, _0007_, _0005_ );
    endmodule
    ```
    """

  prompt = f"""[INST] <<SYS>>
  You are an ATPG tool applied to integrated circuits for fault testing. These circuits will be provided in structural verilog. You need to pay attention to the context within the tokens [INST] and [/INST]. This will be your instruction. Then, think about the reasoning process in your mind and last provide your best answer. The thinking process should be reported after the CHAIN_OF_THOUGHT tag. Your answer will contain the simulation, the input test vector, the output test vector and the detected faults list, which will be provided after the SNAPSHOT, INPUT_VECTOR, EXPECTED_OUTPUT and DETECTED_FAULTS tags, respectively. 
  <</SYS>> {user_prompt} 
  [/INST]
  """

  output = model.generate(tokenizer.encode(prompt, return_tensors='pt').to(model.device), streamer=streamer)
  del output 
  torch.cuda.empty_cache()
  gc.collect()

  example_prompt = False
  print("--------------------------------\n\n")